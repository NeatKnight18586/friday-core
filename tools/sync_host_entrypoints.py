#!/usr/bin/env python3
"""Generate or check repo-local Claude Code/Codex skill folders from canonical Peanuts.

The checked-in host directories are generated distribution snapshots, NOT second
sources of truth. Use --sync after canonical changes; CI uses --check to catch drift.
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_skill_packages import build_all  # noqa: E402
from tools.validate_host_adapters import _safe_extract, HOSTS  # noqa: E402


def expected_host_files(root: Path) -> dict[str, bytes]:
    """Render and preflight the two canonical host archives in a temporary fixture."""
    expected: dict[str, bytes] = {}
    with tempfile.TemporaryDirectory(prefix="friday-repo-host-entrypoints-") as temporary:
        scratch = Path(temporary)
        outputs = scratch / "packages"
        build_all(outputs, root=root)
        for host, settings in HOSTS.items():
            dest = scratch / f"unpack-{host}"
            names = _safe_extract(outputs / settings["archive"], dest)
            prefix = settings["prefix"] + "/"
            if not names or any(not name.startswith(prefix) for name in names):
                raise ValueError(f"unexpected {host} adapter path")
            for name in names:
                if name in expected:
                    raise ValueError(f"host adapter collision: {name}")
                expected[name] = (dest / name).read_bytes()
    return expected


def validate(root: Path = ROOT) -> list[str]:
    expected = expected_host_files(root)
    errors: list[str] = []
    for name, data in expected.items():
        path = root / name
        if not path.is_file() or path.is_symlink():
            errors.append(f"missing generated host path: {name}")
        elif path.read_bytes() != data:
            errors.append(f"generated host source drift: {name}")
    for settings in HOSTS.values():
        base = root / settings["prefix"]
        if base.is_dir():
            for path in base.rglob("*"):
                if path.is_symlink():
                    errors.append(f"unsafe generated host symlink: {path}")
                elif path.is_file() and path.relative_to(root).as_posix() not in expected:
                    errors.append(f"unexpected generated host file: {path.relative_to(root)}")
    return errors


def sync(root: Path = ROOT) -> int:
    expected = expected_host_files(root)
    for name, data in expected.items():
        path = root / name
        if path.is_symlink():
            raise ValueError(f"refusing to overwrite symlink: {name}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: generated {len(expected)} host files from canonical Peanuts, both paths checked.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--sync", action="store_true", help="generate checked-in host folders")
    mode.add_argument("--check", action="store_true", help="verify byte-identical host folders")
    args = parser.parse_args()
    if args.sync:
        return sync()
    errors = validate()
    if errors:
        for issue in errors[:12]:
            print(f"FAIL: {issue}")
        if len(errors) > 12:
            print(f"... and {len(errors)-12} further issues")
        return 1
    print("PASS: repo-local Codex/Claude Code skill files match generated canonical adapters.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
