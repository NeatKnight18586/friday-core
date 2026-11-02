from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.init_project import slugify

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("My New Project", "my-new-project"),
        ("  Friday_Peanuts  ", "friday-peanuts"),
        ("Project_2026", "project-2026"),
    ],
)
def test_slugify_normalizes_project_ids(value: str, expected: str) -> None:
    assert slugify(value) == expected


@pytest.mark.parametrize("value", ["", "---", "../escape", "a/b/../../bad", "你好"])
def test_slugify_rejects_unsafe_or_empty_ids(value: str) -> None:
    with pytest.raises(ValueError):
        slugify(value)


def run_initializer(workspace: Path, project_id: str = "test-project") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/init_project.py"),
            "--id", project_id,
            "--title", "Test Project",
            "--mode", "MODE-IDEA",
            "--workspace-root", str(workspace),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_initializer_creates_complete_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "projects"
    result = run_initializer(workspace)
    project_dir = workspace / "test-project"

    assert result.returncode == 0, result.stderr
    assert (project_dir / "project.json").is_file()
    assert (project_dir / "state.json").is_file()
    assert (project_dir / "records/sources.jsonl").is_file()
    assert (project_dir / "records/claims.jsonl").is_file()
    assert (project_dir / "records/assumptions.jsonl").is_file()
    assert (project_dir / "records/decisions.jsonl").is_file()
    assert (project_dir / "evaluations/results.jsonl").is_file()
    assert (project_dir / "research-plan.json").is_file()
    assert (project_dir / "records/research-questions.jsonl").is_file()
    assert (project_dir / "records/research-findings.jsonl").is_file()
    assert (project_dir / "records/research-rounds.jsonl").is_file()
    assert (project_dir / "records/opportunities.jsonl").is_file()
    research_plan = json.loads((project_dir / "research-plan.json").read_text(encoding="utf-8"))
    assert research_plan["project_id"] == "test-project"
    assert research_plan["desired_outcome"] == "To be clarified with the project owner."

    project = json.loads((project_dir / "project.json").read_text(encoding="utf-8"))
    assert project["project_id"] == "test-project"
    assert project["mode"] == "MODE-IDEA"


def test_initializer_refuses_to_overwrite_existing_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "projects"
    first = run_initializer(workspace)
    assert first.returncode == 0, first.stderr
    project_file = workspace / "test-project/project.json"
    before = project_file.read_bytes()

    second = run_initializer(workspace)
    after = project_file.read_bytes()

    assert second.returncode != 0
    assert "refusing to overwrite" in second.stderr
    assert before == after


def test_initializer_rejects_path_traversal(tmp_path: Path) -> None:
    result = run_initializer(tmp_path / "projects", "../outside")
    assert result.returncode == 2
    assert not (tmp_path / "outside").exists()
