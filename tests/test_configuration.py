from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_pyproject_declares_supported_tool_configuration() -> None:
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]
    assert config["tool"]["ruff"]["target-version"] == "py311"


def test_devcontainer_is_valid_and_uses_non_root_user() -> None:
    config = json.loads((ROOT / ".devcontainer/devcontainer.json").read_text(encoding="utf-8"))
    assert config["image"].startswith(
        "mcr.microsoft.com/devcontainers/python:dev-3.13-bookworm@sha256:"
    )
    assert config["image"].endswith(
        "1244ac1d9a88c54fc7d9591696a21bf83854687b9ce1a148185c3922b305daaa"
    )
    assert config["remoteUser"] != "root"
    assert "requirements-dev.txt" in config["postCreateCommand"]
    assert re.search(r"@sha256:[0-9a-f]{64}$", config["image"])


def test_ci_workflow_is_valid_and_action_refs_are_full_shas() -> None:
    workflow_text = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
    workflow = yaml.load(workflow_text, Loader=yaml.BaseLoader)
    assert "pull_request" in workflow["on"]
    assert "workflow_dispatch" in workflow["on"]
    assert workflow["permissions"] == {"contents": "read"}

    job = workflow["jobs"]["validate"]
    matrix = job["strategy"]["matrix"]
    assert set(matrix["os"]) == {"ubuntu-latest", "windows-latest", "macos-latest"}
    assert set(matrix["python-version"]) == {"3.11", "3.12", "3.13", "3.14"}
    assert job["timeout-minutes"] == "20"

    steps = job["steps"]
    checkout = next(step for step in steps if step.get("uses", "").startswith("actions/checkout@"))
    setup_python = next(step for step in steps if step.get("uses", "").startswith("actions/setup-python@"))
    assert checkout["with"]["persist-credentials"] == "false"
    assert setup_python["with"]["cache"] == "pip"
    assert setup_python["with"]["cache-dependency-path"] == "requirements-dev.txt"
    assert any(step.get("run") == "python tools/verify.py" for step in steps)
    assert "secrets." not in workflow_text

    refs = re.findall(r"(?m)^\s*uses:\s*([^\s#]+)", workflow_text)
    assert refs
    assert all(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}", ref) for ref in refs)


def test_dependabot_covers_workflow_and_python_dependencies() -> None:
    config = yaml.load(
        (ROOT / ".github/dependabot.yml").read_text(encoding="utf-8"),
        Loader=yaml.BaseLoader,
    )
    ecosystems = {item["package-ecosystem"] for item in config["updates"]}
    assert {"pip", "github-actions"}.issubset(ecosystems)


def test_development_requirements_use_exact_version_snapshot() -> None:
    requirements = (ROOT / "requirements-dev.txt").read_text(encoding="utf-8")
    entries = [
        line.strip()
        for line in requirements.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert entries
    assert all("==" in line and not line.startswith(("-", ".")) for line in entries)
    normalized = {line.split("==", 1)[0].lower().replace("_", "-") for line in entries}
    assert {"jsonschema", "pytest", "pyyaml", "ruff"}.issubset(normalized)


def test_windows_style_git_checkout_preserves_source_bytes(tmp_path) -> None:
    """Exercise checkout conversion, including files without a covered extension."""
    import os
    import shutil
    import subprocess

    import pytest

    if shutil.which("git") is None:
        pytest.skip("Git is required for the checkout conversion regression")
    source = tmp_path / "source"
    checkout = tmp_path / "checkout"
    source.mkdir()
    names = [
        ".gitattributes", ".editorconfig", ".gitignore", ".python-version", "LICENSE",
        "evals/results/results.jsonl",
        "examples/vertical-slice-synthetic/campus-service-status/records/claims.jsonl",
        "templates/project/records/analogies.jsonl", "templates/project/records/nuts-runs.jsonl",
    ]
    expected = {name: (ROOT / name).read_bytes() for name in names}
    expected["asset.png"] = b"\x89PNG\r\n\x00binary\n"
    for name, payload in expected.items():
        path = source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}

    def git(*args):
        subprocess.run(["git", *args], cwd=source, env=env, check=True,
                       capture_output=True, encoding="utf-8")

    git("init", "--quiet")
    git("-c", "core.autocrlf=false", "add", "-f", ".")
    git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Checkout fixture")
    git("-c", "core.autocrlf=true", "clone", "--quiet", "--no-local", str(source), str(checkout))
    assert {name: (checkout / name).read_bytes() for name in expected} == expected
