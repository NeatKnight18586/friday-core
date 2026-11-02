# Peanuts Project Records and State Model

**Status:** B2–B7 record model and validators delivered locally; real research/runtime use remains unverified
**Document version:** `1.2.0-draft`; each JSON Schema has its own `schema_version` where applicable
**Last updated:** 2026-11-01

## 1. Purpose

This document defines the minimum persistent record set needed to create, inspect, pause, resume, and evaluate a Peanuts project without relying on chat history as the only source of truth.

The model is deliberately file-centered. It uses JSON for one current project record and state snapshot, JSONL for append-oriented evidence/decision records, Markdown for human-readable project summaries, and versioned JSON Schemas for structural validation.

This is not a database, memory service, or complete project-management application.

## 2. Data-location and privacy rule

Project working data is created by default under `local-workspace/projects/`, which is excluded from Git. This protects user-specific research, participant notes, and unfinished project material from accidental publication.

The repository contains only generic templates, schemas, synthetic evaluation cases, and non-sensitive documentation. A project owner must separately review any decision to commit sanitized project artifacts.

Do not put credentials, personal-memory exports, identifiable participant records, confidential documents, or raw interview recordings in project JSON/Markdown/JSONL files. Store sensitive material in an appropriately protected location and link to it only when permitted.

## 3. Canonical project layout

```text
local-workspace/
  projects/
    <project-id>/
      project.json
      state.json
      PROJECT_BRIEF.md
      STATUS_AND_HANDOFF.md
      records/
        sources.jsonl
        claims.jsonl
        assumptions.jsonl
        decisions.jsonl
        research-questions.jsonl
        research-rounds.jsonl
        research-findings.jsonl
        opportunities.jsonl
        analogies.jsonl
        nuts-runs.jsonl
        assumption-tests.jsonl
        council-reviews.jsonl
      research-plan.json
      artifacts/
        README.md
      evaluations/
        results.jsonl
```

Not every project needs every downstream artifact. The starter record files are empty JSONL files; append records only when relevant.

## 4. Record responsibilities

| Record | Canonical responsibility | Update behavior |
|---|---|---|
| `project.json` | Identity, entry mode, intended outcome, constraints and sensitivity classification | Update current metadata; preserve important changes in decisions when consequential |
| `state.json` | Current lifecycle/workflow stage, blockers, pending decisions and next action | Replace as a current-state snapshot after a meaningful transition |
| `PROJECT_BRIEF.md` | Human-readable summary and current framing | Revise as the project understanding changes; retain version history through local Git/backup where used |
| `STATUS_AND_HANDOFF.md` | Fresh-session continuation summary | Replace at handoff; identify the source records it summarizes |
| `sources.jsonl` | Source metadata, provenance, access and limitations | Append; do not silently rewrite a historical source assessment |
| `claims.jsonl` | Material factual, reported, observed, measured, interpretive or predictive claims | Append; correct through a new record or explicit supersession |
| `assumptions.jsonl` | Unverified propositions that could affect decisions | Append/update status with test and outcome; preserve prior reasoning in project history |
| `decisions.jsonl` | Proposed, approved, rejected, deferred and superseded decisions | Append new decisions; supersede rather than erase material decisions |
| `research-plan.json` | Current decision-led research plan, priorities, methods, scope, timebox and stop criteria | Update the current plan; preserve material plan changes in decisions/notes |
| `research-questions.jsonl` | Stable research questions, methods, status and answer-claim links | Append or supersede; keep questions decision-linked |
| `research-rounds.jsonl` | Planned/conducted user or field research rounds, pseudonymous participant references, participant safeguards and consent status | Append rounds; completed rounds require resolved consent and local review disposition; store no identity mapping here |
| `research-findings.jsonl` | Findings from sources, user statements, observations, measurements or synthesis | Append; participant-derived records require a research-round link, a pseudonymous participant reference listed in that round, and confirmed consent |
| `analogies.jsonl` | Sourced NUTS analogy cards with relationship mappings, transfer mismatches, tests, attribution, and source/claim links | Append; retained-for-test cards require source and claim provenance plus adequate method checks |
| `nuts-runs.jsonl` | NUTS run coverage, domains searched, methods applied, conclusion, and next action | Append; `no_useful_analogy` is a valid documented result |
| `assumption-tests.jsonl` | Pre-registered tests linked to assumptions, with method, thresholds, participant safeguards, outcomes, evidence and limitations | Plan before execution; completed tests require outcomes and traceable evidence; human-participant safeguards must be satisfied before approval/execution |
| `council-reviews.jsonl` | Versioned Four-Council reviews, all 16 core dimensions, reviewer setup, event overlay, severity-ranked findings and progression gate | Append review versions; preserve reviewer limitations; critical/high open findings block ADVANCE; user approval is recorded separately |
| `opportunities.jsonl` | Solution-neutral user opportunities linked to findings, claims and unresolved questions | Append/update maturity; preserve counterevidence and context |
| `evaluations/results.jsonl` | Actual evaluation runs and results | Append; never fabricate or pre-fill a passing result |

