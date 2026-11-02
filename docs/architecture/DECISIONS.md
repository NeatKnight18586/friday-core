# Architecture Decision Records — Friday / Peanuts

**Status:** Mixed: owner-selected directions and proposals  
**Version:** 0.3.0-draft  
**Last updated:** 2026-11-02

This is the authoritative current decision record. [Stage 0 decisions](../DECISIONS.md) are historical and use overlapping local IDs. ADR-046–048 govern the current public product direction and supersede conflicting owner-workflow, visibility and manager-deferral directions below.

A status records the scope of approval. “Owner-selected direction” does not mean implementation details are frozen. A proposal does not become accepted merely because it is documented.

## ADR-001 — Friday is the long-term environment; Peanuts is the first capability
**Status:** Owner-selected direction; clarified by ADR-046  
**Decision:** Friday is the long-term personal AI capability environment; Peanuts is its first bounded research/innovation/project-planning capability.  
**Reason:** Build one useful capability well before expanding Friday.  
**Consequence:** Keep Friday-wide identity/memory/orchestration principles separate from Peanuts implementation.

## ADR-002 — Claude-first, portable-core architecture
**Status:** Superseded by ADR-043, ADR-044 and now ADR-046; retained as a historical adapter direction  
**Historical decision:** Develop/test first in Claude Code while keeping core methods and artifacts portable.  
**Historical reason:** Claude was originally preferred as the primary environment.  
**Current consequence:** ADR-046 makes the product provider-neutral; choose a host by actual access and task needs. Claude Code remains an optional generated adapter; the canonical Peanuts source stays provider-neutral. Compatibility does not imply runtime parity.

## ADR-003 — Platform entry points are distinct
**Status:** Accepted as architecture rule for B1  
**Decision:** Keep concise `CLAUDE.md` and `AGENTS.md` repository guidance separate from the canonical `SKILL.md` skill. Test host-specific skill paths and packaging during B9.  
**Reason:** Claude Code, Codex, and ChatGPT surfaces expose project instructions and skills differently.  
**Consequence:** No assumption that a local skill automatically loads in every ChatGPT client.

## ADR-004 — Start with one main Peanuts skill
**Status:** Proposed  
**Decision:** Start with one main skill and modular references/templates/schemas/scripts/evals as justified.  
**Reason:** Avoid monolithic instructions and premature skill fragmentation.  
**Consequence:** Split only when independent use, stable I/O, permissions, and evaluation justify it.

## ADR-005 — Use an adaptive staged workflow
**Status:** Owner-selected direction  
**Decision:** Use an iterative project workflow whose depth adapts to complexity, consequence, time, and uncertainty.  
**Reason:** Projects differ in scale and risk.  
**Consequence:** Skips/loops must be justified; critical gates remain explicit.

## ADR-006 — NUTS is experimental and cross-domain
**Status:** Owner-selected direction; method remains experimental  
**Decision:** Use NUTS (“Nothing New Under the Sun”) as a philosophy and develop a cross-domain mechanism-transfer method.  
**Reason:** The owner wants to learn from nature, history, engineering, culture, social systems, economics, and existing work.  
**Consequence:** Use structural/relational mapping, source-specific research, transfer mismatch analysis, prior-art checks, attribution, and evaluation.

## ADR-007 — Four-Council is structured critique, not a universal standard
**Status:** Owner-selected direction; calibration pending  
**Decision:** Use Human Value, Strategic Value/Differentiation, Technical Feasibility/Quality, and Red-Team/Risk/Delivery lenses.  
**Reason:** The owner wants a deliberate multi-perspective challenge.  
**Consequence:** Stable dimension anchors, severity rules, no default average, separate event overlay, explicit non-independence caveat.

## ADR-008 — Validate decisive assumptions before final PRD baseline
**Status:** Proposed  
**Decision:** Record a validation disposition before approving a PRD as a product baseline.  
**Reason:** A polished document can formalize unsupported assumptions.  
**Consequence:** Unvalidated assumptions remain visible; time-constrained work may proceed provisionally with explicit owner acceptance.

