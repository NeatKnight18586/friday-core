#!/usr/bin/env python3
"""Create or check the Friday source-package manifest."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from .package_manifest import collect_file_entries, manifest_differences
except ImportError:  # Support direct execution as `python tools/update_manifest.py`.
    from package_manifest import collect_file_entries, manifest_differences

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "PACKAGE_MANIFEST.json"
DEFAULT_VERSION = "0.15.0-rc.3"
DEFAULT_MILESTONE = "Stage 2 — Minimal manager and CI/host preflight"
DEFAULT_STATUS = (
    "STAGE_2_CHECKPOINT: public-release preparation with a provider-neutral canonical Peanuts core. "
    "Read-only Friday selection/intake and a manual manager adapter are implemented; no autonomous execution. "
    "Deterministic verification evidence is in RELEASE_VERIFICATION.md. "
    "Live host acceptance, method effectiveness, and measured savings remain unverified. Hosted CI status is recorded per commit in GitHub Actions. "
    "Existing MIT license preserved; owner selected friday-core for clean source publication; third-party rights and public-release acceptance remain pending; no universal compatibility claim."
)


def create_manifest() -> dict:
    now = datetime.now(timezone.utc).date().isoformat()
    return {
        "project": "Friday / Peanuts",
        "version": DEFAULT_VERSION,
        "milestone": DEFAULT_MILESTONE,
        "status": DEFAULT_STATUS,
        "generated_date": now,
        "schema_version": "1.0.0",
        "files": collect_file_entries(ROOT),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="check the existing manifest without modifying it",
    )
    args = parser.parse_args()

    if args.check:
        try:
            manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"FAIL: cannot read manifest: {exc}", file=sys.stderr)
            return 1
        errors = manifest_differences(ROOT, manifest)
        if errors:
            print(f"FAIL: {len(errors)} manifest issue(s)")
            for error in errors:
                print(f"- {error}")
            print("Run: python tools/update_manifest.py")
            return 1
        print(f"PASS: manifest covers and matches {len(manifest['files'])} source files.")
        return 0

    manifest = create_manifest()
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Updated {MANIFEST_PATH.relative_to(ROOT)} with {len(manifest['files'])} source files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
