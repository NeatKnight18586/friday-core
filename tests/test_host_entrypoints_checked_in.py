"""The ready-to-upload repository must contain both generated coding-host skills."""
from __future__ import annotations

from pathlib import Path

from tools.sync_host_entrypoints import HOSTS, validate

ROOT = Path(__file__).resolve().parents[1]


def test_generated_host_directories_are_exact() -> None:
    assert validate(ROOT) == []


def test_host_entrypoints_and_guides_are_present() -> None:
    for host in HOSTS.values():
        assert (ROOT / host["prefix"] / "SKILL.md").is_file()
        assert (ROOT / host["guidance"]).is_file()
