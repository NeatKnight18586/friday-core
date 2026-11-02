#!/usr/bin/env python3
"""Build deterministic host packages from the single canonical Peanuts skill source."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - environment-specific
    print("ERROR: PyYAML is required. Install requirements-dev.txt.", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SKILL = ROOT / "skills" / "peanuts"
DEFAULT_OUTPUT = ROOT / "build" / "skill-packages"

SCHEMA_GROUPS: dict[str, list[str]] = {
    "01_RESEARCH_AND_EVIDENCE.txt": [
        "source-record.schema.json", "claim-record.schema.json", "research-plan.schema.json",
        "research-question.schema.json", "research-round.schema.json",
        "research-finding.schema.json", "opportunity-record.schema.json",
    ],
    "02_NUTS_AND_REVIEW.txt": [
        "analogy-card.schema.json", "nuts-run.schema.json", "council-review.schema.json",
        "assumption-record.schema.json", "assumption-test.schema.json",
    ],
    "03_PRODUCT_AND_ENGINEERING.txt": [
        "project.schema.json", "project-state.schema.json", "requirement-record.schema.json",
        "acceptance-test.schema.json", "build-task.schema.json", "artifact-record.schema.json",
        "demo-plan.schema.json", "vertical-slice-run.schema.json", "planning-handoff.schema.json",
    ],
    "04_GOVERNANCE_AND_RECORDS.txt": [
        "decision-record.schema.json", "capability-registry.schema.json",
        "evaluation-case.schema.json", "evaluation-result.schema.json",
    ],
}

RECORD_TEMPLATE_GROUPS: dict[str, list[str]] = {
    "01_RESEARCH_AND_EVIDENCE.txt": [
        "source.json", "claim.json", "research-question.json", "research-round.json",
        "research-finding.json", "opportunity.json",
    ],
    "02_NUTS_AND_REVIEW.txt": [
        "analogy-card.json", "nuts-run.json", "council-review.json",
        "assumption.json", "assumption-test.json",
    ],
    "03_PRODUCT_AND_ENGINEERING.txt": [
        "requirement.json", "acceptance-test.json", "build-task.json", "artifact.json",
    ],
    "04_GOVERNANCE_AND_RECORDS.txt": ["decision.json"],
}

SUPPORT_DOC_GROUPS: dict[str, list[str]] = {
    "01_RESEARCH_AND_EVIDENCE.txt": [
        "docs/methods/RESEARCH_PROTOCOL.md", "docs/methods/EVENT_INTELLIGENCE_PROTOCOL.md",
        "docs/methods/HACKATHON_OPPORTUNITY_SPRINT.md",
        "docs/methods/USER_RESEARCH_PROTOCOL.md", "docs/methods/EVIDENCE_SYNTHESIS_PROTOCOL.md",
    ],
    "02_NUTS_AND_REVIEW.txt": [
        "docs/methods/NUTS_METHOD.md", "docs/methods/NUTS_SOURCE_DOMAIN_PLAYBOOK.md",
        "docs/methods/FOUR_COUNCIL_PROTOCOL.md", "docs/methods/METHOD_GOVERNANCE.md",
    ],
    "03_PRODUCT_AND_ENGINEERING.txt": [
        "docs/architecture/VERTICAL_SLICE_AND_STAGE_CONTRACTS.md",
        "docs/architecture/PROJECT_RECORDS_AND_STATE.md",
    ],
    "04_GOVERNANCE_AND_RECORDS.txt": [
        "docs/governance/PROFESSIONAL_PRACTICE_ARCHITECTURE.md",
        "docs/governance/QUALITY_ASSURANCE.md", "docs/governance/TOOL_KNOWLEDGE_REGISTRY.md",
        "docs/governance/RESOURCE_BUDGETS.md", "docs/governance/PUBLICATION_AND_PRIVACY.md",
        "docs/governance/DEVELOPMENT_INCIDENT_PROTOCOL.md", "docs/governance/CONTEXT_EVALUATION.md",
        "docs/architecture/CONTEXT_ENGINEERING.md", "docs/architecture/CAPABILITY_SYSTEM_AND_ROUTING.md",
        "docs/architecture/HOST_ADAPTERS.md", "docs/product/PEANUTS_CONSTITUTION.md",
        "docs/product/PRODUCT_DISCOVERY.md",
    ],
}

PROJECT_TEMPLATE_SOURCES = [
    "templates/project/PROJECT_BRIEF.md", "templates/project/PRD.md",
    "templates/project/TECHNICAL_DESIGN.md", "templates/project/BUILD_PLAN.md",
    "templates/project/DEMO_PLAN.md", "templates/project/STATUS_AND_HANDOFF.md",
    "templates/project/research-plan.json", "templates/project/demo-plan.json",
    "templates/project/records/README.md",
]

CHATGPT_FILES: dict[str, list[str]] = {
    "00_PEANUTS_CORE_SKILL.txt": ["skills/peanuts/SKILL.md"],
    "01_RESEARCH_AND_EVIDENCE.txt": [
        "skills/peanuts/references/research-engine.md",
        "skills/peanuts/references/event-intelligence.md",
        "skills/peanuts/references/hackathon-sprint.md",
        "skills/peanuts/references/user-discovery.md",
        "skills/peanuts/references/evidence-synthesis.md",
        "skills/peanuts/references/evidence-boundaries.md",
        *SUPPORT_DOC_GROUPS["01_RESEARCH_AND_EVIDENCE.txt"],
        *(f"schemas/{name}" for name in SCHEMA_GROUPS["01_RESEARCH_AND_EVIDENCE.txt"]),
        *(f"templates/records/{name}" for name in RECORD_TEMPLATE_GROUPS["01_RESEARCH_AND_EVIDENCE.txt"]),
        "schemas/README.md",
    ],
    "02_NUTS_AND_REVIEW.txt": [
        "skills/peanuts/references/nuts-method.md",
        "skills/peanuts/references/nuts-source-domain-playbook.md",
        "skills/peanuts/references/four-council.md",
        "skills/peanuts/references/quick-council.md",
        "skills/peanuts/references/assumption-validation.md",
        *SUPPORT_DOC_GROUPS["02_NUTS_AND_REVIEW.txt"],
        *(f"schemas/{name}" for name in SCHEMA_GROUPS["02_NUTS_AND_REVIEW.txt"]),
        *(f"templates/records/{name}" for name in RECORD_TEMPLATE_GROUPS["02_NUTS_AND_REVIEW.txt"]),
        "schemas/README.md",
    ],
    "03_PRODUCT_AND_ENGINEERING.txt": [
        "skills/peanuts/references/vertical-slice-workflow.md",
        "skills/peanuts/references/prd-and-requirements.md",
        "skills/peanuts/references/technical-design.md",
        "skills/peanuts/references/delivery-handoff.md",
        "skills/peanuts/references/planning-handoff.md",
        "skills/peanuts/assets/templates/project-dossier.md",
        "skills/peanuts/assets/templates/handoff.json",
        "skills/peanuts/assets/templates/problem-brief.md",
        "skills/peanuts/assets/templates/hackathon-shortlist.md",
        "skills/peanuts/assets/templates/concept-brief.md",
        "skills/peanuts/assets/templates/event-dossier.md",
        "skills/peanuts/assets/templates/interview-guide.md",
        "skills/peanuts/assets/templates/opportunity-map.md",
        "skills/peanuts/assets/templates/research-plan.md",
        "skills/peanuts/assets/templates/research-coverage-matrix.md",
        "skills/peanuts/assets/templates/research-synthesis.md",
        "skills/peanuts/assets/templates/user-research-plan.md",
        "skills/peanuts/assets/templates/analogy-card.md",
        "skills/peanuts/assets/templates/nuts-run.md",
        "skills/peanuts/assets/templates/quick-council-review.md",
        "skills/peanuts/assets/templates/draft-prd.md",
        "skills/peanuts/assets/templates/status-handoff.md",
        *SUPPORT_DOC_GROUPS["03_PRODUCT_AND_ENGINEERING.txt"],
        *(f"schemas/{name}" for name in SCHEMA_GROUPS["03_PRODUCT_AND_ENGINEERING.txt"]),
        *(f"templates/records/{name}" for name in RECORD_TEMPLATE_GROUPS["03_PRODUCT_AND_ENGINEERING.txt"]),
        *PROJECT_TEMPLATE_SOURCES,
        "schemas/README.md",
    ],
    "04_GOVERNANCE_AND_RECORDS.txt": [
        "docs/governance/PROFESSIONAL_PRACTICE_ARCHITECTURE.md",
        "docs/methods/METHOD_GOVERNANCE.md",
        "docs/governance/QUALITY_ASSURANCE.md",
        "docs/governance/TOOL_KNOWLEDGE_REGISTRY.md",
        "docs/architecture/CONTEXT_ENGINEERING.md",
        "docs/architecture/PROJECT_RECORDS_AND_STATE.md",
        "docs/governance/RESOURCE_BUDGETS.md",
        "docs/architecture/CAPABILITY_SYSTEM_AND_ROUTING.md",
        "docs/governance/PUBLICATION_AND_PRIVACY.md",
        "docs/governance/DEVELOPMENT_INCIDENT_PROTOCOL.md",
        "docs/governance/CONTEXT_EVALUATION.md",
        *SUPPORT_DOC_GROUPS["04_GOVERNANCE_AND_RECORDS.txt"],
        *(f"schemas/{name}" for name in SCHEMA_GROUPS["04_GOVERNANCE_AND_RECORDS.txt"]),
        *(f"templates/records/{name}" for name in RECORD_TEMPLATE_GROUPS["04_GOVERNANCE_AND_RECORDS.txt"]),
        "schemas/README.md", "templates/project/records/README.md",
    ],
}

# Supporting repository files are copied into generated standalone skill packages at the
# same relative paths referenced by SKILL.md and its method references. The repository
# remains the only authoring source; these are generated copies, never hand-maintained.
SUPPORT_STATIC_PATHS = [
    *[f"docs/methods/{name}" for name in (
        "RESEARCH_PROTOCOL.md", "EVENT_INTELLIGENCE_PROTOCOL.md", "HACKATHON_OPPORTUNITY_SPRINT.md", "USER_RESEARCH_PROTOCOL.md",
        "EVIDENCE_SYNTHESIS_PROTOCOL.md", "NUTS_METHOD.md", "NUTS_SOURCE_DOMAIN_PLAYBOOK.md",
        "FOUR_COUNCIL_PROTOCOL.md", "METHOD_GOVERNANCE.md",
    )],
    *[f"docs/governance/{name}" for name in (
        "PROFESSIONAL_PRACTICE_ARCHITECTURE.md", "QUALITY_ASSURANCE.md", "TOOL_KNOWLEDGE_REGISTRY.md",
        "RESOURCE_BUDGETS.md", "PUBLICATION_AND_PRIVACY.md", "DEVELOPMENT_INCIDENT_PROTOCOL.md",
        "CONTEXT_EVALUATION.md",
    )],
    *[f"docs/architecture/{name}" for name in (
        "CONTEXT_ENGINEERING.md", "PROJECT_RECORDS_AND_STATE.md", "CAPABILITY_SYSTEM_AND_ROUTING.md",
        "HOST_ADAPTERS.md", "VERTICAL_SLICE_AND_STAGE_CONTRACTS.md",
    )],
    "docs/product/PEANUTS_CONSTITUTION.md", "docs/product/PRODUCT_DISCOVERY.md",
    "schemas/README.md", "templates/project/records/README.md",
    *PROJECT_TEMPLATE_SOURCES,
]


def package_support_source_paths(root: Path) -> list[str]:
    """Return all canonical schemas and record templates plus the explicit support allowlist."""
    dynamic = [
        path.relative_to(root).as_posix()
        for folder in (root / "schemas", root / "templates/records")
        for path in sorted(folder.glob("*.json"))
    ]
    return sorted(set(SUPPORT_STATIC_PATHS + dynamic))


REFERENCE_TO_CHATGPT_FILE = {
    "references/research-engine.md": "01_RESEARCH_AND_EVIDENCE.txt",
    "references/event-intelligence.md": "01_RESEARCH_AND_EVIDENCE.txt",
    "references/hackathon-sprint.md": "01_RESEARCH_AND_EVIDENCE.txt",
    "references/user-discovery.md": "01_RESEARCH_AND_EVIDENCE.txt",
    "references/evidence-synthesis.md": "01_RESEARCH_AND_EVIDENCE.txt",
    "references/evidence-boundaries.md": "01_RESEARCH_AND_EVIDENCE.txt",
    "references/nuts-method.md": "02_NUTS_AND_REVIEW.txt",
    "references/nuts-source-domain-playbook.md": "02_NUTS_AND_REVIEW.txt",
    "references/four-council.md": "02_NUTS_AND_REVIEW.txt",
    "references/quick-council.md": "02_NUTS_AND_REVIEW.txt",
    "references/assumption-validation.md": "02_NUTS_AND_REVIEW.txt",
    "references/vertical-slice-workflow.md": "03_PRODUCT_AND_ENGINEERING.txt",
    "references/prd-and-requirements.md": "03_PRODUCT_AND_ENGINEERING.txt",
    "references/technical-design.md": "03_PRODUCT_AND_ENGINEERING.txt",
    "references/delivery-handoff.md": "03_PRODUCT_AND_ENGINEERING.txt",
    "references/planning-handoff.md": "03_PRODUCT_AND_ENGINEERING.txt",
    "references/context-efficiency.md": "04_GOVERNANCE_AND_RECORDS.txt",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_skill_metadata(skill_dir: Path = CANONICAL_SKILL) -> tuple[dict[str, Any], str]:
    skill_path = skill_dir / "SKILL.md"
    content = skill_path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must begin with YAML frontmatter.")
    metadata = yaml.safe_load(match.group(1))
    if not isinstance(metadata, dict):
        raise ValueError("SKILL.md frontmatter must be a YAML mapping.")
    return metadata, content


def validate_canonical_skill(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    skill_dir = root / "skills" / "peanuts"
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return ["canonical skills/peanuts/SKILL.md is missing"]
    try:
        metadata, content = load_skill_metadata(skill_dir)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"invalid canonical SKILL.md: {exc}"]

    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("Agent Skills name must be lowercase hyphen-case without consecutive hyphens")
    elif len(name) > 64:
        errors.append("Agent Skills name exceeds 64 characters")
    elif name != skill_dir.name:
        errors.append(f"Agent Skills name '{name}' must match parent folder '{skill_dir.name}'")
    if not isinstance(description, str) or not description.strip():
        errors.append("Agent Skills description is required")
    else:
        if len(description) > 1024:
            errors.append("Agent Skills description exceeds 1024 characters")
        if "<" in description or ">" in description:
            errors.append("Skill description must not contain XML tags")

    # Check local Markdown links in the skill's own body. External URLs and anchors are allowed.
    body = re.sub(r"\A---\s*\n.*?\n---\s*", "", content, count=1, flags=re.DOTALL)
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
        target = target.split("#", 1)[0].strip()
        if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        candidate = (skill_dir / target).resolve()
        try:
            candidate.relative_to(skill_dir.resolve())
        except ValueError:
            errors.append(f"skill link escapes canonical package: {target}")
            continue
        if not candidate.is_file():
            errors.append(f"skill link target missing: {target}")

    # Ensure referenced resource trees are present and do not contain symlinks.
    for relative_dir in ("references", "assets/templates"):
        directory = skill_dir / relative_dir
        if not directory.is_dir() or not any(p.is_file() for p in directory.rglob("*")):
            errors.append(f"canonical package resource directory is missing or empty: {relative_dir}")
    for path in skill_dir.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlinks are not permitted in the canonical skill package: {path.relative_to(skill_dir)}")
        elif path.is_file():
            rel = path.relative_to(skill_dir).as_posix()
            if rel.startswith((".git/", "__pycache__/")) or path.suffix.lower() in {".pyc", ".pyo", ".log", ".tmp"}:
                errors.append(f"generated or unsafe file in skill package: {rel}")
    return errors


def compile_markdown(root: Path, title: str, source_paths: list[str]) -> str:
    blocks = [
        f"# {title}",
        "",
        "> Generated from Friday's canonical sources by `tools/build_skill_packages.py`. "
        "Do not edit this generated copy; change the canonical source and regenerate.",
        "",
        "---",
        "",
    ]
    for source in dict.fromkeys(source_paths):
        path = root / source
        text = path.read_text(encoding="utf-8").rstrip()
        blocks.extend([f"## Canonical source: `{source}`", ""])
        if path.suffix.lower() == ".json":
            blocks.extend(["```json", text, "```", ""])
        else:
            blocks.extend([text, ""])
        blocks.extend(["---", ""])
    return "\n".join(blocks).rstrip() + "\n"


def create_chatgpt_core(root: Path) -> str:
    canonical = (root / "skills/peanuts/SKILL.md").read_text(encoding="utf-8").rstrip()
    nav = [
        "## ChatGPT Project reference-file map",
        "",
        "This Project adapter groups the canonical modular references into five source files to respect the current Free Project file-count limit. Retrieve only the relevant file/section; do not treat all of them as mandatory context for every task.",
        "",
        "| Canonical reference | Generated Project file |",
        "|---|---|",
    ]
    for source, destination in REFERENCE_TO_CHATGPT_FILE.items():
        nav.append(f"| `skills/peanuts/{source}` | `{destination}` |")
    nav.extend([
        "| Research/evidence JSON Schemas and record starters | `01_RESEARCH_AND_EVIDENCE.txt` |",
        "| NUTS, Four-Council and assumption-test JSON Schemas and record starters | `02_NUTS_AND_REVIEW.txt` |",
        "| Project, PRD, acceptance-test, task, artifact and demo schemas/templates | `03_PRODUCT_AND_ENGINEERING.txt` |",
        "| Decision, capability and evaluation schemas plus governance methods | `04_GOVERNANCE_AND_RECORDS.txt` |",
        "| PPA, method governance, tool selection, QA, project records, security/privacy and resource/context standards | `04_GOVERNANCE_AND_RECORDS.txt` |",
        "| Reusable Peanuts assets and B8 project document templates | `03_PRODUCT_AND_ENGINEERING.txt` |",
        "",
        "In ChatGPT Projects, relative repository paths are descriptive source identifiers; use the mapped Project filename and canonical-source heading instead of pretending those paths are locally mounted.",
        "Schema text is available as reference material, but a Project chat does not execute JSON Schema or Friday's validators unless an actual tool runs them.",
    ])
    return canonical + "\n\n" + "\n".join(nav) + "\n"


def write_zip(zip_path: Path, files: dict[str, bytes]) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(files):
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts or "\\" in name:
                raise ValueError(f"unsafe package path: {name}")
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.create_system = 3
            archive.writestr(info, files[name])


def copy_skill_files(root: Path) -> dict[str, bytes]:
    """Collect canonical skill files plus generated copies of referenced repo resources.

    Paths outside skills/peanuts are injected from their single repository source so a
    standalone skill ZIP remains operationally self-contained without hand-maintained copies.
    """
    files: dict[str, bytes] = {}
    skill_root = root / "skills" / "peanuts"
    for path in sorted(skill_root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"refusing to package symlink: {path}")
        if not path.is_file():
            continue
        relative = path.relative_to(skill_root).as_posix()
        files[relative] = path.read_bytes()
    if "SKILL.md" not in files:
        raise ValueError("canonical package must contain SKILL.md")

    for relative in package_support_source_paths(root):
        source = root / relative
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"required standalone support source is missing or unsafe: {relative}")
        files[relative] = source.read_bytes()
    return files


def build_all(output_dir: Path, root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    errors = validate_canonical_skill(root)
    if errors:
        raise ValueError("canonical skill validation failed:\n- " + "\n- ".join(errors))

    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    skill_files = copy_skill_files(root)
    built: dict[str, Any] = {"source": {}, "outputs": {}}

    support_paths = set(package_support_source_paths(root))
    for name, data in sorted(skill_files.items()):
        source_path = name if name in support_paths else f"skills/peanuts/{name}"
        built["source"][source_path] = {"bytes": len(data), "sha256": sha256_bytes(data)}

    # Portable Agent Skills archive: directory name and metadata name both equal "peanuts".
    portable_files = {f"peanuts/{name}": data for name, data in skill_files.items()}
    portable_zip = output_dir / "peanuts-agent-skill.zip"
    write_zip(portable_zip, portable_files)
    built["outputs"][portable_zip.name] = {
        "bytes": portable_zip.stat().st_size,
        "sha256": sha256_bytes(portable_zip.read_bytes()),
        "files": len(portable_files),
    }

    # Host packages preserve host discovery paths but use identical canonical contents.
    for prefix, archive_name in (
        (".claude/skills/peanuts", "peanuts-claude-code-adapter.zip"),
        (".agents/skills/peanuts", "peanuts-codex-adapter.zip"),
    ):
        host_files = {f"{prefix}/{name}": data for name, data in skill_files.items()}
        host_zip = output_dir / archive_name
        write_zip(host_zip, host_files)
        built["outputs"][archive_name] = {
            "bytes": host_zip.stat().st_size,
            "sha256": sha256_bytes(host_zip.read_bytes()),
            "files": len(host_files),
            "discovery_path": prefix,
        }

    # ChatGPT Project pack: exactly five plain-text .txt files with Markdown-formatted content; instructions/setup are separate.
    chatgpt_dir = output_dir / "chatgpt-project"
    files_dir = chatgpt_dir / "chatgpt-project-files"
    files_dir.mkdir(parents=True, exist_ok=True)
    # Remove stale outputs from older package formats before regenerating the exact five-file set.
    for pattern in ("*.md", "*.txt"):
        for stale in files_dir.glob(pattern):
            stale.unlink()
    generated: dict[str, bytes] = {}
    for filename, sources in CHATGPT_FILES.items():
        if filename == "00_PEANUTS_CORE_SKILL.txt":
            content = create_chatgpt_core(root)
        else:
            content = compile_markdown(root, filename.removesuffix(".txt").replace("_", " ").title(), sources)
        data = content.encode("utf-8")
        generated[filename] = data
        (files_dir / filename).write_bytes(data)

    instructions = (root / "adapters/chatgpt/PROJECT_INSTRUCTIONS.md").read_bytes()
    setup = (root / "adapters/chatgpt/SETUP.md").read_bytes()
    (chatgpt_dir / "PROJECT_INSTRUCTIONS.md").write_bytes(instructions)
    (chatgpt_dir / "SETUP.md").write_bytes(setup)

    chatgpt_zip = output_dir / "peanuts-chatgpt-project-files.zip"
    write_zip(chatgpt_zip, generated)
    built["outputs"][chatgpt_zip.name] = {
        "bytes": chatgpt_zip.stat().st_size,
        "sha256": sha256_bytes(chatgpt_zip.read_bytes()),
        "files": len(generated),
        "note": "contains exactly five plain-text files with Markdown-formatted content for Project sources; paste PROJECT_INSTRUCTIONS.md separately",
    }

    readme = """# Generated Peanuts host packages\n\nAll packages are generated from the canonical `skills/peanuts/` instruction/reference source plus explicit repository support sources in `docs/`, `schemas/`, and `templates/`. Generated support copies are byte-identical snapshots; do not edit them independently.\n\n- `peanuts-agent-skill.zip`: portable Agent Skills directory (`peanuts/SKILL.md`) plus required schemas, record starters, project templates, and governing references.\n- `peanuts-claude-code-adapter.zip`: install at repository root; contains `.claude/skills/peanuts/` and the same bundled support resources.\n- `peanuts-codex-adapter.zip`: install at repository root; contains `.agents/skills/peanuts/` and the same bundled support resources.\n- `peanuts-chatgpt-project-files.zip`: contains exactly five plain-text references with Markdown formatting, including the full relevant JSON Schemas and record starters; extract and upload each file to a ChatGPT Project. Paste `chatgpt-project/PROJECT_INSTRUCTIONS.md` into Project settings. Follow `chatgpt-project/SETUP.md`.\n\nThe ChatGPT Project adapter is manual reference material; it does not execute schemas or repository scripts. These outputs prove package structure and deterministic integrity only. They do not prove that any target host discovers or correctly executes the skill.\n"""
    (output_dir / "README.md").write_text(readme, encoding="utf-8")

    manifest_path = output_dir / "BUILD_MANIFEST.json"
    manifest = {
        "project": "Friday / Peanuts",
        "milestone": "B9 — Skill packaging and host adapters",
        "generated_from": "skills/peanuts/ plus the explicit canonical docs/schemas/templates support allowlist",
        "schema_version": "1.0.0",
        "source_files": built["source"],
        "outputs": built["outputs"],
        "generated_files": {
            str(path.relative_to(output_dir).as_posix()): {
                "bytes": path.stat().st_size,
                "sha256": sha256_bytes(path.read_bytes()),
            }
            for path in sorted(output_dir.rglob("*"))
            if path.is_file() and path != manifest_path
        },
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT, help="generated output directory (default: build/skill-packages)")
    args = parser.parse_args()
    try:
        manifest = build_all(args.out)
    except (OSError, ValueError, yaml.YAMLError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("PASS: built portable Agent Skills, Claude Code, Codex, and five-file ChatGPT Project packages.")
    print(f"PASS: {len(manifest['source_files'])} canonical skill and generated support resources copied from repository sources.")
    for filename, details in manifest["outputs"].items():
        print(f"- {filename}: {details['files']} files, {details['bytes']} bytes, SHA-256 {details['sha256']}")
    print("NOTE: package validation does not establish runtime discovery or model behavior.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
