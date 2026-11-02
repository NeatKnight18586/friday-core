from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.inspect_context import inspect_files
from tools.validate_capabilities import validate_registry

ROOT = Path(__file__).resolve().parents[1]


def _make_registry_root(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "capabilities").mkdir(parents=True)
    (root / "schemas").mkdir()
    (root / "skills" / "peanuts").mkdir(parents=True)
    (root / "evals" / "cases").mkdir(parents=True)
    shutil.copy2(ROOT / "schemas" / "capability-registry.schema.json", root / "schemas")
    (root / "skills" / "peanuts" / "SKILL.md").write_text(
        "---\nname: peanuts-planner\ndescription: Plan evidence-informed project work when the user asks for project discovery.\n---\n# Test skill\n",
        encoding="utf-8",
    )
    (root / "evals" / "cases" / "EVAL-001.json").write_text("{}\n", encoding="utf-8")
    registry = {
        "schema_version": "1.0.0",
        "registry_version": "0.1.0",
        "purpose": "Test registry for Friday capability catalog validation.",
        "capabilities": [{
            "id": "peanuts",
            "display_name": "Peanuts",
            "summary": "Evidence-informed project discovery and planning for test scenarios.",
            "kind": "harness",
            "lifecycle": "active",
            "maturity": "prototype",
            "canonical_path": "skills/peanuts",
            "entrypoint": "skills/peanuts/SKILL.md",
            "skill_file": "skills/peanuts/SKILL.md",
            "domains": ["product-planning"],
            "intents": ["plan-a-project"],
            "default_mode": "standard",
            "supported_modes": ["quick", "standard", "deep"],
            "host_profiles": [{
                "host": "test-host", "status": "planned", "discovery_path": None,
                "note": "Host runtime is not yet tested."
            }],
            "permissions_profile": "read-project-data-only",
            "evaluation_refs": ["EVAL-001"],
            "dependencies": [],
            "exclusions": ["Unrelated general questions"]
        }]
    }
    (root / "capabilities" / "registry.json").write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    return root


def test_repository_capability_registry_is_valid() -> None:
    assert validate_registry(ROOT) == []


