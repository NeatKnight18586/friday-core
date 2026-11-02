# Friday / Peanuts Build Roadmap

**Status:** B0–B10 delivered locally; B10.1 Claude Chat/Project companion and TXT-compatible Project knowledge exports completed; owner-side Claude/ChatGPT Project UI, actual host runtime, remote CI/Codespaces and independent calibration remain pending  
**Version:** 0.14.1-rc.1  
**Last updated:** 2026-11-02

The current revision sequence is [REVISION_STAGES.md](REVISION_STAGES.md), governed by ADR-046–048. B0–B10.1 below record construction history; their former host priorities and optional-manager direction do not override the current public, provider-neutral manager destination. Historical runtime records remain evidence only for their original scope/version.

## 1. Build objective

Build Friday as a public, provider-neutral capability manager, with Peanuts as its first portable project-discovery and planning harness. Stage 1 repairs the baseline; Stage 2 plans a minimal explicit selector. Use generated adapters and test each claimed host route separately.

The owner currently works from an iPad and relies on the available managed engineering environment to author, inspect, test and package Friday. This build arrangement does not select a required public runtime. The owner should not need a laptop or local development environment during construction. A supported host/runtime test is still required later; assistant-side Linux tests alone cannot prove that Claude Code, Codex, or a native ChatGPT Skill works in the target account/device.

## 2. Numbering

- `B0–B10` identifies Friday construction milestones.
- `P1–P10` identifies the Peanuts workflow used on a project.
- `V0–V5` identifies validation levels in `CHATGPT_IPAD_FIRST_BUILD_AND_RELEASE_PLAN.md`.

Do not mix these identifiers.

## 2A. B10/B10.1 owner-facing environment decisions (2026-11-02)

The current product has no mandatory primary provider. Choose among actual host/account capabilities and keep one canonical core. ChatGPT-managed engineering is the owner's available build workflow in this session, not a public runtime requirement. Consumer Project UI, CLI invocation, source verification and remote CI remain separate acceptance surfaces.

B10/B10.1 established historical ChatGPT/Claude routes and acceptance cases. Preserve those records without treating one surface's result as another's pass. Stage 4 will recheck host requirements and record actual behavior. See `docs/acceptance/CROSS_HOST_RUNTIME_ACCEPTANCE.md`.

## 3. Completed milestones

| Milestone | Status | Evidence and limitations |
|---|---|---|
| B0 — Constitution and architecture | Drafted, refined, and reviewed | Owner-directed foundation exists. Methods remain experimental until evaluated against actual tasks. |
| B1 — Repository foundation | Delivered locally | Root guidance, Git hygiene, docs, local repository scaffold, and privacy defaults. No remote GitHub repository exists. |
| B2 — Project records and evaluation foundation | Delivered locally | Project/state, source, claim, assumption, decision, and evaluation schemas; templates; safe initializer; validator; initial synthetic cases and rubrics. No Peanuts model performance is demonstrated. |
| B3 — Reproducible development and CI foundation | Delivered locally; remote execution pending | Exact-version development dependencies, Python tooling, tests, manifest, verifier, SHA-pinned GitHub Actions matrix, Dependabot, and Dev Container. Ruff was not executed in the managed environment; GitHub-hosted CI and Codespaces have not run. |
| B4 — Structural end-to-end vertical slice | Delivered locally; model runtime pending | Canonical skill prototype, stage contracts, synthetic example, validator, and regression tests. Structural handoff is tested; live Claude/Codex/ChatGPT execution is not. |
| B5 — Research and product discovery | Delivered locally; research/runtime quality pending | Event/user research playbooks, decision-led plan, source/claim/question/round/finding/opportunity records, schemas, consent/local-review safeguards, synthesis guidance, templates, rubrics, and EVAL-020–030. Structural checks do not prove factual accuracy, research quality, user validation, or model behavior. |
| B6 — NUTS cross-domain innovation | Delivered locally; model-method quality pending | NUTS method and source-domain playbook, analogy-card and NUTS-run schemas/ledgers, source/claim traceability, synthetic template records, analogy-quality rubric, EVAL-031–038, project validator integration, and regression tests. Structural checks do not prove analogy accuracy, transfer feasibility, originality, or model performance. |
| B6.5 — Context efficiency and capability-growth architecture | Delivered locally; host behavior pending | Progressive-disclosure policy, Quick/Standard/Deep resource profiles, context evaluation design, capability catalog/schema/validator, optional skill entrypoints for non-skill package types, context inspection, EVAL-039–050, and four-council review. No universal token savings or automatic Friday manager is claimed. |
| B7 — Four-Council and assumption validation | Delivered locally; runtime calibration pending | Four-Council review and assumption-test schemas/ledgers, templates, operational references, issue/gate invariants, EVAL-051–061, project-level traceability, and regression tests. Live model calibration remains a B10 runtime/evaluation gate. |

