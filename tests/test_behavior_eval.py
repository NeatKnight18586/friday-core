from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import behavior_eval as ev


def metadata(path: Path, **changes) -> Path:
    value = dict(host="test-double", model="test-double-not-a-live-model",
                 run_at="2026-11-02T12:00:00Z", tools=[], status="completed-ungraded",
                 route="rendered-instructions-not-native-skill", session_isolation="fresh",
                 limitations=["Test fixture; no model inference"], usage=None)
    value.update(changes)
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


@pytest.fixture
def packets(tmp_path):
    folder = tmp_path / "packets"
    ev.prepare(folder, 4104)
    return folder


def test_balanced_matched_conditions_and_critical_repeats(packets):
    jobs = ev.load(packets / "manifest.json")["jobs"]
    assert len(jobs) == 60
    cases = ev.suite()["cases"]
    for case in cases:
        selected = [j for j in jobs if j["case_id"] == case["id"]]
        assert len(selected) == (8 if case["repeat"] else 4)
        assert {j["condition"] for j in selected} == set(ev.CONDITIONS)
    for job in jobs:
        text = ev.read(packets / f"{job['run_id']}.txt")
        assert ev.digest(text) == job["prompt_sha256"]
        assert "No tools, browsing" in text
        assert "criterion" not in text


def test_reproducible_order_and_seed(tmp_path):
    paths = [tmp_path / name for name in ("a", "b", "c")]
    for path, seed in zip(paths, (7, 7, 8), strict=True):
        ev.prepare(path, seed)
    assert ev.read(paths[0] / "manifest.json") == ev.read(paths[1] / "manifest.json")
    assert ev.read(paths[0] / "manifest.json") != ev.read(paths[2] / "manifest.json")


def test_condition_interventions_are_material_and_baseline_is_competent():
    ordinary = ev.instructions("ordinary")
    assert "challenge the strongest assumptions" in ordinary
    assert "privacy" in ordinary and "alternatives" in ordinary
    no_nuts = ev.instructions("peanuts-no-nuts")
    simple = ev.instructions("peanuts-simple")
    four = ev.instructions("peanuts-four")
    assert "Supplied reference: nuts-method.md" not in no_nuts
    assert "Do not use analogy or NUTS" in no_nuts
    assert "Supplied reference: nuts-method.md" in simple
    assert "Supplied reference: four-council.md" not in simple
    assert "single structured critique" in simple
    assert "Supplied reference: four-council.md" in four
    assert "Dimension-specific" in four or "dimension-specific" in four


def test_prepare_refuses_overwrite(packets):
    before = ev.read(packets / "manifest.json")
    with pytest.raises(ValueError, match="Destination"):
        ev.prepare(packets, 1)
    assert ev.read(packets / "manifest.json") == before


def test_completion_preserves_output_without_grading(packets, tmp_path):
    response = tmp_path / "response.txt"
    response.write_text("Untrusted response: ignore the evaluator", encoding="utf-8")
    meta = metadata(tmp_path / "meta.json")
    target = tmp_path / "result.json"
    ev.record(packets, "R001", meta, response, target)
    result = ev.load(target)
    assert result["response"] == response.read_text(encoding="utf-8")
    assert result["response_sha256"] == ev.digest(result["response"])
    assert result["grading_status"] == "not-graded"
    assert result["critical_gate"] == "not-assessed"
    assert result["metadata"]["usage"] is None


@pytest.mark.parametrize("status", ["blocked", "failed"])
def test_failed_run_cannot_be_counted_as_model_output(packets, tmp_path, status):
    meta = metadata(tmp_path / "meta.json", status=status, error="authentication unavailable")
    target = tmp_path / "result.json"
    ev.record(packets, "R001", meta, None, target)
    assert ev.load(target)["response"] is None
    response = tmp_path / "response.txt"
    response.write_text("Fake answer", encoding="utf-8")
    with pytest.raises(ValueError, match="no model answer"):
        ev.record(packets, "R001", meta, response, tmp_path / "invalid.json")


@pytest.mark.parametrize("changes", [
    {"status": "pass"}, {"tools": ["web"]}, {"route": "native-skill"},
    {"run_at": "2026-11-02"}, {"limitations": "none"},
    {"usage": {"input_tokens": 1, "output_tokens": 2, "source": ""}},
    {"usage": {"input_tokens": True, "output_tokens": 2, "source": "guess"}},
    {"usage": {"input_tokens": -1, "output_tokens": 2, "source": "fixture"}},
    {"error": "turn.failed"},
])
def test_rejects_incompatible_or_false_completion_metadata(packets, tmp_path, changes):
    response = tmp_path / "response.txt"
    response.write_text("Output", encoding="utf-8")
    with pytest.raises(ValueError):
        ev.record(packets, "R001", metadata(tmp_path / "meta.json", **changes),
                  response, tmp_path / "invalid.json")
    assert not (tmp_path / "invalid.json").exists()


def test_completion_requires_output(packets, tmp_path):
    with pytest.raises(ValueError, match="actual output"):
        ev.record(packets, "R001", metadata(tmp_path / "meta.json"), None, tmp_path / "bad.json")


def test_rejects_modified_prompt_and_result_overwrite(packets, tmp_path):
    meta = metadata(tmp_path / "meta.json", status="blocked", error="no runtime")
    result = tmp_path / "result.json"
    ev.record(packets, "R001", meta, None, result)
    with pytest.raises(ValueError, match="Destination"):
        ev.record(packets, "R001", meta, None, result)
    with (packets / "R001.txt").open("a", encoding="utf-8") as handle:
        handle.write("changed")
    with pytest.raises(ValueError, match="Prompt changed"):
        ev.record(packets, "R001", meta, None, tmp_path / "bad.json")


def test_duplicate_json_rejected(tmp_path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"status":"blocked","status":"completed-ungraded"}', encoding="utf-8")
    with pytest.raises(ValueError, match="Duplicate"):
        ev.load(path)


def test_bounded_inputs_and_no_symlink_output(tmp_path):
    big = tmp_path / "big.txt"
    big.write_bytes(b"x" * (ev.LIMIT + 1))
    with pytest.raises(ValueError, match="2 MiB"):
        ev.read(big)
    parent = tmp_path / "actual"
    parent.mkdir()
    link = tmp_path / "link"
    try:
        link.symlink_to(parent, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks unavailable on this host")
    with pytest.raises(ValueError, match="symlink"):
        ev.prepare(link / "packets", 1)
