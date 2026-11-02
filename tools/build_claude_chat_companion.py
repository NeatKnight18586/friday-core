#!/usr/bin/env python3
"""Build Claude chat Skill and Project companions from Friday's canonical sources."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_skill_packages import copy_skill_files, load_skill_metadata, write_zip  # noqa: E402

DEFAULT_OUT = ROOT / "build" / "claude-chat"

PROJECT_KNOWLEDGE: dict[str, list[str]] = {
    "01_FRIDAY_VISION_AND_GOVERNANCE.txt": [
        "docs/vision/FRIDAY_VISION.md",
        "docs/governance/PUBLICATION_AND_PRIVACY.md",
        "docs/governance/DEVELOPMENT_INCIDENT_PROTOCOL.md",
    ],
    "02_PEANUTS_OPERATING_MODEL.txt": [
        "docs/product/PEANUTS_CONSTITUTION.md",
        "docs/product/PRODUCT_DISCOVERY.md",
        "docs/architecture/VERTICAL_SLICE_AND_STAGE_CONTRACTS.md",
    ],
    "03_PROFESSIONAL_METHODS_AND_EVIDENCE.txt": [
        "docs/governance/PROFESSIONAL_PRACTICE_ARCHITECTURE.md",
        "docs/methods/METHOD_GOVERNANCE.md",
        "docs/methods/RESEARCH_PROTOCOL.md",
        "docs/methods/HACKATHON_OPPORTUNITY_SPRINT.md",
        "docs/methods/EVIDENCE_SYNTHESIS_PROTOCOL.md",
        "docs/methods/FOUR_COUNCIL_PROTOCOL.md",
        "docs/methods/NUTS_METHOD.md",
    ],
    "04_ARCHITECTURE_AND_DECISIONS.txt": [
        "docs/architecture/ARCHITECTURE.md",
        "docs/architecture/CAPABILITY_SYSTEM_AND_ROUTING.md",
        "docs/architecture/CONTEXT_ENGINEERING.md",
        "docs/architecture/DECISIONS.md",
        "docs/architecture/HOST_ADAPTERS.md",
    ],
    "05_CURRENT_STATUS_AND_HANDOFF.txt": [
        "docs/acceptance/B10_STATUS_AND_HANDOFF.md",
        "docs/acceptance/B10_1_STATUS_AND_HANDOFF.md",
        "docs/acceptance/CLAUDE_CHAT_PROJECT_ACCEPTANCE.md",
        "docs/acceptance/B10_1_C_OWNER_SMOKE_AND_COST_LOG.md",
        "docs/acceptance/B10_RELEASE_CHECKLIST.md",
        "templates/project/STATUS_AND_HANDOFF.md",
        "skills/peanuts/references/planning-handoff.md",
        "skills/peanuts/assets/templates/project-dossier.md",
        "skills/peanuts/assets/templates/handoff.json",
        "schemas/planning-handoff.schema.json",
    ],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compile_project_knowledge(root: Path, filename: str, sources: list[str]) -> bytes:
    blocks = [
        f"# {Path(filename).stem.replace('_', ' ').title()}",
        "",
        "> Generated from Friday's canonical repository sources by `tools/build_claude_chat_companion.py`. "
        "Do not edit this generated file independently; update the canonical sources and regenerate.",
        "",
        "## How to use this document",
        "",
        "This file is persistent Project knowledge, not an executable instruction or proof that any tool ran. "
        "Use only the sections relevant to the current task. The enabled Peanuts Skill contains the detailed repeatable procedures.",
        "",
        "---",
        "",
    ]
    for source in sources:
        path = root / source
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"missing or unsafe Claude Project knowledge source: {source}")
        blocks.extend([
            f"## Canonical source: `{source}`",
            "",
            path.read_text(encoding="utf-8").rstrip(),
            "",
            "---",
            "",
        ])
    return ("\n".join(blocks).rstrip() + "\n").encode("utf-8")


def load_project_instructions(root: Path) -> bytes:
    path = root / "adapters/claude-chat/PROJECT_INSTRUCTIONS.md"
    if not path.is_file():
        raise ValueError("missing adapters/claude-chat/PROJECT_INSTRUCTIONS.md")
    content = path.read_text(encoding="utf-8")
    if len(content) > 6000:
        raise ValueError(f"Claude Project instructions exceed 6000-character maintainability budget: {len(content)}")
    required = [
        "Peanuts Skill", "Project knowledge", "iPad", "P1–P10", "B0–B10",
        "Professional Practice Architecture", "handoff", "tools actually available",
    ]
    missing = [phrase for phrase in required if phrase.lower() not in content.lower()]
    if missing:
        raise ValueError("Claude Project instructions missing required contract phrases: " + ", ".join(missing))
    return content.encode("utf-8")


def build_all(output_dir: Path, root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    metadata, _ = load_skill_metadata(root / "skills/peanuts")
    description = metadata.get("description")
    if metadata.get("name") != "peanuts":
        raise ValueError("Claude Chat skill name must be exactly 'peanuts'")
    if not isinstance(description, str) or not description.strip() or len(description) > 200:
        raise ValueError(f"Claude Chat skill description must be 1–200 characters; found {len(description) if isinstance(description, str) else 'invalid'}")

    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists():
        for child in output_dir.iterdir():
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)

    canonical_files = copy_skill_files(root)
    chat_files: dict[str, bytes] = {}
    for relative, data in canonical_files.items():
        target = "skill.md" if relative == "SKILL.md" else relative
        if target in chat_files:
            raise ValueError(f"Claude Chat skill path collision: {target}")
        chat_files[target] = data
    if "skill.md" not in chat_files or "SKILL.md" in chat_files:
        raise ValueError("Claude Chat bundle must use lowercase skill.md as its single entrypoint")

    skill_zip = output_dir / "peanuts-claude-chat-skill.zip"
    write_zip(skill_zip, {f"peanuts/{path}": data for path, data in chat_files.items()})

    project_files = {
        filename: compile_project_knowledge(root, filename, sources)
        for filename, sources in PROJECT_KNOWLEDGE.items()
    }
    project_zip = output_dir / "friday-peanuts-claude-project-knowledge.zip"
    write_zip(project_zip, project_files)
    instructions = load_project_instructions(root)
    (output_dir / "CLAUDE_PROJECT_INSTRUCTIONS.md").write_bytes(instructions)

    setup_path = root / "adapters/claude-chat/SETUP_IPAD.md"
    smoke_path = root / "adapters/claude-chat/SMOKE_TESTS.md"
    record_path = root / "adapters/claude-chat/RUN_RECORD_TEMPLATE.md"
    for path in (setup_path, smoke_path, record_path):
        if not path.is_file():
            raise ValueError(f"missing Claude Chat support document: {path.relative_to(root)}")
        # Keep links local to the portable delivery, not to hidden repository-only paths.
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            if target.startswith(("../", "/")):
                raise ValueError(f"Claude Chat support document has non-portable link: {path.name}: {target}")

    # Human-readable output directories for convenient iPad Files uploads.
    project_dir = output_dir / "claude-project-knowledge"
    project_dir.mkdir(parents=True)
    for name, data in project_files.items():
        (project_dir / name).write_bytes(data)
    (output_dir / "CLAUDE_PROJECT_INSTRUCTIONS.md").write_bytes(instructions)
    shutil.copy2(setup_path, output_dir / "CLAUDE_CHAT_IPAD_SETUP.md")
    shutil.copy2(smoke_path, output_dir / "CLAUDE_CHAT_SMOKE_TESTS.md")
    shutil.copy2(record_path, output_dir / "CLAUDE_CHAT_RUN_RECORD_TEMPLATE.md")

    source_files: dict[str, dict[str, Any]] = {}
    for name, data in sorted(chat_files.items()):
        source_path = f"skills/peanuts/{'SKILL.md' if name == 'skill.md' else name}"
        source_files[source_path] = {"bytes": len(data), "sha256": sha256(data)}
    for filename, sources in PROJECT_KNOWLEDGE.items():
        for source in sources:
            data = (root / source).read_bytes()
            source_files[source] = {"bytes": len(data), "sha256": sha256(data)}

    manifest = {
        "project": "Friday / Peanuts",
        "milestone": "B10.1 — Claude Chat and Project integration",
        "canonical_skill": "skills/peanuts/SKILL.md",
        "claude_chat_entrypoint": "peanuts/skill.md",
        "description_characters": len(description),
        "project_knowledge_files": list(project_files),
        "source_files": source_files,
        "outputs": {
            skill_zip.name: {"bytes": skill_zip.stat().st_size, "sha256": sha256(skill_zip.read_bytes()), "files": len(chat_files)},
            project_zip.name: {"bytes": project_zip.stat().st_size, "sha256": sha256(project_zip.read_bytes()), "files": len(project_files)},
        },
    }
    manifest_path = output_dir / "BUILD_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    try:
        manifest = build_all(args.out)
    except (OSError, ValueError, zipfile.BadZipFile, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: Claude Chat Skill and Project companion packages built from canonical Friday sources.")
    print(f"- Claude Skill entry: peanuts/skill.md; description={manifest['description_characters']} chars")
    for name, details in manifest["outputs"].items():
        print(f"- {name}: {details['files']} files, {details['bytes']} bytes, SHA-256 {details['sha256']}")
    print("NOTE: package validation is not a live Claude account upload or model-runtime pass.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