| B8 — PRD, Technical Design, and delivery handoff | Delivered locally; project/model quality pending | Project Brief, PRD, Technical Design, Build Plan, human-readable and structured Demo Plans, requirement/acceptance-test/build-task/artifact ledgers, cross-document traceability, EVAL-062–087, and deterministic validator. Local schema, initializer, positive/negative project integration, artifact integrity, document traceability, and P7–P9 gate tests pass. Real product desirability, design feasibility, estimates, and live model quality remain unproven. |
| B9 — Skill packaging and host adapters | Delivered locally; host runtime pending | Portable Agent Skills archive with generated canonical schemas, record starters, project templates and governing documents; generated Claude Code and Codex discovery-path bundles; ChatGPT Project five-reference-file pack with the actual relevant JSON Schemas and record starters plus separate Project instructions/setup; deterministic packager/validator; B9 rubric and EVAL-088–102. Runtime discovery, actual iPad UI setup, model adherence and host permissions have not yet been tested. |

## 4. Remaining construction milestones

| Milestone | Purpose | Main outputs | Exit criteria |
|---|---|---|---|
| **B9 — Skill packaging and host adapters** | Package canonical Peanuts source and host-specific installation/use routes. | Portable Agent Skill ZIP with required support-resource closure; generated Claude Code and Codex adapters; five-file ChatGPT Project pack with embedded actual schemas/record starters, Project instructions/setup; packaging utility; validation and rubric/evaluation cases. | Deterministic, safe packages; canonical-source parity; Agent Skills metadata/name/description validation; official host-path validation; ChatGPT Free five-file fallback honesty and setup. Runtime checks remain separate. |
| **B10 — ChatGPT-primary full verification and release candidate** | Run deterministic regression, privacy/security, reproducibility, live ChatGPT conversation acceptance, target Project UI/fresh-session acceptance, and optional Codex/Claude host integration acceptance. | Cumulative release ZIP, manifest, B10 ChatGPT and cross-host protocols/rubrics, EVAL-103–134, transparent run records, host installation simulation, Project/host smoke tests, setup guide and release checklist. | Managed V0/V1 pass; ChatGPT and host package structures are verified; owner verifies Project UI and fresh chat; optional Codex/Claude routes are accepted only after actual discovery, invocation, method fidelity and fresh-session tests in each host. Remote CI/Codespaces and independent calibration remain separately labelled. Owner approves publication separately. |

## 5. Historical rationale for B0–B10.1 order

B3 establishes repeatable development and CI before the first working slice. B4 tests one small end-to-end path. B5 establishes research integrity and persistent evidence records. B6 then establishes NUTS source-domain methods and analogy records before Four-Council is fully calibrated. This prevents building elaborate methods on top of untested data contracts and handoffs.

B6.5 provides shared context/resource architecture and capability-growth boundaries for every current and future Friday capability. At B6.5, an active manager was deferred. ADR-046 now establishes the minimal explicit selector as the next manager increment; autonomous coordination remains subject to evidence. Non-skill harnesses, workflows, agents and toolsets are not forced to expose a SKILL.md. B7 has established structured review and assumption testing. B8 deepens product/technical outputs. B9 packages the portable capability and host adapters from the canonical source. B10 consolidates ChatGPT-primary engineering acceptance. B10.1 adds the Claude Chat Skill and Project companion while preserving one canonical Peanuts source; ChatGPT remains the managed repository engineering partner and Claude Chat is the ideation partner. Automated tests and security/documentation reviews continue throughout; they are not postponed until B10.

## 4A. Historical B10.1 — Claude Chat and Project integration

