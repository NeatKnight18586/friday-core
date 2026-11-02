#!/usr/bin/env python3
"""Validate a Peanuts project workspace, JSON/JSONL schemas and cross-record links."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - environment-specific
    Draft202012Validator = None
    FormatChecker = None

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
OPTIONAL_LEGACY_RECORDS = {"analogies.jsonl", "nuts-runs.jsonl", "assumption-tests.jsonl", "council-reviews.jsonl", "requirements.jsonl", "acceptance-tests.jsonl", "build-tasks.jsonl", "artifacts.jsonl"}

RECORDS = {
    "sources.jsonl": ("source-record.schema.json", "source_id"),
    "claims.jsonl": ("claim-record.schema.json", "claim_id"),
    "assumptions.jsonl": ("assumption-record.schema.json", "assumption_id"),
    "decisions.jsonl": ("decision-record.schema.json", "decision_id"),
    "evaluations/results.jsonl": ("evaluation-result.schema.json", "result_id"),
    "research-questions.jsonl": ("research-question.schema.json", "question_id"),
    "research-findings.jsonl": ("research-finding.schema.json", "finding_id"),
    "research-rounds.jsonl": ("research-round.schema.json", "round_id"),
    "opportunities.jsonl": ("opportunity-record.schema.json", "opportunity_id"),
    "analogies.jsonl": ("analogy-card.schema.json", "analogy_id"),
    "nuts-runs.jsonl": ("nuts-run.schema.json", "run_id"),
    "assumption-tests.jsonl": ("assumption-test.schema.json", "test_id"),
    "council-reviews.jsonl": ("council-review.schema.json", "review_id"),
    "requirements.jsonl": ("requirement-record.schema.json", "requirement_id"),
    "acceptance-tests.jsonl": ("acceptance-test.schema.json", "test_id"),
    "build-tasks.jsonl": ("build-task.schema.json", "task_id"),
    "artifacts.jsonl": ("artifact-record.schema.json", "artifact_id"),
}


def load_validator(schema_name: str):
    schema = json.loads((SCHEMAS / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_one(data, validator, label, errors):
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        path = ".".join(str(x) for x in err.absolute_path) or "$"
        errors.append(f"{label}:{path}: {err.message}")


def read_json(path: Path, label: str, validator, errors):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: cannot read valid JSON: {exc}")
        return None
    validate_one(data, validator, label, errors)
    return data


def read_jsonl(path: Path, label: str, validator, id_key: str, errors):
    rows = []
    seen = set()
    if not path.exists():
        errors.append(f"{label}: required JSONL file is missing")
        return rows
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}:{lineno}: invalid JSON: {exc}")
            continue
        validate_one(obj, validator, f"{label}:{lineno}", errors)
        rid = obj.get(id_key) if isinstance(obj, dict) else None
        if rid in seen:
            errors.append(f"{label}:{lineno}: duplicate {id_key} {rid}")
        elif rid:
            seen.add(rid)
        rows.append(obj)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_dir", type=Path, help="Path to a project workspace")
    args = parser.parse_args()
    project_dir = args.project_dir.expanduser().resolve()
    errors = []
    if not project_dir.is_dir():
        print(f"FAIL: project directory does not exist: {project_dir}", file=sys.stderr)
        return 2

    if Draft202012Validator is None:
        print("FAIL: jsonschema is not installed. Run: python -m pip install -r requirements-dev.txt", file=sys.stderr)
        return 2

    try:
        project_v = load_validator("project.schema.json")
        state_v = load_validator("project-state.schema.json")
        research_plan_v = load_validator("research-plan.schema.json")
        demo_plan_v = load_validator("demo-plan.schema.json")
        record_vs = {name: load_validator(schema) for name, (schema, _) in RECORDS.items()}
    except Exception as exc:
        print(f"FAIL: cannot load/validate JSON Schemas: {exc}", file=sys.stderr)
        print("Install development dependencies: python -m pip install -r requirements-dev.txt", file=sys.stderr)
        return 2

    project = read_json(project_dir / "project.json", "project.json", project_v, errors)
    state = read_json(project_dir / "state.json", "state.json", state_v, errors)
    research_plan = read_json(project_dir / "research-plan.json", "research-plan.json", research_plan_v, errors)
    migration_notes = []
    demo_plan_path = project_dir / "demo-plan.json"
    if demo_plan_path.exists():
        demo_plan = read_json(demo_plan_path, "demo-plan.json", demo_plan_v, errors)
    else:
        demo_plan = None
        migration_notes.append("demo-plan.json: legacy project has no B8 demo plan; it will be treated as not yet initialized")
    data = {}
    for filename, (schema_name, id_key) in RECORDS.items():
        if filename.startswith("evaluations/"):
            rel_path = Path(filename)
            full_path = project_dir / rel_path
        else:
            rel_path = Path("records") / filename
            full_path = project_dir / rel_path
        if filename in OPTIONAL_LEGACY_RECORDS and not full_path.exists():
            data[filename] = []
            migration_notes.append(f"{rel_path.as_posix()}: legacy project has no optional milestone ledger; it will be treated as empty until initialized")
        else:
            data[filename] = read_jsonl(full_path, rel_path.as_posix(), record_vs[filename], id_key, errors)

    if project and state and isinstance(project, dict) and isinstance(state, dict):
        if project.get("project_id") != project_dir.name:
            errors.append("project.json: project_id does not match the project directory name")
        if project.get("project_id") != state.get("project_id"):
            errors.append("state.json: project_id does not match project.json")
        if project.get("lifecycle_status") != state.get("lifecycle_status"):
            errors.append("state.json: lifecycle_status does not match project.json")
        if state.get("stage_status") == "completed" and state.get("current_stage") not in state.get("completed_stages", []):
            errors.append("state.json: a completed current stage must appear in completed_stages")

    source_ids = {x.get("source_id") for x in data["sources.jsonl"] if isinstance(x, dict)}
    claim_ids = {x.get("claim_id") for x in data["claims.jsonl"] if isinstance(x, dict)}
    assumption_ids = {x.get("assumption_id") for x in data["assumptions.jsonl"] if isinstance(x, dict)}
    decision_ids = {x.get("decision_id") for x in data["decisions.jsonl"] if isinstance(x, dict)}
    question_ids = {x.get("question_id") for x in data["research-questions.jsonl"] if isinstance(x, dict)}
    finding_ids = {x.get("finding_id") for x in data["research-findings.jsonl"] if isinstance(x, dict)}
    round_ids = {x.get("round_id") for x in data["research-rounds.jsonl"] if isinstance(x, dict)}
    analogy_ids = {a.get("analogy_id") for a in data["analogies.jsonl"] if isinstance(a, dict)}

    for row_no, claim in enumerate(data["claims.jsonl"], start=1):
        if not isinstance(claim, dict):
            continue
        for ref in claim.get("source_ids", []):
            if ref not in source_ids:
                errors.append(f"records/claims.jsonl:{row_no}: missing source reference {ref}")
        sup = claim.get("supersedes_claim_id")
        if sup and sup not in claim_ids:
            errors.append(f"records/claims.jsonl:{row_no}: superseded claim {sup} not found")

    for row_no, assumption in enumerate(data["assumptions.jsonl"], start=1):
        if not isinstance(assumption, dict):
            continue
        for ref in assumption.get("related_claim_ids", []):
            if ref not in claim_ids:
                errors.append(f"records/assumptions.jsonl:{row_no}: missing claim reference {ref}")
        for ref in assumption.get("affected_decision_ids", []):
            if ref not in decision_ids:
                errors.append(f"records/assumptions.jsonl:{row_no}: missing decision reference {ref}")

    for row_no, decision in enumerate(data["decisions.jsonl"], start=1):
        if not isinstance(decision, dict):
            continue
        for ref_obj in decision.get("evidence_refs", []):
            if not isinstance(ref_obj, dict):
                continue
            rtype, rid = ref_obj.get("record_type"), ref_obj.get("record_id")
            lookup = {"source": source_ids, "claim": claim_ids, "assumption": assumption_ids}
            if rtype in lookup and rid not in lookup[rtype]:
                errors.append(f"records/decisions.jsonl:{row_no}: missing {rtype} reference {rid}")
        sup = decision.get("supersedes_decision_id")
        if sup and sup not in decision_ids:
            errors.append(f"records/decisions.jsonl:{row_no}: superseded decision {sup} not found")
        selected = decision.get("selected_option_id")
        option_ids = {opt.get("option_id") for opt in decision.get("options", []) if isinstance(opt, dict)}
        if selected and selected not in option_ids:
            errors.append(f"records/decisions.jsonl:{row_no}: selected_option_id {selected} is not one of the recorded options")

    for row_no, question in enumerate(data["research-questions.jsonl"], start=1):
        if not isinstance(question, dict):
            continue
        for ref in question.get("answer_claim_ids", []):
            if ref not in claim_ids:
                errors.append(f"records/research-questions.jsonl:{row_no}: missing claim reference {ref}")

    for row_no, research_round in enumerate(data["research-rounds.jsonl"], start=1):
        if not isinstance(research_round, dict):
            continue
        for ref in research_round.get("research_question_ids", []):
            if ref not in question_ids:
                errors.append(f"records/research-rounds.jsonl:{row_no}: missing research question reference {ref}")

    round_by_id = {r.get("round_id"): r for r in data["research-rounds.jsonl"] if isinstance(r, dict)}
    for row_no, finding in enumerate(data["research-findings.jsonl"], start=1):
        if not isinstance(finding, dict):
            continue
        for ref in finding.get("source_ids", []):
            if ref not in source_ids:
                errors.append(f"records/research-findings.jsonl:{row_no}: missing source reference {ref}")
        for ref in finding.get("claim_ids", []):
            if ref not in claim_ids:
                errors.append(f"records/research-findings.jsonl:{row_no}: missing claim reference {ref}")
        for ref in finding.get("question_ids", []):
            if ref not in question_ids:
                errors.append(f"records/research-findings.jsonl:{row_no}: missing research question reference {ref}")
        round_ref = finding.get("round_id")
        participant_ref = finding.get("participant_ref")
        if round_ref and round_ref not in round_ids:
            errors.append(f"records/research-findings.jsonl:{row_no}: missing research round reference {round_ref}")
        elif round_ref:
            linked_round = round_by_id[round_ref]
            round_questions = set(linked_round.get("research_question_ids", []))
            for question_ref in finding.get("question_ids", []):
                if question_ref not in round_questions:
                    errors.append(
                        f"records/research-findings.jsonl:{row_no}: question {question_ref} "
                        f"is not linked to research round {round_ref}"
                    )
            if participant_ref and participant_ref not in set(linked_round.get("participant_refs", [])):
                errors.append(
                    f"records/research-findings.jsonl:{row_no}: participant {participant_ref} "
                    f"is not listed in research round {round_ref}"
                )

    for row_no, opportunity in enumerate(data["opportunities.jsonl"], start=1):
        if not isinstance(opportunity, dict):
            continue
        for ref in opportunity.get("finding_ids", []):
            if ref not in finding_ids:
                errors.append(f"records/opportunities.jsonl:{row_no}: missing finding reference {ref}")
        for ref in opportunity.get("claim_ids", []):
            if ref not in claim_ids:
                errors.append(f"records/opportunities.jsonl:{row_no}: missing claim reference {ref}")
        for ref in opportunity.get("unresolved_questions", []):
            if ref not in question_ids:
                errors.append(f"records/opportunities.jsonl:{row_no}: missing research question reference {ref}")

    for row_no, analogy in enumerate(data["analogies.jsonl"], start=1):
        if not isinstance(analogy, dict):
            continue
        for ref in analogy.get("source_ids", []):
            if ref not in source_ids:
                errors.append(f"records/analogies.jsonl:{row_no}: missing source reference {ref}")
        for ref in analogy.get("claim_ids", []):
            if ref not in claim_ids:
                errors.append(f"records/analogies.jsonl:{row_no}: missing claim reference {ref}")

    for row_no, nuts_run in enumerate(data["nuts-runs.jsonl"], start=1):
        if not isinstance(nuts_run, dict):
            continue
        for ref in nuts_run.get("analogy_ids", []):
            if ref not in analogy_ids:
                errors.append(f"records/nuts-runs.jsonl:{row_no}: missing analogy reference {ref}")
        for ref in nuts_run.get("source_ids", []):
            if ref not in source_ids:
                errors.append(f"records/nuts-runs.jsonl:{row_no}: missing source reference {ref}")
        for ref in nuts_run.get("claim_ids", []):
            if ref not in claim_ids:
                errors.append(f"records/nuts-runs.jsonl:{row_no}: missing claim reference {ref}")
        conclusion = nuts_run.get("conclusion")
        if conclusion == "useful_analogy_found" and not nuts_run.get("analogy_ids"):
            errors.append(f"records/nuts-runs.jsonl:{row_no}: useful_analogy_found requires at least one analogy reference")
        if conclusion == "no_useful_analogy" and nuts_run.get("analogy_ids"):
            errors.append(f"records/nuts-runs.jsonl:{row_no}: no_useful_analogy must not reference retained analogy cards")

    if isinstance(research_plan, dict):
        if project and research_plan.get("project_id") != project.get("project_id"):
            errors.append("research-plan.json: project_id does not match project.json")
        for ref in research_plan.get("research_question_ids", []):
            if ref not in question_ids:
                errors.append(f"research-plan.json: missing research question reference {ref}")
        for ref in research_plan.get("research_round_ids", []):
            if ref not in round_ids:
                errors.append(f"research-plan.json: missing research round reference {ref}")
        for ref in research_plan.get("priority_claim_ids", []):
            if ref not in claim_ids:
                errors.append(f"research-plan.json: missing claim reference {ref}")

    # B7 semantic rules: review provenance, assumption-test links, and non-compensatory gates.
    try:
        try:
            from tools.b7_rules import validate_b7_records
        except ModuleNotFoundError:
            # Direct execution as `python tools/validate_project.py` places
            # tools/ (not the repository root) on sys.path.
            from b7_rules import validate_b7_records
        errors.extend(validate_b7_records(
            council_reviews=data["council-reviews.jsonl"],
            assumption_tests=data["assumption-tests.jsonl"],
            assumptions=data["assumptions.jsonl"],
            sources=data["sources.jsonl"],
            claims=data["claims.jsonl"],
            decisions=data["decisions.jsonl"],
            research_findings=data["research-findings.jsonl"],
            opportunities=data["opportunities.jsonl"],
            analogies=data["analogies.jsonl"],
            nuts_runs=data["nuts-runs.jsonl"],
            project_id=project.get("project_id") if isinstance(project, dict) else None,
        ))
    except Exception as exc:
        errors.append(f"B7 semantic validation could not run: {type(exc).__name__}: {exc}")

    # B8 semantic checks are additive: legacy workspaces remain readable, while
    # new workspaces receive requirement, acceptance-test, task and artifact ledgers.
    try:
        try:
            from tools.b8_rules import validate_b8_records
        except ModuleNotFoundError:
            from b8_rules import validate_b8_records
        errors.extend(validate_b8_records(
            project_dir=project_dir,
            requirements=data["requirements.jsonl"],
            acceptance_tests=data["acceptance-tests.jsonl"],
            build_tasks=data["build-tasks.jsonl"],
            artifacts=data["artifacts.jsonl"],
            demo_plan=demo_plan,
            sources=data["sources.jsonl"],
            claims=data["claims.jsonl"],
            assumptions=data["assumptions.jsonl"],
            decisions=data["decisions.jsonl"],
            findings=data["research-findings.jsonl"],
            opportunities=data["opportunities.jsonl"],
            analogies=data["analogies.jsonl"],
            nuts_runs=data["nuts-runs.jsonl"],
            council_reviews=data["council-reviews.jsonl"],
            assumption_tests=data["assumption-tests.jsonl"],
            evaluation_results=data["evaluations/results.jsonl"],
            artifact_ledger_present=(project_dir / "records" / "artifacts.jsonl").exists(),
            state=state if isinstance(state, dict) else None,
        ))
    except Exception as exc:
        errors.append(f"B8 semantic validation could not run: {type(exc).__name__}: {exc}")

    if isinstance(state, dict):
        decision_by_id = {d.get("decision_id"): d for d in data["decisions.jsonl"] if isinstance(d, dict)}
        for ref in state.get("pending_decision_ids", []):
            if ref not in decision_ids:
                errors.append(f"state.json: pending decision reference {ref} not found")
            elif decision_by_id[ref].get("status") not in {"proposed", "deferred"}:
                errors.append(f"state.json: pending decision {ref} is not proposed or deferred")

    case_ids = set()
    for case_path in (ROOT / "evals" / "cases").glob("EVAL-*.json"):
        try:
            case_ids.add(json.loads(case_path.read_text(encoding="utf-8")).get("case_id"))
        except (OSError, json.JSONDecodeError):
            continue
    for row_no, result in enumerate(data["evaluations/results.jsonl"], start=1):
        if isinstance(result, dict) and result.get("case_id") not in case_ids:
            errors.append(f"evaluations/results.jsonl:{row_no}: evaluation case {result.get('case_id')} not found in repository evals/cases")

    if errors:
        print(f"FAIL: {len(errors)} issue(s) in {project_dir}")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"PASS: project record schemas, JSONL records, unique IDs, and cross-record references: {project_dir}")
    for note in migration_notes:
        print(f"WARNING: {note}")
    print("NOTE: structural integrity does not establish factual truth, source credibility, or project viability.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
