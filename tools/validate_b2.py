#!/usr/bin/env python3
"""Validate B2 schemas, synthetic cases, and a temporary project-workspace workflow."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - environment-specific
    print("FAIL: jsonschema is not installed. Run: python -m pip install -r requirements-dev.txt", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def load_schema(name: str):
    schema = json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)


def test_workspace_workflow(errors: list[str]) -> None:
    """Create a temporary workspace and exercise positive/negative integrity paths."""
    with tempfile.TemporaryDirectory(prefix="peanuts-b2-test-") as temp:
        workspace = Path(temp) / "projects"
        init_cmd = [
            sys.executable, str(ROOT / "tools" / "init_project.py"),
            "--id", "b2-test-project", "--title", "B2 Test Project",
            "--mode", "MODE-IDEA", "--outcome", "Test project record continuity",
            "--workspace-root", str(workspace),
        ]
        init = run(init_cmd)
        project_dir = workspace / "b2-test-project"
        if init.returncode != 0 or not project_dir.is_dir():
            errors.append(f"workspace initializer failed: {init.stdout} {init.stderr}")
            return

        validator_cmd = [sys.executable, str(ROOT / "tools" / "validate_project.py"), str(project_dir)]

        def check_pass(label: str) -> bool:
            result = run(validator_cmd)
            if result.returncode != 0:
                errors.append(f"{label}: expected valid project; got {result.stdout} {result.stderr}")
                return False
            return True

        def check_fail(label: str, expected_text: str) -> bool:
            result = run(validator_cmd)
            if result.returncode == 0 or expected_text not in result.stdout:
                errors.append(f"{label}: expected rejection containing {expected_text!r}; got {result.stdout} {result.stderr}")
                return False
            return True

        if not check_pass("new workspace"):
            return

        source = json.loads((ROOT / "templates" / "records" / "source.json").read_text(encoding="utf-8"))
        claim = json.loads((ROOT / "templates" / "records" / "claim.json").read_text(encoding="utf-8"))
        source_path = project_dir / "records" / "sources.jsonl"
        claim_path = project_dir / "records" / "claims.jsonl"
        source_path.write_text(json.dumps(source) + "\n", encoding="utf-8")
        claim_path.write_text(json.dumps(claim) + "\n", encoding="utf-8")
        if not check_pass("valid source/claim links"):
            return

        # Duplicate IDs must fail.
        source_path.write_text(json.dumps(source) + "\n" + json.dumps(source) + "\n", encoding="utf-8")
        if not check_fail("duplicate IDs", "duplicate source_id"):
            return
        source_path.write_text(json.dumps(source) + "\n", encoding="utf-8")

        # A dangling claim reference must fail.
        bad_claim = dict(claim)
        bad_claim["source_ids"] = ["SRC-9999"]
        claim_path.write_text(json.dumps(bad_claim) + "\n", encoding="utf-8")
        if not check_fail("dangling reference", "missing source reference SRC-9999"):
            return
        claim_path.write_text(json.dumps(claim) + "\n", encoding="utf-8")

        # Pending decisions must exist and remain proposed/deferred.
        decision = json.loads((ROOT / "templates" / "records" / "decision.json").read_text(encoding="utf-8"))
        decision_path = project_dir / "records" / "decisions.jsonl"
        decision_path.write_text(json.dumps(decision) + "\n", encoding="utf-8")
        state_path = project_dir / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["pending_decision_ids"] = [decision["decision_id"]]
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        if not check_pass("proposed pending decision"):
            return

        # A selected option must belong to the decision's options.
        invalid_option = dict(decision)
        invalid_option.update({"status":"approved", "selected_option_id":"NOT_AN_OPTION", "decided_at":"2026-10-31T01:00:00Z", "approved_by":"user"})
        decision_path.write_text(json.dumps(invalid_option) + "\n", encoding="utf-8")
        if not check_fail("invalid selected option", "selected_option_id NOT_AN_OPTION"):
            return

        # Even an otherwise valid approval cannot remain on the pending list.
        approved = dict(decision)
        approved.update({"status":"approved", "selected_option_id":approved["options"][0]["option_id"], "decided_at":"2026-10-31T01:00:00Z", "approved_by":"user"})
        decision_path.write_text(json.dumps(approved) + "\n", encoding="utf-8")
        if not check_fail("approved decision still pending", "is not proposed or deferred"):
            return

        # A completed current stage must appear in completed_stages.
        state["pending_decision_ids"] = []
        state["stage_status"] = "completed"
        state["completed_stages"] = []
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        decision_path.write_text("", encoding="utf-8")
        if not check_fail("invalid completed-stage state", "completed current stage must appear"):
            return

        # Evaluation results must refer to a known case; a blocked run is still an actual attempted run.
        state["stage_status"] = "not_started"
        state["current_stage"] = "P1"
        state["completed_stages"] = []
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        result = {
            "result_id":"RUN-0001", "case_id":"EVAL-999", "run_at":"2026-10-31T00:00:00Z",
            "system_version":"b2-test", "runtime":"temporary validation test", "model":None,
            "status":"blocked", "evaluator_type":"deterministic", "evidence":[],
            "dimension_scores":[], "notes":"Temporary schema/cross-reference test only.",
            "limitations":["No Peanuts model evaluation was performed."], "reviewer_approved":False
        }
        results_path = project_dir / "evaluations" / "results.jsonl"
        results_path.write_text(json.dumps(result) + "\n", encoding="utf-8")
        if not check_fail("unknown evaluation case", "not found in repository evals/cases"):
            return
        results_path.write_text("", encoding="utf-8")
        if not check_pass("recovered valid workspace"):
            return

        # No-overwrite must fail without modifying the existing project.
        before = (project_dir / "project.json").read_bytes()
        no_overwrite = run(init_cmd)
        after = (project_dir / "project.json").read_bytes()
        if no_overwrite.returncode == 0 or before != after:
            errors.append("project initializer failed to protect an existing workspace from overwrite")


def main() -> int:
    errors: list[str] = []
    mapping = {
        "project.schema.json": [ROOT / "templates/project/project.json"],
        "project-state.schema.json": [ROOT / "templates/project/state.json"],
        "source-record.schema.json": [ROOT / "templates/records/source.json"],
        "claim-record.schema.json": [ROOT / "templates/records/claim.json"],
        "assumption-record.schema.json": [ROOT / "templates/records/assumption.json"],
        "decision-record.schema.json": [ROOT / "templates/records/decision.json"],
    }
    for schema_name, sample_paths in mapping.items():
        try:
            validator = load_schema(schema_name)
            for path in sample_paths:
                sample = json.loads(path.read_text(encoding="utf-8"))
                for error in validator.iter_errors(sample):
                    errors.append(f"{path.relative_to(ROOT)}: {error.message}")
        except Exception as exc:  # report all validation failures together
            errors.append(f"{schema_name}: {exc}")

    cases_dir = ROOT / "evals" / "cases"
    try:
        case_validator = load_schema("evaluation-case.schema.json")
        cases = sorted(cases_dir.glob("EVAL-*.json"))
        if not cases:
            errors.append("no evaluation case files found")
        for path in cases:
            sample = json.loads(path.read_text(encoding="utf-8"))
            for error in case_validator.iter_errors(sample):
                errors.append(f"{path.relative_to(ROOT)}: {error.message}")
    except Exception as exc:
        errors.append(f"evaluation-case validation: {exc}")

    try:
        load_schema("evaluation-result.schema.json")
    except Exception as exc:
        errors.append(f"evaluation-result.schema.json: {exc}")

    test_workspace_workflow(errors)

    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"PASS: 8 schemas checked; {len(list(cases_dir.glob('EVAL-*.json')))} evaluation cases validated.")
    print("PASS: temporary workspace lifecycle, source/claim traceability, duplicate/dangling-ID rejection, decision/state invariants, evaluation-case references, and no-overwrite behavior.")
    print("NOTE: These are structural/workflow checks. They are not AI performance evaluations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
