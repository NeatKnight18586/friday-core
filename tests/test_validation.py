from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.validate_project import read_json, read_jsonl


def test_read_json_reports_malformed_file(tmp_path: Path) -> None:
    path = tmp_path / "broken.json"
    path.write_text('{"project_id":', encoding="utf-8")
    errors: list[str] = []
    validator = Draft202012Validator({"type": "object"})

    result = read_json(path, "broken.json", validator, errors)

    assert result is None
    assert len(errors) == 1
    assert errors[0].startswith("broken.json: cannot read valid JSON:")


def test_read_jsonl_reports_malformed_line_and_keeps_valid_records(tmp_path: Path) -> None:
    path = tmp_path / "records.jsonl"
    path.write_text('{"source_id":"SRC-1"}\n{invalid}\n', encoding="utf-8")
    errors: list[str] = []
    validator = Draft202012Validator({"type": "object", "required": ["source_id"]})

    rows = read_jsonl(path, "records.jsonl", validator, "source_id", errors)

    assert rows == [{"source_id": "SRC-1"}]
    assert any("records.jsonl:2: invalid JSON:" in error for error in errors)


def test_read_jsonl_detects_duplicate_record_ids(tmp_path: Path) -> None:
    path = tmp_path / "records.jsonl"
    record = {"source_id": "SRC-1"}
    path.write_text(json.dumps(record) + "\n" + json.dumps(record) + "\n", encoding="utf-8")
    errors: list[str] = []
    validator = Draft202012Validator({"type": "object", "required": ["source_id"]})

    rows = read_jsonl(path, "records.jsonl", validator, "source_id", errors)

    assert len(rows) == 2
    assert any("duplicate source_id SRC-1" in error for error in errors)
