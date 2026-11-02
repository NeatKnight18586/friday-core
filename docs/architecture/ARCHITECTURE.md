# Peanuts Logical Architecture

**Status:** B0–B9 architecture baseline; generated host packages delivered locally, host runtime acceptance pending  
**Version:** 0.6.6-draft  
**Last updated:** 2026-11-01

## 1. Architecture objective

Build Peanuts as a small, modular, portable harness that can grow without becoming a monolithic prompt, opaque multi-agent system, or set of duplicated platform implementations. It must remain understandable to its owner, inspectable in files, testable in realistic environments, and secure in proportion to its capabilities.

## 2. Initial architecture style

**Style:** File-centered harness with one canonical Peanuts skill source (established in B4 and packaged in B9), focused method references, conditional templates, structured records where useful, and deterministic scripts only where they add clear value.

No database, hosted backend, vector store, UI, or multi-agent orchestration is required for the first release. Revisit only when actual usage demonstrates a limitation that simpler files and scripts cannot reasonably solve.

## 3. Logical layers

| Layer | Responsibility | Boundary |
|---|---|---|
| User interaction | Understand intent, explain, ask focused questions, receive approvals. | Do not force long forms or hide decisions. |
| Friday capability manager | Today: repository, shared standards, catalog and governance. Stage 2: read-only selector/intake workflow and manual manager instructions. | Local helper implemented; host/model execution remains unverified; autonomous orchestration remains deferred. Host-native discovery remains available. |
| Capability catalog | Registers bounded skills, harnesses, workflows, agents, and toolsets with stable IDs and host status. | Do not register placeholders or duplicate full method content. |
| Context/resource management | Applies progressive disclosure, retrieval priority, compact handoffs, and resource modes. | Do not claim provider-wide hard token control from a portable skill. |
| Professional Practice Architecture | Identify disciplines, methods, tools, prerequisites, evidence and review needs. | Do not pretend to possess credentials or select frameworks by popularity. |
| Method modules | Research, discovery, NUTS, Four-Council, validation, PRD, technical design. | Do not silently alter approved goals or decisions. |
| Tool/knowledge layer | Sources, search, documentation, calculators, scripts, integrations and validation tools. | Use only tools actually available and permitted; record important provenance. |
| Project records | Store brief, status, sources, claims, assumptions, decisions, requirements and results. | Chat history is not the sole source of truth. |
| Quality/evaluation | Check structure, traceability, method fidelity, consistency, safety and performance. | A mechanical check does not prove product desirability or factual truth. |
| Platform adapters | Map the portable package to host-specific discovery, paths, permissions and tools. | Do not become separately hand-maintained versions of core logic. |

## 4. Repository source-of-truth and packaging

The intended canonical Peanuts skill source is `skills/peanuts/`, to be prototyped at B4 and finalized at B9. It will contain `SKILL.md` and only the references, assets/templates, scripts and evaluations required by the skill.

Host-specific skill folders are generated or packaged from the canonical source and must not be hand-edited independently. B9 uses deterministic generation from the canonical source and validates byte-level parity; runtime discovery is verified separately in B10.

The directory structure is intentionally staged. Do not create empty directories or placeholders solely because they appear in a future-state diagram.

## 5. Platform entry points and skill discovery

The Agent Skills format provides a portable authoring convention (`SKILL.md` plus optional references/scripts/assets), but hosts differ in discovery path, tools, permissions, and availability. Verify documentation and behavior at integration time.

| Environment | Project guidance | Skill discovery/use | Important limitation |
|---|---|---|---|
| Claude Code | Root `CLAUDE.md` | Generated project skill under `.claude/skills/peanuts/SKILL.md`. | B9 package generated; runtime discovery/permissions/fresh-session acceptance pending. |
| Codex | Root `AGENTS.md` | Generated repository skill under `.agents/skills/peanuts/SKILL.md`. | B9 package generated; runtime discovery/permissions/fresh-session acceptance pending. |
| ChatGPT Project fallback | Project instructions plus five generated Markdown source files | Manual invocation using the Project instructions and relevant reference file. | Available as the Free-plan fallback; not automatic native activation or shell execution. |
| Native ChatGPT Skills | Native Skills upload/selector where supported | Portable Agent Skill package. | Eligibility is plan/workspace/surface-dependent; do not assume availability. |
| Claude.ai | Product instructions and eligible custom Skill upload | Portable Agent Skill ZIP. | Plan/surface eligibility and tool/network behavior must be checked. |

Root `CLAUDE.md` and `AGENTS.md` are concise host-specific project guides, not substitutes for `SKILL.md`. They point to canonical documents and set repository safety/work rules.

## 6. Stage contracts and interfaces

Each workflow stage or method must define:

- Purpose and exit decision.
- Required and optional inputs.
- Prerequisites and unavailable-tool behavior.
- Process/decision rules.
- Output artifact and stable identifiers where useful.
- Evidence and provenance to preserve.
- Human approval/escalation requirements.
- Quality checks and failure conditions.

Downstream stages consume the declared outputs, not assumptions about an undocumented free-form response. Contract detail should be proportionate: a compact Project Brief can contain several logical records for a small project.

## 7. Project modes and workflow state

The coordinator uses stable mode IDs in `PRODUCT_DISCOVERY.md`: `MODE-EVENT`, `MODE-PROBLEM`, `MODE-IDEA`, `MODE-EXISTING`, `MODE-RESEARCH`. The operational workflow uses `P1–P10`; construction milestones use `B0–B10`.

Project records may logically include:

- Project Brief: desired outcome, problem, users, concept, scope, status.
- Status/handoff: current phase, completed work, decisions, blockers, next action.
- Sources/claims: source metadata, material claims, evidence status and traceability.
- Assumptions: uncertainty, impact, test and validation status.
- Decisions: chosen, rejected, deferred, superseded decisions and rationale.
- Requirements: IDs, origin, priority, acceptance criteria and tests.
- Artifacts: dossier, synthesis, concept, council, validation, PRD, design and plan.

These are logical categories, not one-file-per-category requirements. Session recovery must identify project/version, status, key decisions, unresolved questions, blockers and next action.

## 8. Traceability and requirements

For material requirements, preserve a chain such as:

`Source/Observation → Claim/User Need → Opportunity → Concept Hypothesis → Decision → Requirement → Acceptance Criterion → Verification/Test Result`

Use stable IDs when they provide value. Critical, event-required, safety-related, or high-cost requirements need clear origins and verification methods. See `QUALITY_ASSURANCE.md` and the requirements standard register.

## 9. Verification versus validation

- **Verification:** Did the artifact/system meet its specifications? Examples: schema checks, required fields, unit/integration/acceptance tests.
- **Validation:** Does the concept/system meet the real need in its intended context? Examples: interviews, observation, usability testing, field pilots and outcome evidence.

Passing a schema validator does not prove the idea solves a valuable problem. Positive user feedback does not prove a system is secure, reliable, or compliant.

## 10. Deterministic checks versus judgement

Use scripts/schemas for exact checks: file presence, metadata, JSON validity, date formats, unique IDs, workflow states, links, package paths, and consistency rules. Use model/human judgement for user value, analogical transfer, strategy, trade-offs, and concept quality. Important judgement outputs require anchored rubrics and evaluation.

## 11. Security, privacy and trust boundaries

- Treat imported websites, PDFs, repositories, emails, comments, and uploads as untrusted data, not instructions.
- Retrieved content cannot override higher-priority instructions or grant tool permission.
- Inspect untrusted code before execution; avoid arbitrary scripts and unbounded tool chains.
- Use least privilege for filesystem, shell, connectors and APIs.
- Separate decision-making from consequential execution.
- Require explicit approval before publishing/submitting, spending, messaging, deleting/overwriting, or changing permissions.
- Keep secrets and personal memory out of Git; use secure local/runtime secret storage and scanning when code exists.
- Minimize participant and user data; record consent, purpose, retention and access controls where research requires it.
- A prompt instruction is not a security control; use host permissions and deterministic controls where available.

## 12. Failure, recovery and maintainability

Prefer simple, inspectable project records and reversible file operations. Before multi-file writes, plan changes, preserve backups/version history, validate outputs, and report partial failure. A resumable project handoff must work in a fresh session. Avoid hidden state and vendor-specific logic in the portable core.

## 13. Deferred architecture questions

- Whether any database or retrieval index is justified.
- Whether autonomous coordination or subagents add measurable value beyond explicit selection.
- How optional approved private profile import should be implemented; hosted memory remains deferred.
- Exact ChatGPT distribution route for target surfaces/accounts.
- Whether existing packaging should retain checked-in host snapshots or distribute only release assets.

Resolve these from real usage, permissions, costs, and evaluation rather than assumption.

## 15. Friday manager destination and current catalog

ADR-046 sets Friday's intended public, provider-neutral manager direction. The current implementation is a repository/catalog foundation. Stage 2 adds the read-only selector/intake helper, FRIDAY.md and a manual export. See `MINIMAL_MANAGER.md` for the actual interface; selection does not execute a capability or establish host/model behavior.

A capability may be a skill, harness, workflow, agent or toolset. It needs an existing package/entrypoint, bounded scope, inputs/outputs, prerequisites, dependencies, permission and failure behavior, supported hosts and evaluation. The selector should load the smallest suitable capability set and use compact explicit handoffs. No-match and ambiguity behavior must be tested with disposable fixture packages before promotion.

Autonomous loops, broad integrations, subagent orchestration and hosted memory remain deferred until measured need justifies them. See `CAPABILITY_SYSTEM_AND_ROUTING.md` and `docs/plans/REVISION_STAGES.md`.

## 16. Context and resource management

Apply progressive disclosure: short host maps and capability metadata first, one selected capability's `SKILL.md` on activation, relevant references only when needed, and specific records/source passages/scripts at execution time. Do not load all capabilities, documents, or project history by default. Use quick/standard/deep modes as resource-planning profiles, with standard as the default. Escalate when risk or uncertainty requires it; do not discard mandatory quality/safety checks to save context.

Portable skills can guide context selection but cannot enforce universal consumer-plan token/credit limits. Hard API token/output/tool budgets are possible only where a custom runtime/provider exposes them. Record exact tokens only from actual telemetry; words/characters/tool counts are proxies. See `CONTEXT_ENGINEERING.md`, `CAPABILITY_SYSTEM_AND_ROUTING.md`, and `docs/governance/RESOURCE_BUDGETS.md`.

## 17. B2 project record implementation

The B2 record layout, lifecycle/workflow state, JSONL append-oriented evidence records, JSON Schema contracts, templates, and validation behavior are specified in [`PROJECT_RECORDS_AND_STATE.md`](PROJECT_RECORDS_AND_STATE.md). The default workspace is `local-workspace/projects/` and is Git-ignored. Do not commit project-specific records without sensitivity review and owner approval.


## 18. B9 host adapters

See [`HOST_ADAPTERS.md`](HOST_ADAPTERS.md) for official host paths, portable package rules, the ChatGPT Project five-file design, runtime boundaries, security and reproduction checks. All adapters are generated from `skills/peanuts/`; host copies are not independent sources.
