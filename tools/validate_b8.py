#!/usr/bin/env python3
"""Validate B8 requirement, acceptance-test, delivery and artifact contracts."""
from __future__ import annotations

import json
import sys
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


def main() -> int:
    errors: list[str] = []
    templates = [
        ("requirement-record.schema.json", "templates/records/requirement.json"),
        ("acceptance-test.schema.json", "templates/records/acceptance-test.json"),
        ("build-task.schema.json", "templates/records/build-task.json"),
        ("artifact-record.schema.json", "templates/records/artifact.json"),
        ("demo-plan.schema.json", "templates/project/demo-plan.json"),
    ]
    for schema_name, template_name in templates:
        try:
            check = validator(schema_name)
            template = json.loads((ROOT / template_name).read_text(encoding="utf-8"))
            for issue in check.iter_errors(template):
                errors.append(f"{template_name}: {list(issue.absolute_path)}: {issue.message}")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{template_name}: {exc}")

    evaluation_validator = validator("evaluation-case.schema.json")
    evaluated_case_count = 0
    for number in range(62, 88):
        path = ROOT / "evals" / "cases" / f"EVAL-{number:03d}.json"
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
            evaluated_case_count += 1
            for issue in evaluation_validator.iter_errors(case):
                errors.append(f"{path.relative_to(ROOT)}: {list(issue.absolute_path)}: {issue.message}")
            if case.get("case_status") != "ready":
                errors.append(f"{path.relative_to(ROOT)}: B8 evaluation case must be ready")
            for rubric_ref in case.get("rubric_refs", []):
                rubric_path = ROOT / "evals" / "rubrics" / rubric_ref
                if not rubric_path.is_file():
                    errors.append(f"{path.relative_to(ROOT)}: missing rubric reference {rubric_ref}")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    # Ensure the B8 templates are discoverable by the canonical Peanuts instructions.
    skill = (ROOT / "skills/peanuts/SKILL.md").read_text(encoding="utf-8")
    for reference in (
        "references/prd-and-requirements.md",
        "references/technical-design.md",
        "references/delivery-handoff.md",
    ):
        target = ROOT / "skills/peanuts" / reference
        if reference not in skill:
            errors.append(f"skills/peanuts/SKILL.md: missing B8 reference {reference}")
        if not target.is_file():
            errors.append(f"missing B8 reference file: {target.relative_to(ROOT)}")

    if errors:
        print(f"FAIL: {len(errors)} B8 schema/template/evaluation issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: B8 requirement, acceptance-test, task, artifact and demo schemas/templates.")
    print(f"PASS: {evaluated_case_count} B8 evaluation cases (EVAL-062–087) are structurally valid, rubric-linked, and marked ready for runtime evaluation.")
    print("NOTE: ready means prepared for evaluation, not passed by a live model.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
