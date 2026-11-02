#!/usr/bin/env python3
"""Validate/resume a portable planning handoff; never execute its suggested actions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

try:
    from .capability_manager import contained_file, load_json
    from .resource_modes import normalize_mode, mode_label
except ImportError:
    from capability_manager import contained_file, load_json
    from resource_modes import normalize_mode, mode_label

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = (
    "Outcome and people",
    "Evidence and current alternatives",
    "Concepts and choice",
    "Mechanisms and attribution",
    "Event constraints",
    "MVP and non-goals",
    "Demo and acceptance",
    "Risks and tests",
    "Delivery outline",
    "Decisions and approval",
    "Sources and limitations",
    "Next action",
)


def create_starter(
    destination: Path,
    *,
    project_id: str,
    title: str,
    outcome: str,
    owner: str,
    updated_at: str,
    resource_mode: str,
    project_mode: str = "MODE-IDEA",
    root: Path = ROOT,
) -> None:
    """Populate a new staging directory; caller owns atomic rename/no-overwrite behavior."""
    templates = root / "skills/peanuts/assets/templates"
    dossier = (templates / "project-dossier.md").read_text(encoding="utf-8")
    dossier = dossier.replace("<Project title>", title).replace("<project-id>", project_id)
    dossier = dossier.replace("<desired-outcome>", outcome).replace("<project-mode>", project_mode)
    (destination / "PROJECT_DOSSIER.md").write_text(dossier, encoding="utf-8", newline="\n")
    data = load_json(templates / "handoff.json")
    data.update(
        project_id=project_id,
        summary=outcome,
        updated_at=updated_at,
        resource_mode=normalize_mode(resource_mode),
        project_mode=project_mode,
    )
    data["next_action"]["owner"] = owner
    data["dossier"]["sha256"] = hashlib.sha256(
        (destination / "PROJECT_DOSSIER.md").read_bytes()
    ).hexdigest()
    (destination / "handoff.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )

    _, errors = validate(destination, root)
    if errors:
        raise ValueError("Invalid compact starter: " + "; ".join(errors))


def validate(project: Path, root: Path = ROOT) -> tuple[dict | None, list[str]]:
    try:
        project = project.resolve()
        data = load_json(contained_file(project, "handoff.json"))
        schema = load_json(root / "schemas/planning-handoff.schema.json")
        Draft202012Validator.check_schema(schema)
        errors = [
            f"{list(e.path)}: {e.message}"
            for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)
        ]
        if errors:
            return None, errors
        dossier = contained_file(project, data["dossier"]["path"])
        if dossier.stat().st_size > 262144:
            errors.append("dossier exceeds the compact 256 KiB limit; link detailed appendices")
        else:
            payload = dossier.read_bytes()
            if data["dossier"]["sha256"] is None:
                errors.append("dossier digest NOT RUN: reviewed SHA-256 is unavailable")
            elif hashlib.sha256(payload).hexdigest() != data["dossier"]["sha256"]:
                errors.append(
                    "dossier digest mismatch: refresh the handoff after reviewing changed content"
                )
            text = payload.decode("utf-8")
            for heading in HEADINGS:
                if f"## {heading}" not in text:
                    errors.append(f"dossier section missing: {heading}")
        for key in ["sources", "claims", "decisions", "risks"]:
            ids = [item["id"] for item in data[key]]
            if len(ids) != len(set(ids)):
                errors.append(f"duplicate {key} ID")
        sources = {s["id"]: s for s in data["sources"]}
        for claim in data["claims"]:
            linked = [sources[cid] for cid in claim["source_ids"] if cid in sources]
            if len(linked) != len(claim["source_ids"]):
                errors.append(f"{claim['id']}: dangling source reference")
            if claim["basis"] == "sourced" and (
                not linked or any(s["status"] != "inspected" for s in linked)
            ):
                errors.append(f"{claim['id']}: sourced claim requires inspected sources")
            if claim["basis"] == "synthetic" and (
                data["evidence_context"] == "real"
                or any(s["status"] != "synthetic" for s in linked)
            ):
                errors.append(f"{claim['id']}: synthetic evidence must remain explicitly synthetic")
        if data["evidence_context"] == "real" and any(
            s["status"] == "synthetic" for s in sources.values()
        ):
            errors.append("real evidence context contains synthetic sources")
        for decision in data["decisions"]:
            if decision["status"] == "approved" and (
                not decision["approval_evidence"].strip() or data["evidence_context"] == "synthetic"
            ):
                errors.append(
                    f"{decision['id']}: approved decision requires real approval evidence and scope"
                )
        critical_open = False
        for risk in data["risks"]:
            if risk["status"] == "mitigated" and not risk["evidence"].strip():
                errors.append(f"{risk['id']}: mitigation requires result evidence")
            critical_open |= risk["severity"] == "critical" and risk["status"] == "open"
        if (critical_open or data["blockers"]) and data["disposition"] != "blocked":
            errors.append("open critical risks/blockers require blocked disposition")
        if data["disposition"] == "blocked" and not data["blockers"]:
            errors.append("blocked handoff needs an explicit blocker and next action")
        return (None if errors else data), errors
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as exc:
        return None, [str(exc)]


def resume(project: Path, available_tools: tuple[str, ...] = ()) -> dict:
    data, errors = validate(project)
    if errors:
        return {"status": "invalid_handoff", "errors": errors, "execution": "not-performed"}
    assert data is not None
    missing = sorted(set(data["next_action"]["required_tools"]) - set(available_tools))
    return {
        "status": "blocked" if missing or data["disposition"] == "blocked" else "resumable",
        "execution": "not-performed",
        "context": data,
        "mode_label": mode_label(data["resource_mode"]),
        "missing_tools_in_this_host": missing,
        "next_step": "Read the linked dossier and relevant source passages. Recheck time-sensitive facts; resolve blockers before dependent work. Use only actual session permissions.",
        "limits": "Artifact integrity and traceability only; does not establish truth, user validation, model behavior, formal P7–P9 approval, or permission to execute.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument(
        "--resume", action="store_true", help="return self-contained context after validation"
    )
    parser.add_argument("--available-tool", action="append", default=[])
    args = parser.parse_args()
    result = resume(args.project, tuple(args.available_tool))
    if not args.resume and result["status"] != "invalid_handoff":
        result = {key: value for key, value in result.items() if key != "context"}
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result["status"] == "resumable" else 2


if __name__ == "__main__":
    raise SystemExit(main())
