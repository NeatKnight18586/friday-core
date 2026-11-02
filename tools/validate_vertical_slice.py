#!/usr/bin/env python3
"""Validate the B4 synthetic vertical-slice fixture and its artifact/record chain."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DEFAULT = ROOT / "examples" / "vertical-slice-synthetic" / "campus-service-status"

RECORDS = {
    "records/sources.jsonl": ("source-record.schema.json", "source_id"),
    "records/claims.jsonl": ("claim-record.schema.json", "claim_id"),
    "records/assumptions.jsonl": ("assumption-record.schema.json", "assumption_id"),
    "records/decisions.jsonl": ("decision-record.schema.json", "decision_id"),
}

REQUIRED_HEADINGS = {
    "artifacts/01-event-dossier.md": ["## 1. Summary", "## 4. Source register", "## 5. Next action"],
    "artifacts/02-problem-brief.md": ["## 1. Target users", "## 5. Evidence", "## 8. Disposition"],
    "artifacts/03-nuts-analogy-card.md": ["## Target function", "## Abstract principle", "## NUTS decision"],
    "artifacts/04-concept-brief.md": ["## 1. One-sentence concept", "## 8. MVP boundary", "## 10. Recommendation"],
    "artifacts/05-quick-council-review.md": ["## Council I", "## Council II", "## Council III", "## Council IV", "## Final decision"],
    "artifacts/06-draft-prd.md": ["## 1. Executive summary", "## 6. Functional requirements", "## 12. Open decisions"],
    "artifacts/07-status-and-handoff.md": ["## Completed stages", "## Pending decision", "## Exact next action"],
}


def load_json(path: Path, errors: list[str], label: str):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: cannot read valid JSON: {exc}")
        return None


def safe_file(root: Path, relative: str, errors: list[str], label: str) -> Path | None:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        errors.append(f"{label}: path must be relative and cannot traverse parents: {relative}")
        return None
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label}: path escapes fixture directory: {relative}")
        return None
    if not resolved.is_file():
        errors.append(f"{label}: required file is missing: {relative}")
        return None
    return resolved


def read_jsonl(path: Path, schema_path: Path, errors: list[str], label: str, id_key: str) -> list[dict]:
    rows: list[dict] = []
    try:
        validator = Draft202012Validator(
            json.loads(schema_path.read_text(encoding="utf-8")),
            format_checker=FormatChecker(),
        )
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: cannot load file/schema: {exc}")
        return rows
    seen: set[str] = set()
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"{label}:{line_no}: invalid JSON: {exc}")
            continue
        for issue in validator.iter_errors(obj):
            errors.append(f"{label}:{line_no}: {issue.message}")
        if isinstance(obj, dict):
            record_id = obj.get(id_key)
            if record_id in seen:
                errors.append(f"{label}:{line_no}: duplicate {id_key} {record_id}")
            if record_id:
                seen.add(record_id)
            rows.append(obj)
    return rows


def validate_fixture(fixture: Path) -> list[str]:
    errors: list[str] = []
    fixture = fixture.expanduser().resolve()
    if not fixture.is_dir():
        return [f"fixture directory does not exist: {fixture}"]

    run_path = safe_file(fixture, "vertical-slice-run.json", errors, "run manifest")
    if run_path is None:
        return errors
    run = load_json(run_path, errors, "vertical-slice-run.json")
    if not isinstance(run, dict):
        return errors

    try:
        schema = json.loads((ROOT / "schemas/vertical-slice-run.schema.json").read_text(encoding="utf-8"))
        run_validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for issue in run_validator.iter_errors(run):
            errors.append(f"vertical-slice-run.json: {issue.message}")
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load vertical-slice-run schema: {exc}"]

    project_path = safe_file(fixture, "project.json", errors, "project record")
    state_path = safe_file(fixture, "state.json", errors, "project state")
    if project_path:
        project = load_json(project_path, errors, "project.json")
        try:
            schema = json.loads((ROOT / "schemas/project.schema.json").read_text(encoding="utf-8"))
            for issue in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(project):
                errors.append(f"project.json: {issue.message}")
            if project.get("project_id") != run.get("project_id"):
                errors.append("project.json: project_id does not match run manifest")
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            errors.append(f"project.json: schema validation failed: {exc}")
    if state_path:
        state = load_json(state_path, errors, "state.json")
        try:
            schema = json.loads((ROOT / "schemas/project-state.schema.json").read_text(encoding="utf-8"))
            for issue in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(state):
                errors.append(f"state.json: {issue.message}")
            if state.get("project_id") != run.get("project_id"):
                errors.append("state.json: project_id does not match run manifest")
        except (OSError, json.JSONDecodeError, AttributeError) as exc:
            errors.append(f"state.json: schema validation failed: {exc}")

    record_data: dict[str, list[dict]] = {}
    for relative, (schema_name, id_key) in RECORDS.items():
        record_path = safe_file(fixture, relative, errors, "record file")
        if record_path:
            record_data[relative] = read_jsonl(
                record_path, ROOT / "schemas" / schema_name, errors, relative, id_key
            )

    sources = {row.get("source_id") for row in record_data.get("records/sources.jsonl", [])}
    claims = {row.get("claim_id") for row in record_data.get("records/claims.jsonl", [])}
    assumptions = {row.get("assumption_id") for row in record_data.get("records/assumptions.jsonl", [])}
    decisions = {row.get("decision_id") for row in record_data.get("records/decisions.jsonl", [])}

    for row in record_data.get("records/claims.jsonl", []):
        for ref in row.get("source_ids", []):
            if ref not in sources:
                errors.append(f"claim {row.get('claim_id')}: source reference {ref} is missing")
    for row in record_data.get("records/assumptions.jsonl", []):
        for ref in row.get("related_claim_ids", []):
            if ref not in claims:
                errors.append(f"assumption {row.get('assumption_id')}: claim reference {ref} is missing")
        for ref in row.get("affected_decision_ids", []):
            if ref not in decisions:
                errors.append(f"assumption {row.get('assumption_id')}: decision reference {ref} is missing")
    for row in record_data.get("records/decisions.jsonl", []):
        for ref_obj in row.get("evidence_refs", []):
            if ref_obj.get("record_type") == "source" and ref_obj.get("record_id") not in sources:
                errors.append(f"decision {row.get('decision_id')}: source reference {ref_obj.get('record_id')} is missing")
            if ref_obj.get("record_type") == "claim" and ref_obj.get("record_id") not in claims:
                errors.append(f"decision {row.get('decision_id')}: claim reference {ref_obj.get('record_id')} is missing")
            if ref_obj.get("record_type") == "assumption" and ref_obj.get("record_id") not in assumptions:
                errors.append(f"decision {row.get('decision_id')}: assumption reference {ref_obj.get('record_id')} is missing")

    if state_path and isinstance(state, dict):
        pending = set(state.get("pending_decision_ids", []))
        for decision_id in pending:
            matching = [row for row in record_data.get("records/decisions.jsonl", []) if row.get("decision_id") == decision_id]
            if not matching or matching[0].get("status") not in {"proposed", "deferred"}:
                errors.append(f"state.json: pending decision {decision_id} is missing or not proposed/deferred")

    stage_records = run.get("stage_records", [])
    stage_ids = [row.get("stage_id") for row in stage_records]
    if len(stage_ids) != len(set(stage_ids)):
        errors.append("vertical-slice-run.json: duplicate stage_id")
    if set(stage_ids) != {"P1", "P2", "P3", "P4", "P5", "P6", "P7"}:
        errors.append("vertical-slice-run.json: vertical slice must account for P1 through P7")

    artifact_paths = set(run.get("required_artifacts", []))
    for row in stage_records:
        path = row.get("artifact", "")
        if path not in artifact_paths:
            errors.append(f"stage {row.get('stage_id')}: artifact is not listed in required_artifacts")
        safe_file(fixture, path, errors, f"stage {row.get('stage_id')} artifact")
    for relative in run.get("required_artifacts", []):
        artifact = safe_file(fixture, relative, errors, "required artifact")
        if artifact:
            content = artifact.read_text(encoding="utf-8")
            if run.get("scenario_type") == "synthetic" and "SYNTHETIC TEST DATA" not in content:
                errors.append(f"{relative}: synthetic scenario must be clearly labelled")
            for heading in REQUIRED_HEADINGS.get(relative, []):
                if heading not in content:
                    errors.append(f"{relative}: required section missing: {heading}")

    if run.get("scenario_type") == "synthetic":
        if "No real user interviews" not in " ".join(run.get("limitations", [])):
            errors.append("synthetic run must disclose that no real user interviews were performed")
        if run.get("decision_disposition") != "VALIDATE":
            errors.append("synthetic example with unvalidated user assumptions must not be presented as an unconditional advance")
    if run.get("workflow_status") == "complete_with_open_validation" and run.get("decision_disposition") not in {"VALIDATE", "REVISE", "PIVOT", "STOP"}:
        errors.append("open validation state must use a non-final/conditional disposition")

    if errors:
        return errors
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", nargs="?", type=Path, default=FIXTURE_DEFAULT)
    args = parser.parse_args()
    errors = validate_fixture(args.fixture)
    if errors:
        print(f"FAIL: {len(errors)} vertical-slice issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: B4 vertical-slice schemas, source/claim/assumption/decision links, stage coverage, artifact continuity, synthetic-data labeling, and handoff invariants.")
    print("NOTE: This is structural validation of a synthetic fixture; it is not an LLM runtime or real-user evaluation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
