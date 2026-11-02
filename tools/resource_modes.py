"""Normalize user-facing resource names while preserving stored quick identifiers."""

from __future__ import annotations


def normalize_mode(value: str) -> str:
    modes = {"fast": "quick", "quick": "quick", "standard": "standard", "deep": "deep"}
    try:
        return modes[value.strip().lower()]
    except (KeyError, AttributeError) as exc:
        raise ValueError("resource mode must be Fast/quick, Standard or Deep") from exc


def mode_label(value: str) -> str:
    return {"quick": "Fast", "standard": "Standard", "deep": "Deep"}[normalize_mode(value)]