## 5. Stable identifiers

Use identifiers only where they aid traceability. Recommended prefixes:

- `SRC-0001` — source
- `CLM-0001` — claim
- `ASM-0001` — assumption
- `DEC-0001` — decision
- `EVAL-0001` — evaluation case
- `RUN-0001` — evaluation result/run
- `REQ-0001` — requirement (introduced in the PRD stage)
- `ANL-0001` — analogy card
- `NUTS-0001` — NUTS run
- `TST-0001` — assumption test
- `REV-0001` — Four-Council review
- `CRF-0001` — council review finding

IDs are project-scoped except evaluation-case IDs, which may be shared in the repository test library. Never reuse an ID after rejection or supersession.

## 6. Provenance and evidence chain

For important decisions, preserve a chain where useful:

`Source / Observation → Claim / User Need → Opportunity → Concept Hypothesis → Decision → Requirement → Acceptance Criterion → Test Result`

Not every early-stage idea needs every link. If evidence is missing, mark the uncertainty instead of inventing a link. A user's statement can be recorded as user input without treating it as an independently verified external fact.

## 7. Project lifecycle and workflow state

Lifecycle status describes the project's overall condition:

- `draft`
- `active`
- `paused`
- `blocked`
- `completed`
- `archived`

Workflow stage uses `P1`–`P10` from the Peanuts workflow. Stage status is:

- `not_started`
- `in_progress`
- `awaiting_user`
- `blocked`
- `completed`

Projects may revisit earlier stages. Do not enforce a strictly linear stage progression. A state snapshot must identify completed stages, current stage, blockers, pending decisions, a concrete next action, and a concise handoff summary.

A project is resumable only when a fresh session can answer: What is this project? What was done? What decisions are approved? What remains uncertain or blocked? What is the next useful action?

## 8. JSON and JSONL conventions

- `project.json` and `state.json` contain one JSON object each.
- Each non-empty line in a `.jsonl` file is one independent JSON object validated against the corresponding schema.
- UTF-8, one JSON object per line, no trailing commas, and no comments in JSON.
- Dates use ISO 8601 (`YYYY-MM-DD` or timezone-aware date-time as specified by the schema).
- Use `null` for genuinely unknown optional values; do not invent placeholder facts.
- A JSONL record is append-oriented. If a past statement must be corrected, preserve the correction/supersession relationship rather than silently erasing its history.

## 9. Validation and integrity

`tools/validate_project.py` validates the JSON records against Draft 2020-12 JSON Schemas, checks duplicate record IDs, verifies cross-record references, and checks basic state invariants. It does not validate factual truth, source credibility, user demand, or whether a decision is wise.

`tools/init_project.py` creates a new workspace from the generic templates (including B6 analogy/run and B7 assumption-test/council-review ledgers) and refuses to overwrite an existing project directory. Older workspaces without optional B6/B7 ledgers remain readable: the validator treats absent ledgers as empty and emits a warning; it does not silently modify or migrate user data. B7 semantic checks also enforce review provenance, assumption-test links, and non-compensatory decision-gate invariants.

Install the development dependency with `python -m pip install -r requirements-dev.txt` before using schema-based validation.

## 10. Schema evolution

Schemas use an explicit `schema_version`. A future incompatible change requires:

1. A documented reason and decision record.
2. A new schema version.
3. A migration or explicit manual conversion procedure.
4. Tests using old and new example records.
5. A backup before modifying real project data.

Do not silently reinterpret older records using a new schema.

## 11. B2 acceptance boundary

B2 supplies templates, schemas, a safe local project initializer, validators, and initial synthetic evaluation cases. It does not supply a production memory service, database, autonomous resume engine, real project research, or evidence that Peanuts improves project outcomes. B4 must prove a fresh-session handoff with a small synthetic vertical slice; B3 first establishes the reproducible test environment.


## 12. B7 review and validation boundary

B7 introduces `council-reviews.jsonl` and `assumption-tests.jsonl`. Council reviews preserve every core dimension even in quick mode; unknowns remain explicit, and event alignment is separate from product-merit scores. Four simulated lenses do not establish statistical independence. `ADVANCE` is prohibited while critical/high findings remain open. Accepted high residual risks require a conditional gate; critical and mandatory safety/legal/compliance issues cannot be waived through an accepted-risk field.

Assumption tests are designed before execution. Human interviews, observation and usability tests require appropriate consent and data controls before approval or execution. Completed tests require an outcome, traceable evidence, limitations, and completion date. These records support traceability; they do not prove the truth or generalizability of the results.
