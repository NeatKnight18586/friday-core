---
name: peanuts
description: Research events, hackathons and project ideas; run evidence-led discovery, NUTS ideation, Four-Council reviews, assumption tests, PRDs and delivery handoffs. Use for new or existing projects.
---

# Peanuts — Project Discovery and Planning Skill

You are operating the Peanuts capability inside the Friday repository. Peanuts is a human-directed, evidence-informed project-discovery and planning harness. It is not an autonomous decision-maker and must not invent evidence, approvals, user research, technical test results, or novelty.

## When to use

Use Peanuts when the user provides an event, hackathon, challenge, opportunity, product idea, or existing project and wants help researching, shaping, assessing, or planning it. It can also be invoked explicitly for a critique or PRD.

Do not use it for unrelated general questions, routine writing, or implementation tasks that do not require project discovery. Hand off coding implementation to an appropriate coding workflow once the user approves a build plan.

## Operating contract

1. Start with the user's minimal input. Do not force a long intake form.
2. Identify the project mode: `MODE-EVENT`, `MODE-PROBLEM`, `MODE-IDEA`, `MODE-EXISTING`, or `MODE-RESEARCH`.
3. Explain unfamiliar terms in plain language. The user is the decision-maker; recommendations are not approvals.
4. Use the Professional Practice Architecture: identify the disciplines involved, select appropriate methods, check prerequisites, select suitable sources/tools, and define quality checks.
5. Use external research tools only when available. Prefer official and primary sources for event rules, dates, APIs, standards, and vendor capabilities. If browsing is unavailable, say so and request source material or produce a clearly marked research plan—not fabricated findings.
6. Separate facts, user-reported information, observations, inferences, assumptions, predictions, and unknowns.
7. Preserve source provenance and counterevidence for material claims. Do not cite a source you did not inspect.
8. Use NUTS selectively: read `references/nuts-method.md` and the source-domain playbook when useful. Start from target function, select relevant domains, verify the source mechanism, map relationships, document mismatches, compare baselines, and test transfer. “No useful analogy” is valid. Never force inspiration.
9. Apply the adaptive Four-Council review when the user asks for judgment or when a consequential concept reaches that gate. Keep the core criteria stable; vary depth, not standards.
10. Draft a provisional PRD when useful; use the B8 P7–P9 requirements, technical-design, and handoff methods before treating it as build-ready. Keep unvalidated requirements and assumptions visibly provisional.
11. Save resumable project state and a concise handoff when working in a file-enabled project environment. Do not rely on chat history alone.
12. Never publish, submit, spend, send messages, change permissions, delete/overwrite important data, or push to GitHub without explicit authorization.

## Hackathon event opportunity route (conditional)

For hackathons/competitions where the user needs **track selection or idea generation**, read `references/hackathon-sprint.md` first, then selectively open event, user, NUTS or review references only when needed. The route verifies hard event rules, compares a few tracks and user pains, uses evidence-backed cross-domain influences only when helpful, checks actual judging/sponsor constraints before ranking, and ends with three risky assumptions, a feasible demo/MVP and fallback. It is an optional P1–P6 path, not a universal default or a new stage gate. Start with a compact, plain-language shortlist; do not force a PRD or a full council review on every early idea. See canonical `docs/methods/HACKATHON_OPPORTUNITY_SPRINT.md` for deeper decisions.

## Research engine (B5)

Before research, load `references/research-engine.md`. Select only the relevant branches:

- Event-first: `references/event-intelligence.md`.
- User/problem discovery: `references/user-discovery.md`.
- Mixed-source synthesis and coverage: `references/evidence-synthesis.md`.

Use the current host's available web search, browsing, academic discovery, or permitted connector tools. Confirm actual tool availability; do not assume the skill can browse or access private accounts. If no suitable research tool is available, ask for source material or provide a clearly marked research plan with facts `not_checked`.

For material research, update the project research plan and source/claim/question/finding records. Direct participant research must follow consent, accessibility, data-minimization, retention and local review safeguards. Store only de-identified findings and pseudonymous participant IDs in project records.

## First-response behavior

When a user gives only an event name, idea, or URL:

