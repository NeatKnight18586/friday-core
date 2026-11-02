#!/usr/bin/env python3
"""Shared rules for creating and checking the distributable source manifest."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

MANIFEST_NAME = "PACKAGE_MANIFEST.json"
EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "env", "__pycache__", ".pytest_cache",
    ".ruff_cache", ".mypy_cache", ".tox", ".nox", "node_modules", "dist",
    "build", "coverage", "htmlcov", "local-workspace", "private-memory",
    "personal-memory", "private-data", "private-projects", "participant-data",
    "research-recordings", "secrets", "credentials",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".zip", ".log", ".tmp", ".bak", ".swp", ".swo"}


def is_packaged_source(path: Path, root: Path) -> bool:
    """Return whether a path is safe and appropriate to include in a source ZIP."""
    if path.is_symlink() or not path.is_file():
        return False
    relative = path.relative_to(root)
    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False
    if path.name == MANIFEST_NAME or path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    if path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example"):
        return False
    return True


def collect_file_entries(root: Path) -> list[dict[str, Any]]:
    """Collect sorted path/size/SHA-256 entries, excluding generated and private data."""
    root = root.resolve()
    entries: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*")):
        if not is_packaged_source(path, root):
            continue
        data = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return entries


def manifest_differences(root: Path, manifest: dict[str, Any]) -> list[str]:
    """Compare manifest file coverage, byte counts, and hashes with the working tree."""
    errors: list[str] = []
    recorded = manifest.get("files")
    if not isinstance(recorded, list):
        return ["manifest 'files' must be an array"]

    current = collect_file_entries(root)
    current_by_path = {entry["path"]: entry for entry in current}
    recorded_by_path: dict[str, dict[str, Any]] = {}
    for item in recorded:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            errors.append("manifest contains an invalid file entry")
            continue
        file_path = item["path"]
        if file_path in recorded_by_path:
            errors.append(f"manifest contains duplicate path: {file_path}")
        recorded_by_path[file_path] = item

    for file_path in sorted(set(current_by_path) - set(recorded_by_path)):
        errors.append(f"manifest missing source file: {file_path}")
    for file_path in sorted(set(recorded_by_path) - set(current_by_path)):
        errors.append(f"manifest contains unexpected or excluded file: {file_path}")
    for file_path in sorted(set(current_by_path) & set(recorded_by_path)):
        expected = current_by_path[file_path]
        actual = recorded_by_path[file_path]
        if actual.get("bytes") != expected["bytes"]:
            errors.append(f"manifest size mismatch: {file_path}")
        if actual.get("sha256") != expected["sha256"]:
            errors.append(f"manifest SHA-256 mismatch: {file_path}")
    return errors
