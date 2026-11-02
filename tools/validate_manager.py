#!/usr/bin/env python3
"""Validate Stage 2 catalog contracts and manual manager export."""

from __future__ import annotations

try:
    from .capability_manager import ROOT, contracts, load_catalog
    from .build_manager_adapter import render
except ImportError:
    from capability_manager import ROOT, contracts, load_catalog
    from build_manager_adapter import render


def main() -> int:
    try:
        _, errors = contracts(ROOT, load_catalog(ROOT))
        if errors:
            raise ValueError("; ".join(errors))
        render(ROOT)
    except (OSError, ValueError, TypeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(
        "PASS: manager capability contracts and manual export; no capability execution or runtime certification."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
