# B10 Status and Handoff

**Project:** Friday / Peanuts  
**Version:** 0.13.2-rc.1  
**Date:** 2026-11-02  
**Milestone:** B10 — ChatGPT-primary acceptance and release candidate

## Goal

Complete and validate Peanuts/Friday with ChatGPT Projects as the primary owner-facing environment, while preserving a provider-neutral canonical skill and optional generated host adapters.

## Completed in this B10 build

- Recovered the B9 release archive and review; continued without rebuilding B0–B9.
- Verified current official ChatGPT Project and upload constraints.
- Reconciled architecture records and build plans to make ChatGPT primary and Claude/Codex optional.
- Added the ChatGPT Primary Runtime Acceptance protocol and rubric.
- Added EVAL-103–122 and RUN-001–020 (20 records: 16 passed, 1 partial, 3 blocked; all unapproved).
- Executed a live ChatGPT runtime demonstration using the synthetic Campus Service Access Challenge; preserved the output and limitations.
- Performed one exploratory same-input comparison of generic critique and Four-Council; no general improvement claim is made.
- Added B10 deterministic validation and pytest coverage; integrated it into the consolidated verifier.
- Added a Codex/Claude Code host installation simulation, current host-path/command checks, full relative-reference/source-parity checks, no-auto-permission/package-security checks, and actual host runtime smoke-test instructions.
- Added EVAL-123–134 and RUN-021–032: four deterministic package/install checks plus three malicious-archive security checks passed; five actual Codex/Claude Code/claude.ai runtime/UI cases remain blocked.
- Managed regression passed: 171/171 tests across six bounded module runs (11 initializer + 7 B5 + 6 B6 + 18 B7 + 54 B8 + 75 B9/B10/configuration/release and host-security tests).
- Individual B2/B4/B5/B6/B7/B8/B9/B10 and host-adapter validators, repository integrity, capability registry and context-budget checks passed.

## Evidence

- `docs/acceptance/CHATGPT_PRIMARY_RUNTIME_ACCEPTANCE.md`
- `docs/acceptance/CHATGPT_RUNTIME_DEMO.md`
- `evals/cases/EVAL-103.json` through `EVAL-122.json`
- `evals/results/results.jsonl`
- `evals/rubrics/CHATGPT_PRIMARY_RUNTIME.md`

## Accepted decisions

- ChatGPT Projects are the primary owner-facing environment for the current iPad workflow (ADR-015 in `docs/DECISIONS.md`; ADR-043 in `docs/architecture/DECISIONS.md`).
- `skills/peanuts/` remains the single canonical portable source.
- The manual five-file Project adapter is the current route; native ChatGPT Skills are conditional, not required.
- Claude Code and Codex remain optional generated adapters, now with tested filesystem installation simulations and explicit actual-host runtime gates.
- Friday remains an umbrella, not an autonomous manager.

## Open gates / limitations

- **NOT RUN:** actual user Project UI installation check and fresh Project chat (EVAL-117). The assistant cannot inspect the owner's iPad Project settings/source list here.
- **BLOCKED:** repeated independent fresh-Project runs and human-labelled calibration (EVAL-118).
- **NOT RUN:** Ruff, GitHub Actions, Codespaces, native Skills, actual Claude Code/Codex CLI sessions, and claude.ai custom-Skill upload/runtime.
- **PASS (targeted):** `python tools/validate_b2.py` completed with 8 schemas, 134 evaluation cases and temporary-workspace lifecycle checks. The consolidated `python tools/verify.py --skip-lint` still timed out when it reached B2 after repository integrity; this runner interaction is separately unresolved and is not represented as a full consolidated pass.
- The current live run is one ChatGPT conversation and is self-evaluated by the same model family; no claim of independent expert review or statistical reliability.

## Exact next action

After the owner installs the B10 `PROJECT_INSTRUCTIONS.md` and five `.txt` references in the actual `Friday — Peanuts` Project, run the B10 smoke prompt in a new Project chat. For optional PC use, install the Codex or Claude Code adapter as described in `docs/acceptance/CROSS_HOST_RUNTIME_ACCEPTANCE.md` and record actual host discovery/invocation separately. Save a concise status/handoff as a Project source, then open a second fresh Project chat and verify state recovery. Record the actual date, visible plan/surface, five sources, verbatim answer excerpt and disposition in `docs/acceptance/CHATGPT_PROJECT_UI_RUN_RECORD.md`.


## B10.1 update — Claude Chat integration (2026-11-02)

- Owner-selected role split: ordinary Claude Chat is the primary ideation/concept-development environment; ChatGPT remains the primary managed engineering/build partner while the owner is iPad-only. This is recorded in ADR-044.
- Added a dedicated consumer Skill package with lowercase `peanuts/skill.md` while preserving the canonical `skills/peanuts/SKILL.md` for portable/Codex/Claude Code use. The canonical description is 191 characters and meets Anthropic's current documented 200-character consumer limit.
- Added a separate five-document Claude Project knowledge pack, Project instructions, iPad setup, smoke prompts and owner run-record template.
- Added EVAL-135–140 and RUN-033–038. First three deterministic package/context checks pass; owner-side upload, Project creation/fresh-chat continuity and live tool-boundary cases remain blocked.
- Actual Claude iPad account upload/enablement and Project UI acceptance are pending; no laptop or Claude Code is required for the ordinary chat route.

**Next owner action:** install the Claude Skill and create the Friday Project using `docs/acceptance/CLAUDE_CHAT_PROJECT_ACCEPTANCE.md`; capture actual UI and fresh-chat results. Continue repository authoring/testing in ChatGPT's managed build environment.
