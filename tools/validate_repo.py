#!/usr/bin/env python3
"""Validate Friday files, links, CI/container configuration, privacy patterns and manifest."""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

import yaml

try:
    from .package_manifest import collect_file_entries, manifest_differences
except ImportError:  # Support direct execution as `python tools/validate_repo.py`.
    from package_manifest import collect_file_entries, manifest_differences

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md", "CHANGELOG.md",
    ".gitignore", ".gitattributes", ".editorconfig", ".python-version", "pyproject.toml",
    "requirements-dev.txt", "PACKAGE_MANIFEST.json",
    ".devcontainer/devcontainer.json", ".github/workflows/ci.yml", ".github/dependabot.yml",
    "docs/product/PEANUTS_CONSTITUTION.md", "docs/product/PRODUCT_DISCOVERY.md",
    "docs/methods/NUTS_METHOD.md", "docs/methods/NUTS_SOURCE_DOMAIN_PLAYBOOK.md", "docs/methods/FOUR_COUNCIL_PROTOCOL.md",
    "docs/governance/PROFESSIONAL_PRACTICE_ARCHITECTURE.md",
    "docs/governance/TOOL_KNOWLEDGE_REGISTRY.md", "docs/governance/QUALITY_ASSURANCE.md",
    "docs/reviews/STAGE_1_REVIEW.md", "docs/reviews/B2_REVIEW.md",
    "docs/architecture/PROJECT_RECORDS_AND_STATE.md", "docs/architecture/REPRODUCIBLE_DEVELOPMENT.md",
    "docs/reviews/B3_REVIEW.md",
    "docs/methods/RESEARCH_PROTOCOL.md", "docs/methods/EVENT_INTELLIGENCE_PROTOCOL.md",
    "docs/methods/USER_RESEARCH_PROTOCOL.md", "docs/methods/EVIDENCE_SYNTHESIS_PROTOCOL.md",
    "schemas/project.schema.json", "schemas/project-state.schema.json",
    "schemas/source-record.schema.json", "schemas/claim-record.schema.json",
    "schemas/assumption-record.schema.json", "schemas/decision-record.schema.json",
    "schemas/evaluation-case.schema.json", "schemas/evaluation-result.schema.json",
    "schemas/research-plan.schema.json", "schemas/research-question.schema.json",
    "schemas/research-finding.schema.json", "schemas/research-round.schema.json",
    "schemas/opportunity-record.schema.json", "schemas/analogy-card.schema.json", "schemas/nuts-run.schema.json",
    "evals/README.md", "evals/cases/EVAL-001.json", "evals/cases/EVAL-012.json",
    "evals/cases/EVAL-015.json", "evals/cases/EVAL-018.json",
    "templates/project/PROJECT_BRIEF.md", "templates/project/state.json",
    "templates/project/records/sources.jsonl", "templates/project/records/claims.jsonl",
    "templates/project/records/assumptions.jsonl", "templates/project/records/decisions.jsonl",
    "templates/project/evaluations/results.jsonl", "templates/project/research-plan.json",
    "templates/project/records/research-questions.jsonl", "templates/project/records/research-findings.jsonl",
    "templates/project/records/research-rounds.jsonl", "templates/project/records/opportunities.jsonl",
    "templates/records/research-question.json", "templates/records/research-finding.json",
    "templates/records/research-round.json", "templates/records/opportunity.json",
    "tools/init_project.py", "tools/validate_project.py", "tools/validate_b2.py", "tools/validate_b5.py", "tools/package_manifest.py",
    "tools/update_manifest.py", "tools/verify.py", "tools/validate_b6.py", "tools/validate_capabilities.py", "tools/inspect_context.py", "tests/test_init_project.py",
    "tests/test_validation.py", "tests/test_configuration.py", "tests/test_manifest.py", "tests/test_b5_research.py",
    "evals/rubrics/USER_RESEARCH_ETHICS.md", "evals/rubrics/RESEARCH_PLAN_QUALITY.md",
    "evals/rubrics/EVENT_INTELLIGENCE_QUALITY.md", "evals/rubrics/USER_RESEARCH_QUALITY.md",
    "evals/cases/EVAL-020.json", "evals/cases/EVAL-030.json",
    "skills/peanuts/SKILL.md", "skills/peanuts/references/vertical-slice-workflow.md",
    "skills/peanuts/references/evidence-boundaries.md", "skills/peanuts/references/quick-council.md",
    "schemas/vertical-slice-run.schema.json", "tools/validate_vertical_slice.py",
    "examples/vertical-slice-synthetic/campus-service-status/vertical-slice-run.json",
    "tests/test_vertical_slice.py", "evals/cases/EVAL-019.json",
    "docs/architecture/VERTICAL_SLICE_AND_STAGE_CONTRACTS.md", "docs/reviews/B4_REVIEW.md",
    "skills/peanuts/references/research-engine.md", "skills/peanuts/references/event-intelligence.md",
    "skills/peanuts/references/user-discovery.md", "skills/peanuts/references/evidence-synthesis.md",
    "skills/peanuts/assets/templates/research-plan.md", "skills/peanuts/assets/templates/research-coverage-matrix.md",
    "skills/peanuts/assets/templates/user-research-plan.md", "skills/peanuts/assets/templates/interview-guide.md",
    "skills/peanuts/assets/templates/research-synthesis.md", "skills/peanuts/assets/templates/opportunity-map.md",
    "docs/reviews/B5_REVIEW.md", "tests/test_b6_nuts.py",
    "templates/records/analogy-card.json", "templates/records/nuts-run.json",
    "templates/project/records/analogies.jsonl", "templates/project/records/nuts-runs.jsonl",
    "evals/cases/EVAL-031.json", "evals/cases/EVAL-038.json", "evals/rubrics/NUTS_ANALOGY_QUALITY.md",
    "skills/peanuts/references/nuts-method.md", "skills/peanuts/references/nuts-source-domain-playbook.md", "skills/peanuts/assets/templates/nuts-run.md",
    "docs/reviews/B6_REVIEW.md", "docs/reviews/B6_5_REVIEW.md",
    "docs/governance/DEVELOPMENT_INCIDENT_PROTOCOL.md",
    "capabilities/README.md", "capabilities/registry.json", "schemas/capability-registry.schema.json",
    "docs/architecture/CONTEXT_ENGINEERING.md", "docs/architecture/CAPABILITY_SYSTEM_AND_ROUTING.md",
    "docs/governance/RESOURCE_BUDGETS.md", "docs/governance/CONTEXT_EVALUATION.md",
    "templates/session/SESSION_HANDOFF.md", "evals/rubrics/CONTEXT_AND_RESOURCE_EFFICIENCY.md",
    "evals/cases/EVAL-039.json", "evals/cases/EVAL-046.json", "evals/cases/EVAL-050.json", "tests/test_context_architecture.py",
    "schemas/requirement-record.schema.json", "schemas/acceptance-test.schema.json",
    "schemas/build-task.schema.json", "schemas/artifact-record.schema.json", "schemas/demo-plan.schema.json",
    "templates/records/requirement.json", "templates/records/acceptance-test.json",
    "templates/records/build-task.json", "templates/records/artifact.json",
    "templates/project/PRD.md", "templates/project/TECHNICAL_DESIGN.md",
    "templates/project/BUILD_PLAN.md", "templates/project/DEMO_PLAN.md",
    "templates/project/demo-plan.json", "templates/project/records/requirements.jsonl",
    "templates/project/records/acceptance-tests.jsonl", "templates/project/records/build-tasks.jsonl",
    "templates/project/records/artifacts.jsonl", "tools/b8_rules.py", "tools/validate_b8.py",
    "tests/test_b8_delivery.py", "docs/reviews/B8_REVIEW.md",
    "skills/peanuts/references/prd-and-requirements.md",
    "skills/peanuts/references/technical-design.md",
    "skills/peanuts/references/delivery-handoff.md",
    "evals/rubrics/PRD_AND_REQUIREMENTS_QUALITY.md",
    "evals/rubrics/TECHNICAL_DESIGN_QUALITY.md",
    "evals/rubrics/DELIVERY_HANDOFF_QUALITY.md",
    "evals/cases/EVAL-062.json", "evals/cases/EVAL-086.json", "evals/cases/EVAL-087.json",
    "docs/architecture/HOST_ADAPTERS.md", "docs/plans/CHATGPT_PROJECT_ADAPTER.md",
    "docs/reviews/B9_REVIEW.md", "adapters/chatgpt/PROJECT_INSTRUCTIONS.md",
    "adapters/chatgpt/SETUP.md", "tools/build_skill_packages.py", "tools/validate_b9.py",
    "tests/test_b9_packaging.py", "evals/rubrics/SKILL_PACKAGING_AND_HOST_COMPATIBILITY.md",
    "evals/cases/EVAL-088.json", "evals/cases/EVAL-102.json",
]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
SECRET_PATTERNS = [
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
]
SHA_REF_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{40}$")


