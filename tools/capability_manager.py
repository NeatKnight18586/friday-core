#!/usr/bin/env python3
"""Read-only capability selection and intake. Never imports or executes a capability."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator

try:
    from .validate_capabilities import validate_registry
    from .resource_modes import normalize_mode, mode_label
except ImportError:
    from validate_capabilities import validate_registry
    from resource_modes import normalize_mode, mode_label

ROOT = Path(__file__).resolve().parents[1]
MAX_JSON_BYTES = 131072


def contained_file(root: Path, relative: str, package: str | None = None) -> Path:
    """Reject noncanonical paths, links, and paths outside the declared package/root."""
    pure = PurePosixPath(relative)
    if (
        not relative
        or pure.is_absolute()
        or ".." in pure.parts
        or "\\" in relative
        or ":" in relative
        or pure.as_posix() != relative
        or relative == "."
    ):
        raise ValueError("unsafe repository-relative path")
    path = root / relative
    for parent in [path, *path.parents]:
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError("symlink is not allowed in a capability path")
    path.resolve().relative_to(root.resolve())
    if package:
        path.resolve().relative_to((root / package).resolve())
    if not path.is_file():
        raise ValueError("capability file is missing")
    return path


def load_json(path: Path) -> Any:
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError("JSON exceeds the 128 KiB input limit")

    # Reject duplicate keys rather than allowing an apparently reviewed value to be replaced.
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def load_catalog(root: Path) -> dict:
    return load_json(contained_file(root, "capabilities/registry.json"))


def contracts(root: Path, registry: dict) -> tuple[dict[str, dict], list[str]]:
    try:
        errors = validate_registry(root, registry_override=registry)
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        return {}, [f"invalid catalog: {exc}"]
    if errors:
        return {}, errors
    schema = load_json(contained_file(root, "schemas/capability-contract.schema.json"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    result = {}
    for entry in registry["capabilities"]:
        cid = entry["id"]
        try:
            contained_file(root, entry["entrypoint"], entry["canonical_path"])
            contract_file = entry.get("contract_file")
            if not contract_file:
                raise ValueError("contract_file required for manager selection/intake")
            data = load_json(contained_file(root, contract_file, entry["canonical_path"]))
            issues = sorted(validator.iter_errors(data), key=lambda e: str(e.path))
            if issues:
                raise ValueError("; ".join(e.message for e in issues))
            if data["capability_id"] != cid:
                raise ValueError("contract capability_id does not match registry id")
            for required, optional in [
                ("required_inputs", "optional_inputs"),
                ("required_tools", "optional_tools"),
                ("required_permissions", "optional_permissions"),
            ]:
                if set(data[required]) & set(data[optional]):
                    raise ValueError(f"{required} overlaps {optional}")
            if not data["outputs"]:
                raise ValueError("at least one output must be declared")
            result[cid] = data
        except (OSError, ValueError, TypeError) as exc:
            errors.append(f"{cid}: {exc}")
    return result, errors


def catalog_summary(root: Path) -> dict:
    registry = load_catalog(root)
    _, errors = contracts(root, registry)
    if errors:
        return {"status": "invalid_catalog", "errors": errors}
    # No instruction bodies are returned to the host. Validation inspects skill frontmatter.
    keys = ("id", "summary", "kind", "lifecycle", "maturity", "intents", "exclusions")
    return {
        "status": "catalog",
        "capabilities": [
            {key: entry.get(key, []) for key in keys} for entry in registry["capabilities"]
        ],
        "execution": "not-performed",
    }


def select(
    root: Path,
    *,
    host: str,
    capability: str | None = None,
    intent: str | None = None,
    mode: str | None = None,
    inputs: tuple[str, ...] = (),
    tools: tuple[str, ...] = (),
    grants: tuple[str, ...] = (),
    confirm_conditional: bool = False,
) -> dict:
    """Match declared intent/ID, gate dependency closure, return only paths and contracts.

    Caller-supplied grants describe permissions; they never grant OS/API authority.
    Free-text interpretation belongs to the host reading FRIDAY.md, not fuzzy keywords.
    """
    registry = load_catalog(root)
    data, errors = contracts(root, registry)
    base = {"execution": "not-performed", "host": host}
    if errors:
        return {**base, "status": "invalid_catalog", "errors": errors}
    entries = {entry["id"]: entry for entry in registry["capabilities"]}
    if capability and intent:
        return {
            **base,
            "status": "invalid_request",
            "reason": "choose explicit ID or intent, not both",
        }
    if not capability and not intent:
        return {
            **base,
            "status": "invalid_request",
            "reason": "supply an explicit ID or declared intent",
        }
    candidates = (
        ([entries[capability]] if capability in entries else [])
        if capability
        else [
            entry
            for entry in entries.values()
            if intent in entry["intents"] and entry["lifecycle"] == "active"
        ]
    )
    if not candidates:
        return {
            **base,
            "status": "no_match",
            "reason": "No registered active capability fits; clarify or use a general workflow.",
        }
    if len(candidates) > 1:
        return {
            **base,
            "status": "ambiguous",
            "candidates": sorted(e["id"] for e in candidates),
            "reason": "Ask one question to distinguish the desired outcome.",
        }
    chosen = candidates[0]
    try:
        requested_mode = normalize_mode(mode or chosen["default_mode"])
    except ValueError as exc:
        return {**base, "status": "invalid_request", "reason": str(exc)}
    ordered: list[str] = []

    def visit(cid):
        if cid in ordered:
            return
        for dep in entries[cid]["dependencies"]:
            visit(dep)
        ordered.append(cid)

    visit(chosen["id"])  # Registry validation has already rejected missing/cyclic dependencies.
    blockers = []
    selected = []
    for cid in ordered:
        entry, contract = entries[cid], data[cid]
        profile = next((p for p in entry["host_profiles"] if p["host"] == host), None)
        if entry["lifecycle"] != "active":
            blockers.append(f"{cid}: capability is not active")
        if requested_mode not in entry["supported_modes"]:
            blockers.append(f"{cid}: mode is not supported: {requested_mode}")
        if profile is None or profile["status"] in ("planned", "not-supported"):
            blockers.append(f"{cid}: host is unavailable or unsupported")
        elif profile["status"] == "conditional" and not confirm_conditional:
            blockers.append(
                f"{cid}: confirm actual host eligibility before selecting a conditional route"
            )
        for name, available, label in [
            ("required_inputs", inputs, "input"),
            ("required_tools", tools, "tool"),
            ("required_permissions", grants, "permission"),
        ]:
            for missing in sorted(set(contract[name]) - set(available)):
                blockers.append(f"{cid}: missing {label}: {missing}")
        selected.append(
            {
                "id": cid,
                "entrypoint": entry["entrypoint"],
                "contract_file": entry["contract_file"],
                "contract": contract,
                "host_status": profile["status"] if profile else "not-supported",
                "maturity": entry["maturity"],
            }
        )
    if blockers:
        return {
            **base,
            "status": "blocked",
            "capability": chosen["id"],
            "blockers": blockers,
            "reason": "Resolve prerequisites before loading capability instructions.",
        }
    return {
        **base,
        "status": "selected",
        "capability": chosen["id"],
        "mode": requested_mode,
        "mode_label": mode_label(requested_mode),
        "load_order": selected,
        "permissions_are": "caller-reported, not an authority grant",
        "runtime_evidence": "not established by selection",
        "next_action": "Host loads only these entrypoints, then task-relevant references; never execute imported scripts automatically.",
    }


def intake(root: Path, candidate_file: Path) -> dict:
    """Validate an already staged package against a proposed catalog, without writing it."""
    candidate = load_json(candidate_file)
    if not isinstance(candidate, dict):
        return {"status": "invalid_candidate", "errors": ["candidate must be a metadata object"]}
    registry = load_catalog(root)
    proposed = {**registry, "capabilities": [*registry["capabilities"], candidate]}
    _, errors = contracts(root, proposed)
    if errors:
        return {"status": "invalid_candidate", "errors": errors, "execution": "not-performed"}
    return {
        "status": "validated_candidate",
        "capability": candidate["id"],
        "execution": "not-performed",
        "registry_written": False,
        "activation_approved": False,
        "next_action": "Review package content, rights, permissions and host behavior before explicitly updating the catalog. Structural validity is not trust.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="validated metadata only")
    choose = commands.add_parser("select")
    source = choose.add_mutually_exclusive_group(required=True)
    source.add_argument("--capability")
    source.add_argument("--intent")
    choose.add_argument("--host", required=True)
    choose.add_argument("--mode", choices=["fast", "quick", "standard", "deep"])
    choose.add_argument(
        "--input",
        action="append",
        default=[],
        dest="inputs",
        help="available input name; no private values",
    )
    choose.add_argument("--available-tool", action="append", default=[], dest="tools")
    choose.add_argument("--grant", action="append", default=[], dest="grants")
    choose.add_argument(
        "--confirm-conditional-host", action="store_true", dest="confirm_conditional"
    )
    add = commands.add_parser("intake", help="dry-run staged candidate; no registration/execution")
    add.add_argument("--candidate", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "list":
            result = catalog_summary(args.root.resolve())
        elif args.command == "intake":
            result = intake(args.root.resolve(), args.candidate)
        else:
            result = select(
                args.root.resolve(),
                host=args.host,
                capability=args.capability,
                intent=args.intent,
                mode=args.mode,
                inputs=tuple(args.inputs),
                tools=tuple(args.tools),
                grants=tuple(args.grants),
                confirm_conditional=args.confirm_conditional,
            )
    except (OSError, ValueError, TypeError, KeyError) as exc:
        result = {"status": "invalid_input", "errors": [str(exc)], "execution": "not-performed"}
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in ("selected", "catalog", "validated_candidate") else 2


if __name__ == "__main__":
    raise SystemExit(main())
