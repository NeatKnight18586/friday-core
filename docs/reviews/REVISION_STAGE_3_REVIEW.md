# Stage 3 — Selective Peanuts context and portable planning

**Version:** 0.16.0-rc.1. **Scope:** smaller compulsory context, Fast compatibility, coherent dossier and compact handoff. **Authority:** owner-approved Stage 3 and ADR-052/053.

## Delivered

- Reduced canonical SKILL.md from 1,949 to 831 whitespace-delimited words (14,955 to 6,581 characters). It now routes by the current decision rather than repeating each method. Governing references, full records and critical approval/evidence gates remain available and mandatory for their formal workflow. Root host maps make engineering references conditional; the Claude Code map was also condensed.
- Added Fast as a user/CLI alias for stored quick. Standard/Deep and existing registry/record IDs remain unchanged; no migration is needed.
- Added `--layout compact` to the existing initializer: only PROJECT_DOSSIER.md and handoff.json, under the ignored private workspace. Default full initialization is preserved. Early questions may still stay in one response without any files.
- Added a portable planning contract and read-only integrity/recovery helper. It checks safe paths, dossier hash/sections, schema, source/claim references, inspected versus synthetic labels, approval evidence and critical blockers. It reports missing next-step tools instead of executing anything. Chat-only exports leave an unavailable digest null and report NOT RUN; they cannot pass deterministic integrity checks until reviewed/fingerprinted.
- Kept a single narrative dossier: link existing PRD/design/full records rather than duplicating them. Compact exports are planning-context-only and cannot assert completed formal P7–P9 stages or grant tool/action authority.
- Added authored synthetic Fast/Standard/Deep examples and 31 new regression cases. ChatGPT retains exactly five Project reference files, now including the handoff schema/templates; Claude Skill/Project resources are generated from the same sources.

## Evidence and limits

The complete local Stage 3 verifier passed 258 tests, 15 validators and Ruff. Examples and tests cover Fast/quick equivalence, compact no-overwrite/no-partial-write initialization, missing-tool fallback, deep critical blockers, corrupt hashes/IDs/paths/labels/approvals, symlinks, duplicate JSON, null digest and safe read-only continuation.

A fresh Python process in an empty working directory reconstructs context from only the exported dossier/handoff, preserving assumptions, proposed decisions and NOT RUN checks without old chat or ledgers. This is deterministic fresh-process continuity, not an actual model's fresh-chat success. The injection fixture demonstrates no code execution by the helper, not that all models resist prompt injection. Schema/digest checks cannot prove factual truth or authenticate an asserted approval.

Word/character changes are static measurements. No measured provider token/credit saving, quality improvement, user validation, NUTS advantage or consumer-host success is claimed. Stage 4 remains responsible for comparative behavioral cases and actual host/account acceptance. Historical hosted CI for Stage 2 passed all 12 OS/Python jobs; Stage 3 hosted results are commit-specific in Actions.

## Stage 4 handoff

Use representative event, problem, idea and existing-project tasks; include unavailable browsing, conflicting rules, false analogies, high-risk data, partial approval and stale handoffs. Compare simpler prompted chat, Peanuts without NUTS, full Peanuts and simple critique versus Four-Council on matched cases. Save actual outputs/trajectories, host/model/date/mode/tool availability, critical errors, recovery and real usage when exposed. Separate structural checks from model/user usefulness. Reuse the three synthetic examples as contract fixtures, not as outcome evidence. Do not add infrastructure or broad memory/agents merely to run a pilot.
