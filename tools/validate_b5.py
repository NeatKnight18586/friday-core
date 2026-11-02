#!/usr/bin/env python3
"""Validate B5 research schemas, evaluation cases, and project-record traceability."""
from __future__ import annotations

import json
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from types import SimpleNamespace
from copy import deepcopy
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - environment-specific
    print("FAIL: jsonschema is not installed. Install requirements-dev.txt.", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SCHEMAS = ROOT / "schemas"


def load_validator(name: str):
    schema = json.loads((SCHEMAS / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def run_main_in_process(module_name: str, argv: list[str]):
    """Invoke a repository CLI entry point without spawning a nested process."""
    import importlib

    module = importlib.import_module(module_name)
    previous_argv = sys.argv[:]
    stdout = StringIO()
    stderr = StringIO()
    sys.argv = [module_name.replace(".", "/") + ".py", *argv]
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            return_code = module.main()
    except SystemExit as exc:
        return_code = int(exc.code or 0)
    finally:
        sys.argv = previous_argv
    return SimpleNamespace(returncode=return_code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


def run_project_validator(project_dir: Path):
    return run_main_in_process("tools.validate_project", [str(project_dir)])


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    schema_examples = {
        "research-plan.schema.json": [ROOT / "templates/project/research-plan.json"],
        "research-question.schema.json": [ROOT / "templates/records/research-question.json"],
        "research-finding.schema.json": [ROOT / "templates/records/research-finding.json"],
        "research-round.schema.json": [ROOT / "templates/records/research-round.json"],
        "opportunity-record.schema.json": [ROOT / "templates/records/opportunity.json"],
    }

    validators = {}
    for schema_name, paths in schema_examples.items():
        try:
            validator = load_validator(schema_name)
            validators[schema_name] = validator
            for path in paths:
                sample = json.loads(path.read_text(encoding="utf-8"))
                for issue in validator.iter_errors(sample):
                    errors.append(f"{path.relative_to(ROOT)}: {issue.message}")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{schema_name}: {exc}")

    eval_validator = load_validator("evaluation-case.schema.json")
    for number in range(20, 31):
        path = ROOT / "evals/cases" / f"EVAL-{number:03d}.json"
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
            for issue in eval_validator.iter_errors(case):
                errors.append(f"{path.relative_to(ROOT)}: {issue.message}")
            if case.get("case_status") != "ready":
                errors.append(f"{path.relative_to(ROOT)}: B5 evaluation case must be ready for runtime evaluation")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if errors:
        print(f"FAIL: {len(errors)} schema/template/evaluation issue(s)")
        for issue in errors:
            print(f"- {issue}")
        return 1

    with tempfile.TemporaryDirectory(prefix="peanuts-b5-") as temporary:
        workspace = Path(temporary) / "projects"
        init = run_main_in_process(
            "tools.init_project",
            [
                "--id", "b5-research-test",
                "--title", "B5 Research Test",
                "--mode", "MODE-EVENT",
                "--outcome", "Validate B5 research record integrity",
                "--workspace-root", str(workspace),
            ],
        )
        project = workspace / "b5-research-test"
        if init.returncode != 0 or not project.is_dir():
            print(f"FAIL: initializer could not create B5 test workspace: {init.stdout} {init.stderr}")
            return 1

        baseline = run_project_validator(project)
        if baseline.returncode != 0:
            print(f"FAIL: empty initialized research workspace: {baseline.stdout} {baseline.stderr}")
            return 1

        def load_template(name: str) -> dict:
            return json.loads((ROOT / "templates/records" / name).read_text(encoding="utf-8"))

        source = load_template("source.json")
        claim = load_template("claim.json")
        claim["claim_id"] = "CLM-0001"
        claim["source_ids"] = [source["source_id"]]

        question = load_template("research-question.json")
        question["answer_claim_ids"] = [claim["claim_id"]]
        question["status"] = "answered"

        research_round = load_template("research-round.json")

        finding = load_template("research-finding.json")
        finding["source_ids"] = [source["source_id"]]
        finding["claim_ids"] = [claim["claim_id"]]
        finding["question_ids"] = [question["question_id"]]
        finding["round_id"] = research_round["round_id"]

        opportunity = load_template("opportunity.json")
        opportunity["finding_ids"] = [finding["finding_id"]]
        opportunity["claim_ids"] = [claim["claim_id"]]
        opportunity["unresolved_questions"] = []

        records = project / "records"
        write_jsonl(records / "sources.jsonl", [source])
        write_jsonl(records / "claims.jsonl", [claim])
        write_jsonl(records / "research-questions.jsonl", [question])
        write_jsonl(records / "research-rounds.jsonl", [research_round])
        write_jsonl(records / "research-findings.jsonl", [finding])
        write_jsonl(records / "opportunities.jsonl", [opportunity])

        research_plan_path = project / "research-plan.json"
        research_plan = json.loads(research_plan_path.read_text(encoding="utf-8"))
        research_plan.update(
            {
                "research_question_ids": [question["question_id"]],
                "research_round_ids": [research_round["round_id"]],
                "priority_claim_ids": [claim["claim_id"]],
                "status": "planned",
            }
        )
        research_plan_path.write_text(json.dumps(research_plan, indent=2) + "\n", encoding="utf-8")

        valid = run_project_validator(project)
        if valid.returncode != 0:
            print(f"FAIL: valid linked B5 records were rejected: {valid.stdout} {valid.stderr}")
            return 1

        # Cross-record dangling claim reference must fail.
        bad_question = deepcopy(question)
        bad_question["answer_claim_ids"] = ["CLM-9999"]
        write_jsonl(records / "research-questions.jsonl", [bad_question])
        result = run_project_validator(project)
        if result.returncode == 0 or "missing claim reference CLM-9999" not in result.stdout:
            print(f"FAIL: dangling research-question claim reference was not rejected: {result.stdout} {result.stderr}")
            return 1

        # Restore question and test user statement consent requirements.
        write_jsonl(records / "research-questions.jsonl", [question])
        bad_finding = deepcopy(finding)
        bad_finding.update(
            {
                "finding_type": "user_statement",
                "evidence_label": "user_reported",
                "round_id": research_round["round_id"],
                "participant_ref": "P-0001",
                "consent_status": "unknown",
            }
        )
        round_with_participant = deepcopy(research_round)
        round_with_participant["participant_refs"] = ["P-0001"]
        write_jsonl(records / "research-rounds.jsonl", [round_with_participant])
        write_jsonl(records / "research-findings.jsonl", [bad_finding])
        result = run_project_validator(project)
        if result.returncode == 0 or "consent_status" not in result.stdout:
            print(f"FAIL: unconsented user statement was not rejected: {result.stdout} {result.stderr}")
            return 1

        # A participant-derived finding must refer to a pseudonymous participant in its round.
        bad_participant = deepcopy(bad_finding)
        bad_participant["consent_status"] = "confirmed"
        write_jsonl(records / "research-rounds.jsonl", [research_round])
        write_jsonl(records / "research-findings.jsonl", [bad_participant])
        result = run_project_validator(project)
        if result.returncode == 0 or "is not listed in research round" not in result.stdout:
            print(f"FAIL: unknown participant reference was not rejected: {result.stdout} {result.stderr}")
            return 1

        # Restore records; a finding must refer only to questions assigned to its round.
        write_jsonl(records / "research-rounds.jsonl", [research_round])
        write_jsonl(records / "research-findings.jsonl", [finding])
        second_question = deepcopy(question)
        second_question["question_id"] = "RQ-0002"
        second_question["question"] = "Which workarounds are used when the primary process fails?"
        write_jsonl(records / "research-questions.jsonl", [question, second_question])
        bad_linked_finding = deepcopy(finding)
        bad_linked_finding["question_ids"] = [second_question["question_id"]]
        write_jsonl(records / "research-findings.jsonl", [bad_linked_finding])
        result = run_project_validator(project)
        if result.returncode == 0 or "is not linked to research round" not in result.stdout:
            print(f"FAIL: finding/question round mismatch was not rejected: {result.stdout} {result.stderr}")
            return 1

        # Restore records and test completed round without valid consent.
        write_jsonl(records / "research-questions.jsonl", [question])
        write_jsonl(records / "research-findings.jsonl", [finding])
        bad_round = deepcopy(research_round)
        bad_round.update(
            {
                "status": "completed",
                "consent_status": "incomplete",
                "started_at": "2026-11-01T09:00:00Z",
                "completed_at": "2026-11-01T10:00:00Z",
            }
        )
        write_jsonl(records / "research-rounds.jsonl", [bad_round])
        result = run_project_validator(project)
        if result.returncode == 0 or "consent_status" not in result.stdout:
            print(f"FAIL: completed round with incomplete consent was not rejected: {result.stdout} {result.stderr}")
            return 1

        # Consent can be valid while required local review is still unresolved; completion must fail.
        bad_review_round = deepcopy(research_round)
        bad_review_round.update(
            {
                "status": "completed",
                "consent_status": "obtained_for_all",
                "local_review_status": "unknown",
                "started_at": "2026-11-01T09:00:00Z",
                "completed_at": "2026-11-01T10:00:00Z",
            }
        )
        write_jsonl(records / "research-rounds.jsonl", [bad_review_round])
        result = run_project_validator(project)
        if result.returncode == 0 or "local_review_status" not in result.stdout:
            print(f"FAIL: completed round with unresolved local review was not rejected: {result.stdout} {result.stderr}")
            return 1

        # Restore round and test opportunity-to-finding traceability.
        write_jsonl(records / "research-rounds.jsonl", [research_round])
        bad_opportunity = deepcopy(opportunity)
        bad_opportunity["finding_ids"] = ["FND-9999"]
        write_jsonl(records / "opportunities.jsonl", [bad_opportunity])
        result = run_project_validator(project)
        if result.returncode == 0 or "missing finding reference FND-9999" not in result.stdout:
            print(f"FAIL: dangling opportunity finding reference was not rejected: {result.stdout} {result.stderr}")
            return 1

        # Restore opportunity and test research-plan references.
        write_jsonl(records / "opportunities.jsonl", [opportunity])
        bad_plan = deepcopy(research_plan)
        bad_plan["research_question_ids"] = ["RQ-9999"]
        research_plan_path.write_text(json.dumps(bad_plan, indent=2) + "\n", encoding="utf-8")
        result = run_project_validator(project)
        if result.returncode == 0 or "missing research question reference RQ-9999" not in result.stdout:
            print(f"FAIL: dangling research-plan reference was not rejected: {result.stdout} {result.stderr}")
            return 1

        # Restore baseline and confirm recovery.
        research_plan_path.write_text(json.dumps(research_plan, indent=2) + "\n", encoding="utf-8")
        final = run_project_validator(project)
        if final.returncode != 0:
            print(f"FAIL: valid project did not recover after negative tests: {final.stdout} {final.stderr}")
            return 1

    print("PASS: 5 B5 schemas and templates; EVAL-020–030; initialized workspace; research traceability; round/question/participant linkage; negative consent/local-review/reference tests; recovery.")
    print("NOTE: Structural validation does not prove source truth, research quality, or model behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