## ADR-009 — Separate product requirements from technical design
**Status:** Proposed  
**Decision:** PRD describes what/why; Technical Design describes how; Build Plan describes execution.  
**Reason:** Preserve product intent if technical choices change.  
**Consequence:** Trace evidence to requirements, acceptance criteria and tests.

## ADR-010 — Project artifacts are durable source of truth
**Status:** Proposed  
**Decision:** Preserve approved status, claims, assumptions, decisions, requirements, and next steps in project records.  
**Reason:** Work must survive conversation/context loss.  
**Consequence:** Define small state model and templates in B2.

## ADR-011 — Human approval for consequential actions
**Status:** Proposed  
**Decision:** Require approval for consequential decisions/external actions and use deterministic permission controls where available.  
**Reason:** Prompt text alone is not security enforcement.  
**Consequence:** Define permission and action logging during implementation.

## ADR-012 — No infrastructure without demonstrated need
**Status:** Accepted as design constraint for first release  
**Decision:** Begin with Markdown, Git, skills, and small scripts only when justified; defer databases, vector stores, hosted services, UI, and multi-agent orchestration.  
**Reason:** Premature complexity increases maintenance burden.  
**Consequence:** Revisit when usage/evaluation demonstrates a limitation.

## ADR-013 — Evidence type and method maturity are separate
**Status:** Accepted as governance rule  
**Decision:** Record evidence supporting a method separately from Peanuts' pilot/evaluation/adoption status.  
**Reason:** A standard, paper, practitioner framework, and internal test support different claims.  
**Consequence:** No single generic “proven” badge.

## ADR-014 — Private context stays outside the shareable core
**Status:** Accepted as privacy rule  
**Decision:** Keep personal memory, credentials, private files and confidential project data outside the shareable repository unless specifically reviewed and approved.  
**Reason:** Friday may eventually contain sensitive context.  
**Consequence:** Keep repository private pending license/publication decision; use secret scanning and secure storage when code exists.

## ADR-015 — Balanced validation is the default
**Status:** Owner-selected direction  
**Decision:** Start with desk research; seek direct user/field evidence when actual needs, behavior, severity, workflow or adoption materially affects a decision.  
**Reason:** Owner selected balanced validation.  
**Guardrail:** No fixed ratio; desk research is not user validation; no invented user evidence or universal interview quota.

## ADR-016 — NUTS uses broad but selective cross-domain inspiration
**Status:** Owner-selected direction; method remains experimental  
**Decision:** Use relevant source domains across nature, history, engineering, culture, social systems, economics, and existing systems.  
**Guardrail:** Select by function and constraint; avoid superficial analogies, forced search, and unsupported novelty claims.

## ADR-017 — Four-Council depth adapts while criteria remain stable
**Status:** Owner-selected direction; calibration pending  
**Decision:** Use quick-screen, standard and deep reviews.  
**Guardrail:** Same core dimensions and anchors; deep review triggered by consequence, uncertainty, complexity or commitment.

## ADR-018 — Use a selective product-discovery stack
**Status:** Proposed  
**Decision:** Use Double Diamond as a flexible process map, JTBD for progress/context, OST for opportunity/solution mapping when prerequisites exist, and hypothesis tests for assumptions.  
**Consequence:** Use selectively; formal and provisional artifacts must be distinguished.

## ADR-019 — Separate product merit from event alignment
**Status:** Accepted as design rule  
**Decision:** Assess user/product value and feasibility separately from event eligibility, rules and published judging criteria.  
**Consequence:** Use official weights only; never invent or blend them without explanation.

## ADR-020 — Collect team capability and constraints progressively
**Status:** Proposed  
**Decision:** Gather skills, time, budget, assets, access and restrictions conversationally when relevant.  
**Consequence:** Unknowns remain unknown; no unnecessary intake form.

## ADR-021 — Prefer concise Project Brief with conditional artifacts
**Status:** Proposed  
**Decision:** Project Brief is the primary summary; create supporting artifacts only when useful.  
**Consequence:** Avoid documentation bloat and repeated facts.

## ADR-022 — Prove integration with an early vertical slice
**Status:** Accepted as roadmap rule  
**Decision:** B4 builds one small end-to-end workflow after B3 establishes reproducible tests and CI configuration.  
**Consequence:** Test real handoffs and resumability before expanding.

