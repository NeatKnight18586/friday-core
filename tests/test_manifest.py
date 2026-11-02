from __future__ import annotations

import json
from pathlib import Path

from tools.package_manifest import collect_file_entries, is_packaged_source, manifest_differences

ROOT = Path(__file__).resolve().parents[1]


def test_manifest_covers_exact_current_source_file_set() -> None:
    manifest = json.loads((ROOT / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    # The test intentionally compares path coverage only; byte/hash checks are also
    # executed by validate_repo.py and tools/update_manifest.py --check.
    actual = {entry["path"] for entry in collect_file_entries(ROOT)}
    recorded = {entry["path"] for entry in manifest["files"]}
    assert actual == recorded


def test_manifest_ignores_private_generated_and_archive_files(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    (root / "private-memory").mkdir()
    (root / "private-memory/profile.md").write_text("private", encoding="utf-8")
    (root / "local-workspace").mkdir()
    (root / "local-workspace/project.json").write_text("{}", encoding="utf-8")
    (root / "__pycache__").mkdir()
    (root / "__pycache__/temp.pyc").write_bytes(b"generated")
    (root / ".env").write_text("SECRET=example", encoding="utf-8")
    (root / ".env.example").write_text("KEY=replace-me", encoding="utf-8")
    (root / "README.md").write_text("Friday", encoding="utf-8")

    entries = collect_file_entries(root)
    paths = {entry["path"] for entry in entries}
    assert paths == {".env.example", "README.md"}


def test_manifest_detects_missing_and_changed_files(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    file_path = root / "README.md"
    file_path.write_text("original", encoding="utf-8")
    entry = collect_file_entries(root)[0]
    manifest = {"files": [entry]}
    assert manifest_differences(root, manifest) == []

    file_path.write_text("changed", encoding="utf-8")
    errors = manifest_differences(root, manifest)
    assert any("size mismatch" in error or "SHA-256 mismatch" in error for error in errors)


def test_symlink_is_not_packaged(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    target = root / "target.txt"
    target.write_text("safe", encoding="utf-8")
    link = root / "link.txt"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        return
    assert not is_packaged_source(link, root)
