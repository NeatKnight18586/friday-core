from __future__ import annotations

import json

from tools.validate_b10 import ROOT, validate_b10


def test_b10_acceptance_suite_and_results_validate() -> None:
    assert validate_b10(ROOT) == []


def test_b10_evaluation_inventory_has_thirty_two_cases() -> None:
    paths = sorted((ROOT / "evals/cases").glob("EVAL-1*.json"))
    b10 = [p for p in paths if 103 <= int(p.stem.split("-")[1]) <= 134]
    assert len(b10) == 32


def test_project_ui_independent_calibration_and_live_host_runtimes_remain_blocked() -> None:
    records = [
        json.loads(line)
        for line in (ROOT / "evals/results/results.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by_case = {record["case_id"]: record for record in records}
    assert by_case["EVAL-117"]["status"] == "blocked"
    assert by_case["EVAL-118"]["status"] == "blocked"
    assert by_case["EVAL-122"]["status"] == "blocked"
    assert by_case["EVAL-117"]["reviewer_approved"] is False
    assert by_case["EVAL-118"]["reviewer_approved"] is False
    assert by_case["EVAL-122"]["reviewer_approved"] is False
    for case_id in ("EVAL-127", "EVAL-128", "EVAL-129", "EVAL-130", "EVAL-131"):
        assert by_case[case_id]["status"] == "blocked"
        assert by_case[case_id]["reviewer_approved"] is False
    for case_id in ("EVAL-123", "EVAL-124", "EVAL-125", "EVAL-126", "EVAL-132", "EVAL-133", "EVAL-134"):
        assert by_case[case_id]["status"] == "passed"
        assert by_case[case_id]["reviewer_approved"] is False


def test_acceptance_protocol_separates_live_chat_from_project_ui() -> None:
    text = (ROOT / "docs/acceptance/CHATGPT_PRIMARY_RUNTIME_ACCEPTANCE.md").read_text(encoding="utf-8")
    assert "live chatgpt conversation" in text.lower()
    assert "target Project UI" in text
    assert "NOT RUN" in text
    cross_host = (ROOT / "docs/acceptance/CROSS_HOST_RUNTIME_ACCEPTANCE.md").read_text(encoding="utf-8")
    assert ".agents/skills/peanuts/SKILL.md" in cross_host
    assert ".claude/skills/peanuts/SKILL.md" in cross_host
    assert "simulated filesystem installation only" in cross_host.lower()
