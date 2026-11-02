from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

import pytest

from tools.build_skill_packages import (
    CHATGPT_FILES,
    RECORD_TEMPLATE_GROUPS,
    SCHEMA_GROUPS,
    build_all,
    copy_skill_files,
    load_skill_metadata,
    validate_canonical_skill,
    write_zip,
)
from tools.validate_b9 import validate_b9, validate_packaged_markdown_links, validate_package_outputs

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_skill_name_matches_parent_and_description_is_cross_host_compatible() -> None:
    metadata, _ = load_skill_metadata(ROOT / "skills/peanuts")
    assert metadata["name"] == "peanuts"
    assert len(metadata["description"]) <= 1024
    assert validate_canonical_skill(ROOT) == []


def test_all_chatgpt_source_files_and_setup_instructions_exist() -> None:
    errors = validate_b9(ROOT)
    assert not errors, "\n".join(errors)


def test_standalone_skill_packages_include_required_support_resources(tmp_path: Path) -> None:
    output = tmp_path / "skill-packages"
    build_all(output, root=ROOT)
    package_sources = copy_skill_files(ROOT)
    expected_support = {
        "schemas/council-review.schema.json",
        "schemas/assumption-test.schema.json",
        "schemas/requirement-record.schema.json",
        "templates/records/council-review.json",
        "templates/records/requirement.json",
        "templates/project/PRD.md",
        "docs/methods/FOUR_COUNCIL_PROTOCOL.md",
        "docs/methods/NUTS_METHOD.md",
        "docs/architecture/CONTEXT_ENGINEERING.md",
    }
    assert expected_support <= set(package_sources)
    for archive_name, prefix in (
        ("peanuts-agent-skill.zip", "peanuts/"),
        ("peanuts-claude-code-adapter.zip", ".claude/skills/peanuts/"),
        ("peanuts-codex-adapter.zip", ".agents/skills/peanuts/"),
    ):
        with zipfile.ZipFile(output / archive_name) as archive:
            assert {f"{prefix}{name}" for name in package_sources} == set(archive.namelist())
            for relative in expected_support:
                assert archive.read(f"{prefix}{relative}") == (ROOT / relative).read_bytes()


def test_all_relative_markdown_links_resolve_inside_standalone_skill_package() -> None:
    package_sources = copy_skill_files(ROOT)
    assert validate_packaged_markdown_links(package_sources) == []


def test_standalone_link_validator_rejects_missing_and_escaping_targets() -> None:
    files = {
        "docs/example.md": b"[Missing](../missing.md)\n[Escape](../../../outside.md)\n",
    }
    errors = validate_packaged_markdown_links(files)
    assert any("target missing" in error for error in errors)
    assert any("escapes bundle" in error for error in errors)


def test_chatgpt_project_bundles_contain_all_json_schemas_and_record_starters(tmp_path: Path) -> None:
    output = tmp_path / "skill-packages"
    build_all(output, root=ROOT)
    files_dir = output / "chatgpt-project/chatgpt-project-files"
    for filename, schema_names in SCHEMA_GROUPS.items():
        content = (files_dir / filename).read_text(encoding="utf-8")
        for schema_name in schema_names:
            assert f"## Canonical source: `schemas/{schema_name}`" in content
    for filename, template_names in RECORD_TEMPLATE_GROUPS.items():
        content = (files_dir / filename).read_text(encoding="utf-8")
        for template_name in template_names:
            assert f"## Canonical source: `templates/records/{template_name}`" in content
    assert len(CHATGPT_FILES) == 5


def test_chatgpt_schema_blocks_are_valid_json_and_project_setup_discloses_daily_limit(tmp_path: Path) -> None:
    output = tmp_path / "skill-packages"
    build_all(output, root=ROOT)
    files_dir = output / "chatgpt-project/chatgpt-project-files"
    for filename in CHATGPT_FILES:
        content = (files_dir / filename).read_text(encoding="utf-8")
        matches = re.findall(
            r"## Canonical source: `(schemas/[^`]+\.json|templates/records/[^`]+\.json)`\s+```json\s+(.*?)\s+```",
            content,
            flags=re.DOTALL,
        )
        for source_path, payload in matches:
            json.loads(payload)
    setup = (output / "chatgpt-project/SETUP.md").read_text(encoding="utf-8").lower()
    assert "three file uploads per day" in setup or "three uploads per day" in setup or "daily upload-rate limit" in setup


def test_build_generates_four_packaging_routes_and_exactly_five_chatgpt_sources(tmp_path: Path) -> None:
    output = tmp_path / "skill-packages"
    build_all(output, root=ROOT)
    assert validate_package_outputs(output, root=ROOT) == []
    chatgpt_files = sorted((output / "chatgpt-project/chatgpt-project-files").glob("*.txt"))
    assert len(chatgpt_files) == 5

    expected = {
        "peanuts-agent-skill.zip": "peanuts/SKILL.md",
        "peanuts-claude-code-adapter.zip": ".claude/skills/peanuts/SKILL.md",
        "peanuts-codex-adapter.zip": ".agents/skills/peanuts/SKILL.md",
    }
    for archive_name, skill_path in expected.items():
        with zipfile.ZipFile(output / archive_name) as archive:
            assert skill_path in archive.namelist()
            assert archive.read(skill_path) == (ROOT / "skills/peanuts/SKILL.md").read_bytes()


