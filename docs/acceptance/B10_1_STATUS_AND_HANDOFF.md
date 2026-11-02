# B10.1 Status and Handoff

**Project:** Friday / Peanuts  
**Version:** 0.13.4-rc.1  
**Date:** 2026-11-02  
**Milestone:** B10.1 — Claude Chat and Project integration

## Owner-selected environment split

- **Claude ordinary chat:** primary ideation, exploration, concept development, critique and research planning.
- **ChatGPT:** primary managed repository engineering, file authoring, deterministic testing, packaging and release work while owner is iPad-only.
- **Codex / Claude Code:** optional filesystem/CLI workflows when a laptop or appropriate development host is available.

The roles are not separate Peanuts implementations. One canonical `skills/peanuts/` source remains authoritative.

## Completed in B10.1

- Verified current Anthropic Skills and Projects documentation.
- Added Claude consumer Skill archive using `peanuts/skill.md` (lowercase) with the same canonical source content and 191-character description.
- Preserved uppercase canonical `SKILL.md` for portable/Codex/Claude Code routes.
- Added Friday Project instructions and five generated `.txt` knowledge documents containing Markdown-formatted text.
- Added iPad setup guide, smoke tests and owner run record.
- Added ADR-044 (workflow split) and ADR-045 (documented TXT Project export format); updated capability registry/host architecture.
- Added EVAL-135–146 and RUN-033–044; six deterministic checks passed, six owner/runtime checks remain blocked. All records remain unapproved pending owner review.
- Added a standalone builder, validator and twelve tests.

## Verification evidence

- `python tools/build_claude_chat_companion.py --out <dir>` — PASS.
- `python tools/validate_claude_chat.py` — PASS.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/test_claude_chat_companion.py` — 12 passed after TXT Project export hardening.
- Claude Skill ZIP: 102 files, correct folder and lowercase entrypoint, source-byte parity.
- Claude Project knowledge ZIP: exactly five `.txt` files containing Markdown-formatted text generated from canonical sources, including the B10.1 status/acceptance handoff.
- All actual Claude UI/runtime results remain unrun pending owner iPad actions. The five `.txt` documents are a curated pack, not a per-Project file limit; Anthropic documents unlimited Project files subject to context window, with Free users limited to five Projects.

## Owner next action

Use `docs/acceptance/CLAUDE_CHAT_PROJECT_ACCEPTANCE.md` and `adapters/claude-chat/SETUP_IPAD.md` to install the Skill, create the Friday Project, add instructions and five `.txt` knowledge documents containing Markdown-formatted text, run T1–T8, and test a second fresh chat from the saved handoff.

## Guardrails

- Do not rewrite accepted B0–B10 methods.
- Do not treat Skill upload as model-method acceptance.
- Do not assume normal Claude chat has local repository or terminal access.
- Project knowledge is durable background; save updated handoffs after substantive work.
- Keep all external actions and release decisions under owner approval.