## ADR-023 — Host-specific entry points and skill paths are separate
**Status:** Accepted as architecture rule  
**Decision:** Canonical portable skill source; Claude Code `CLAUDE.md`/`.claude/skills`, Codex `AGENTS.md`/`.agents/skills`, and ChatGPT-specific supported routes/fallback.  
**Consequence:** Verify platform-specific capabilities at B9; no hand-maintained duplicate logic.

## ADR-024 — Evaluation begins before capability expansion
**Status:** Accepted as roadmap rule  
**Decision:** Define test cases, rubrics, and baselines in B2; add evals as each capability is built.  
**Consequence:** B10 is full regression/release evaluation, not the first test.

## ADR-025 — Use Professional Practice Architecture
**Status:** Proposed; approved for B1 documentation scaffold only  
**Decision:** Select relevant disciplines, methods, tools, evidence, and review requirements for each task.  
**Reason:** Professional practice is domain-specific; method names alone do not ensure method fidelity.  
**Consequence:** Create PPA and Tool & Knowledge Registry docs; evaluate selection accuracy later.

## ADR-026 — Research ethics and synthesis are explicit discovery requirements
**Status:** Accepted as method-design rule  
**Decision:** Discovery guidance includes participant recruitment, consent, accessibility, privacy, synthesis, triangulation and sample limitations.  
**Consequence:** No field research claims without actual evidence and appropriate safeguards.

## ADR-027 — Four-Council uses dimension-specific rubric and severity
**Status:** Proposed for pilot  
**Decision:** Define dimensions, 1/3/5 anchors, issue severity, owner boundaries and baseline evaluation.  
**Consequence:** Scores remain separate; critical risks are not averaged away.


## ADR-028 — ChatGPT/iPad-first construction with staged proof
**Status:** Owner-selected delivery constraint; implementation plan accepted for current build
**Decision:** ChatGPT authors and tests the repository in its managed environment while the owner is iPad-only. Build a repeatable Dev Container and GitHub Actions CI before method expansion.
**Reason:** The owner currently has no laptop and should not be required to perform local coding during construction.
**Guardrail:** Managed Linux tests do not prove Windows/macOS behavior or Claude/ChatGPT runtime integration. Report validation levels separately.

## ADR-029 — Private ZIP bootstrap and Codespaces fallback
**Status:** Historical operational proposal; private staging is optional under ADR-046
**Decision:** Prepare a cumulative ZIP for one-file private upload, then use browser-based Codespaces for extraction and cloud terminal checks if needed.
**Reason:** Minimize iPad file-management friction while retaining a normal Git repository structure.
**Guardrail:** Check upload limits and Codespaces quotas/billing. Keep the repository private; never treat `github.dev` as a terminal.

## ADR-030 — Separate pre-upload readiness from runtime readiness
**Status:** Accepted as quality governance rule
**Decision:** Use explicit V0–V5 validation levels; pre-upload readiness covers managed-environment tests and package integrity, while CI/Codespaces/Claude/ChatGPT checks are only passed after actually running in those environments.
**Reason:** Avoid false claims about untested target hosts or account-specific features.
**Consequence:** A private upload may be required to run remote CI; public release remains a separate owner decision.


## ADR-031 — Progressive disclosure is the default context strategy
**Status:** Accepted as B6.5 architecture rule
**Decision:** Use small host maps and capability metadata, load one selected capability's instructions, then retrieve only task-relevant references/evidence.
**Reason:** Context is a scarce resource; a monolithic instruction corpus increases cost, noise, and maintenance.
**Guardrail:** Do not omit mandatory evidence, safety, or method prerequisites to save context.

## ADR-032 — Friday capability management as an initial long-term hypothesis
**Status:** Superseded by ADR-036
**Original decision:** Friday was expected to become a control plane for multiple bounded capabilities, with Peanuts independently useful and extractable.
**Reason at adoption:** The owner intended to build more skills, harnesses, and agents under Friday over time.
**Historical consequence:** This led to the capability catalog and interface-contract work. ADR-036 refines the direction: a manager is optional and must be justified by observed coordination needs.