def test_repeated_builds_are_byte_reproducible(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    build_all(first, root=ROOT)
    build_all(second, root=ROOT)
    for filename in (
        "peanuts-agent-skill.zip",
        "peanuts-claude-code-adapter.zip",
        "peanuts-codex-adapter.zip",
        "peanuts-chatgpt-project-files.zip",
    ):
        a = (first / filename).read_bytes()
        b = (second / filename).read_bytes()
        assert hashlib.sha256(a).hexdigest() == hashlib.sha256(b).hexdigest()


def test_chatgpt_project_bundle_has_separate_instruction_and_five_files(tmp_path: Path) -> None:
    output = tmp_path / "skill-packages"
    build_all(output, root=ROOT)
    project_dir = output / "chatgpt-project"
    assert (project_dir / "PROJECT_INSTRUCTIONS.md").is_file()
    assert (project_dir / "SETUP.md").is_file()
    with zipfile.ZipFile(output / "peanuts-chatgpt-project-files.zip") as archive:
        assert len(archive.namelist()) == 5
        assert all(name.endswith(".txt") for name in archive.namelist())
        assert "PROJECT_INSTRUCTIONS.md" not in archive.namelist()


def test_generated_host_adapters_do_not_claim_runtime_verification(tmp_path: Path) -> None:
    output = tmp_path / "skill-packages"
    build_all(output, root=ROOT)
    for filename in ("README.md", "chatgpt-project/SETUP.md", "chatgpt-project/PROJECT_INSTRUCTIONS.md"):
        content = (output / filename).read_text(encoding="utf-8").lower()
        if filename.endswith("README.md"):
            assert "do not prove that any target host" in content
        elif filename.endswith("SETUP.md"):
            assert "not a native installed chatgpt skill" in content
            assert "do not create local directories" in content
        else:
            assert "manual project adapter" in content
            assert "not automatic skill activation" in content


def test_packager_rejects_archive_traversal(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unsafe package path"):
        write_zip(tmp_path / "unsafe.zip", {"../escape.txt": b"unsafe"})


def test_validator_detects_host_package_content_drift(tmp_path: Path) -> None:
    output = tmp_path / "skill-packages"
    build_all(output, root=ROOT)
    path = output / "peanuts-codex-adapter.zip"
    with zipfile.ZipFile(path, "r") as source:
        items = {name: source.read(name) for name in source.namelist()}
    items[".agents/skills/peanuts/SKILL.md"] += b"\nDrift.\n"
    with zipfile.ZipFile(path, "w") as target:
        for name, data in items.items():
            target.writestr(name, data)
    errors = validate_package_outputs(output, root=ROOT)
    assert any("source drift" in error for error in errors)


def test_skill_validator_rejects_missing_local_reference(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills/peanuts"
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "assets/templates").mkdir(parents=True)
    (skill_dir / "references/exists.md").write_text("# present\n", encoding="utf-8")
    (skill_dir / "assets/templates/sample.md").write_text("# template\n", encoding="utf-8")
    (skill_dir / "SKILL.md").write_text(
        "---\nname: peanuts\ndescription: "
        "Research event and project opportunities with evidence.\n---\n\n"
        "[Missing](references/missing.md)\n",
        encoding="utf-8",
    )
    errors = validate_canonical_skill(tmp_path)
    assert any("skill link target missing" in error for error in errors)


def test_skill_validator_rejects_description_above_documented_1024_character_maximum(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills/peanuts"
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "assets/templates").mkdir(parents=True)
    (skill_dir / "references/example.md").write_text("# reference\n", encoding="utf-8")
    (skill_dir / "assets/templates/example.md").write_text("# template\n", encoding="utf-8")
    description = "x" * 1025
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: peanuts\ndescription: {description}\n---\n\n# Peanuts\n",
        encoding="utf-8",
    )
    errors = validate_canonical_skill(tmp_path)
    assert any("description exceeds 1024 characters" in error for error in errors)


def test_skill_validator_rejects_directory_name_mismatch(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills/peanuts"
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "assets/templates").mkdir(parents=True)
    (skill_dir / "references/example.md").write_text("# reference", encoding="utf-8")
    (skill_dir / "assets/templates/example.md").write_text("# template", encoding="utf-8")
    (skill_dir / "SKILL.md").write_text(
        "---\nname: peanuts-planner\ndescription: Research events and projects with evidence.\n---\n",
        encoding="utf-8",
    )
    errors = validate_canonical_skill(tmp_path)
    assert any("must match parent folder" in error for error in errors)


def test_full_b9_validator_checks_evaluation_inventory_and_registry() -> None:
    assert validate_b9(ROOT) == []


def test_builder_removes_stale_markdown_project_sources_from_previous_format(tmp_path: Path) -> None:
    output = tmp_path / "skill-packages"
    files_dir = output / "chatgpt-project/chatgpt-project-files"
    files_dir.mkdir(parents=True)
    (files_dir / "obsolete-reference.md").write_text("stale generated source", encoding="utf-8")
    build_all(output, root=ROOT)
    actual = {path.name for path in files_dir.iterdir() if path.is_file()}
    assert actual == {
        "00_PEANUTS_CORE_SKILL.txt",
        "01_RESEARCH_AND_EVIDENCE.txt",
        "02_NUTS_AND_REVIEW.txt",
        "03_PRODUCT_AND_ENGINEERING.txt",
        "04_GOVERNANCE_AND_RECORDS.txt",
    }
    assert validate_package_outputs(output, root=ROOT) == []
