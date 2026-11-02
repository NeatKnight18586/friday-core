#!/usr/bin/env python3
"""Validate Friday's capability catalog against schemas and available package entrypoints."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "capabilities" / "registry.json"
SCHEMA_PATH = ROOT / "schemas" / "capability-registry.schema.json"


def safe_repo_path(value: str) -> bool:
    pure = PurePosixPath(value)
    return bool(value) and not pure.is_absolute() and ".." not in pure.parts and "\\" not in value


def read_skill_metadata(skill_path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        content = skill_path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, f"cannot read skill file: {exc}"
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)", content, re.DOTALL)
    if not match:
        return None, "missing or malformed YAML frontmatter"
    try:
        metadata = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"invalid YAML frontmatter: {exc}"
    if not isinstance(metadata, dict):
        return None, "YAML frontmatter must be a mapping"
    return metadata, None


def validate_registry(root: Path = ROOT, registry_override: dict | None = None) -> list[str]:
    errors: list[str] = []
    registry_path = root / "capabilities" / "registry.json"
    schema_path = root / "schemas" / "capability-registry.schema.json"
    try:
        registry = (json.loads(registry_path.read_text(encoding="utf-8"))
                    if registry_override is None else registry_override)
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        errors.extend(f"registry schema: {error.message}" for error in Draft202012Validator(schema).iter_errors(registry))
        if errors:
            return errors
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"cannot load capability registry/schema: {exc}"]

    entries = registry.get("capabilities", [])
    ids: set[str] = set()
    skill_names: set[str] = set()
    registered_skill_paths: set[str] = set()
    canonical_paths: dict[str, str] = {}
    dependency_edges: list[tuple[str, str]] = []
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            continue
        capability_id = entry.get("id")
        label = f"capabilities[{index}] ({capability_id or 'unknown'})"
        if capability_id in ids:
            errors.append(f"{label}: duplicate capability ID")
        ids.add(capability_id)

        canonical = entry.get("canonical_path", "")
        skill_file = entry.get("skill_file")
        if not safe_repo_path(canonical):
            errors.append(f"{label}: canonical_path must be a safe repository-relative path")
            continue
        canonical_key = PurePosixPath(canonical).as_posix().casefold()
        if canonical_key in canonical_paths:
            errors.append(f"{label}: canonical package path is already registered by {canonical_paths[canonical_key]}")
        else:
            canonical_paths[canonical_key] = str(capability_id)
        canonical_path = root / PurePosixPath(canonical)
        try:
            canonical_path.resolve().relative_to(root.resolve())
        except ValueError:
            errors.append(f"{label}: canonical package path escapes repository root")
            continue
        if not canonical_path.is_dir():
            errors.append(f"{label}: canonical package directory missing: {canonical}")

        entrypoint = entry.get("entrypoint")
        if not isinstance(entrypoint, str) or not safe_repo_path(entrypoint):
            errors.append(f"{label}: entrypoint must be a safe repository-relative file path")
        else:
            entrypoint_path = root / PurePosixPath(entrypoint)
            try:
                entrypoint_path.resolve().relative_to(canonical_path.resolve())
            except ValueError:
                errors.append(f"{label}: entrypoint must be inside canonical_path")
            else:
                if not entrypoint_path.is_file():
                    errors.append(f"{label}: package entrypoint file missing: {entrypoint}")

        if entry.get("kind") == "skill" and not skill_file:
            errors.append(f"{label}: kind=skill requires skill_file")
        if entry.get("kind") == "skill" and isinstance(skill_file, str) and entrypoint != skill_file:
            errors.append(f"{label}: for kind=skill, entrypoint must equal skill_file (SKILL.md is the skill entrypoint)")
        if skill_file is not None:
            if not safe_repo_path(skill_file):
                errors.append(f"{label}: skill_file must be a safe repository-relative path")
                continue
            registered_skill_paths.add(skill_file)
            skill_path = root / PurePosixPath(skill_file)
            try:
                skill_path.resolve().relative_to(root.resolve())
            except ValueError:
                errors.append(f"{label}: skill_file escapes repository root")
                continue
            if not skill_path.is_file():
                errors.append(f"{label}: skill file missing: {skill_file}")
                continue
            try:
                skill_path.resolve().relative_to(canonical_path.resolve())
            except ValueError:
                errors.append(f"{label}: skill_file must be inside canonical_path")
                continue

            metadata, metadata_error = read_skill_metadata(skill_path)
            if metadata_error:
                errors.append(f"{label}: {metadata_error}")
                continue
            assert metadata is not None
            name = metadata.get("name")
            description = metadata.get("description")
            if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                errors.append(f"{label}: skill name must be lowercase hyphen-case and at most 64 characters")
            elif name in skill_names:
                errors.append(f"{label}: duplicate Agent Skills name: {name}")
            skill_names.add(name)
            if not isinstance(description, str) or not description.strip():
                errors.append(f"{label}: skill description is required")
            elif len(description) > 1024:
                errors.append(f"{label}: skill description exceeds the current 1024-character specification limit")
            elif "<" in description or ">" in description:
                errors.append(f"{label}: skill description must not contain XML tags")

        for dependency in entry.get("dependencies", []):
            dependency_edges.append((capability_id, dependency))

        host_names = [profile.get("host") for profile in entry.get("host_profiles", []) if isinstance(profile, dict)]
        if len(host_names) != len(set(host_names)):
            errors.append(f"{label}: duplicate host profile")
        for profile in entry.get("host_profiles", []):
            if not isinstance(profile, dict):
                continue
            discovery_path = profile.get("discovery_path")
            if discovery_path is not None and not safe_repo_path(discovery_path):
                errors.append(f"{label}: unsafe host discovery_path: {discovery_path}")
            if profile.get("status") == "verified":
                if discovery_path is None:
                    errors.append(f"{label}: verified host profile requires discovery_path")
                else:
                    host_path = root / PurePosixPath(discovery_path)
                    try:
                        host_path.resolve().relative_to(root.resolve())
                    except ValueError:
                        errors.append(f"{label}: verified host discovery_path escapes repository")
                    else:
                        if not host_path.exists():
                            errors.append(f"{label}: verified host discovery_path does not exist: {discovery_path}")
        if entry.get("default_mode") not in entry.get("supported_modes", []):
            errors.append(f"{label}: default_mode must be included in supported_modes")
        for eval_ref in entry.get("evaluation_refs", []):
            eval_path = root / "evals" / "cases" / f"{eval_ref}.json"
            if not eval_path.is_file():
                errors.append(f"{label}: evaluation reference does not exist: {eval_ref}")

    dependency_graph: dict[str, list[str]] = {capability_id: [] for capability_id in ids if isinstance(capability_id, str)}
    for source_id, dependency_id in dependency_edges:
        if dependency_id not in ids:
            errors.append(f"capability {source_id}: dependency is not registered: {dependency_id}")
            continue
        if dependency_id == source_id:
            errors.append(f"capability {source_id}: capability cannot depend on itself")
            continue
        if source_id in dependency_graph and isinstance(dependency_id, str):
            dependency_graph[source_id].append(dependency_id)

    # Capability dependencies must remain acyclic so future composition can be bounded.
    visiting: set[str] = set()
    visited: set[str] = set()
    reported_cycles: set[tuple[str, ...]] = set()

    def visit(node: str, trail: list[str]) -> None:
        if node in visiting:
            cycle_start = trail.index(node) if node in trail else 0
            cycle = tuple(trail[cycle_start:] + [node])
            normalized = tuple(sorted(set(cycle)))
            if normalized not in reported_cycles:
                errors.append("capability dependency cycle: " + " -> ".join(cycle))
                reported_cycles.add(normalized)
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in dependency_graph.get(node, []):
            visit(dependency, trail + [node])
        visiting.remove(node)
        visited.add(node)

    for capability_id in dependency_graph:
        visit(capability_id, [])

    # Prevent skill packages from silently bypassing the Friday catalog.
    skill_root = root / "skills"
    if skill_root.is_dir():
        for skill_file in skill_root.glob("*/SKILL.md"):
            relative = skill_file.relative_to(root).as_posix()
            if relative not in registered_skill_paths:
                errors.append(f"unregistered skill package: {relative}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="list registered capabilities after validation")
    args = parser.parse_args()
    errors = validate_registry()
    if errors:
        print(f"FAIL: {len(errors)} capability registry issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1

    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    print(f"PASS: capability registry schema, package paths, optional skill entrypoints, dependencies, metadata, and references ({len(registry['capabilities'])} capability/capabilities).")
    if args.list:
        for entry in registry["capabilities"]:
            print(f"- {entry['id']}: {entry['display_name']} [{entry['kind']}/{entry['maturity']}] — {entry['canonical_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
