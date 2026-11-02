#!/usr/bin/env python3
"""Validate B6 NUTS schemas, evaluation cases, and project-level traceability."""
from __future__ import annotations

import json
import sys
import tempfile
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


def validator(schema_name: str):
    schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def call_main(module_name: str, argv: list[str]):
    import importlib
    from io import StringIO
    from types import SimpleNamespace

    module = importlib.import_module(module_name)
    previous = sys.argv[:]
    out, err = StringIO(), StringIO()
    sys.argv = [module_name.replace(".", "/") + ".py", *argv]
    try:
        code = module.main()
    except SystemExit as exc:
        code = int(exc.code or 0)
    finally:
        sys.argv = previous
    return SimpleNamespace(returncode=code, stdout=out.getvalue(), stderr=err.getvalue())


def validate_project(project: Path):
    from contextlib import redirect_stderr, redirect_stdout
    from io import StringIO
    from types import SimpleNamespace
    import tools.validate_project as module

    previous = sys.argv[:]
    out, err = StringIO(), StringIO()
    sys.argv = ["tools/validate_project.py", str(project)]
    try:
        with redirect_stdout(out), redirect_stderr(err):
            code = module.main()
    finally:
        sys.argv = previous
    return SimpleNamespace(returncode=code, stdout=out.getvalue(), stderr=err.getvalue())


