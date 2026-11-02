#!/usr/bin/env python3
"""Create a new, private Peanuts project workspace from generic templates."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    from .handoff import create_starter
except ImportError:
    from handoff import create_starter

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE = ROOT / "local-workspace" / "projects"
MODES = ["MODE-EVENT", "MODE-PROBLEM", "MODE-IDEA", "MODE-EXISTING", "MODE-RESEARCH"]


def slugify(value: str) -> str:
    value = value.strip().lower()
    if "/" in value or "\\" in value or value in {".", ".."}:
        raise ValueError("Project ID must not contain path separators or traversal segments.")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if not value or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise ValueError("Project ID must contain letters/numbers separated by hyphens.")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True, help="kebab-case project ID")
    parser.add_argument("--title", required=True, help="Human-readable project title")
    parser.add_argument("--mode", choices=MODES, default="MODE-IDEA")
    parser.add_argument("--outcome", default="To be clarified with the project owner.")
    parser.add_argument("--owner", default="project owner")
    parser.add_argument("--layout", choices=["full", "compact"], default="full",
                        help="Compact planning: dossier + handoff only; full retains existing records/gates")
    parser.add_argument("--resource-mode", choices=["fast", "quick", "standard", "deep"], default="standard",
                        help="Compact layout depth; stored fast mode remains quick")
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=DEFAULT_WORKSPACE,
        help="Defaults to ignored local-workspace/projects",
    )
    args = parser.parse_args()

    try:
        project_id = slugify(args.id)
        if len(args.title.strip()) < 3:
            raise ValueError("Project title must contain at least 3 characters.")
        if len(args.outcome.strip()) < 3:
            raise ValueError("Desired outcome must contain at least 3 characters.")
        if len(args.title.strip()) > 160 or len(args.outcome.strip()) > 2000:
            raise ValueError("Title/outcome exceeds the project contract limit.")
        if args.layout == "compact" and (not args.owner.strip() or len(args.owner.strip()) > 120):
            raise ValueError("Compact project owner must contain 1–120 characters.")
        if args.layout == "full" and args.resource_mode != "standard":
            raise ValueError("--resource-mode applies to --layout compact")
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    workspace = args.workspace_root.expanduser().resolve()
    target = workspace / project_id
    if target.exists():
        print(f"ERROR: refusing to overwrite existing project: {target}", file=sys.stderr)
        return 2

    template = ROOT / "templates" / "project"
    if not template.is_dir():
        print("ERROR: project templates are missing.", file=sys.stderr)
        return 2

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    workspace.mkdir(parents=True, exist_ok=True)
    stage_dir = Path(tempfile.mkdtemp(prefix=f".{project_id}.", dir=workspace))

    try:
        if args.layout == "compact":
            create_starter(stage_dir, project_id=project_id, title=args.title.strip(),
                           outcome=args.outcome.strip(), owner=args.owner.strip(),
                           updated_at=now, resource_mode=args.resource_mode, project_mode=args.mode)
            if target.exists():
                raise FileExistsError(f"refusing to overwrite existing project: {target}")
            stage_dir.rename(target)
            print(f"Created compact planning workspace: {target}")
            print("Next: python tools/handoff.py <project-directory> --resume")
            print("Planning context only; full P7–P9 gates and external-action permissions remain separate.")
            return 0
        shutil.copytree(template, stage_dir, dirs_exist_ok=True)
        project = json.loads((stage_dir / "project.json").read_text(encoding="utf-8"))
        state = json.loads((stage_dir / "state.json").read_text(encoding="utf-8"))
        research_plan_path = stage_dir / "research-plan.json"
        research_plan = json.loads(research_plan_path.read_text(encoding="utf-8"))
        demo_plan_path = stage_dir / "demo-plan.json"
        demo_plan = json.loads(demo_plan_path.read_text(encoding="utf-8"))

        project.update(
            {
                "project_id": project_id,
                "title": args.title.strip(),
                "mode": args.mode,
                "created_at": now,
                "updated_at": now,
                "summary": "New project. Discovery has not yet been completed.",
                "desired_outcome": args.outcome.strip(),
                "owner_label": args.owner.strip(),
            }
        )
        state.update({"project_id": project_id, "updated_at": now})
        research_plan.update({"project_id": project_id, "updated_at": now, "created_at": now})
        research_plan["desired_outcome"] = args.outcome.strip()
        demo_plan.update({"project_id": project_id, "created_at": now, "updated_at": now, "owner": args.owner.strip()})

        (stage_dir / "project.json").write_text(
            json.dumps(project, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (stage_dir / "state.json").write_text(
            json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        research_plan_path.write_text(
            json.dumps(research_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        demo_plan_path.write_text(
            json.dumps(demo_plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        brief = (template / "PROJECT_BRIEF.md").read_text(encoding="utf-8")
        brief = brief.replace("<Project title>", args.title.strip())
        brief = brief.replace("<project-id>", project_id).replace("MODE-*", args.mode)
        brief = brief.replace("YYYY-MM-DD", now[:10])
        (stage_dir / "PROJECT_BRIEF.md").write_text(brief, encoding="utf-8")

        handoff = (template / "STATUS_AND_HANDOFF.md").read_text(encoding="utf-8")
        handoff = handoff.replace("<project-id>", project_id)
        handoff = handoff.replace("YYYY-MM-DDTHH:MM:SSZ", now)
        (stage_dir / "STATUS_AND_HANDOFF.md").write_text(handoff, encoding="utf-8")

        # Personalize B8 document headers without treating generated templates as approved plans.
        for filename in ["PRD.md", "TECHNICAL_DESIGN.md", "BUILD_PLAN.md", "DEMO_PLAN.md"]:
            doc_path = stage_dir / filename
            content = doc_path.read_text(encoding="utf-8")
            content = content.replace("<Project title>", args.title.strip())
            content = content.replace("<project-id>", project_id)
            content = content.replace("YYYY-MM-DD", now[:10])
            content = content.replace("project owner", args.owner.strip())
            doc_path.write_text(content, encoding="utf-8")

        # Register the initial human-readable documents so future references can be
        # checked against real workspace files. Draft registrations are not approvals.
        artifact_rows = []
        artifact_specs = [
            ("ART-0001", "Project Brief", "project_brief", "PROJECT_BRIEF.md"),
            ("ART-0002", "Product Requirements Document", "prd", "PRD.md"),
            ("ART-0003", "Technical Design", "technical_design", "TECHNICAL_DESIGN.md"),
            ("ART-0004", "Build and Delivery Plan", "build_plan", "BUILD_PLAN.md"),
            ("ART-0005", "Demonstration Plan", "demo_plan", "DEMO_PLAN.md"),
            ("ART-0006", "Structured Demonstration Plan", "demo_plan_data", "demo-plan.json"),
        ]
        for artifact_id, title, artifact_type, artifact_path in artifact_specs:
            artifact_rows.append({
                "schema_version": "1.0.0", "artifact_id": artifact_id,
                "title": title, "artifact_type": artifact_type, "path": artifact_path,
                "status": "draft", "version": "0.1.0", "owner": args.owner.strip(),
                "created_at": now, "updated_at": now,
            })
        artifact_ledger = stage_dir / "records" / "artifacts.jsonl"
        artifact_ledger.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in artifact_rows),
            encoding="utf-8",
        )

        if target.exists():
            raise FileExistsError(f"refusing to overwrite existing project: {target}")
        stage_dir.rename(target)
    except Exception:
        shutil.rmtree(stage_dir, ignore_errors=True)
        raise

    print(f"Created new project workspace: {target}")
    print("Next: python tools/validate_project.py <project-directory>")
    print("Privacy: the default workspace is excluded from Git; review sensitivity before sharing any project data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
