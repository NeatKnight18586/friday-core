# Friday Host Adapter Architecture

**Status:** B9 packages implemented; B10 Codex/Claude Code fixture-install simulation and package-security checks passed; actual host runtime acceptance pending.
**Version:** 0.1.0-draft
**Reviewed:** 2026-11-02

## 1. Purpose and design rule

The portable capability source is `skills/peanuts/`. Host adapters provide discovery paths, packaging, concise host guidance, and interaction-specific constraints. They must not become separately maintained copies of Peanuts' methods. Generate every runnable/attachable copy with `tools/build_skill_packages.py` and validate it with `tools/validate_b9.py`.

The portable Agent Skills specification requires a `SKILL.md` with YAML frontmatter and Markdown instructions. The required `name` must be a valid lowercase/hyphen identifier and match the parent skill directory. Descriptions should communicate function and invocation context. This repository uses `name: peanuts` to match `skills/peanuts/`. The description is intentionally concise for reliable discovery, but it is validated against the documented 1,024-character metadata maximum—not an unsupported universal 200-character limit. Anthropic's current Agent Skills documentation also specifies a 1,024-character maximum and requires the description to explain both function and when the Skill should trigger.

## 2. Supported routes

| Host | Generated package path | Guidance | Runtime status |
|---|---|---|---|
| Portable Agent Skills / eligible uploaders | `peanuts/SKILL.md` at ZIP root | Agent Skills package | Package generated and structurally validated; host upload/invocation not run |
| Claude Code | `.claude/skills/peanuts/SKILL.md` | Root `CLAUDE.md` plus skill; invoke `/peanuts` | Package, safe fixture installation, metadata, references and source parity passed; actual Claude Code CLI/model runtime `NOT RUN` |
| Codex | `.agents/skills/peanuts/SKILL.md` | Root `AGENTS.md` plus skill; invoke `$peanuts` or select via `/skills` | Package, safe fixture installation, metadata, references and source parity passed; actual Codex CLI/model runtime `NOT RUN` |
| ChatGPT Project | Five generated plain-text reference files containing Markdown-formatted content plus `PROJECT_INSTRUCTIONS.md` | Manual Project instructions | Pack generated and constrained for a Free Project; real UI installation/invocation not run |
| Native ChatGPT Skills | Conditional upload route | Native SKILL package | Only use when account, surface, and workspace eligibility are confirmed; not assumed available |
| Claude Chat (claude.ai / Claude iOS app) | B10.1 custom Skill ZIP with `peanuts/skill.md` plus a separate Friday Project knowledge bundle and Project instructions | Upload Skill in Customize → Skills; create Friday Project and add its five knowledge files | Current consumer Skill format/200-character metadata, Project docs and iPad guide validated locally; owner account upload, enablement, Project UI and fresh-chat runtime NOT RUN |

Claude Code and Codex filesystem skill directories differ and are not automatically synced with their other product surfaces. The same package must be separately installed where needed. Do not infer discovery from a successful ZIP build.

## 3. ChatGPT Project fallback

The five-file manual Project adapter is an existing fallback design, not an assumption about the current user's subscription or a universal product limit. Choose a route based on actual account/surface access and recheck current official limits during Stage 4 installation acceptance. Native Skills availability does not establish Project parity. The public product has no mandatory primary provider under ADR-046.

The Project route supplies instructions and text references. It does not automatically install a native Skill, grant a shell, synchronize private memory or run repository validators. Report unavailable checks as `NOT RUN`.


## 4. Progressive disclosure

- Level 0: short Project/host instructions and capability metadata.
- Level 1: `skills/peanuts/SKILL.md` after explicit or implicit task match.
- Level 2: only the stage-specific reference modules needed.
- Level 3: only the relevant project records, evidence passages, templates or deterministic tool output.

For ChatGPT Project use, the generated reference files group canonical references by stage. Instructions tell the model which file and method family to consult, while the full portable package retains the original modular files.

## 5. Reproducibility and security

The packager must:

- Copy rather than rewrite method sources.
- Keep host copies byte-identical to the canonical skill source.
- Include all canonical references and assets in the portable skill ZIP.
- Use deterministic ZIP timestamps and sorted entries.
- Reject symlinks, path traversal, absolute paths, unsafe names, duplicates and unexpected files.
- Generate a source-to-package SHA-256 manifest.
- Keep outputs under an ignored build directory and never overwrite the canonical source.
- Include no secrets, private project records, participant data, or unreviewed network-calling scripts.

## 6. Non-goals

B9 does not implement a custom API service, MCP server, plugin, autonomous Friday manager, multi-agent orchestration, database, or remote repository. Those would introduce separate security, credential, deployment, cost and maintenance obligations without demonstrated need. Reconsider only after actual host use reveals a material limitation that the Project fallback and native discovery paths cannot solve.

## 7. Official references checked 2026-11-02

- Agent Skills specification: https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx
- Claude Agent Skills / Claude Code: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- ChatGPT Skills: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- ChatGPT Projects: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- ChatGPT upload limits: https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt
- ChatGPT/Codex build skills: https://learn.chatgpt.com/docs/build-skills

## 8. B10 cross-host acceptance supplement (2026-11-02)

The B10 host adapter validator safely extracts each generated adapter into a disposable Friday repository fixture, checks the exact Codex/Claude Code discovery path and corresponding root guidance file, validates SKILL.md YAML/name alignment and relative links, confirms canonical byte parity, and rejects unexpected executable content or implicit `allowed-tools` grants. The tests are recorded in `docs/acceptance/CROSS_HOST_RUNTIME_ACCEPTANCE.md`. This is a filesystem install simulation only. B10.1 separately builds the claude.ai consumer upload package using lowercase `peanuts/skill.md` per the current Help Center wording, and generates Project instructions/knowledge. These package checks do not prove owner account upload, Skill activation, or Claude Project runtime.


## B10 cross-host acceptance hardening

The current Codex and Claude Code generated adapters are validated by `tools/validate_host_adapters.py`. Claude Chat and its Project companion are built by `tools/build_claude_chat_companion.py` and checked by `tools/validate_claude_chat.py`. The validator safely preflights archives before writing, checks official host discovery paths and root guidance, validates skill metadata and local links, verifies canonical byte parity, and rejects executable helpers and implicit `allowed-tools` grants. Malicious archive tests cover traversal, duplicate/case-colliding paths, symlinks, file/directory conflicts and uncompressed-size/compression limits.

The filesystem installation simulation is deterministic package evidence only. Actual `codex`/`claude` CLI discovery, invocation, model-method fidelity, tool permissions and fresh-session recovery must be tested in each real host.
