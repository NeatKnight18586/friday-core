#!/usr/bin/env python3
"""Validate the Claude Chat Skill and Friday Project companion."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_claude_chat_companion import (  # noqa: E402 — direct script path bootstrap
    PROJECT_KNOWLEDGE,
    build_all,
    compile_project_knowledge,
    load_project_instructions,
)
from tools.build_skill_packages import copy_skill_files, load_skill_metadata  # noqa: E402

EXPECTED_RESULTS = {
    "EVAL-135": "passed",
    "EVAL-136": "passed",
    "EVAL-137": "passed",
    "EVAL-138": "blocked",
    "EVAL-139": "blocked",
    "EVAL-140": "blocked",
    "EVAL-141": "passed",
    "EVAL-142": "passed",
    "EVAL-143": "passed",
    "EVAL-144": "blocked",
    "EVAL-145": "blocked",
    "EVAL-146": "blocked",
}


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        metadata, _ = load_skill_metadata(root / "skills/peanuts")
        description = metadata.get("description")
        if metadata.get("name") != "peanuts":
            errors.append("canonical skill name must remain 'peanuts'")
        if not isinstance(description, str) or not description.strip() or len(description) > 200:
            errors.append("Claude consumer Skill description must be 1–200 characters")
        instructions = load_project_instructions(root)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"Claude Chat source validation failed: {exc}"]

    if len(instructions.decode("utf-8")) > 6000:
        errors.append("Claude Project instructions exceed the 6000-character maintainability budget")

    for relative in (
        "adapters/claude-chat/SETUP_IPAD.md",
        "adapters/claude-chat/SMOKE_TESTS.md",
        "adapters/claude-chat/RUN_RECORD_TEMPLATE.md",
        "evals/rubrics/CLAUDE_CHAT_AND_PROJECT_QUALITY.md",
        "docs/acceptance/CLAUDE_CHAT_PROJECT_ACCEPTANCE.md",
    ):
        path = root / relative
        if not path.is_file() or path.is_symlink():
            errors.append(f"required Claude Chat acceptance file missing or unsafe: {relative}")

    schema_path = root / "schemas/evaluation-case.schema.json"
    result_schema_path = root / "schemas/evaluation-result.schema.json"
    try:
        case_validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")))
        result_validator = Draft202012Validator(
            json.loads(result_schema_path.read_text(encoding="utf-8")),
            format_checker=FormatChecker(),
        )
    except (OSError, json.JSONDecodeError) as exc:
        return errors + [f"cannot load shared evaluation schemas: {exc}"]

    case_ids: set[str] = set()
    for number in range(135, 147):
        path = root / "evals/cases" / f"EVAL-{number}.json"
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
            continue
        for issue in case_validator.iter_errors(case):
            errors.append(f"{path.relative_to(root)} {list(issue.absolute_path)}: {issue.message}")
        case_id = case.get("case_id")
        if case_id in case_ids:
            errors.append(f"duplicate Claude Chat case: {case_id}")
        case_ids.add(case_id)
        if case.get("case_status") != "ready":
            errors.append(f"{case_id} must be marked ready for later model evaluation")
        for ref in case.get("rubric_refs", []):
            if not (root / "evals/rubrics" / ref).is_file():
                errors.append(f"{case_id} references missing rubric: {ref}")
    if len(case_ids) != 12:
        errors.append(f"expected 12 Claude Chat cases EVAL-135–146, found {len(case_ids)}")

    result_path = root / "evals/results/results.jsonl"
    results: dict[str, dict[str, Any]] = {}
    try:
        lines = result_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return errors + [f"cannot read evaluation result ledger: {exc}"]
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            result = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"results.jsonl:{line_number}: {exc}")
            continue
        for issue in result_validator.iter_errors(result):
            errors.append(f"results.jsonl:{line_number} {list(issue.absolute_path)}: {issue.message}")
        if result.get("result_id") in results:
            errors.append(f"duplicate result ID: {result.get('result_id')}")
        results[result.get("result_id")] = result

    for case_id, expected_status in EXPECTED_RESULTS.items():
        matching = [r for r in results.values() if r.get("case_id") == case_id]
        if len(matching) != 1:
            errors.append(f"expected one Claude Chat result for {case_id}; found {len(matching)}")
        else:
            record = matching[0]
            if record.get("status") != expected_status:
                errors.append(f"{case_id} must remain {expected_status}; found {record.get('status')}")
            if record.get("reviewer_approved") is not False:
                errors.append(f"{case_id} must remain unapproved pending owner-side review")

    # Build the actual generated outputs in a temporary directory and validate their exact contents.
    try:
        with tempfile.TemporaryDirectory(prefix="friday-claude-chat-") as temporary:
            out = Path(temporary)
            build_all(out, root=root)
            skill_zip = out / "peanuts-claude-chat-skill.zip"
            with zipfile.ZipFile(skill_zip) as archive:
                names = set(archive.namelist())
                canonical = copy_skill_files(root)
                expected = {f"peanuts/{'skill.md' if name == 'SKILL.md' else name}" for name in canonical}
                if names != expected:
                    errors.append("Claude Chat Skill ZIP file set does not exactly match generated canonical resources")
                if "peanuts/skill.md" not in names:
                    errors.append("Claude Chat Skill ZIP must contain lowercase peanuts/skill.md")
                if "peanuts/SKILL.md" in names:
                    errors.append("Claude Chat Skill ZIP must not contain a duplicate uppercase SKILL.md")
                if archive.testzip() is not None:
                    errors.append("Claude Chat Skill ZIP CRC check failed")
                for name, data in canonical.items():
                    packaged_name = f"peanuts/{'skill.md' if name == 'SKILL.md' else name}"
                    if packaged_name in names and archive.read(packaged_name) != data:
                        errors.append(f"Claude Chat package drift from canonical source: {packaged_name}")
                skill_bytes = archive.read("peanuts/skill.md") if "peanuts/skill.md" in names else b""
                skill_text = skill_bytes.decode("utf-8")
                match = re.match(r"\A---\s*\n(.*?)\n---", skill_text, re.DOTALL)
                if not match:
                    errors.append("Claude Chat skill.md frontmatter is missing or malformed")
                else:
                    skill_metadata = yaml.safe_load(match.group(1))
                    if skill_metadata.get("name") != "peanuts":
                        errors.append("Claude Chat skill metadata name must match the 'peanuts' folder")
                    if len(skill_metadata.get("description", "")) > 200:
                        errors.append("Claude Chat skill description exceeds Anthropic's documented 200-character limit")

            project_zip = out / "friday-peanuts-claude-project-knowledge.zip"
            with zipfile.ZipFile(project_zip) as archive:
                expected_names = set(PROJECT_KNOWLEDGE)
                if set(archive.namelist()) != expected_names:
                    errors.append("Claude Project knowledge ZIP must contain exactly the five curated .txt files")
                if any(not name.endswith(".txt") for name in archive.namelist()):
                    errors.append("Claude Project knowledge files must use .txt extensions")
                if archive.testzip() is not None:
                    errors.append("Claude Project knowledge ZIP CRC check failed")
                for name, sources in PROJECT_KNOWLEDGE.items():
                    if name in archive.namelist():
                        expected_data = compile_project_knowledge(root, name, sources)
                        if archive.read(name) != expected_data:
                            errors.append(f"Claude Project knowledge drift: {name}")

    except (OSError, ValueError, zipfile.BadZipFile, yaml.YAMLError) as exc:
        errors.append(f"Claude Chat package build/validation failed: {exc}")

    # Required semantic claims in the setup and Project instructions.
    setup = (root / "adapters/claude-chat/SETUP_IPAD.md").read_text(encoding="utf-8").lower()
    for phrase in ("ordinary claude chat", "lowercase `peanuts/skill.md`", "claude code", "project knowledge", "not a git checkout", "`.txt` documents", "not a claude file-count limit"):
        if phrase not in setup:
            errors.append(f"Claude Chat iPad setup is missing boundary/installation phrase: {phrase}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"FAIL: {len(errors)} Claude Chat integration issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: Claude Chat Skill entrypoint/metadata, canonical parity, Project knowledge, instructions, twelve EVAL cases and owner-side runtime blocks validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
