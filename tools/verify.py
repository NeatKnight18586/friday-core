#!/usr/bin/env python3
"""Run independent, bounded validation processes for Friday's release checks.

Each validator runs in a fresh interpreter to prevent shared module/pytest state from
contaminating later checks. Pytest modules run in bounded groups, not one giant process.
This checks repository behavior, not actual model behavior in provider applications.
"""
from __future__ import annotations

import argparse
import compileall
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Ordered, independent script invocations; no evaluator changes are needed.
VALIDATORS = (
    ("Repository integrity", "tools/validate_repo.py"),
    ("B2 schemas and workspace", "tools/validate_b2.py"),
    ("B4 vertical slice", "tools/validate_vertical_slice.py"),
    ("B5 research", "tools/validate_b5.py"),
    ("B6 NUTS", "tools/validate_b6.py"),
    ("Capability registry", "tools/validate_capabilities.py"),
    ("Manager contracts", "tools/validate_manager.py"),
    ("Portable planning", "tools/validate_planning.py"),
    ("Context budget", "tools/inspect_context.py"),
    ("B7 Four-Council", "tools/validate_b7.py"),
    ("B8 delivery", "tools/validate_b8.py"),
    ("B9 packages", "tools/validate_b9.py"),
    ("Cross-host installation", "tools/validate_host_adapters.py"),
    ("B10 evaluations", "tools/validate_b10.py"),
    ("Claude Chat companion", "tools/validate_claude_chat.py"),
)

# Every module must occur exactly once. Grouping isolates the known cross-module
# order/process interaction in integration tests while retaining all assertions.
PYTEST_GROUPS = (
    ("Project initializer", ("tests/test_init_project.py",)),
    ("Capability manager", ("tests/test_capability_manager.py",)),
    ("Planning handoff", ("tests/test_planning_handoff.py",)),
    ("B5 research", ("tests/test_b5_research.py",)),
    ("B6 NUTS", ("tests/test_b6_nuts.py",)),
    ("B7 Four-Council", ("tests/test_b7_four_council.py",)),
    ("B8 delivery", ("tests/test_b8_delivery.py",)),
    ("Shared, packaging, and release", (
        "tests/test_b9_packaging.py", "tests/test_b10_acceptance.py",
        "tests/test_claude_chat_companion.py", "tests/test_configuration.py",
        "tests/test_context_architecture.py", "tests/test_hackathon_sprint.py",
        "tests/test_host_adapters.py", "tests/test_manifest.py",
        "tests/test_package_release.py", "tests/test_validation.py",
        "tests/test_vertical_slice.py", "tests/test_verifier_runner.py",
        "tests/test_host_entrypoints_checked_in.py",
    )),
)


def run_step(label: str, args: list[str], timeout_seconds: int = 180) -> bool:
    """Run one bounded check and expose its output directly to CI/user logs."""
    print(f"\n=== {label} ===", flush=True)
    env = os.environ.copy()
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    try:
        result = subprocess.run(
            [sys.executable, *args], cwd=ROOT, env=env, check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        print(f"FAIL: {label} exceeded {timeout_seconds} seconds.", flush=True)
        return False
    except OSError as exc:
        print(f"FAIL: {label} could not launch: {exc}", flush=True)
        return False
    if result.returncode:
        print(f"FAIL: {label} returned {result.returncode}.", flush=True)
        return False
    print(f"PASS: {label}", flush=True)
    return True


def validate_pytest_coverage() -> bool:
    expected = {p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("test_*.py")}
    configured = [name for _, names in PYTEST_GROUPS for name in names]
    if len(configured) != len(set(configured)) or set(configured) != expected:
        print("FAIL: pytest groups must cover all and only test modules exactly once.", flush=True)
        print(f"missing={sorted(expected-set(configured))}, extra={sorted(set(configured)-expected)}", flush=True)
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-lint", action="store_true", help="local fallback only; CI runs Ruff")
    args = parser.parse_args()
    if sys.version_info < (3, 11):
        print("FAIL: Python 3.11+ required", flush=True)
        return 2
    print(f"Friday verification | Python {sys.version.split()[0]} | {sys.platform}", flush=True)
    if not (compileall.compile_dir(ROOT / "tools", quiet=1) and compileall.compile_dir(ROOT / "tests", quiet=1)):
        print("FAIL: Python compilation", flush=True)
        return 1
    if not validate_pytest_coverage():
        return 1
    failures: list[str] = []
    for label, script in VALIDATORS:
        if not run_step(label, [script]):
            failures.append(label)
    if args.skip_lint:
        print("NOT RUN: Ruff (--skip-lint).", flush=True)
    elif not run_step("Ruff", ["-m", "ruff", "check", "tools", "tests"]):
        failures.append("Ruff")
    for label, modules in PYTEST_GROUPS:
        if not run_step(f"Pytest: {label}", ["-m", "pytest", "-q", *modules]):
            failures.append(f"Pytest: {label}")
    if failures:
        print("\nVERIFY FAILED: " + ", ".join(failures), flush=True)
        return 1
    print("\nVERIFY PASSED" + (" WITH LINT SKIPPED" if args.skip_lint else ""), flush=True)
    print("Provider UI/model runtime and remote CI remain separate acceptance checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