B10.1 adds ordinary Claude chat as the owner's primary ideation environment while keeping ChatGPT as the primary managed engineering/build partner during the iPad-only period. It generates a Claude consumer Skill ZIP using the product-specific `peanuts/skill.md` entrypoint (the canonical cross-host source remains `skills/peanuts/SKILL.md`), plus separate Friday Project instructions and five `.txt` knowledge exports containing Markdown-formatted text. The Skill carries repeatable methods; the Project carries durable context and status handoffs.

**Exit criteria:** consumer metadata and package paths match current Anthropic documentation; generated resources match canonical bytes; Project instructions and knowledge docs validate; twelve B10.1 acceptance cases are recorded; owner-side iPad Skill upload/enablement, Project setup, and fresh-chat handoff tests are explicitly `NOT RUN` until observed. A package pass is not a live Claude behavior pass. See `docs/acceptance/CLAUDE_CHAT_PROJECT_ACCEPTANCE.md`.

## 4B. Historical B11 — Real-world pilot and cross-model calibration

After the owner installs the Claude Skill and Project, run real but bounded Peanuts projects and compare Claude Chat and ChatGPT on paired cases. Use source-backed tasks, repeated fresh sessions, an independent human reviewer, and a simpler-critique baseline. Measure useful decision coverage, factual accuracy, critical-risk detection, method adherence, handoff completeness, resource/context cost where telemetry is available, and owner effort. Do not claim one model or framework is superior from one synthetic example.

## 6. Peanuts operational workflow (`P1–P10`)

1. P1 — Intake and event/opportunity intelligence.
2. P2 — Problem and user discovery.
3. P3 — NUTS cross-domain exploration.
4. P4 — Collaborative concept development.
5. P5 — Adaptive Four-Council review.
6. P6 — Validation of critical assumptions.
7. P7 — PRD/product definition.
8. P8 — Technical design.
9. P9 — Execution handoff.
10. P10 — Retrospective and learning.

This workflow is iterative and risk-adaptive. It is not a rigid checklist. The system may loop backward when new evidence changes the framing or idea.

## 7. ChatGPT/iPad-first execution protocol

For each milestone, ChatGPT must:

1. Read the current roadmap, architecture decisions, and latest milestone status.
2. State the milestone objective, dependencies, files to create/change, and acceptance criteria.
3. Create complete files in the managed build environment.
4. Run available tests in the actual available environment and identify that environment.
5. Inspect diffs, links, schemas, references, privacy, and cross-file consistency.
6. Record test commands/results and untested limitations.
7. Regenerate the manifest and cumulative ZIP.
8. Stop at the milestone boundary.

The owner should only need to provide direction, approve consequential decisions, say `GO`, and download/review packages when useful. No local terminal use is required during the construction milestones.

## 8. Validation levels

- **V0 — Integrity:** file list, links, schemas, manifest, privacy/secret-pattern scans.
- **V1 — Managed-environment tests:** Python unit/integration and workflow tests in the assistant's Linux/container environment.
- **V2 — GitHub Actions:** configured cross-platform OS/Python matrix; actual remote runs are required. Private staging is optional.
- **V3 — Codespaces:** Dev Container creation and execution in a cloud Linux terminal accessible through a browser.
- **V4 — Claude runtime:** actual Claude Code discovery, invocation, permission, and fresh-session test on an eligible host.
- **V5 — ChatGPT route:** test native Skills only if account/surface eligible; otherwise test the documented manual file/Project fallback.

A result must be marked `NOT RUN` when the relevant environment or access is unavailable. See `CHATGPT_IPAD_FIRST_BUILD_AND_RELEASE_PLAN.md` and `PC_READINESS_ACCEPTANCE.md`. Final B10 handoff must include a complete beginner-friendly iPad/GitHub/Codespaces and PC/Claude/Codex installation guide; the owner does not need to memorize commands during build.

## 9. Source checkpoint and final release

Deliver a complete source ZIP and V0/V1 report before remote work. An authorized cloud workspace may extract and verify it; uploading a ZIP as a repository file does not unpack it. Private staging is optional for GitHub Actions/Codespaces evidence. The destination is public distribution after licensing, privacy and release gates, with the concrete release artifact reviewed before publication. Personal data remains separate from reusable source.

## 10. Quality gates

