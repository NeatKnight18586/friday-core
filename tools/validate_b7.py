#!/usr/bin/env python3
"""Validate B7 review/assumption-test schemas, templates and eval cases."""
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


def load_validator(schema_name: str):
    schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def main() -> int:
    errors: list[str] = []
    for schema_name, template_path in [
        ("council-review.schema.json", "templates/records/council-review.json"),
        ("assumption-test.schema.json", "templates/records/assumption-test.json"),
        ("assumption-record.schema.json", "templates/records/assumption.json"),
    ]:
        try:
            validator = load_validator(schema_name)
            template = json.loads((ROOT / template_path).read_text(encoding="utf-8"))
            for issue in validator.iter_errors(template):
                errors.append(f"{template_path}: {list(issue.absolute_path)}: {issue.message}")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"{template_path}: {exc}")

    case_validator = load_validator("evaluation-case.schema.json")
    for number in range(51, 62):
        path = ROOT / "evals" / "cases" / f"EVAL-{number:03d}.json"
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
            for issue in case_validator.iter_errors(case):
                errors.append(f"{path.relative_to(ROOT)}: {issue.message}")
            if case.get("case_status") != "ready":
                errors.append(f"{path.relative_to(ROOT)}: B7 case must be ready for runtime evaluation")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if errors:
        print(f"FAIL: {len(errors)} B7 schema/template/evaluation issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: B7 council-review, assumption-test and assumption schemas; templates; EVAL-051–061.")
    print("NOTE: structural validation does not establish that the model follows the protocol or that real-world findings are true.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
