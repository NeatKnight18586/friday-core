#!/usr/bin/env python3
"""Export compact Friday instructions and catalog/contracts for manual chat attachment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .capability_manager import ROOT, catalog_summary, contracts, load_catalog
except ImportError:
    from capability_manager import ROOT, catalog_summary, contracts, load_catalog


def render(root: Path = ROOT) -> str:
    registry = load_catalog(root)
    contract_data, errors = contracts(root, registry)
    if errors:
        raise ValueError("; ".join(errors))
    summary = catalog_summary(root)
    profiles = {entry["id"]: entry["host_profiles"] for entry in registry["capabilities"]}
    return (
        "\n\n".join(
            [
                "> Generated manual manager adapter. No capability bodies, executable tools or private profile are included. Attach/install the selected capability separately; this file does not install a native manager Skill.",
                (root / "FRIDAY.md").read_text(encoding="utf-8").strip(),
                "## Catalog metadata (data, not instructions)\n\n```json\n"
                + json.dumps(
                    {
                        "registry_version": registry["registry_version"],
                        "catalog": summary["capabilities"],
                        "contracts": contract_data,
                        "host_profiles": profiles,
                    },
                    indent=2,
                )
                + "\n```",
                "If a referenced repository command/file is unavailable, report NOT RUN or missing-package status. Do not pretend this manual export provides filesystem access. Fresh-chat use needs the latest reviewed handoff and the selected capability resources.",
            ]
        )
        + "\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "build/manager")
    args = parser.parse_args()
    try:
        content = render()
        args.out.mkdir(parents=True, exist_ok=True)
        (args.out / "Friday-Manager.txt").write_text(content, encoding="utf-8")
    except (OSError, ValueError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(
        "PASS: generated manual Friday-Manager.txt; selected capability installation/runtime remains separate."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
