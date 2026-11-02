#!/usr/bin/env python3
"""Simulate Claude Code and Codex project-skill installation from generated adapters.

This validates filesystem layout and package/resource integrity. It does not start either
host CLI, authenticate a user, or prove that a model discovers or follows the skill.
"""
from __future__ import annotations

import argparse
import json
import shutil
import stat
import sys
import tempfile
import unicodedata
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print(f"ERROR: missing validation dependency: {exc}", file=sys.stderr)
    raise SystemExit(2)

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_skill_packages import build_all, copy_skill_files  # noqa: E402
from tools.validate_b9 import validate_packaged_markdown_links  # noqa: E402

HOSTS = {
    "claude-code": {
        "archive": "peanuts-claude-code-adapter.zip",
        "prefix": ".claude/skills/peanuts",
        "guidance": "CLAUDE.md",
        "invocation": "/peanuts",
        "description": "Claude Code project skill adapter",
    },
    "codex": {
        "archive": "peanuts-codex-adapter.zip",
        "prefix": ".agents/skills/peanuts",
        "guidance": "AGENTS.md",
        "invocation": "$peanuts",
        "description": "Codex repository skill adapter",
    },
}


def _safe_extract(archive_path: Path, destination: Path) -> list[str]:
    """Preflight and extract a bounded ZIP containing only safe regular files.

    The complete archive is validated before the first write. This avoids partial installs
    when a later member is malicious or collides with an earlier destination.
    """
    max_files = 500
    max_member_bytes = 10 * 1024 * 1024
    max_total_bytes = 30 * 1024 * 1024

    with zipfile.ZipFile(archive_path) as archive:
        infos = archive.infolist()
        if len(infos) > max_files:
            raise ValueError(f"archive has too many entries: {len(infos)} > {max_files}")

        seen_exact: set[str] = set()
        seen_portable: dict[str, str] = {}
        file_paths: set[tuple[str, ...]] = set()
        directories: set[tuple[str, ...]] = set()
        total_bytes = 0
        normalized: list[tuple[zipfile.ZipInfo, PurePosixPath, bool]] = []

        for info in infos:
            name = info.filename
            is_dir = info.is_dir()
            raw_name = name[:-1] if is_dir and name.endswith("/") else name
            pure = PurePosixPath(raw_name)
            parts = pure.parts
            if (
                not raw_name
                or pure.is_absolute()
                or not parts
                or any(part in {"", ".", ".."} for part in parts)
                or "\\" in raw_name
                or "\x00" in raw_name
                or raw_name.startswith("/")
                or (len(parts[0]) >= 2 and parts[0][1] == ":")
                or pure.as_posix() != raw_name
            ):
                raise ValueError(f"unsafe archive path: {name!r}")

            if name in seen_exact:
                raise ValueError(f"duplicate archive path: {name}")
            seen_exact.add(name)

            # Catch case/Unicode-normalization-independent collisions at every path
            # component, including directory prefixes on case-insensitive hosts.
            for index in range(1, len(parts) + 1):
                prefix = "/".join(parts[:index])
                portable_key = unicodedata.normalize("NFC", prefix).casefold()
                previous = seen_portable.get(portable_key)
                if previous is not None and previous != prefix:
                    raise ValueError(f"cross-platform path collision: {previous!r} vs {prefix!r}")
                seen_portable[portable_key] = prefix

            mode = (info.external_attr >> 16) & 0xFFFF
            file_type = stat.S_IFMT(mode)
            if stat.S_ISLNK(mode):
                raise ValueError(f"symlink entry is not allowed: {name}")
            if file_type not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError(f"non-regular ZIP member is not allowed: {name}")
            if is_dir and file_type not in (0, stat.S_IFDIR):
                raise ValueError(f"invalid directory entry type: {name}")
            if not is_dir and file_type == stat.S_IFDIR:
                raise ValueError(f"directory entry missing trailing slash: {name}")

            if not is_dir:
                if info.file_size > max_member_bytes:
                    raise ValueError(f"archive member exceeds size limit: {name}")
                if info.file_size and (info.compress_size == 0 or info.file_size / info.compress_size > 1000):
                    raise ValueError(f"archive member compression ratio exceeds limit: {name}")
                total_bytes += info.file_size
                if total_bytes > max_total_bytes:
                    raise ValueError(f"archive exceeds total uncompressed size limit: {total_bytes}")
                file_paths.add(parts)
            else:
                directories.add(parts)
            normalized.append((info, pure, is_dir))

        # No file may also be a parent directory, or collide with a declared directory.
        for parts in file_paths:
            for index in range(1, len(parts)):
                if parts[:index] in file_paths:
                    raise ValueError(f"file/directory path conflict: {'/'.join(parts)}")
            if parts in directories:
                raise ValueError(f"file/directory path conflict: {'/'.join(parts)}")

        # CRC verification comes after size/path preflight so a ZIP bomb cannot force
        # unbounded decompression before the archive limits are applied.
        bad_member = archive.testzip()
        if bad_member:
            raise ValueError(f"ZIP CRC failure in {bad_member}")

        # Only after every member has passed validation do we write to the fixture.
        destination.mkdir(parents=True, exist_ok=True)
        names: list[str] = []
        for info, pure, is_dir in normalized:
            target = destination.joinpath(*pure.parts)
            if is_dir:
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(info))
            names.append(info.filename)
        return names