def validate_links(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in {".git", "__pycache__", ".venv", "local-workspace"} for part in path.parts):
            continue
        content = path.read_text(encoding="utf-8")
        if content.count("```") % 2:
            errors.append(f"unbalanced triple-backtick fence: {path.relative_to(ROOT)}")
        for raw in LINK_RE.findall(content):
            first = raw.strip().split()[0].strip("<>") if raw.strip() else ""
            if not first or first.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target_path, _, _fragment = first.partition("#")
            if not target_path:
                continue
            resolved = (path.parent / target_path.split("?", 1)[0]).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"link escapes repository: {path.relative_to(ROOT)} -> {first}")
                continue
            if not resolved.exists():
                errors.append(f"broken relative link: {path.relative_to(ROOT)} -> {first}")



def validate_skill_contract(errors: list[str]) -> None:
    skill_path = ROOT / "skills/peanuts/SKILL.md"
    try:
        content = skill_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"Peanuts SKILL.md: cannot read: {exc}")
        return
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        errors.append("Peanuts SKILL.md: YAML frontmatter is missing or malformed")
        return
    fields = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("\"'")
    name = fields.get("name", "")
    description = fields.get("description", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("Peanuts SKILL.md: name must be lowercase hyphen-case")
    elif name != skill_path.parent.name:
        errors.append("Peanuts SKILL.md: name must match the canonical skill directory")
    if not description:
        errors.append("Peanuts SKILL.md: description is required")
    if len(description) > 1024:
        errors.append("Peanuts SKILL.md: description exceeds the 1,024-character Agent Skills/Claude metadata limit")
    for relative in [
        "references/vertical-slice-workflow.md",
        "references/evidence-boundaries.md",
        "references/quick-council.md",
        "references/research-engine.md",
        "references/event-intelligence.md",
        "references/user-discovery.md",
        "references/evidence-synthesis.md",
        "references/nuts-method.md",
        "references/nuts-source-domain-playbook.md",
        "references/context-efficiency.md",
        "references/prd-and-requirements.md",
        "references/technical-design.md",
        "references/delivery-handoff.md",
        "assets/templates/research-plan.md",
        "assets/templates/research-coverage-matrix.md",
        "assets/templates/user-research-plan.md",
        "assets/templates/interview-guide.md",
        "assets/templates/research-synthesis.md",
        "assets/templates/opportunity-map.md",
        "assets/templates/event-dossier.md",
        "assets/templates/problem-brief.md",
        "assets/templates/analogy-card.md",
        "assets/templates/nuts-run.md",
        "assets/templates/concept-brief.md",
        "assets/templates/quick-council-review.md",
        "assets/templates/draft-prd.md",
        "assets/templates/status-handoff.md",
    ]:
        if not (skill_path.parent / relative).is_file():
            errors.append(f"Peanuts SKILL.md: referenced skill resource missing: {relative}")


def validate_configuration(errors: list[str]) -> None:
    try:
        with (ROOT / "pyproject.toml").open("rb") as stream:
            config = tomllib.load(stream)
        if config.get("tool", {}).get("pytest", {}).get("ini_options", {}).get("testpaths") != ["tests"]:
            errors.append("pyproject.toml: pytest testpaths must be ['tests']")
        if config.get("tool", {}).get("ruff", {}).get("target-version") != "py311":
            errors.append("pyproject.toml: Ruff target-version must be py311")
    except (OSError, tomllib.TOMLDecodeError) as exc:
        errors.append(f"pyproject.toml: invalid configuration: {exc}")

    try:
        devcontainer = json.loads((ROOT / ".devcontainer/devcontainer.json").read_text(encoding="utf-8"))
        image = devcontainer.get("image")
        if not isinstance(image, str) or not image.startswith(
            "mcr.microsoft.com/devcontainers/python:dev-3.13-bookworm@sha256:"
        ):
            errors.append("devcontainer.json: expected the reviewed Python 3.13 Bookworm Dev Container image")
        elif not re.search(r"@sha256:[0-9a-f]{64}$", image):
            errors.append("devcontainer.json: development image must be pinned by SHA-256 digest")
        if "requirements-dev.txt" not in devcontainer.get("postCreateCommand", ""):
            errors.append("devcontainer.json: postCreateCommand must install requirements-dev.txt")
        if devcontainer.get("remoteUser") == "root":
            errors.append("devcontainer.json: do not default the development container to root")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"devcontainer.json: invalid JSON: {exc}")

    workflow_path = ROOT / ".github/workflows/ci.yml"
    try:
        workflow_text = workflow_path.read_text(encoding="utf-8")
        workflow = yaml.load(workflow_text, Loader=yaml.BaseLoader)
        if not isinstance(workflow, dict) or "on" not in workflow or "jobs" not in workflow:
            errors.append("ci.yml: workflow must define 'on' and 'jobs'")
        permissions = workflow.get("permissions", {}) if isinstance(workflow, dict) else {}
        if permissions != {"contents": "read"}:
            errors.append("ci.yml: permissions must be least-privilege contents: read")
        if "pull_request" not in workflow.get("on", {}):
            errors.append("ci.yml: pull_request trigger is required")
        if "workflow_dispatch" not in workflow.get("on", {}):
            errors.append("ci.yml: workflow_dispatch trigger is required")
        uses_refs = re.findall(r"(?m)^\s*uses:\s*([^\s#]+)", workflow_text)
        if not uses_refs:
            errors.append("ci.yml: no GitHub Actions dependencies found")
        for ref in uses_refs:
            if not SHA_REF_RE.fullmatch(ref):
                errors.append(f"ci.yml: action must be pinned to a full 40-character SHA: {ref}")
        jobs = workflow.get("jobs", {}) if isinstance(workflow, dict) else {}
        validate_job = jobs.get("validate", {}) if isinstance(jobs, dict) else {}
        matrix = validate_job.get("strategy", {}).get("matrix", {}) if isinstance(validate_job, dict) else {}
        expected_os = {"ubuntu-latest", "windows-latest", "macos-latest"}
        expected_python = {"3.11", "3.12", "3.13", "3.14"}
        if not expected_os.issubset(set(matrix.get("os", []))):
            errors.append("ci.yml: matrix must cover Ubuntu, Windows, and macOS")
        if not expected_python.issubset(set(matrix.get("python-version", []))):
            errors.append("ci.yml: matrix must cover Python 3.11 through 3.14")
        steps = validate_job.get("steps", []) if isinstance(validate_job, dict) else []
        checkout_steps = [step for step in steps if str(step.get("uses", "")).startswith("actions/checkout@")]
        if not checkout_steps or checkout_steps[0].get("with", {}).get("persist-credentials") != "false":
            errors.append("ci.yml: checkout must set persist-credentials: false")
        if not any(step.get("run") == "python tools/verify.py" for step in steps):
            errors.append("ci.yml: complete verification command is not invoked")
        if "secrets." in workflow_text:
            errors.append("ci.yml: B3 validation workflow must not require repository secrets")
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"ci.yml: invalid YAML: {exc}")

    try:
        dependabot = yaml.load((ROOT / ".github/dependabot.yml").read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        ecosystems = {item.get("package-ecosystem") for item in dependabot.get("updates", [])}
        if not {"pip", "github-actions"}.issubset(ecosystems):
            errors.append("dependabot.yml: pip and github-actions updates must be configured")
    except (OSError, yaml.YAMLError, AttributeError) as exc:
        errors.append(f"dependabot.yml: invalid YAML or structure: {exc}")

    requirements_path = ROOT / "requirements-dev.txt"
    try:
        lines = [line.strip() for line in requirements_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
        invalid = [line for line in lines if not re.fullmatch(r"[A-Za-z0-9_.-]+==[^=\s]+", line)]
        if invalid:
            errors.append(f"requirements-dev.txt: entries must be exact direct pins: {invalid}")
        required_packages = {"jsonschema", "pytest", "PyYAML", "ruff"}
        package_names = {line.split("==", 1)[0].lower().replace("_", "-") for line in lines if "==" in line}
        missing_packages = {name.lower() for name in required_packages} - package_names
        if missing_packages:
            errors.append(f"requirements-dev.txt: required development packages missing: {sorted(missing_packages)}")
    except OSError as exc:
        errors.append(f"requirements-dev.txt: cannot read: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-secret-scan", action="store_true", help="skip heuristic token-pattern scan")
    args = parser.parse_args()
    errors: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    validate_links(errors)
    validate_skill_contract(errors)
    validate_configuration(errors)

    if not args.skip_secret_scan:
        for entry in collect_file_entries(ROOT):
            path = ROOT / entry["path"]
            try:
                data = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for pattern in SECRET_PATTERNS:
                if pattern.search(data):
                    errors.append(f"possible secret pattern in {entry['path']} ({pattern.pattern})")

    manifest_path = ROOT / "PACKAGE_MANIFEST.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            errors.extend(manifest_differences(ROOT, manifest))
        except (ValueError, OSError) as exc:
            errors.append(f"manifest invalid: {exc}")

    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: required files, Markdown links/fences, configuration contracts, heuristic secret scan, and full manifest coverage.")
    print("NOTE: heuristic secret scanning cannot prove absence of every secret; CI/runtime compatibility is proven only by actual runs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
