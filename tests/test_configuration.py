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
