#!/usr/bin/env python3
"""Build and verify a deterministic, repository-root ZIP for Friday uploads."""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from .package_manifest import manifest_differences
except ImportError:  # Support direct execution as `python tools/package_release.py`.
    from package_manifest import manifest_differences

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "PACKAGE_MANIFEST.json"


def load_manifest(root: Path) -> dict[str, Any]:
    path = root / "PACKAGE_MANIFEST.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(manifest.get("files"), list):
        raise ValueError("PACKAGE_MANIFEST.json must contain a files array")
    return manifest


def validate_manifest_paths(files: list[dict[str, Any]]) -> None:
    seen: set[str] = set()
    for item in files:
        name = item.get("path")
        if not isinstance(name, str) or not name:
            raise ValueError("Manifest contains an empty or invalid path")
        pure = PurePosixPath(name)
        if pure.is_absolute() or ".." in pure.parts or "\\" in name:
            raise ValueError(f"Unsafe manifest path: {name}")
        if name == "PACKAGE_MANIFEST.json":
            raise ValueError("Manifest must not list itself")
        if name in seen:
            raise ValueError(f"Duplicate manifest path: {name}")
        seen.add(name)


def manifest_tree_errors(root: Path, manifest: dict[str, Any]) -> list[str]:
    """Verify manifest paths, sizes, and hashes against the working tree."""
    errors: list[str] = []
    entries = manifest["files"]
    try:
        validate_manifest_paths(entries)
    except ValueError as exc:
        return [str(exc)]

    recorded = {item["path"]: item for item in entries}
    for name, item in recorded.items():
        path = root / PurePosixPath(name)
        if not path.is_file() or path.is_symlink():
            errors.append(f"Missing or unsafe source file: {name}")
            continue
        payload = path.read_bytes()
        if len(payload) != item.get("bytes"):
            errors.append(f"Size mismatch: {name}")
        digest = hashlib.sha256(payload).hexdigest()
        if digest != item.get("sha256"):
            errors.append(f"SHA-256 mismatch: {name}")
    return errors


def build_release_archive(root: Path, output: Path) -> int:
    """Write all manifest-listed files at the ZIP root plus the manifest."""
    root = root.resolve()
    output = output.resolve()
    manifest = load_manifest(root)
    errors = manifest_tree_errors(root, manifest)
    errors.extend(manifest_differences(root, manifest))
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and output.is_dir():
        print(f"FAIL: output is a directory: {output}", file=sys.stderr)
        return 1

    entries = sorted(manifest["files"], key=lambda item: item["path"])
    temporary_output = output.with_name(output.name + ".tmp")
    temporary_output.unlink(missing_ok=True)
    try:
        with zipfile.ZipFile(temporary_output, "w") as archive:
            for item in entries:
                path = root / PurePosixPath(item["path"])
                info = zipfile.ZipInfo(item["path"], date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (stat.S_IFREG | (path.stat().st_mode & 0o777)) << 16
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED)

            manifest_info = zipfile.ZipInfo("PACKAGE_MANIFEST.json", date_time=(2026, 1, 1, 0, 0, 0))
            manifest_info.compress_type = zipfile.ZIP_DEFLATED
            manifest_info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(
                manifest_info,
                (root / "PACKAGE_MANIFEST.json").read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
            )
    except (OSError, zipfile.BadZipFile) as exc:
        temporary_output.unlink(missing_ok=True)
        print(f"FAIL: cannot create archive: {exc}", file=sys.stderr)
        return 1

    ok, message = verify_release_archive(temporary_output)
    if not ok:
        temporary_output.unlink(missing_ok=True)
        print(f"FAIL: {message}", file=sys.stderr)
        return 1
    temporary_output.replace(output)
    print(f"PASS: created {output} with {len(entries) + 1} root-level files.")
    print("Archive layout: repository contents at ZIP root (no enclosing Friday/ directory).")
    print(message)
    return 0


def verify_release_archive(archive_path: Path) -> tuple[bool, str]:
    """Check ZIP integrity, exact file coverage, byte counts, and SHA-256 hashes."""
    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            bad_member = archive.testzip()
            if bad_member:
                return False, f"ZIP CRC failure: {bad_member}"
            names = archive.namelist()
            if len(names) != len(set(names)):
                return False, "ZIP contains duplicate member paths"
            if any(name.startswith("Friday/") for name in names):
                return False, "ZIP has an enclosing Friday/ directory; expected repository-root layout"
            if "PACKAGE_MANIFEST.json" not in names:
                return False, "ZIP is missing PACKAGE_MANIFEST.json"
            manifest = json.loads(archive.read("PACKAGE_MANIFEST.json").decode("utf-8"))
            entries = manifest.get("files")
            if not isinstance(entries, list):
                return False, "Embedded manifest has no files array"
            validate_manifest_paths(entries)
            expected = {item["path"] for item in entries} | {"PACKAGE_MANIFEST.json"}
            actual = set(names)
            if actual != expected:
                missing = sorted(expected - actual)
                extra = sorted(actual - expected)
                return False, f"ZIP coverage mismatch; missing={missing[:5]}, extra={extra[:5]}"
            for item in entries:
                payload = archive.read(item["path"])
                if len(payload) != item.get("bytes"):
                    return False, f"ZIP size mismatch: {item['path']}"
                digest = hashlib.sha256(payload).hexdigest()
                if digest != item.get("sha256"):
                    return False, f"ZIP SHA-256 mismatch: {item['path']}"
    except (OSError, zipfile.BadZipFile, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        return False, f"ZIP verification error: {exc}"
    return True, f"PASS: ZIP integrity and all {len(entries)} source hashes verified."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Friday repository root")
    parser.add_argument("--output", type=Path, required=True, help="destination ZIP path")
    args = parser.parse_args()
    return build_release_archive(args.root, args.output)


if __name__ == "__main__":
    raise SystemExit(main())