## ADR-033 — Resource modes are provider-neutral guidance, not universal hard token caps
**Status:** Accepted as B6.5 operating rule
**Decision:** Provide quick, standard, and deep resource profiles. Standard is default; risk and evidence needs can require escalation.
**Reason:** Claude, ChatGPT, Codex, API and other runtimes expose different tokenization, hidden context, billing and control mechanisms.
**Guardrail:** Exact usage only from actual telemetry; hard budgets only where the host/API exposes enforcement controls.

## ADR-034 — Do not auto-load or install every future capability
**Status:** Accepted as design rule
**Decision:** Use curated host activation profiles and on-demand loading where supported. Keep a registry of actual capabilities; no placeholders.
**Reason:** Metadata and discovery overhead can grow with the skill catalog, while unrelated capabilities add noise and maintenance.
**Consequence:** Test catalog-only, curated, and direct-install options at B9 for each host.

## ADR-035 — Context efficiency must preserve task quality
**Status:** Accepted as evaluation rule
**Decision:** Compare selective retrieval against a controlled broader-context baseline using the same task/evidence and quality rubric.
**Reason:** Token reduction is not an improvement if correctness, traceability, safety, or completeness deteriorates.
**Consequence:** Record actual host usage where available; never equate word counts with tokens or fabricate savings.


## ADR-036 — Friday is an umbrella first; an active manager is optional
**Status:** Historical direction; superseded where conflicting by ADR-046 (Stage 1, 2026-11-02)  
**Decision:** Friday is initially the repository umbrella and shared governance foundation for independent capabilities. It may evolve into an active manager/control plane only if real use demonstrates recurring routing, handoff, permission, or continuity problems that simpler host-native discovery and a curated catalog cannot solve.
**Reason:** A manager creates extra context, runtime, security, evaluation, and maintenance costs. Building it before multiple stable capabilities exist would be premature.
**Consequence:** Keep the catalog and capability contracts; defer autonomous routing, multi-agent coordination, and manager runtime until a measured decision gate is passed.

## ADR-037 — Capability packages may have non-skill entrypoints
**Status:** Accepted as B6.5 registry-contract refinement
**Decision:** A registry entry must identify a real canonical package, but only `kind: skill` requires an Agent Skills `SKILL.md`. Harnesses, workflows, agents, and toolsets may expose their own documented entrypoints.
**Reason:** Friday is intended to host different capability types without imposing a single package format on all of them.
**Consequence:** The registry validator checks `SKILL.md` metadata when one is declared, and validates package paths/dependencies for every capability type.

## ADR-038 — Context efficiency uses progressive disclosure and curated activation
**Status:** Accepted as B6.5 refinement
**Decision:** Keep root host instructions concise, activate only relevant capability packages, and retrieve task-specific references/evidence on demand. Do not load/install every capability by default.
**Reason:** Context and provider usage are constrained, while a growing skill catalog can add metadata and routing noise.
**Consequence:** Keep capability metadata compact; use deterministic filtering before considering an AI manager. Recheck host-specific discovery at B9/B10.

## ADR-039 — Friday resource modes are quality-bounded guidance
**Status:** Accepted as B6.5 refinement
**Decision:** Quick, Standard, and Deep modes guide the level of work. They do not lower truthfulness, safety, consent, mandatory evidence, or critical-risk requirements.
**Reason:** A portable skill cannot enforce universal provider credit/token caps, and cheap output is not useful if it is materially worse.
**Consequence:** Use provider telemetry where available, report proxies honestly, and compare context-saving changes against quality baselines before claiming benefit.


## ADR-040 — Use a manager maturity ladder; do not jump to an autonomous router
**Status:** Historical direction; superseded where conflicting by ADR-046 (Stage 1, 2026-11-02)  
**Decision:** Friday evolves only through the lowest-complexity level that solves observed needs: repository umbrella, curated activation, deterministic catalog helper, assisted selector, bounded manager, and only then agentic orchestration if evaluated benefit justifies it.  
**Reason:** A model-backed manager adds context, cost, latency, security, and maintenance. It may not be necessary even as the capability catalog grows.  
**Consequence:** Record actual routing/handoff incidents and compare simpler alternatives; no arbitrary usage-count threshold or automatic manager implementation.

