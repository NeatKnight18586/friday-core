from __future__ import annotations

import json
from pathlib import Path

from tools.validate_host_adapters import HOSTS, _validate_one_host, validate_host_adapters
from tools.build_skill_packages import build_all

ROOT = Path(__file__).resolve().parents[1]


def test_codex_and_claude_adapter_install_simulations_pass() -> None:
    assert validate_host_adapters(ROOT) == []


def test_host_discovery_locations_match_current_vendor_documents() -> None:
    assert HOSTS["codex"]["prefix"] == ".agents/skills/peanuts"
    assert HOSTS["codex"]["guidance"] == "AGENTS.md"
    assert HOSTS["codex"]["invocation"] == "$peanuts"
    assert HOSTS["claude-code"]["prefix"] == ".claude/skills/peanuts"
    assert HOSTS["claude-code"]["guidance"] == "CLAUDE.md"
    assert HOSTS["claude-code"]["invocation"] == "/peanuts"


def test_simulated_installs_report_runtime_not_run(tmp_path: Path) -> None:
    packages = tmp_path / "packages"
    build_all(packages, root=ROOT)
    for host in HOSTS:
        fixture = tmp_path / host
        errors = _validate_one_host(
            root=ROOT,
            package_output=packages,
            fixture_root=fixture,
            host=host,
        )
        assert errors == []
        record = json.loads((fixture / f"{host}-INSTALL-SIMULATION-PASS.json").read_text())
        assert record["result"].startswith("PASS")
        assert record["runtime_claim"].startswith("NOT RUN")


def test_packages_do_not_preapprove_tools_or_ship_executable_scripts(tmp_path: Path) -> None:
    output = tmp_path / "packages"
    build_all(output, root=ROOT)
    for host, spec in HOSTS.items():
        import zipfile

        with zipfile.ZipFile(output / spec["archive"]) as archive:
            names = archive.namelist()
            skill_file = archive.read(f"{spec['prefix']}/SKILL.md").decode("utf-8")
            frontmatter = skill_file.split("---", 2)[1]
            assert "allowed-tools" not in frontmatter
            assert not any(name.lower().endswith((".py", ".sh", ".ps1", ".bat", ".cmd", ".exe", ".dll")) for name in names)


def test_root_guidance_files_are_present_and_host_specific() -> None:
    assert (ROOT / "AGENTS.md").is_file()
    assert (ROOT / "CLAUDE.md").is_file()
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8").lower()
    assert ".agents/skills/peanuts" in agents
    assert "do not bypass sandbox or approval controls" in agents
    assert ".claude/skills/peanuts" in claude
    assert "--dangerously-skip-permissions" in claude


def _write_test_zip(path: Path, entries: list[tuple[str, bytes, int | None]]) -> None:
    import zipfile

    with zipfile.ZipFile(path, "w") as archive:
        for name, payload, external_attr in entries:
            info = zipfile.ZipInfo(name)
            if external_attr is not None:
                info.external_attr = external_attr
            archive.writestr(info, payload)


def test_safe_extractor_rejects_path_traversal_before_writing(tmp_path: Path) -> None:
    import pytest

    from tools.validate_host_adapters import _safe_extract

    archive = tmp_path / "unsafe-path.zip"
    _write_test_zip(archive, [("safe.txt", b"safe", None), ("../escape.txt", b"bad", None)])
    destination = tmp_path / "install"
    with pytest.raises(ValueError, match="unsafe archive path"):
        _safe_extract(archive, destination)
    assert not destination.exists() or not any(destination.rglob("*"))
    assert not (tmp_path / "escape.txt").exists()


def test_safe_extractor_rejects_symlinks_and_duplicate_destinations(tmp_path: Path) -> None:
    import stat
    import zipfile
    import pytest

    from tools.validate_host_adapters import _safe_extract

    symlink = tmp_path / "symlink.zip"
    _write_test_zip(
        symlink,
        [("link", b"target.txt", (stat.S_IFLNK | 0o777) << 16)],
    )
    with pytest.raises(ValueError, match="symlink entry"):
        _safe_extract(symlink, tmp_path / "symlink-install")

    duplicate = tmp_path / "duplicate.zip"
    with pytest.warns(UserWarning, match="Duplicate name"):
        with zipfile.ZipFile(duplicate, "w") as archive:
            archive.writestr("same.txt", b"one")
            archive.writestr("same.txt", b"two")
    with pytest.raises(ValueError, match="duplicate archive path"):
        _safe_extract(duplicate, tmp_path / "duplicate-install")


def test_safe_extractor_rejects_case_collisions_and_file_directory_conflicts(tmp_path: Path) -> None:
    import pytest

    from tools.validate_host_adapters import _safe_extract

    case_collision = tmp_path / "case-collision.zip"
    _write_test_zip(case_collision, [("Peanuts/SKILL.md", b"a", None), ("peanuts/skill.md", b"b", None)])
    with pytest.raises(ValueError, match="cross-platform path collision"):
        _safe_extract(case_collision, tmp_path / "case-install")

    parent_conflict = tmp_path / "parent-conflict.zip"
    _write_test_zip(parent_conflict, [("peanuts", b"file", None), ("peanuts/SKILL.md", b"child", None)])
    with pytest.raises(ValueError, match="file/directory path conflict"):
        _safe_extract(parent_conflict, tmp_path / "parent-install")


def test_safe_extractor_rejects_windows_and_non_normalized_paths(tmp_path: Path) -> None:
    import pytest

    from tools.validate_host_adapters import _safe_extract

    for index, bad_name in enumerate((r"C:\\outside.txt", "folder/./file.txt", "folder//file.txt")):
        archive = tmp_path / f"bad-path-{index}.zip"
        _write_test_zip(archive, [(bad_name, b"bad", None)])
        with pytest.raises(ValueError, match="unsafe archive path"):
            _safe_extract(archive, tmp_path / f"bad-install-{index}")


def test_safe_extractor_rejects_case_collisions_in_directory_prefixes(tmp_path: Path) -> None:
    import pytest

    from tools.validate_host_adapters import _safe_extract

    archive = tmp_path / "prefix-collision.zip"
    _write_test_zip(archive, [("Peanuts/a.txt", b"a", None), ("peanuts/b.txt", b"b", None)])
    with pytest.raises(ValueError, match="cross-platform path collision"):
        _safe_extract(archive, tmp_path / "prefix-install")


def test_safe_extractor_enforces_uncompressed_size_before_crc_read(tmp_path: Path) -> None:
    import pytest

    from tools.validate_host_adapters import _safe_extract

    archive = tmp_path / "oversized.zip"
    _write_test_zip(archive, [("large.txt", b"x" * (10 * 1024 * 1024 + 1), None)])
    destination = tmp_path / "oversized-install"
    with pytest.raises(ValueError, match="exceeds size limit"):
        _safe_extract(archive, destination)
    assert not destination.exists() or not any(destination.rglob("*"))
