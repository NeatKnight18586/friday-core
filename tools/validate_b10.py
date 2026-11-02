#!/usr/bin/env python3
"""Validate B10 ChatGPT-primary acceptance cases and recorded live-run evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError as exc:  # pragma: no cover
    print(f"ERROR: missing validation dependency: {exc}", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]


def validate_b10(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    case_schema = json.loads((root / "schemas/evaluation-case.schema.json").read_text(encoding="utf-8"))
    result_schema = json.loads((root / "schemas/evaluation-result.schema.json").read_text(encoding="utf-8"))
    case_validator = Draft202012Validator(case_schema)
    result_validator = Draft202012Validator(result_schema, format_checker=FormatChecker())

    case_ids: set[str] = set()
    for number in range(103, 135):
        path = root / "evals/cases" / f"EVAL-{number:03d}.json"
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
            continue
        for issue in case_validator.iter_errors(case):
            errors.append(f"{path.relative_to(root)}: {list(issue.absolute_path)}: {issue.message}")
        if case.get("case_id") in case_ids:
            errors.append(f"duplicate B10 case id: {case.get('case_id')}")
        case_ids.add(case.get("case_id"))
        if case.get("case_status") != "ready":
            errors.append(f"{path.relative_to(root)}: B10 evaluation case must be ready")
        for rubric_ref in case.get("rubric_refs", []):
            if not (root / "evals/rubrics" / rubric_ref).is_file():
                errors.append(f"{path.relative_to(root)}: missing rubric reference {rubric_ref}")
    if len(case_ids) != 32:
        errors.append(f"expected 32 B10 evaluation cases (EVAL-103–134), found {len(case_ids)}")

    result_path = root / "evals/results/results.jsonl"
    results: dict[str, dict] = {}
    try:
        lines = result_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return errors + [f"cannot read evaluation results: {exc}"]
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"evals/results/results.jsonl:{line_no}: invalid JSON: {exc}")
            continue
        for issue in result_validator.iter_errors(record):
            errors.append(f"evals/results/results.jsonl:{line_no}: {list(issue.absolute_path)}: {issue.message}")
        result_id = record.get("result_id")
        if result_id in results:
            errors.append(f"duplicate evaluation result id: {result_id}")
        results[result_id] = record

    # These cases require owner-controlled Project UI, repeatability, or actual host-runtime evidence.
    required_blocked = (
        "EVAL-117", "EVAL-118", "EVAL-122",
        "EVAL-127", "EVAL-128", "EVAL-129", "EVAL-130", "EVAL-131",
    )
    for case_id in required_blocked:
        matching = [r for r in results.values() if r.get("case_id") == case_id]
        if len(matching) != 1:
            errors.append(f"expected exactly one explicit result record for {case_id}; found {len(matching)}")
        elif matching[0].get("status") != "blocked":
            errors.append(f"{case_id} must remain blocked until the required target Project UI, host-runtime, repeatability or independent-calibration evidence exists")

    # Deterministic host-fixture checks are recorded as passes; real host/model runs remain blocked.
    expected_cross_host = {
        "EVAL-123": "passed",
        "EVAL-124": "passed",
        "EVAL-125": "passed",
        "EVAL-126": "passed",
        "EVAL-127": "blocked",
        "EVAL-128": "blocked",
        "EVAL-129": "blocked",
        "EVAL-130": "blocked",
        "EVAL-131": "blocked",
        "EVAL-132": "passed",
        "EVAL-133": "passed",
        "EVAL-134": "passed",
    }
    for case_id, expected_status in expected_cross_host.items():
        matching = [r for r in results.values() if r.get("case_id") == case_id]
        if len(matching) != 1:
            errors.append(f"expected exactly one cross-host result record for {case_id}; found {len(matching)}")
        elif matching[0].get("status") != expected_status:
            errors.append(f"{case_id} must remain {expected_status} based on available evidence")
        elif matching[0].get("reviewer_approved") is not False:
            errors.append(f"{case_id} result must remain unapproved pending owner review")

    doc_path = root / "docs/acceptance/CHATGPT_PRIMARY_RUNTIME_ACCEPTANCE.md"
    if not doc_path.is_file():
        errors.append("missing ChatGPT primary runtime acceptance protocol")
    else:
        text = doc_path.read_text(encoding="utf-8").lower()
        for phrase in ("not run", "project ui", "fresh project", "five", "self-evaluation", "codex", "claude code"):
            if phrase not in text:
                errors.append(f"B10 acceptance protocol missing disclosure phrase: {phrase}")

    return errors


def main() -> int:
    errors = validate_b10()
    if errors:
        print(f"FAIL: {len(errors)} B10 validation issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: 32 B10 evaluation cases, rubric links, result records, ChatGPT Project gates and cross-host runtime blocks validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
