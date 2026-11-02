"""Regression checks for the optional hackathon method and cross-host exports."""
from __future__ import annotations

from pathlib import Path

from tools.build_claude_chat_companion import PROJECT_KNOWLEDGE, compile_project_knowledge
from tools.build_skill_packages import CHATGPT_FILES, package_support_source_paths, copy_skill_files

ROOT = Path(__file__).resolve().parents[1]


def test_method_is_event_triggered_not_a_new_universal_stage():
    skill = (ROOT / "skills/peanuts/SKILL.md").read_text()
    assert "hackathon-sprint.md" in skill
    assert "optional P1–P6" in skill
    assert "not a universal default" in skill
    assert "P1–P10" in (ROOT / "docs/methods/HACKATHON_OPPORTUNITY_SPRINT.md").read_text()


def test_hard_gates_and_no_false_sponsor_scoring():
    method = (ROOT / "docs/methods/HACKATHON_OPPORTUNITY_SPRINT.md").read_text()
    for phrase in ("official", "hard gates", "three", "consent", "NOT CHECKED", "NO_USEFUL_ANALOGY", "fallback"):
        assert phrase.lower() in method.lower()
    assert "fit × wow × buildability" in method
    assert "not an empirical formula" in method


def test_crosshost_refs_are_generated_from_canonical_sources():
    support = package_support_source_paths(ROOT)
    assert "docs/methods/HACKATHON_OPPORTUNITY_SPRINT.md" in support
    files = copy_skill_files(ROOT)
    assert files["references/hackathon-sprint.md"] == (ROOT / "skills/peanuts/references/hackathon-sprint.md").read_bytes()
    assert "assets/templates/hackathon-shortlist.md" in files
    assert "docs/methods/HACKATHON_OPPORTUNITY_SPRINT.md" in files


def test_chatgpt_and_claude_project_include_method_from_same_source():
    assert "skills/peanuts/references/hackathon-sprint.md" in CHATGPT_FILES["01_RESEARCH_AND_EVIDENCE.txt"]
    assert "docs/methods/HACKATHON_OPPORTUNITY_SPRINT.md" in PROJECT_KNOWLEDGE["03_PROFESSIONAL_METHODS_AND_EVIDENCE.txt"]
    compiled = compile_project_knowledge(ROOT,"03_PROFESSIONAL_METHODS_AND_EVIDENCE.txt", PROJECT_KNOWLEDGE["03_PROFESSIONAL_METHODS_AND_EVIDENCE.txt"])
    assert (ROOT / "docs/methods/HACKATHON_OPPORTUNITY_SPRINT.md").read_bytes() in compiled


def test_token_honesty_and_no_force_nuts():
    context = (ROOT / "skills/peanuts/references/context-efficiency.md").read_text()
    method = (ROOT / "skills/peanuts/references/hackathon-sprint.md").read_text()
    assert "Exact tokens/cost only when actually exposed" in context
    assert "NO_USEFUL_ANALOGY" in method
    assert "never" in context.lower()


def test_owner_live_gate_is_not_pretended_completed():
    checklist = (ROOT / "docs/acceptance/B10_1_C_OWNER_SMOKE_AND_COST_LOG.md").read_text()
    assert "Owner action required" in checklist
    assert "NOT AVAILABLE" in checklist
    assert "READY_FOR_CLAUDE_CHAT_MANUAL_USE" in checklist
    assert "No auto-success" in checklist


def test_new_shortlist_template_does_not_pretend_validated():
    template = (ROOT / "skills/peanuts/assets/templates/hackathon-shortlist.md").read_text()
    for phrase in ("provisional", "UNKNOWN", "owner approval: pending", "What wasn't checked"):
        assert phrase.lower() in template.lower()
