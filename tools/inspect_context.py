#!/usr/bin/env python3
"""Inspect repository-owned context files using word/character proxies, never token estimates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Host entry points are alternatives, not files loaded together in one runtime.
PROFILES = {
    "claude-code": ["CLAUDE.md", "skills/peanuts/SKILL.md"],
    "codex": ["AGENTS.md", "skills/peanuts/SKILL.md"],
    "peanuts-skill-only": ["skills/peanuts/SKILL.md"],
    "host-maps": ["CLAUDE.md", "AGENTS.md"],
    "compact-handoff": ["skills/peanuts/SKILL.md", "skills/peanuts/references/planning-handoff.md"],
    "fast-event-start": ["skills/peanuts/SKILL.md", "skills/peanuts/references/hackathon-sprint.md"],
}

# Soft maintainability ceilings, not model-token budgets or host-enforced limits.
WORD_TARGETS = {
    "CLAUDE.md": 600,
    "AGENTS.md": 600,
    "skills/peanuts/SKILL.md": 1100,
}


def inspect_files(root: Path = ROOT, paths: list[str] | None = None) -> dict:
    results = []
    for relative in paths or ["CLAUDE.md", "AGENTS.md", "skills/peanuts/SKILL.md"]:
        path = root / relative
        if not path.is_file():
            results.append({"path": relative, "status": "missing"})
            continue
        content = path.read_text(encoding="utf-8")
        words = len(content.split())
        target = WORD_TARGETS.get(relative)
        results.append({
            "path": relative,
            "status": "present",
            "characters": len(content),
            "words": words,
            "lines": len(content.splitlines()),
            "soft_word_target": target,
            "within_soft_target": None if target is None else words <= target,
        })
    return {
        "measurement": "characters_words_lines_only",
        "warning": "These are maintainability proxies, not model-token counts, context-window usage, or provider usage telemetry.",
        "note": "Claude Code and Codex use different host entry points; the claude-code and codex profiles are alternatives, not simultaneous context loads.",
        "files": results,
    }


def inspect_profiles(root: Path = ROOT, profile: str = "overview") -> dict:
    names = list(PROFILES) if profile == "overview" else [profile]
    return {
        "measurement": "characters_words_lines_only",
        "warning": "These are maintainability proxies, not model-token counts, context-window usage, or provider usage telemetry.",
        "profiles": [
            {"profile": name, **inspect_files(root, PROFILES[name])}
            for name in names
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print machine-readable output")
    parser.add_argument(
        "--profile",
        choices=["overview", *PROFILES.keys()],
        default="overview",
        help="inspect host-specific context paths separately; overview never implies all are loaded together",
    )
    parser.add_argument("paths", nargs="*", help="optional repository-relative files; overrides --profile")
    args = parser.parse_args()

    report = inspect_files(paths=args.paths) if args.paths else inspect_profiles(profile=args.profile)
    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("Friday context inspection (maintainability proxies, not a token meter)")
    if "profiles" in report:
        for profile_data in report["profiles"]:
            print(f"\n[{profile_data['profile']}]")
            for item in profile_data["files"]:
                if item["status"] != "present":
                    print(f"NOT FOUND: {item['path']}")
                else:
                    target = item.get("soft_word_target")
                    suffix = f"; soft target {target} words: {'within' if item['within_soft_target'] else 'over'}" if target else ""
                    print(f"{item['path']}: {item['words']} words, {item['characters']} characters, {item['lines']} lines{suffix}")
    else:
        for item in report["files"]:
            if item["status"] != "present":
                print(f"NOT FOUND: {item['path']}")
            else:
                print(f"{item['path']}: {item['words']} words, {item['characters']} characters, {item['lines']} lines")
    print(f"\n{report['warning']}")
    if "note" in report:
        print(report["note"])

    if "profiles" in report:
        return 0 if all(
            item["status"] == "present"
            for profile_data in report["profiles"]
            for item in profile_data["files"]
        ) else 1
    return 0 if all(item["status"] == "present" for item in report["files"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