## ADR-041 — Significant development limits must be disclosed and recovered without weakening gates
**Status:** Accepted as B6.5 development-governance rule  
**Decision:** Use the incident protocol and explicit statuses (`PASS`, `FAIL`, `TIMEOUT`, `NOT RUN`, `BLOCKED`, `PASS WITH SKIPS`, `INCONCLUSIVE`). Preserve evidence, diagnose root cause, recover, and run regression checks.  
**Reason:** Execution limits and environment gaps must not be hidden or mistaken for code failures or successful tests.  
**Consequence:** A timeout remains unresolved until a valid recovery path proves the required coverage. Acceptance criteria are not weakened to produce a green result.

## ADR-042 — Capability packages require a real entrypoint but not a universal format
**Status:** Accepted as B6.5 registry-contract rule  
**Decision:** Every capability requires a unique canonical package and a documented entrypoint inside it. Only `kind: skill` requires `skill_file`, and for a skill the registry entrypoint must be that `SKILL.md`. Other kinds may expose their own appropriate entrypoint.  
**Reason:** Friday must support future harnesses, workflows, agents, and toolsets without forcing them into an Agent Skills package.  
**Consequence:** The capability validator checks package path uniqueness, entrypoint existence, skill metadata where applicable, host discovery claims, dependencies, and cycles.


## ADR-043 — ChatGPT Projects are the primary owner-facing environment
**Status:** Historical direction; superseded where conflicting by ADR-046 (Stage 1, 2026-11-02)  
**Decision:** Use ChatGPT Projects as the primary owner-facing environment for completing and operating Peanuts/Friday on the current iPad workflow. Preserve `skills/peanuts/` as the single canonical portable source. Keep the five-file manual Project adapter and separate Project instructions as the baseline route; native ChatGPT Skills are conditional. Claude Code and Codex remain optional generated coding-host adapters.  
**Reason:** The owner explicitly selected ChatGPT as the environment where Peanuts/Friday should be completed and used. Requiring migration to another provider would add friction and split continuity.  
**Guardrails:** A Project is not a shell/runtime merely because the repository references scripts. Distinguish live ChatGPT conversation behavior from the user's configured Project UI. Do not claim the Project files are installed without UI evidence. Mark unavailable checks `NOT RUN`; preserve source verification, privacy, human approval and deterministic validation boundaries.  
**Consequence:** B10 acceptance prioritizes ChatGPT live conversation and manual Project behavior. Actual Project fresh-session testing remains owner-side; optional host adapters do not block ChatGPT-first use.

## ADR-044 — Split owner workflow across Claude Chat ideation and ChatGPT engineering
**Status:** Historical direction; superseded where conflicting by ADR-046 (Stage 1, 2026-11-02)  
**Decision:** Use ordinary Claude Chat with the Peanuts custom Skill and a Friday Project as the owner's primary ideation/concept-development environment. Keep ChatGPT as the primary managed engineering/build partner while the owner is iPad-only. Preserve one canonical `skills/peanuts/` source and share work through reviewed, explicit status handoffs. Codex and Claude Code remain optional filesystem/CLI hosts when a suitable computer is available.  
**Reason:** The owner wants Claude's regular chat app for sustained ideation while relying on ChatGPT's managed build environment to author, test, package, and deploy the repository without a laptop. A split by task fits the available tools better than forcing one provider to handle every job.  
**Guardrails:** Do not maintain separate Peanuts methodologies. Claude Project knowledge stores durable background; a handoff remains the auditable cross-chat state. Claude Chat cannot be presumed to have Friday's local Git checkout, terminal or validators. ChatGPT's managed container is not the user's repository or Project UI. Each host/runtime must report only tools actually used and checks actually completed.  
**Consequence:** B10.1 must provide a Claude consumer Skill upload plus a separate Claude Project companion and owner-side acceptance protocol. The current managed build can verify packages and instructions, but only the owner can complete the real Claude iPad upload, Skill activation, Project setup and fresh-chat tests.


