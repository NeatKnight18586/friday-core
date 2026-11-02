# B10.1 — Claude Chat Skill and Project Integration Review

**Date:** 2026-11-02  
**Status:** **PASS WITH BOUNDED LIMITATIONS** — generated Claude consumer Skill and Project companions, source parity, metadata, deterministic validation, evaluation records and regression tests pass. Actual iPad account upload, Skill activation, Project setup, fresh-chat handoff recovery and live Claude behavior remain `NOT RUN`.  
**Version:** 0.13.4-rc.1  
**Scope:** Claude ordinary chat (claude.ai / Claude iOS app), custom Peanuts Skill upload package, Friday Project instructions/knowledge in supported TXT format, iPad setup, smoke tests, cross-chat continuity, B10.1 EVAL-135–146, B1–B10 regression boundaries.

This is a four-perspective engineering review, not four independent human reviewers, product certification or proof of model performance. Scores below are qualitative assessments of this local design and implementation.

## 1. Executive verdict

B10.1 adds ordinary Claude Chat as the owner's primary ideation/concept-development environment while keeping ChatGPT as the primary managed engineering/build partner during the iPad-only period. This is recorded in ADR-044 and does not change the canonical methodology or rebuild any earlier milestone.

The implementation separates two Claude product surfaces that must not be conflated:

- **Custom Peanuts Skill:** repeatable task procedures and supporting references, uploaded through Customize → Skills. The consumer ZIP has one top-level `peanuts/` folder and a lowercase `peanuts/skill.md` entry generated from canonical `skills/peanuts/SKILL.md`.
- **Friday — Peanuts Project:** Project instructions plus five curated `.txt` knowledge documents containing Markdown-formatted text for Friday vision/governance, Peanuts operating model, professional methods/evidence, architecture/decisions, and current status/handoff.

Anthropic's current consumer Help Center states that Skills are available on Free/Pro/Max/Ultra/Team/Enterprise when code execution is enabled; the name maximum is 64 characters and description maximum is 200 characters. The canonical description is 191 characters. The current upload instructions also say the skill folder name must match the skill name and show a top-level folder ZIP. The canonical Agent Skills file remains uppercase `SKILL.md` for compatible cross-host consumers; B10.1 generates a lowercase consumer-specific entry without creating a second authored methodology.

Claude Project knowledge is persistent context for Project chats, while the current chat transcript is not a reliable cross-chat source of truth. B10.1 therefore preserves an explicit status handoff and does not rely exclusively on model memory.

## 2. Four professional perspectives

### Council 1 — Product and platform integration

**Assessment: 9.0/10 — Pass**

Strengths:
- Correct product separation: reusable Skill instructions versus persistent Project context.
- Correct consumer package layout: one root `peanuts/` folder, lowercase `skill.md`, matching name and 191-character description.
- Existing uppercase canonical `SKILL.md` and generated Codex/Claude Code adapters remain unchanged.
- Five Project knowledge documents are curated rather than indiscriminately uploading the full repository.
- The owner workflow is explicitly split: Claude Chat ideation; ChatGPT managed engineering/build; Codex/Claude Code optional when a laptop or suitable development host exists.

Limitations:
- The product UI and account entitlements remain owner-specific and are not observed here.
- Current Help Center file naming guidance is product-specific and can change; recheck at upload time.

Recommendation: Keep the generated consumer package separate. Never hand-edit the `skill.md` copy.

### Council 2 — Context engineering and continuity

**Assessment: 8.8/10 — Pass**

Strengths:
- Skill carries reusable method; Project carries durable context; each layer has a clear responsibility.
- Project knowledge files provide cross-chat context without forcing every method into Project instructions.
- Fresh-chat continuity is based on `STATUS_AND_HANDOFF.md`, not assumed chat-history sharing.
- The five-document pack is small enough to upload and inspect from iPad while preserving essential Friday decisions and methods.

Limitations:
- This is a deliberate curation; it does not replicate every project-specific record or the full repository.
- Fresh-chat handoff recovery remains a human-observed acceptance gate.

