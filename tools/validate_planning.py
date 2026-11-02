#!/usr/bin/env python3
"""Validate the portable examples; no model/user execution is inferred."""

from __future__ import annotations

try:
    from .handoff import ROOT, validate
except ImportError:
    from handoff import ROOT, validate


def main() -> int:
    failures = []
    for mode in ["fast", "standard", "deep"]:
        _, errors = validate(ROOT / "examples/planning-handoff" / mode)
        failures.extend(f"{mode}: {error}" for error in errors)
    if failures:
        print("\n".join(failures))
        return 1
    print(
        "PASS: three synthetic mode dossiers/handoffs; integrity and traceability only, not model behavior."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