## ADR-045 — Use documented TXT format for Claude Project knowledge exports
**Status:** Accepted for B10.1 package refinement (2026-11-02)  
**Decision:** Generate the five curated Claude Project knowledge exports as `.txt` files containing Markdown-formatted text. Keep the consumer Skill entrypoint as `peanuts/skill.md` and the canonical cross-host source as `skills/peanuts/SKILL.md`.  
**Reason:** Anthropic's current Project file upload documentation explicitly lists TXT among supported document types but does not explicitly list Markdown as a separate extension. TXT reduces upload-format ambiguity on the owner's iPad. The five documents are a curation design, not a Claude Project file-count limit.  
**Guardrails:** Do not rename the Skill entrypoint to TXT. Project knowledge is limited by total context, not the Free-plan maximum number of Projects. The builder must regenerate all consumer exports from canonical sources; generated TXT files must not be edited independently.  
**Consequence:** B10.1's Project knowledge ZIP contains exactly five generated TXT documents; deterministic tests protect extension, content and source parity.


## ADR-046 — Public, provider-neutral capability manager direction
**Status:** Owner-selected product direction; Stage 1 execution approved (2026-11-02)  
**Decision:** Build Friday as a manager for reusable skills, harnesses, workflows, agents and toolsets. Preserve a portable Peanuts core and generated host adapters. Plan a minimal explicit capability selector/intake workflow for Stage 2; it is not implemented in this checkpoint. Target a public repository after release gates, without requiring users to adopt a particular provider.  
**Reason:** The current owner brief explicitly requests a public manager that can adopt future capabilities. Earlier optional-manager/private-owner directions no longer define the destination.  
**Guardrails:** An explicit selector does not justify autonomous orchestration. Retain least privilege, bounded handoffs, no-match behavior and progressive disclosure. Host-native discovery remains a supported simpler route. Do not promise identical features or successful behavior across untested hosts.  
**Consequence:** ADR-036/040 manager deferral applies to autonomous coordination, not to the planned minimal selector. ADR-043/044 remain historical owner workflows; neither determines public user platform choice. Private staging is optional; publication itself still requires review of a concrete release artifact.

## ADR-047 — Separate public source from optional private profile context
**Status:** Accepted design boundary for staged revision; profile importer not implemented  
**Decision:** Keep reusable capabilities separate from personal resumes, profiles, writings and project evidence. Plan optional document-to-profile import after manager/handoff work: candidate extraction, explicit user review, provenance, private export, correction and deletion.  
**Reason:** Personalization is useful but should not leak private data or silently preserve model inferences.  
**Consequence:** No automatic memory ingestion, cross-account synchronization or hosted memory service is claimed. License/rights review is required before public release; no reuse license has been selected by Stage 1.

## ADR-048 — Evidence gates and sequential revision checkpoints
**Status:** Accepted for the approved staged process  
**Decision:** Follow the six stages in `docs/plans/REVISION_STAGES.md`, completing one checkpoint at a time. Use deterministic checks for exact contracts, actual host trials for runtime behavior, and comparative tasks/user feedback for usefulness and method claims.  
**Reason:** A valid ZIP, a structured document and a model's confidence are different from a successful user workflow.  
**Consequence:** Record failures and unrun checks explicitly. Regenerate adapters/manifests and verify a freshly extracted source archive. Do not weaken lint/test rules to obtain green results or claim universal compatibility, proven NUTS effectiveness or measured savings from scaffolding.


## ADR-049 — Implement minimal host-mediated selection and dry-run intake
**Status:** Accepted for Stage 2 (2026-11-02); host/model behavior remains unverified  
**Decision:** Use FRIDAY.md for portable manager instructions, a deterministic read-only selector/intake helper and a generated manual chat export. Per-package contracts declare inputs/outputs, tools, permissions, fallback and handoff. Retain direct Peanuts invocation.  
**Reason:** Provides actual capability-management behavior with bounded complexity and extension through metadata/contracts, without an autonomous loop.  
**Guardrails:** All dependency/host/mode/prerequisite gates must pass; ambiguity/no-match is explicit. Uploaded code is never executed by intake/selection. Grant flags only report existing authorization. Manual export does not install a native Skill or provide capability bodies.  
**Consequence:** ADR-046's planned minimal selector is delivered locally; future runtime/autonomy work remains gated. Schema 1.0.0 gains optional contract_file metadata for older-catalog compatibility; manager selection requires contracts. See `docs/architecture/MINIMAL_MANAGER.md`.