Recommendation: Update the handoff after each significant ideation or architecture decision and add the current version to Project knowledge.

### Council 3 — Professional methods and user workflow

**Assessment: 8.7/10 — Pass with bounded limitations**

Strengths:
- The Project instructions operationalize PPA: classify the task/decision, select relevant disciplines/methods, check prerequisites, select tools actually available, preserve evidence, and verify/escalate.
- Existing research, NUTS, Four-Council, assumptions, PRD and engineering gates remain unchanged.
- Explicitly distinguishes P1–P10 operational stages from B0–B10 repository construction milestones.
- The iPad-only constraint is reflected in setup and response expectations; local terminal/CLI steps are not falsely assumed.

Limitations:
- Method fidelity in a live Claude session remains untested.
- No independent human calibration, real user discovery, or real-world project pilot was performed in this milestone.

Recommendation: Run the smoke suite on a real project and review outputs rather than adding more frameworks.

### Council 4 — AI assurance, security and quality

**Assessment: 8.9/10 — Pass with bounded limitations**

Strengths:
- Builder checks canonical source parity, file naming, frontmatter and project instruction character budget.
- Validator checks exactly five generated `.txt` Project knowledge documents, local CRC, source parity, twelve evaluation cases and result records.
- Six deterministic B10.1 cases are recorded as passed; six owner/runtime cases remain blocked. The additional deterministic checks cover TXT Project file compatibility, correct interpretation of Claude Project limits, and Skill prerequisites.
- Instructions require tool honesty, prompt-injection resistance, approval boundaries and explicit unrun status.

Limitations:
- Package tests do not exercise Anthropic's uploader or runtime.
- Same-model self-evaluation is not independent adjudication.
- No mobile accessibility/UI usability check was performed.

Recommendation: Require the owner run T1–T8 and repeat T1/T4/T6/T8 in fresh chats; independent review is needed before claiming reliability.

## 3. Deterministic verification evidence

- `python tools/build_claude_chat_companion.py --out <dir>` — passed.
- `python tools/validate_claude_chat.py` — passed.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/test_claude_chat_companion.py` — 12 passed.
- Claude Chat Skill ZIP contains 102 files with `peanuts/skill.md`; all generated support resources match canonical files byte-for-byte.
- Skill description length: 191 characters; current documented consumer maximum: 200.
- Claude Project knowledge ZIP contains exactly five `.txt` documents containing Markdown-formatted text; generated from canonical Friday sources.
- Project instructions are under the 6,000-character maintainability budget.
- EVAL-135–137 and EVAL-141–143: `passed` using deterministic package/context validation.
- EVAL-138–140 and EVAL-144–146: `blocked` pending owner upload/UI/runtime evidence.

## 4. Not run / not claimed

- Actual claude.ai Custom Skill upload, Skill visibility and enablement: **NOT RUN**.
- Actual Claude iPad app skill invocation: **NOT RUN**.
- Actual `Friday — Peanuts` Project settings and five `.txt` knowledge files visibility: **NOT RUN**.
- Fresh Project chat and second-chat handoff recovery: **NOT RUN**.
- Eight smoke prompts T1–T8 and three-run repeats: **NOT RUN**.
- Claude Code and Codex actual runtime remain separate and **NOT RUN**.
- No claim that Claude Chat has local Friday repository or terminal access.
- No independent human adjudication or field research.

## 5. Release disposition and next action

**Disposition:** B10.1 managed build accepted with bounded limitations; Claude Chat route is `READY_FOR_OWNER_TEST`, not verified.

Owner next action: install `peanuts-claude-chat-skill.zip`, create the `Friday — Peanuts` Project with the five `.txt` knowledge documents containing Markdown-formatted text and instructions, run T1–T8, then save a handoff and test a second fresh chat. Record observed results in `adapters/claude-chat/RUN_RECORD_TEMPLATE.md`.

Do not change the canonical method or mark Claude Chat verified merely because the package uploaded. A runtime pass requires observed activation and behavioral evidence.
