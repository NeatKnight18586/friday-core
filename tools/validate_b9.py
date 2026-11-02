#!/usr/bin/env python3
"""Validate B9 Agent Skills metadata, host adapters, ChatGPT Project pack and eval cases."""
from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - environment-specific
    print(f"ERROR: missing validation dependency: {exc}. Install requirements-dev.txt.", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_skill_packages import (  # noqa: E402
    CHATGPT_FILES,
    SCHEMA_GROUPS,
    build_all,
    copy_skill_files,
    load_skill_metadata,
    sha256_bytes,
    validate_canonical_skill,
)


def validate_eval_cases(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    schema = json.loads((root / "schemas/evaluation-case.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    count = 0
    for number in range(88, 103):
        path = root / "evals" / "cases" / f"EVAL-{number:03d}.json"
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path.relative_to(root)}: {exc}")
            continue
        count += 1
        for issue in validator.iter_errors(case):
            errors.append(f"{path.relative_to(root)}: {list(issue.absolute_path)}: {issue.message}")
        if case.get("case_status") != "ready":
            errors.append(f"{path.relative_to(root)}: B9 evaluation case must be ready")
        for rubric_ref in case.get("rubric_refs", []):
            if not (root / "evals/rubrics" / rubric_ref).is_file():
                errors.append(f"{path.relative_to(root)}: missing rubric reference {rubric_ref}")
    if count != 15:
        errors.append(f"expected 15 B9 evaluation cases (EVAL-088–102), found {count}")
    return errors


def validate_packaged_markdown_links(files: dict[str, bytes]) -> list[str]:
    """Require every relative Markdown link in a standalone bundle to resolve."""
    errors: list[str] = []
    for source_path, payload in files.items():
        if not source_path.lower().endswith(".md"):
            continue
        try:
            content = payload.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"packaged Markdown file is not UTF-8: {source_path}")
            continue
        # Avoid treating examples inside fenced code blocks as live navigation links.
        content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
            target = target.split("#", 1)[0].split("?", 1)[0].strip()
            if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            if target.startswith("/"):
                candidate = PurePosixPath(target.lstrip("/"))
            else:
                joined = PurePosixPath(source_path).parent.joinpath(target)
                parts: list[str] = []
                escaped = False
                for part in joined.parts:
                    if part in ("", "."):
                        continue
                    if part == "..":
                        if not parts:
                            escaped = True
                            break
                        parts.pop()
                    else:
                        parts.append(part)
                if escaped:
                    errors.append(f"packaged Markdown link escapes bundle: {source_path} -> {target}")
                    continue
                candidate = PurePosixPath(*parts)
            if candidate.as_posix() not in files:
                errors.append(f"packaged Markdown link target missing: {source_path} -> {target} ({candidate.as_posix()})")
    return errors


def validate_package_outputs(output: Path, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    try:
        package_files = copy_skill_files(root)
        errors.extend(validate_packaged_markdown_links(package_files))
    except (OSError, ValueError) as exc:
        return [f"cannot collect canonical skill/support sources: {exc}"]

    archive_expectations = {
        "peanuts-agent-skill.zip": "peanuts/",
        "peanuts-claude-code-adapter.zip": ".claude/skills/peanuts/",
        "peanuts-codex-adapter.zip": ".agents/skills/peanuts/",
    }
    for archive_name, prefix in archive_expectations.items():
        archive_path = output / archive_name
        if not archive_path.is_file():
            errors.append(f"missing generated archive: {archive_name}")
            continue
        try:
            with zipfile.ZipFile(archive_path) as archive:
                bad_member = archive.testzip()
                if bad_member:
                    errors.append(f"{archive_name}: CRC failure in {bad_member}")
                names = archive.namelist()
                expected_names = {f"{prefix}{rel}" for rel in package_files}
                if set(names) != expected_names:
                    errors.append(f"{archive_name}: package file set differs from canonical source")
                for rel, data in package_files.items():
                    member = f"{prefix}{rel}"
                    try:
                        if archive.read(member) != data:
                            errors.append(f"{archive_name}: source drift in {member}")
                    except KeyError:
                        pass
                for name in names:
                    pure = PurePosixPath(name)
                    if pure.is_absolute() or ".." in pure.parts or "\\" in name:
                        errors.append(f"{archive_name}: unsafe archive path {name}")
        except (OSError, zipfile.BadZipFile) as exc:
            errors.append(f"{archive_name}: {exc}")

    chatgpt_dir = output / "chatgpt-project"
    files_dir = chatgpt_dir / "chatgpt-project-files"
    expected_chatgpt = set(CHATGPT_FILES)
    actual_chatgpt = {p.name for p in files_dir.iterdir()} if files_dir.is_dir() else set()
    if actual_chatgpt != expected_chatgpt:
        errors.append(f"ChatGPT Project adapter must contain exactly five expected plain-text files; found {sorted(actual_chatgpt)}")
    for filename in ("PROJECT_INSTRUCTIONS.md", "SETUP.md"):
        if not (chatgpt_dir / filename).is_file():
            errors.append(f"ChatGPT Project adapter missing {filename}")

    if (chatgpt_dir / "PROJECT_INSTRUCTIONS.md").is_file():
        text = (chatgpt_dir / "PROJECT_INSTRUCTIONS.md").read_text(encoding="utf-8")
        if len(text) > 6000:
            errors.append("ChatGPT Project instructions exceed the internal 6000-character design budget")
        if "not automatic skill activation" not in text.lower():
            errors.append("ChatGPT Project instructions must disclose that this is a manual adapter")
        if "only tools actually present" not in text.lower():
            errors.append("ChatGPT Project instructions must forbid assuming unavailable host tools")

    # The five-file fallback must carry the actual JSON contracts, not only a README
    # that describes them. This keeps structured work possible without extra uploads.
    for filename, schema_names in SCHEMA_GROUPS.items():
        source_file = files_dir / filename
        if not source_file.is_file():
            continue
        content = source_file.read_text(encoding="utf-8")
        for schema_name in schema_names:
            marker = f"## Canonical source: `schemas/{schema_name}`"
            if marker not in content:
                errors.append(f"ChatGPT Project source {filename} is missing schema {schema_name}")

    chatgpt_zip = output / "peanuts-chatgpt-project-files.zip"
    if not chatgpt_zip.is_file():
        errors.append("missing ChatGPT five-file ZIP")
    else:
        try:
            with zipfile.ZipFile(chatgpt_zip) as archive:
                if archive.testzip():
                    errors.append("ChatGPT Project ZIP has a CRC failure")
                if set(archive.namelist()) != expected_chatgpt:
                    errors.append("ChatGPT Project ZIP must contain exactly the five reference files and no setup/instruction extra")
                for filename in expected_chatgpt:
                    if filename in archive.namelist() and (files_dir / filename).read_bytes() != archive.read(filename):
                        errors.append(f"ChatGPT Project ZIP drift: {filename}")
        except (OSError, zipfile.BadZipFile) as exc:
            errors.append(f"ChatGPT Project ZIP: {exc}")

    return errors


def validate_b9(root: Path = ROOT) -> list[str]:
    errors = validate_canonical_skill(root)
    if errors:
        return errors
    try:
        metadata, _ = load_skill_metadata(root / "skills/peanuts")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"cannot load skill metadata: {exc}"]
    if metadata.get("name") != "peanuts":
        errors.append("canonical skill name must be 'peanuts' to match its directory")

    registry_path = root / "capabilities/registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    peanuts = next((item for item in registry.get("capabilities", []) if item.get("id") == "peanuts"), None)
    if not peanuts:
        errors.append("capability registry does not contain Peanuts")
    else:
        expected_hosts = {
            "claude-code": ("ready-for-test", ".claude/skills/peanuts"),
            "codex": ("ready-for-test", ".agents/skills/peanuts"),
            "chatgpt-project": ("manual-fallback", None),
            "chatgpt-skills": ("conditional", None),
        }
        profiles = {p.get("host"): p for p in peanuts.get("host_profiles", [])}
        for host, (status, path) in expected_hosts.items():
            profile = profiles.get(host)
            if not profile:
                errors.append(f"capability registry missing host profile: {host}")
            elif profile.get("status") != status or profile.get("discovery_path") != path:
                errors.append(f"capability registry profile is stale or incorrect: {host}")

    errors.extend(validate_eval_cases(root))

    # Build the packages in a disposable temp directory to verify the actual generator.
    try:
        with tempfile.TemporaryDirectory(prefix="friday-b9-check-") as temp:
            output = Path(temp) / "packages"
            build_all(output, root=root)
            errors.extend(validate_package_outputs(output, root=root))
            # Rebuild in a second directory and compare ZIP hashes for reproducibility.
            output_2 = Path(temp) / "packages-second"
            build_all(output_2, root=root)
            for archive_name in (
                "peanuts-agent-skill.zip",
                "peanuts-claude-code-adapter.zip",
                "peanuts-codex-adapter.zip",
                "peanuts-chatgpt-project-files.zip",
            ):
                first = output / archive_name
                second = output_2 / archive_name
                if first.is_file() and second.is_file() and sha256_bytes(first.read_bytes()) != sha256_bytes(second.read_bytes()):
                    errors.append(f"package build is not deterministic: {archive_name}")
    except (OSError, ValueError, zipfile.BadZipFile, yaml.YAMLError) as exc:
        errors.append(f"package build/validation failed: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, help="validate an existing package output directory; otherwise build to a temporary directory")
    args = parser.parse_args()
    errors = validate_b9()
    if args.out:
        errors.extend(validate_package_outputs(args.out.resolve()))
    if errors:
        print(f"FAIL: {len(errors)} B9 issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: Agent Skills metadata, directory/name alignment, relative references, and Claude-compatible description budget.")
    print("PASS: Claude Code and Codex discovery package paths are correct; host package contents match canonical source byte-for-byte.")
    print("PASS: portable Agent Skills ZIP and ChatGPT Project five-file manual adapter are safe and reproducible.")
    print("PASS: 15 B9 evaluation cases (EVAL-088–102) are structurally valid and rubric-linked.")
    print("NOTE: `ready` evaluation cases and valid packages do not establish runtime discovery, model quality, or host permissions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
