from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.validate_vertical_slice import validate_fixture

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "examples" / "vertical-slice-synthetic" / "campus-service-status"


def test_synthetic_vertical_slice_fixture_passes() -> None:
    assert validate_fixture(FIXTURE) == []


def test_vertical_slice_rejects_missing_artifact(tmp_path: Path) -> None:
    target = tmp_path / "fixture"
    shutil.copytree(FIXTURE, target)
    (target / "artifacts/06-draft-prd.md").unlink()
    errors = validate_fixture(target)
    assert any("06-draft-prd.md" in error for error in errors)


def test_vertical_slice_rejects_dangling_source_reference(tmp_path: Path) -> None:
    target = tmp_path / "fixture"
    shutil.copytree(FIXTURE, target)
    claims_path = target / "records/claims.jsonl"
    rows = [json.loads(line) for line in claims_path.read_text(encoding="utf-8").splitlines() if line]
    rows[0]["source_ids"] = ["SRC-9999"]
    claims_path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    errors = validate_fixture(target)
    assert any("SRC-9999" in error for error in errors)


def test_synthetic_fixture_must_be_labelled(tmp_path: Path) -> None:
    target = tmp_path / "fixture"
    shutil.copytree(FIXTURE, target)
    artifact = target / "artifacts/04-concept-brief.md"
    artifact.write_text(artifact.read_text(encoding="utf-8").replace("SYNTHETIC TEST DATA", "DEMO DATA"), encoding="utf-8")
    errors = validate_fixture(target)
    assert any("must be clearly labelled" in error for error in errors)


def test_vertical_slice_rejects_path_traversal(tmp_path: Path) -> None:
    target = tmp_path / "fixture"
    shutil.copytree(FIXTURE, target)
    run_path = target / "vertical-slice-run.json"
    run = json.loads(run_path.read_text(encoding="utf-8"))
    run["required_artifacts"][0] = "../outside.md"
    run_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    errors = validate_fixture(target)
    assert any("cannot traverse parents" in error or "escapes fixture" in error for error in errors)