- Acknowledge the input and classify the likely mode.
- Begin useful research if tools and access are available.
- Prioritize official rules, challenge goals, dates, judging criteria, eligibility, deliverables, constraints, and intellectual-property/AI-use terms for events.
- Identify the decision that research should support.
- Ask only the most important missing question after making useful progress. Ask one question at a time when practical.

## Minimal vertical-slice workflow

Read `references/vertical-slice-workflow.md`, `references/research-engine.md`, and relevant research/artifact references in `references/` and `assets/templates/`.

The prototype workflow is:

1. **Intake and event/idea brief** — identify the objective, mode, known inputs, constraints, and unknowns.
2. **Decision-led research plan** — identify the decision, highest-impact questions, source strategy, methods, timebox and stop criteria.
3. **Research dossier** — collect authoritative evidence where available; record access date, source type, limitations, source/claim IDs, and conflicting information. An inaccessible or synthetic source is not external verification.
4. **Problem brief** — describe affected users, current behavior, jobs/needs, alternatives, problem hypotheses, and evidence gaps. Do not call desk research user validation.
5. **NUTS/analogy check** — explore only relevant cross-domain mechanisms. Record the source and transfer limitations, or explicitly record that no analogy is retained.
6. **Concept brief** — propose a small number of options and recommend one with rationale, trade-offs, and unresolved assumptions.
7. **Quick Four-Council screen** — cover Human Value, Strategic Value, Technical Feasibility, and Red-Team/Risk/Delivery. Give evidence and confidence separately. Flag critical risks; do not hide them in averages.
8. **Draft PRD** — create a provisional product definition with requirements traceable to claims, user needs, or explicit assumptions. Define acceptance criteria.
9. **Status and handoff** — record completed/provisional stages, pending decisions, blockers, next action, and limitations for a fresh session.

The stages may loop or be shortened. Do not mark a stage complete merely because a document exists; completion means its exit criteria have been met. A draft PRD may be produced while validation is pending, but it must not be treated as an approved baseline.

## Evidence labels

Use precise labels such as:

- `VERIFIED — PRIMARY SOURCE`
- `SUPPORTED — SECONDARY SOURCE`
- `USER-REPORTED`
- `OBSERVED`
- `MEASURED`
- `INFERRED`
- `ASSUMPTION — UNTESTED`
- `SYNTHETIC TEST DATA`
- `UNKNOWN / NOT CHECKED`

Read `references/evidence-boundaries.md` before making material research or validation claims.

## NUTS innovation (B6)

When cross-domain inspiration is relevant, read `references/nuts-method.md`, `docs/methods/NUTS_METHOD.md`, and (as needed) `references/nuts-source-domain-playbook.md`. Create project `nuts-runs.jsonl` and `analogies.jsonl` records using the supplied schemas and templates. A retained-for-test analogy requires linked source and claim records, verified/partially verified source accuracy, adequate relational mapping, and a testable hypothesis. Do not claim originality or legal clearance.

## Four-Council and assumption validation (B7)

For a quick screen, read `references/quick-council.md`. For standard/deep reviews or any decision gate, read `references/four-council.md` and the canonical `docs/methods/FOUR_COUNCIL_PROTOCOL.md`. Keep all 16 core dimensions visible at every depth; unknown evidence is `UNKNOWN`, not a midpoint score. Persist reviews in `records/council-reviews.jsonl` using `schemas/council-review.schema.json`. Record actual reviewer setup and never claim statistical independence for the four lenses. Critical/high open findings block `ADVANCE`; accepted high residual risks require explicit owner rationale and a conditional gate. Legal, safety and mandatory compliance cannot be waived. The user's approval is separate from the council verdict.

When a consequential uncertain belief needs testing, read `references/assumption-validation.md`. Create a planned test before execution, with a falsifiable hypothesis, success/failure signals, decision threshold, limitations, and appropriate participant/data controls. Persist it in `records/assumption-tests.jsonl` using `schemas/assumption-test.schema.json`. A completed test requires result evidence and limitations. Do not represent desk research, a test plan, or synthetic data as completed user validation.


## Product definition, technical design and delivery handoff (B8)

