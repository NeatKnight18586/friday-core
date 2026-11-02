# B6.5 — Context Efficiency and Capability Growth: Four-Council Review

**Review date:** 2026-11-01  
**Status:** Passed as an architecture/policy and deterministic-structure milestone; context savings and model-host behavior are not established.

## Scope

Reviewed the context-engineering policy, resource modes, context evaluation protocol, capability registry/schema/validator, Friday vision, capability system/routing architecture, Peanuts skill instructions, context inspection utility, EVAL-039–050, and B2–B6 regression boundaries.

This is a structured four-perspective review, not four independent human experts or proof of runtime efficacy.

## Council 1 — Principal Systems Architect

**Assessment: 8.8/10 — Pass with bounded limitations**

Strengths:
- Friday is the repository umbrella and shared governance foundation first; an active manager/control plane is optional, not an assumed requirement.
- Peanuts remains an independent, extractable capability.
- The registry supports different package kinds, requires a real package entrypoint, and does not force every harness, workflow, agent, or toolset to expose `SKILL.md`.
- Capability dependencies are explicit and checked for missing references and cycles.
- The design avoids premature databases, agent orchestration, and dynamic marketplaces.

Limitations:
- A real Friday routing/control plane does not exist and should not be built until repeated coordination friction is observed.
- Catalog discovery and host metadata overhead need re-evaluation as the number of capabilities grows.

Recommendation: Preserve the lightweight registry and revisit the manager decision only after real multi-capability use demonstrates a problem that host-native discovery and a curated set cannot solve.

## Council 2 — Context Engineering and AI Efficiency

**Assessment: 8.7/10 — Pass with bounded limitations**

Strengths:
- Four-level progressive disclosure separates map, selected capability, relevant references, and specific evidence/execution.
- Root host instructions remain small maps rather than methodology manuals.
- Quick/Standard/Deep modes change scope and resource planning without waiving truth, safety, consent, or evidence requirements.
- Compact handoffs and deterministic scripts reduce repeated conversation replay and raw-data injection.
- Context inspection reports word/character proxies per host profile and does not call them tokens.

Limitations:
- No live host/model comparison has established a token-saving percentage.
- Skill metadata and auto-discovery costs differ by host; curated installation profiles require host-specific tests.

Recommendation: Keep progressive disclosure as the default. At B9/B10, run controlled same-host comparisons and evaluate quality alongside actual resource use.

## Council 3 — Developer Experience and Student Practicality

**Assessment: 8.9/10 — Pass with bounded limitations**

Strengths:
- No laptop or local token tooling is required during the current authoring stage.
- Standard is the default mode; Quick and Deep are explicit alternatives.
- The architecture avoids requiring the owner to memorize commands or provider-specific token rules.
- Friday remains a light umbrella rather than creating a manager runtime before it is useful.

Limitations:
- Codespaces, Claude Code, Codex, and ChatGPT runtime behavior remain untested.
- A custom API/orchestrator could enable stronger hard spend limits later, but would add credentials, cost, maintenance, and security responsibilities.

Recommendation: Do not introduce a custom API runtime for token control during Peanuts' first release. Use host-native products and a lean context architecture first.

## Council 4 — AI Quality, Security and Evaluation

**Assessment: 8.6/10 — Pass with bounded limitations**

Strengths:
- Context efficiency is treated as constrained optimization: mandatory evidence, safety, and method prerequisites are non-negotiable.
- Broad-context versus progressive-disclosure comparisons have controlled conditions and predeclared quality criteria.
- A cheaper but materially worse output is explicitly not an improvement.
- Registry validation checks optional skill entrypoints for non-skill packages, dependency references/cycles, package entrypoints, host discovery paths, and registered skill coverage.
- EVAL-047–050 cover multi-capability loading, no-forced-routing, quality-over-budget escalation, and manager deferral.

Limitations:
- Synthetic cases and deterministic validators do not establish AI behavior, retrieval precision, or actual token savings.
- Small samples cannot support broad statistical claims.

Recommendation: Retain the runtime evaluation plan and report per-case failures, actual host/model data where available, and limitations.

## Consolidated verdict

**PASS WITH BOUNDED LIMITATIONS.** The B6.5 architecture is suitable as a portable design and local repository foundation. It does not prove universal token savings, automatic routing, or model-host compatibility. Friday's active manager role is intentionally optional.

## Required follow-up

1. At B9, verify host skill metadata/discovery and provide curated install options.
2. At B10, perform host-specific runtime acceptance where access exists.
3. Compare broad-context and progressive-disclosure conditions using identical tasks, models, tools, and rubrics before claiming efficiency gains.
4. Revisit a Friday manager only if multiple real capabilities produce repeatable routing/handoff friction.


## Final B6.5 refinement review — 2026-11-01

The following refinements were added after the initial B6.5 review, without changing earlier milestone acceptance criteria:

- Friday's role is stated consistently as repository umbrella/shared governance foundation first. An active manager is a possible future role, not a requirement. A manager maturity ladder prefers host-native discovery and curated activation, then deterministic catalog filtering, assisted selection, bounded management, and only then agentic orchestration if measured benefit justifies it.
- Capability package kinds remain extensible (`skill`, `harness`, `workflow`, `agent`, `toolset`). Every package has a unique canonical path and real documented entrypoint. Only `kind: skill` must expose a `SKILL.md`, and that file is its entrypoint. Non-skill packages are not forced into the Agent Skills format.
- Registry validation now protects against duplicate canonical package paths, mismatched skill entrypoints, unregistered/unsafe skill paths, missing evaluation references, dependency cycles, and host profiles claiming `verified` without an existing discovery path.
- Evaluation documentation was consolidated to report 50 synthetic cases accurately. Synthetic/schema-valid cases are not live model passes.
- The development incident protocol formalizes timeout/failure disclosure, evidence preservation, severity, recovery, regression checks, and honest reporting of skipped or unavailable tools.

### Final four-council reassessment

| Council | Assessment | Final judgment |
|---|---:|---|
| Principal Systems Architect | 9.0/10 | Pass; package types and optional manager direction are coherent. |
| Context Engineering and AI Efficiency | 8.8/10 | Pass; progressive disclosure is bounded by quality and host-specific verification. |
| Developer Experience and Student Practicality | 9.0/10 | Pass; iPad-first build and incident communication are documented. |
| AI Quality, Security and Evaluation | 8.8/10 | Pass with bounded limitations; remote and live-host checks remain pending. |

Scores are qualitative specification assessments, not independent human reviews, benchmarks, or proof of runtime performance.

**Final verdict: B6.5 is accepted as a local architecture/policy and deterministic-structure milestone, with bounded limitations.** It does not establish actual provider token savings, universal credit controls, automatic Friday routing, or live Claude/Codex/ChatGPT compatibility. No autonomous manager is implemented.

### Remaining release gates

1. Execute Ruff and full CI in a network-enabled environment.
2. Execute GitHub Actions and Codespaces after private upload.
3. Test real Claude Code, Codex, and ChatGPT routes where the owner's access and chosen host permit.
4. Compare broad-context and progressive-disclosure tasks under controlled conditions before claiming usage savings.
5. Reconsider a Friday manager only after documented multi-capability usage demonstrates friction that simpler approaches cannot solve.