## ADR-050 — Pull CI/host preflight forward without claiming runtime parity
**Status:** Accepted for Stage 2 follow-up to owner's explicit testing request  
**Decision:** Check workflow syntax/pins, clean dependency/full-verifier runs and real read-only CLI access now, retaining exact evidence and blockers. Run GitHub-hosted CI only on an authorized source commit; consumer account tests remain distinct.  
**Reason:** Catch integration defects before later features depend on them.  
**Consequence:** The current actual Codex attempt is authentication-BLOCKED, not passed. Linux containers and actionlint are useful layers, not substitutes for macOS/Windows or consumer UI testing. See `docs/acceptance/CI_AND_HOST_PREFLIGHT.md`.


## ADR-051 — Preserve the existing owner MIT license
**Status:** Existing owner repository choice observed and preserved in Stage 2 (2026-11-02)  
**Decision:** Include the MIT LICENSE already present in `NeatKnight18586/Friday`, verbatim with its existing copyright holder.  
**Reason:** Connected-source inspection reveals an existing owner decision that was absent from the uploaded source ZIP. Asking the owner to choose again or replacing that license would create unnecessary inconsistency.  
**Consequence:** Stage 1's unset-license statement describes that earlier ZIP only. Third-party content/rights review remains required; this does not license material the owner does not own. Remote main/source are not modified by this local preservation.


## ADR-052 — Selective Peanuts context and compact planning exports
**Status:** Accepted for owner-approved Stage 3 (2026-11-02)  
**Decision:** Keep a concise skill entrypoint with conditional method references; add an explicit compact initializer producing only Project Dossier and handoff.json. Preserve the existing full initializer default, record schemas and P7–P9 approval gates.  
**Reason:** Early discovery and cross-chat continuation need a coherent explanation and state without compulsory full-ledger duplication. More files or shorter prompts do not establish better outcomes.  
**Guardrails:** Export authority is planning-context-only. Preserve inspected/synthetic evidence boundaries, actual approval scope, critical blockers, unavailable checks and the next action. Digest/schema checks establish integrity, not truth or human/model validation. Fresh-process recovery is tested separately from Stage 4 fresh-chat behavior.  
**Consequence:** Existing source contracts remain compatible; the new planning-handoff schema is version 1.0.0. Full deliverables are linked rather than duplicated. Chat-only drafts leave unverified digests null and report NOT RUN.

## ADR-053 — Fast is a boundary alias for stored quick
**Status:** Accepted for Stage 3  
**Decision:** Display Fast/Standard/Deep; accept fast and legacy quick at the manager/compact initializer boundaries and persist quick.  
**Reason:** Matches the owner's naming while preserving existing registries, records and integrations.  
**Consequence:** No bulk migration or weakening of resource/evidence rules. A caller declaring a tool or permission still does not grant authority or prove its use.

## ADR-054 — Separate behavioral evaluation readiness from runtime evidence
**Status:** Accepted for owner-approved Stage 4 (2026-11-02); live evidence gate open
**Decision:** Predeclare twelve synthetic tasks, four instruction conditions, critical-case repeats, criterion-based grading and immutable-by-default local evidence records. Add the full-NUTS/simple-critique condition to separate council and NUTS comparisons. Publish the actual blocked preflight rather than authored outcomes.
**Reason:** Package correctness, model behavior and user usefulness require distinct evidence. The available Codex CLI failed authentication before inference; no other model runtime is configured. A seeded suite and recorder enable genuine trials without inventing them.
**Guardrails:** No provider calls or spending from the collector, no automatic quality grades, no secret publication, no credential replacement, no native discovery inference from rendered prompts. Actual token telemetry or null; critical failures cannot be averaged away. Small public synthetic cases are development evidence, not a reliability guarantee.
**Consequence:** Stage 4 infrastructure can be published as an experimental checkpoint while actual comparative/native-host acceptance remains open. Optional profile import and broad public-release claims do not become approved or verified by this checkpoint.