- **Gate 0 — Foundation:** purpose, scope, methods, and owner choices documented.
- **Gate 1 — Repository safety:** platform-specific instructions, private-data exclusion, and package integrity.
- **Gate 2 — Reproducibility:** declared dependencies, one-command tests, Dev Container, and CI.
- **Gate 3 — Vertical slice:** end-to-end sample and fresh-session handoff structure.
- **Gate 4 — Method fidelity:** prerequisites, limitations, evidence, and test cases respected.
- **Gate 5 — Skill packaging:** host paths and metadata valid.
- **Gate 6 — Runtime:** actual Claude/ChatGPT routes tested where available.
- **Gate 7 — Release:** regression, privacy/security, documentation, known limitations, and owner approval.

## 11. Current status (2026-11-02)

- B0–B6: delivered locally as documented, structural, or method-specification milestones. B2, B4, B5 and B6 validators and the Python test suite have been run in the assistant's Linux environment.
- Ruff: configured and mandatory in full CI; not installed/executed in the current managed environment, so status remains `NOT RUN` until a network-enabled environment runs the full verifier.
- B3 remote GitHub Actions and Codespaces: not run; no GitHub remote is configured.
- B4/B5 actual Claude/Codex/ChatGPT skill execution: not run; remains a B9/B10 runtime gate.
- B5 real event research, participant interviews, and direct field validation: not performed as part of the milestone. Evaluation cases are `ready`, not `passed` by a model.
- B6.5 refinement: progressive-disclosure, context/resource policy, and multi-type capability catalog refined; autonomous manager remains an optional future decision.
- B7: delivered locally; schema/record/semantic validation and regression tests pass. Live model rubric calibration is not run.
- B8: delivered locally. B8 schemas, semantic rules, templates, project initialization, EVAL-062–087, and regression/integration tests are present. Live-model quality, lint, remote CI, Codespaces, and host-runtime checks remain unverified.
- B9: generated Agent Skills, Claude Code, Codex, and ChatGPT Project packages; canonical metadata/name, package parity, archive safety/reproducibility, five-file adapter and 15 B9 cases structurally validated. Actual host UI/runtime and model-quality checks remain not run.
- B10: remaining full release verification, remote CI/Codespaces, host runtime, evaluation calibration, privacy/security and owner release approval.
- No remote GitHub repository or public release exists.

## 12. Change management

For each meaningful change record: the issue, why the change is needed, affected files, decision record, tests, results, migration implications, and whether previous evaluations must be rerun. Preserve superseded decisions rather than silently deleting them. Do not introduce a database, agent, tool, dependency, or framework without a documented need and trade-off.

## B6 delivery note (2026-11-01)

B6 adds the operational NUTS skill reference and source-domain playbook; structured analogy-card and NUTS-run schemas/records; project-level source/claim/analogy traceability; templates; an analogy-quality rubric; EVAL-031–038; deterministic validation and regression tests. B6 structural checks do not establish biological/historical source accuracy, novelty, patentability, transfer feasibility, or live-model performance. See `docs/reviews/B6_REVIEW.md`.

## B5 delivery note (2026-11-01)

B5 adds the research and product-discovery engine specifications, event intelligence, user research ethics and consent safeguards, research synthesis/triangulation, research-plan and record schemas, project record validation, templates, rubrics, and EVAL-020–030. The structural validator checks schemas, references, consent/local-review conditions, round/question linkage, and recovery. It does not establish factual correctness, research saturation, real user validation, or model performance. See `docs/reviews/B5_REVIEW.md`.

## B4 delivery note (2026-11-01)

B4 introduces the canonical Peanuts skill prototype, skill references/templates, a synthetic end-to-end example, a vertical-slice schema/validator, evaluation case EVAL-019, and tests. Structural fixture validation is not equivalent to Claude/Codex/ChatGPT runtime evaluation. See `docs/architecture/VERTICAL_SLICE_AND_STAGE_CONTRACTS.md` and `docs/reviews/B4_REVIEW.md`.


## B6.5 delivery note (2026-11-01)

B6.5 establishes progressive disclosure, context/resource modes, context evaluation, compact session handoff, a capability catalog/schema/validator, and context inspection. The refinement makes Friday an umbrella/shared foundation first and an optional future manager only if real coordination needs justify it; non-skill harnesses, workflows, agents, and toolsets are not forced to expose a SKILL.md. EVAL-039–050 cover capability boundaries, context selection, mode quality, tool cost, and manager deferral. No universal provider token/credit cap or token-saving percentage is claimed. See `docs/reviews/B6_5_REVIEW.md`.