def main() -> int:
    errors: list[str] = []
    examples = {
        "analogy-card.schema.json": ROOT / "templates/records/analogy-card.json",
        "nuts-run.schema.json": ROOT / "templates/records/nuts-run.json",
    }
    for schema_name, example_path in examples.items():
        try:
            v = validator(schema_name)
            sample = json.loads(example_path.read_text(encoding="utf-8"))
            for issue in v.iter_errors(sample):
                errors.append(f"{example_path.relative_to(ROOT)}: {issue.message}")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{schema_name}: {exc}")

    eval_v = validator("evaluation-case.schema.json")
    for number in range(31, 39):
        path = ROOT / "evals/cases" / f"EVAL-{number:03d}.json"
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
            for issue in eval_v.iter_errors(case):
                errors.append(f"{path.relative_to(ROOT)}: {issue.message}")
            if case.get("case_status") != "ready":
                errors.append(f"{path.relative_to(ROOT)}: B6 case must be ready for runtime evaluation")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if errors:
        print(f"FAIL: {len(errors)} B6 schema/template/evaluation issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    with tempfile.TemporaryDirectory(prefix="peanuts-b6-") as temp:
        workspace = Path(temp) / "projects"
        init = call_main("tools.init_project", [
            "--id", "b6-nuts-test", "--title", "B6 NUTS Test", "--mode", "MODE-IDEA",
            "--outcome", "Test NUTS record validation", "--workspace-root", str(workspace),
        ])
        project = workspace / "b6-nuts-test"
        if init.returncode != 0 or not project.is_dir():
            print("FAIL: B6 test project could not be initialized")
            return 1
        baseline = validate_project(project)
        if baseline.returncode != 0:
            print(f"FAIL: initialized project did not validate: {baseline.stdout} {baseline.stderr}")
            return 1

        source = json.loads((ROOT / "templates/records/source.json").read_text(encoding="utf-8"))
        claim = json.loads((ROOT / "templates/records/claim.json").read_text(encoding="utf-8"))
        claim.update({
            "claim_id": "CLM-0001", "origin_type": "source", "source_ids": [source["source_id"]],
            "evidence_status": "supported", "confidence": "medium",
            "evidence_summary": "Synthetic validator fixture; not a real research finding."
        })
        card = json.loads((ROOT / "templates/records/analogy-card.json").read_text(encoding="utf-8"))
        card.update({
            "status": "retained_for_test",
            "source_ids": [source["source_id"]],
            "claim_ids": [claim["claim_id"]],
            "assessment": {
                "source_accuracy": "partially_verified", "functional_relevance": "adequate",
                "relational_mapping": "adequate", "context_fit": "adequate", "incremental_value": "unknown",
                "testability": "strong", "disposition": "plausible_needs_test",
                "rationale": "Synthetic test fixture with traceable records and an explicit need for testing.",
                "reviewed_at": "2026-11-01T00:00:00Z"
            }
        })
        run = json.loads((ROOT / "templates/records/nuts-run.json").read_text(encoding="utf-8"))
        run.update({
            "status": "completed", "analogy_ids": [card["analogy_id"]],
            "source_ids": [source["source_id"]], "claim_ids": [claim["claim_id"]],
            "conclusion": "useful_analogy_found",
            "conclusion_rationale": "Synthetic validator scenario only; no external analogy or research is claimed."
        })
        records = project / "records"
        write_jsonl(records / "sources.jsonl", [source])
        write_jsonl(records / "claims.jsonl", [claim])
        write_jsonl(records / "analogies.jsonl", [card])
        write_jsonl(records / "nuts-runs.jsonl", [run])

        result = validate_project(project)
        if result.returncode != 0:
            print(f"FAIL: valid linked NUTS records rejected: {result.stdout} {result.stderr}")
            return 1

        # Dangling source reference must fail.
        bad_card = deepcopy(card)
        bad_card["source_ids"] = ["SRC-9999"]
        write_jsonl(records / "analogies.jsonl", [bad_card])
        result = validate_project(project)
        if result.returncode == 0 or "missing source reference SRC-9999" not in result.stdout:
            print(f"FAIL: dangling analogy source reference accepted: {result.stdout} {result.stderr}")
            return 1

        # Restore card and check dangling claim.
        write_jsonl(records / "analogies.jsonl", [card])
        bad_card = deepcopy(card)
        bad_card["claim_ids"] = ["CLM-9999"]
        write_jsonl(records / "analogies.jsonl", [bad_card])
        result = validate_project(project)
        if result.returncode == 0 or "missing claim reference CLM-9999" not in result.stdout:
            print(f"FAIL: dangling analogy claim reference accepted: {result.stdout} {result.stderr}")
            return 1

        # Retained-for-test with unverified source accuracy must fail schema validation.
        bad_card = deepcopy(card)
        bad_card["assessment"]["source_accuracy"] = "unverified"
        card_v = validator("analogy-card.schema.json")
        if not list(card_v.iter_errors(bad_card)):
            print("FAIL: retained_for_test card with unverified source was accepted")
            return 1

        # Useful analogy run must point to an existing analogy record.
        write_jsonl(records / "analogies.jsonl", [card])
        bad_run = deepcopy(run)
        bad_run["analogy_ids"] = ["ANL-9999"]
        write_jsonl(records / "nuts-runs.jsonl", [bad_run])
        result = validate_project(project)
        if result.returncode == 0 or "missing analogy reference ANL-9999" not in result.stdout:
            print(f"FAIL: dangling NUTS-run analogy reference accepted: {result.stdout} {result.stderr}")
            return 1

        # A no-useful-analogy conclusion must not point to cards.
        write_jsonl(records / "nuts-runs.jsonl", [run])
        no_analogy = deepcopy(run)
        no_analogy.update({"conclusion": "no_useful_analogy", "conclusion_rationale": "A bounded search of relevant sources found no mechanism with sufficient relational fit.", "analogy_ids": [card["analogy_id"]]})
        run_v = validator("nuts-run.schema.json")
        if not list(run_v.iter_errors(no_analogy)):
            print("FAIL: no_useful_analogy record with analogy IDs was accepted")
            return 1

        # Recovery to valid state.
        write_jsonl(records / "nuts-runs.jsonl", [run])
        final = validate_project(project)
        if final.returncode != 0:
            print(f"FAIL: project did not recover after negative tests: {final.stdout} {final.stderr}")
            return 1

        # Backward compatibility: older project workspaces may not have B6 ledgers.
        (records / "analogies.jsonl").unlink()
        (records / "nuts-runs.jsonl").unlink()
        legacy = validate_project(project)
        legacy_warnings = (
            "records/analogies.jsonl" in legacy.stdout
            and "records/nuts-runs.jsonl" in legacy.stdout
            and "legacy project has no optional milestone ledger" in legacy.stdout
        )
        if legacy.returncode != 0 or not legacy_warnings:
            print(f"FAIL: legacy project without B6 ledgers was not handled safely: {legacy.stdout} {legacy.stderr}")
            return 1

    print("PASS: B6 analogy/run schemas and templates; EVAL-031–038; project initialization; source/claim/analogy traceability; retained-card evidence gate; useful/no-useful analogy invariants; negative tests; recovery; and backward-compatible legacy handling.")
    print("NOTE: Structural validation does not establish the truth of analogy sources, originality, transfer feasibility, or model performance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
