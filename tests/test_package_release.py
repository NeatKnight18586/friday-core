from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

from tools.package_release import build_release_archive, verify_release_archive


def _make_repo(root: Path) -> None:
    (root / "docs").mkdir()
    (root / "README.md").write_text("# Friday\n", encoding="utf-8")
    (root / "docs" / "example.md").write_text("Example\n", encoding="utf-8")
    files = []
    for name in ("README.md", "docs/example.md"):
        data = (root / name).read_bytes()
        files.append({"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    (root / "PACKAGE_MANIFEST.json").write_text(
        json.dumps({"project": "Friday", "files": files}, indent=2) + "\n",
        encoding="utf-8",
    )


def test_release_archive_has_repository_root_layout_and_verified_hashes(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    output = tmp_path.parent / f"{tmp_path.name}-release.zip"
    try:
        assert build_release_archive(tmp_path, output) == 0
        ok, message = verify_release_archive(output)
        assert ok, message
        with zipfile.ZipFile(output) as archive:
            names = set(archive.namelist())
            assert "README.md" in names
            assert "docs/example.md" in names
            assert "Friday/README.md" not in names
    finally:
        output.unlink(missing_ok=True)


def test_release_archive_refuses_stale_manifest(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    (tmp_path / "README.md").write_text("changed after manifest\n", encoding="utf-8")
    output = tmp_path.parent / f"{tmp_path.name}-bad.zip"
    try:
        assert build_release_archive(tmp_path, output) == 1
        assert not output.exists()
    finally:
        output.unlink(missing_ok=True)


def test_release_archive_rejects_unsafe_manifest_path(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    manifest = json.loads((tmp_path / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    manifest["files"].append({"path": "../escape.txt", "bytes": 0, "sha256": ""})
    (tmp_path / "PACKAGE_MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
    output = tmp_path.parent / f"{tmp_path.name}-unsafe.zip"
    try:
        assert build_release_archive(tmp_path, output) == 1
        assert not output.exists()
    finally:
        output.unlink(missing_ok=True)


def test_release_archive_refuses_unmanifested_source_file(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    (tmp_path / "untracked.md").write_text("not in manifest\n", encoding="utf-8")
    output = tmp_path.parent / f"{tmp_path.name}-untracked.zip"
    try:
        assert build_release_archive(tmp_path, output) == 1
        assert not output.exists()
    finally:
        output.unlink(missing_ok=True)


def test_release_archive_is_deterministic_for_unchanged_sources(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    first = tmp_path.parent / f"{tmp_path.name}-first.zip"
    second = tmp_path.parent / f"{tmp_path.name}-second.zip"
    try:
        assert build_release_archive(tmp_path, first) == 0
        assert build_release_archive(tmp_path, second) == 0
        assert first.read_bytes() == second.read_bytes()
    finally:
        first.unlink(missing_ok=True)
        second.unlink(missing_ok=True)