### B6.5 refinement amendment — 2026-11-01

B6.5 explicitly treats Friday as a repository umbrella and shared governance foundation first; an active manager is optional and must be justified by observed coordination needs. The capability catalog supports `skill`, `harness`, `workflow`, `agent`, and `toolset` package kinds. Every package requires a documented entrypoint, while only `kind: skill` requires `SKILL.md`. Context inspection separates host profiles and reports word/character maintainability proxies rather than token estimates. The development incident protocol requires disclosure, evidence preservation, severity classification, controlled recovery, and regression verification for significant setbacks. No earlier milestone acceptance criteria are weakened by this amendment.


## B7 delivery note (2026-11-01)

B7 adds Four-Council review records with 16 stable dimensions, reviewer-setup disclosure, a separate event-alignment overlay, severity-ranked findings, and non-compensatory decision gates. It adds assumption-test records with predeclared hypotheses/signals/thresholds, participant safeguards, result evidence, and limitations. Project validation checks B7 cross-record references and gate invariants. New projects receive the ledgers; older workspaces without them remain compatible with a migration warning. EVAL-051–061 are synthetic cases marked ready for later runtime evaluation, not live model passes. See `docs/architecture/DECISION_GATES_AND_REVIEW_RECORDS.md` and `docs/reviews/B7_REVIEW.md`.


## B8 delivery note (2026-11-01)

B8 adds structured requirement, acceptance-test, build-task, and artifact records; Project Brief/PRD/Technical Design/Build Plan/Demo Plan templates; a linked structured demo plan; Peanuts P7–P9 procedures; PRD, technical-design, and delivery-handoff rubrics; EVAL-062–087; and deterministic project validation. The validator checks requirement evidence and approval, criterion-to-test coverage, requirement/task dependency graphs, status explanations, human-participant controls, artifact path/hash integrity, earlier-stage artifact references, cross-document ID traceability, demo-claim evidence strength, and stage-completion gates. The B8 validator is included in the consolidated verifier. These checks establish structure and record consistency, not real-world product validity or model behavior. See `docs/reviews/B8_REVIEW.md`.


## B9 delivery note (2026-11-02)

B9 corrects the canonical Agent Skills name to match the `skills/peanuts/` directory and validates metadata against the documented 1,024-character description maximum; the actual description remains concise by editorial choice. `tools/build_skill_packages.py` generates a portable Agent Skills archive, Claude Code project adapter, Codex repository adapter, and an exactly five-file ChatGPT Project source pack made of plain-text `.txt` files containing Markdown-formatted content with separate Project instructions/setup guide. The three skill archives each include 102 files: 30 canonical skill files and 72 generated support resources (schemas, record starters, project templates and governing documents) copied from canonical repository sources. The five ChatGPT files embed relevant schemas/starters/governing source excerpts while staying within the five-file route. The ChatGPT route is designed for Free Projects and explicitly does not imply native Skill activation, shell execution, or deterministic schema validation. `tools/validate_b9.py`, a packaging rubric, and EVAL-088–102 validate structure, metadata, path correctness, resource closure, byte parity, ZIP safety, deterministic output and fallback honesty. No actual target-host runtime pass is claimed. See `docs/architecture/HOST_ADAPTERS.md`, `docs/plans/CHATGPT_PROJECT_ADAPTER.md`, and `docs/reviews/B9_REVIEW.md`.


## B10 delivery note (2026-11-02)

B10 makes ChatGPT the primary owner-facing environment. It adds a ChatGPT runtime acceptance protocol, a fixed EVAL-103–122 acceptance set, a rubric separating live conversation behavior from configured Project UI acceptance, an owner-side fresh-Project smoke-test procedure, and a result-record path. Current ChatGPT official documentation was checked for Project instructions/files, mobile use, Free five-file Project limit, three-file-per-day upload limit, and TXT support. The managed ChatGPT conversation is used as the primary live model runtime where its tools are actually available; it is not misrepresented as the user's configured Project UI. The Project UI fresh-session test remains an owner-side gate. See `docs/acceptance/CHATGPT_PRIMARY_RUNTIME_ACCEPTANCE.md` and `docs/reviews/B10_REVIEW.md`.