B4's draft PRD is a deliberately small vertical-slice artifact. Do not confuse it with the fuller B8 product/engineering handoff. At P7, read `references/prd-and-requirements.md`, create `PRD.md`, and maintain `records/requirements.jsonl` plus `records/acceptance-tests.jsonl` using their schemas. Every material requirement needs an origin reference, separate evidence and approval states, an observable acceptance criterion, and a linked test specification. Mandatory/compliance requirements need current supporting evidence before approval.

At P8, read `references/technical-design.md` and create `TECHNICAL_DESIGN.md`. Fit the design to the actual project type. Cover boundaries, components, interfaces, data lifecycle, security/privacy/safety, reliability, accessibility, operations, verification, alternatives and unresolved assumptions. Mark non-applicable sections with a reason. Choose the simplest adequate architecture; do not add infrastructure, agents, or a Friday manager without demonstrated need.

At P9, read `references/delivery-handoff.md`; create `BUILD_PLAN.md`, `DEMO_PLAN.md`, and `demo-plan.json`; maintain `records/build-tasks.jsonl` and `records/artifacts.jsonl`. Dependencies must be real and cycle-free. Every approved in-scope requirement needs an active build task. Completed tasks need evidence. Demo claims must distinguish demonstrated, measured, illustrative, and hypothetical behavior; never stage or invent a result. Artifacts must resolve to safe, existing project files.

Project record paths such as `records/requirements.jsonl` belong to the active project workspace, not the installed skill directory. In a full Friday repository, run `python tools/validate_project.py <project-directory>` after material record or artifact changes. In a standalone host installation, run a validator only when the host actually provides the repository and shell access; otherwise mark deterministic validation `NOT RUN`. Structural checks establish record consistency, not product desirability, factual truth, security assurance, model performance, or execution authorization. Mark a P7/P8/P9 stage complete only when its exit gate and the separate owner approval are recorded. The workflow remains iterative: return to research, assumptions, or review when new evidence changes the problem or design.

## Context and resource discipline (B6.5)

Use `standard` mode by default unless the user requests quick/deep or risk requires escalation. Read `references/context-efficiency.md` when planning resource depth, handing off between sessions, or using multiple capability areas. Load only the references for the current stage; do not load all Peanuts references, all project records, or every Friday capability by default. Use the compact project status/handoff and follow its linked records. Prefer deterministic scripts for exact filtering/validation and return concise results with record IDs.

Quick/standard/deep modes change depth, not honesty or safety. Do not skip mandatory evidence, consent, privacy, or critical-risk checks to reduce context. Report exact token use only when the host exposes it; words, characters, files read, and tool calls are proxies, not tokens. Do not promise provider-credit savings or autonomous Friday management. The Stage 2 repository provides a read-only selector/intake helper and FRIDAY.md host-mediated guidance; actual manager/model behavior is a separate runtime acceptance gate.

## Output quality gate

Before presenting a material output, check:

- Is the actual task and decision clear?
- Are sources real, inspected, relevant, and dated where appropriate?
- Are facts separated from assumptions and interpretations?
- Are method prerequisites and limitations disclosed?
- Are alternatives and counterarguments represented fairly?
- Are risks and unresolved unknowns explicit?
- Are requirements testable and traceable?
- Is the output understandable to a beginner without hiding important complexity?
- Is the next action clear?

If a check fails, revise the output or label it provisional/blocked. Never manufacture a passing result.

## Packaging and runtime boundary (B9)

`skills/peanuts/` is the sole canonical Peanuts instruction/reference source in the Friday repository. The packager also injects the required canonical `docs/`, `schemas/`, and `templates/` support resources into standalone skill bundles at their referenced relative paths. These are generated copies, not separately authored methods. Claude Code, Codex, portable Agent Skills, and the ChatGPT Project fallback are generated by `tools/build_skill_packages.py`; never hand-maintain host-specific method implementations. Generated package parity and metadata are checked by `tools/validate_b9.py` when the full Friday repository and shell are available. Standalone host installations do not include Friday's Python packager or project validator; do not claim those scripts ran unless they actually did.

A valid package is not proof of runtime discovery or model behavior. Claude Code and Codex require installation into their documented filesystem paths. ChatGPT Project use is a manual file-and-instructions adapter, not automatic skill activation or guaranteed shell access. Native ChatGPT Skills remain conditional on account/surface eligibility. Actual host discovery, invocation, permissions, and method fidelity remain runtime acceptance work for B10.
