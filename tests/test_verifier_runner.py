"""Guards against incomplete test groups and hidden verifier failures."""
from __future__ import annotations

import subprocess
from types import SimpleNamespace

from tools import verify


def test_groups_exhaustively_cover_modules() -> None:
    assert verify.validate_pytest_coverage()


def test_timeout_is_failure(monkeypatch) -> None:
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=args[0], timeout=kwargs["timeout"])
    monkeypatch.setattr(verify.subprocess, "run", timeout)
    assert not verify.run_step("timeout-test", ["-V"], 1)


def test_nonzero_is_failure(monkeypatch) -> None:
    monkeypatch.setattr(verify.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=2))
    assert not verify.run_step("nonzero-test", ["-V"], 1)


def test_success_passes(monkeypatch) -> None:
    monkeypatch.setattr(verify.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0))
    assert verify.run_step("success-test", ["-V"], 1)