def _read_frontmatter(skill_file: Path) -> dict[str, Any]:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"missing YAML frontmatter: {skill_file}")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError(f"unterminated YAML frontmatter: {skill_file}")
    metadata = yaml.safe_load(text[4:closing])
    if not isinstance(metadata, dict):
        raise ValueError(f"frontmatter must be a YAML mapping: {skill_file}")
    return metadata


def _collect_files(skill_root: Path) -> dict[str, bytes]:
    return {
        p.relative_to(skill_root).as_posix(): p.read_bytes()
        for p in sorted(skill_root.rglob("*"))
        if p.is_file()
    }


def _validate_one_host(
    *, root: Path, package_output: Path, fixture_root: Path, host: str
) -> list[str]:
    errors: list[str] = []
    spec = HOSTS[host]
    archive_path = package_output / spec["archive"]
    if not archive_path.is_file():
        return [f"{host}: missing generated package {spec['archive']}"]

    # The real repository guidance file is copied into the disposable host fixture.
    guidance_source = root / spec["guidance"]
    if not guidance_source.is_file():
        errors.append(f"{host}: canonical {spec['guidance']} is missing")
        return errors
    fixture_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(guidance_source, fixture_root / spec["guidance"])

    try:
        names = _safe_extract(archive_path, fixture_root)
    except (OSError, zipfile.BadZipFile, ValueError) as exc:
        return errors + [f"{host}: safe install simulation failed: {exc}"]

    skill_root = fixture_root / spec["prefix"]
    skill_file = skill_root / "SKILL.md"
    if not skill_file.is_file():
        errors.append(f"{host}: expected discovery entrypoint missing at {spec['prefix']}/SKILL.md")
        return errors
    if not (fixture_root / spec["guidance"]).is_file():
        errors.append(f"{host}: root project guidance {spec['guidance']} missing after install")

    try:
        metadata = _read_frontmatter(skill_file)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return errors + [f"{host}: invalid skill frontmatter: {exc}"]

    if metadata.get("name") != "peanuts":
        errors.append(f"{host}: skill name must be 'peanuts'")
    if skill_root.name != metadata.get("name"):
        errors.append(f"{host}: skill directory and frontmatter name do not match")
    description = metadata.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        errors.append(f"{host}: skill description is empty or exceeds 1,024 characters")
    if "allowed-tools" in metadata or "allowed_tools" in metadata:
        errors.append(f"{host}: skill must not silently pre-authorize host tools")

    files = _collect_files(skill_root)
    errors.extend(validate_packaged_markdown_links(files))

    # The generated host folder must be a byte-identical copy of the canonical skill
    # plus approved support resources, never an independently authored implementation.
    canonical = copy_skill_files(root)
    if set(files) != set(canonical):
        missing = sorted(set(canonical) - set(files))
        extra = sorted(set(files) - set(canonical))
        errors.append(f"{host}: installed file set differs from canonical package (missing={missing[:5]}, extra={extra[:5]})")
    for rel, payload in canonical.items():
        if files.get(rel) != payload:
            errors.append(f"{host}: installed file differs from canonical source: {rel}")

    # This product is intentionally instruction/reference-only. It contains no helper
    # executable or auto-granted tool permission that could surprise the host owner.
    executable_suffixes = {".py", ".sh", ".ps1", ".bat", ".cmd", ".exe", ".dll"}
    executable_files = sorted(
        p.relative_to(skill_root).as_posix()
        for p in skill_root.rglob("*")
        if p.is_file() and p.suffix.lower() in executable_suffixes
    )
    if executable_files:
        errors.append(f"{host}: unexpected executable content: {executable_files[:10]}")

    # Confirm the relevant operating map keeps the root/skill boundary explicit.
    guidance_text = (fixture_root / spec["guidance"]).read_text(encoding="utf-8").lower()
    if host == "claude-code":
        required = (
            "claude code", ".claude/skills/peanuts", "canonical peanuts skill source",
            "--dangerously-skip-permissions", "normal workspace trust",
        )
    else:
        required = (
            "codex", ".agents/skills/peanuts", "canonical peanuts source",
            "do not bypass sandbox or approval controls", "do not run untrusted code",
        )
    for phrase in required:
        if phrase not in guidance_text:
            errors.append(f"{host}: root guidance is missing expected phrase: {phrase}")

    # Return a machine-readable success marker to tests/reports via an adjacent file.
    if not errors:
        (fixture_root / f"{host}-INSTALL-SIMULATION-PASS.json").write_text(
            json.dumps(
                {
                    "host": host,
                    "discovery_entrypoint": f"{spec['prefix']}/SKILL.md",
                    "root_guidance": spec["guidance"],
                    "explicit_invocation": spec["invocation"],
                    "files_installed": len(names),
                    "skill_name": metadata["name"],
                    "result": "PASS — simulated filesystem installation only",
                    "runtime_claim": "NOT RUN — host CLI/model was not invoked",
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    return errors


def validate_host_adapters(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="friday-cross-host-acceptance-") as temp:
        base = Path(temp)
        package_output = base / "packages"
        try:
            build_all(package_output, root=root)
        except (OSError, ValueError, yaml.YAMLError, zipfile.BadZipFile) as exc:
            return [f"could not build host packages: {exc}"]

        for host in HOSTS:
            fixture = base / "fixtures" / host
            errors.extend(
                _validate_one_host(
                    root=root,
                    package_output=package_output,
                    fixture_root=fixture,
                    host=host,
                )
            )

        # Both installed host folders must preserve exact source parity.
        claude_root = base / "fixtures/claude-code/.claude/skills/peanuts"
        codex_root = base / "fixtures/codex/.agents/skills/peanuts"
        if claude_root.is_dir() and codex_root.is_dir():
            claude_files = _collect_files(claude_root)
            codex_files = _collect_files(codex_root)
            if claude_files != codex_files:
                errors.append("Claude Code and Codex installed skill resources are not byte-identical")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    errors = validate_host_adapters()
    if errors:
        print(f"FAIL: {len(errors)} host adapter issue(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: Codex adapter safely installs to .agents/skills/peanuts/ with AGENTS.md present.")
    print("PASS: Claude Code adapter safely installs to .claude/skills/peanuts/ with CLAUDE.md present.")
    print("PASS: frontmatter, folder-name alignment, relative links, support files and canonical byte parity.")
    print("PASS: no executable scripts or implicit allowed-tools grants in either skill package.")
    print("NOTE: simulated filesystem installation only; Codex/Claude Code CLI and model-runtime tests remain NOT RUN.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
