from __future__ import annotations

import json
import zipfile
from pathlib import Path

from tools.build_claude_chat_companion import PROJECT_KNOWLEDGE, build_all
from tools.build_skill_packages import copy_skill_files, load_skill_metadata
from tools.validate_claude_chat import validate

ROOT = Path(__file__).resolve().parents[1]


def test_claude_chat_skill_zip_uses_lowercase_entrypoint_and_matching_folder(tmp_path: Path) -> None:
    output = tmp_path / "claude-chat"
    build_all(output, root=ROOT)
    with zipfile.ZipFile(output / "peanuts-claude-chat-skill.zip") as archive:
        names = set(archive.namelist())
        assert "peanuts/skill.md" in names
        assert "peanuts/SKILL.md" not in names
        assert all(name.startswith("peanuts/") for name in names)
        assert archive.testzip() is None


def test_claude_chat_skill_metadata_obeys_current_consumer_limit_and_is_canonical(tmp_path: Path) -> None:
    metadata, canonical = load_skill_metadata(ROOT / "skills/peanuts")
    assert metadata["name"] == "peanuts"
    assert len(metadata["description"]) <= 200
    output = tmp_path / "claude-chat"
    build_all(output, root=ROOT)
    with zipfile.ZipFile(output / "peanuts-claude-chat-skill.zip") as archive:
        assert archive.read("peanuts/skill.md").decode("utf-8") == canonical


def test_claude_chat_skill_bundle_is_byte_identical_to_all_canonical_resources(tmp_path: Path) -> None:
    output = tmp_path / "claude-chat"
    build_all(output, root=ROOT)
    canonical = copy_skill_files(ROOT)
    with zipfile.ZipFile(output / "peanuts-claude-chat-skill.zip") as archive:
        for relative, data in canonical.items():
            target = f"peanuts/{'skill.md' if relative == 'SKILL.md' else relative}"
            assert archive.read(target) == data


def test_claude_project_knowledge_zip_contains_five_curated_context_documents(tmp_path: Path) -> None:
    output = tmp_path / "claude-chat"
    build_all(output, root=ROOT)
    with zipfile.ZipFile(output / "friday-peanuts-claude-project-knowledge.zip") as archive:
        assert set(archive.namelist()) == set(PROJECT_KNOWLEDGE)
        assert archive.testzip() is None
        for name in PROJECT_KNOWLEDGE:
            assert archive.read(name).startswith(b"# ")


def test_claude_project_instructions_are_compact_and_ipad_aware(tmp_path: Path) -> None:
    output = tmp_path / "claude-chat"
    build_all(output, root=ROOT)
    text = (output / "CLAUDE_PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert len(text) <= 6000
    for phrase in ("iPad", "P1–P10", "B0–B10", "tools actually available", "handoff", "Project knowledge"):
        assert phrase.lower() in text.lower()


def test_claude_chat_installer_does_not_claim_claude_code_slash_command() -> None:
    setup = (ROOT / "adapters/claude-chat/SETUP_IPAD.md").read_text(encoding="utf-8")
    assert "ordinary Claude chat" in setup
    assert "does not use the `/peanuts` Claude Code slash-command convention" in setup


def test_project_companion_distinguishes_skill_procedure_from_durable_context() -> None:
    instructions = (ROOT / "adapters/claude-chat/PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert "Skill provides methods and task procedures" in instructions
    assert "Project knowledge" in instructions
    assert "conversation details are not automatically a durable handoff" in instructions.lower()


def test_b10_1_cases_and_results_validate_and_keep_owner_runtime_blocked() -> None:
    assert validate(ROOT) == []
    results = [json.loads(line) for line in (ROOT / "evals/results/results.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    by_case = {record["case_id"]: record for record in results}
    assert by_case["EVAL-138"]["status"] == "blocked"
    assert by_case["EVAL-139"]["status"] == "blocked"
    assert by_case["EVAL-140"]["status"] == "blocked"


def test_claude_project_knowledge_uses_supported_txt_extensions(tmp_path: Path) -> None:
    output = tmp_path / "claude-chat"
    build_all(output, root=ROOT)
    with zipfile.ZipFile(output / "friday-peanuts-claude-project-knowledge.zip") as archive:
        names = archive.namelist()
        assert len(names) == 5
        assert all(name.endswith(".txt") for name in names)
        assert all(archive.read(name).decode("utf-8").startswith("# ") for name in names)


def test_claude_project_pack_includes_current_b10_1_status_and_acceptance(tmp_path: Path) -> None:
    output = tmp_path / "claude-chat"
    build_all(output, root=ROOT)
    with zipfile.ZipFile(output / "friday-peanuts-claude-project-knowledge.zip") as archive:
        status_doc = archive.read("05_CURRENT_STATUS_AND_HANDOFF.txt").decode("utf-8")
        assert "B10.1 Status and Handoff" in status_doc
        assert "Claude Chat and Project Acceptance" in status_doc


def test_claude_project_guide_distinguishes_project_count_from_file_count() -> None:
    setup = (ROOT / "adapters/claude-chat/SETUP_IPAD.md").read_text(encoding="utf-8").lower()
    assert "unlimited project files" in setup
    assert "five projects" in setup
    assert "not a claude file-count limit" in setup


def test_claude_project_docs_use_supported_txt_not_markdown_extension() -> None:
    from tools.build_claude_chat_companion import PROJECT_KNOWLEDGE
    assert len(PROJECT_KNOWLEDGE) == 5
    assert all(name.endswith(".txt") for name in PROJECT_KNOWLEDGE)