def test_registry_rejects_duplicate_capability_ids(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    path = root / "capabilities" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["capabilities"].append(dict(data["capabilities"][0]))
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("duplicate capability ID" in error for error in validate_registry(root))


def test_registry_rejects_path_traversal(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    path = root / "capabilities" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["capabilities"][0]["canonical_path"] = "../outside"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("safe repository-relative" in error for error in validate_registry(root))


def test_registry_rejects_missing_skill_package(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    path = root / "capabilities" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["capabilities"][0]["skill_file"] = "skills/peanuts/MISSING.md"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("skill file missing" in error for error in validate_registry(root))


def test_registry_rejects_unregistered_skill_package(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    extra = root / "skills" / "another-skill"
    extra.mkdir()
    (extra / "SKILL.md").write_text("---\nname: another-skill\ndescription: An extra skill for testing.\n---\n", encoding="utf-8")
    assert any("unregistered skill package" in error for error in validate_registry(root))


def test_registry_rejects_invalid_skill_frontmatter(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    (root / "skills" / "peanuts" / "SKILL.md").write_text("# No frontmatter\n", encoding="utf-8")
    assert any("missing or malformed YAML frontmatter" in error for error in validate_registry(root))


def test_registry_rejects_oversized_description(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    path = root / "skills" / "peanuts" / "SKILL.md"
    path.write_text("---\nname: peanuts-planner\ndescription: " + ("x" * 1025) + "\n---\n", encoding="utf-8")
    assert any("1024-character" in error for error in validate_registry(root))


def test_inspect_context_reports_character_and_word_proxies_not_tokens(tmp_path: Path) -> None:
    (tmp_path / "small.md").write_text("one two three\n", encoding="utf-8")
    report = inspect_files(tmp_path, ["small.md"])
    assert report["measurement"] == "characters_words_lines_only"
    assert "not model-token counts" in report["warning"]
    assert report["files"][0]["words"] == 3
    assert report["files"][0]["characters"] == 14


def test_inspect_context_reports_missing_file(tmp_path: Path) -> None:
    report = inspect_files(tmp_path, ["missing.md"])
    assert report["files"][0]["status"] == "missing"


def test_non_skill_harness_can_be_registered_without_skill_file(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    data_path = root / "capabilities" / "registry.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    capability = data["capabilities"][0]
    capability["kind"] = "harness"
    capability["canonical_path"] = "harnesses/demo"
    capability["entrypoint"] = "harnesses/demo/README.md"
    capability.pop("skill_file", None)
    (root / "skills" / "peanuts" / "SKILL.md").unlink()
    (root / "harnesses" / "demo").mkdir(parents=True)
    (root / "harnesses" / "demo" / "README.md").write_text("# Demo harness\n", encoding="utf-8")
    data_path.write_text(json.dumps(data), encoding="utf-8")
    assert validate_registry(root) == []


def test_skill_kind_requires_skill_file(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    data_path = root / "capabilities" / "registry.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    data["capabilities"][0].pop("skill_file", None)
    data["capabilities"][0]["kind"] = "skill"
    data_path.write_text(json.dumps(data), encoding="utf-8")
    errors = validate_registry(root)
    assert any("skill_file" in error for error in errors)


def test_registry_rejects_unregistered_dependency(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    data_path = root / "capabilities" / "registry.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    data["capabilities"][0]["dependencies"] = ["missing-capability"]
    data_path.write_text(json.dumps(data), encoding="utf-8")
    assert any("dependency is not registered" in error for error in validate_registry(root))


def test_registry_rejects_unsafe_host_discovery_path(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    data_path = root / "capabilities" / "registry.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    data["capabilities"][0]["host_profiles"][0]["discovery_path"] = "../../outside"
    data_path.write_text(json.dumps(data), encoding="utf-8")
    assert any("unsafe host discovery_path" in error for error in validate_registry(root))


def test_registry_rejects_dependency_cycles(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    harness_dir = root / "harnesses" / "writer"
    harness_dir.mkdir(parents=True)
    (harness_dir / "README.md").write_text("# Writer harness\n", encoding="utf-8")
    data_path = root / "capabilities" / "registry.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    data["capabilities"].append({
        "id": "writer",
        "display_name": "Writer",
        "summary": "A separate test harness for checking cyclic capability dependencies.",
        "kind": "harness",
        "lifecycle": "active",
        "maturity": "prototype",
        "canonical_path": "harnesses/writer",
        "entrypoint": "harnesses/writer/README.md",
        "domains": ["writing"],
        "intents": ["draft-text"],
        "default_mode": "standard",
        "supported_modes": ["quick", "standard", "deep"],
        "host_profiles": [],
        "permissions_profile": "read-project-data-only",
        "evaluation_refs": [],
        "dependencies": ["peanuts"],
        "exclusions": []
    })
    data["capabilities"][0]["dependencies"] = ["writer"]
    data_path.write_text(json.dumps(data), encoding="utf-8")
    assert any("dependency cycle" in error for error in validate_registry(root))


def test_inspect_context_separates_host_profiles() -> None:
    from tools.inspect_context import inspect_profiles

    report = inspect_profiles(ROOT, "overview")
    names = [profile["profile"] for profile in report["profiles"]]
    assert "claude-code" in names
    assert "codex" in names
    claude_paths = [item["path"] for item in report["profiles"][0]["files"]]
    codex_paths = [item["path"] for item in report["profiles"][1]["files"]]
    assert "CLAUDE.md" in claude_paths
    assert "AGENTS.md" in codex_paths
    assert "AGENTS.md" not in claude_paths
    assert "CLAUDE.md" not in codex_paths


def test_registry_rejects_missing_package_entrypoint(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    data_path = root / "capabilities" / "registry.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    data["capabilities"][0]["entrypoint"] = "skills/peanuts/DOES_NOT_EXIST.md"
    data_path.write_text(json.dumps(data), encoding="utf-8")
    assert any("package entrypoint file missing" in error for error in validate_registry(root))


def test_registry_rejects_duplicate_canonical_package_paths(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    path = root / "capabilities" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    duplicate = dict(data["capabilities"][0])
    duplicate["id"] = "peanuts-copy"
    duplicate["display_name"] = "Peanuts Copy"
    duplicate["summary"] = "Duplicate package path used to test registry separation."
    data["capabilities"].append(duplicate)
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("canonical package path is already registered" in error for error in validate_registry(root))


def test_skill_kind_requires_skill_file_as_entrypoint(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    path = root / "capabilities" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["capabilities"][0]["kind"] = "skill"
    data["capabilities"][0]["entrypoint"] = "skills/peanuts/README.md"
    (root / "skills" / "peanuts" / "README.md").write_text("# Package readme\n", encoding="utf-8")
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("entrypoint must equal skill_file" in error for error in validate_registry(root))


def test_verified_host_profile_requires_existing_discovery_path(tmp_path: Path) -> None:
    root = _make_registry_root(tmp_path)
    path = root / "capabilities" / "registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["capabilities"][0]["host_profiles"][0]["status"] = "verified"
    data["capabilities"][0]["host_profiles"][0]["discovery_path"] = ".agents/skills/peanuts"
    path.write_text(json.dumps(data), encoding="utf-8")
    assert any("verified host discovery_path does not exist" in error for error in validate_registry(root))


def test_incident_protocol_defines_timeout_as_unresolved() -> None:
    content = (ROOT / "docs" / "governance" / "DEVELOPMENT_INCIDENT_PROTOCOL.md").read_text(encoding="utf-8")
    assert "`TIMEOUT`" in content
    assert "Treat as unresolved" in content
    assert "Never delete or dilute an acceptance test" in content
