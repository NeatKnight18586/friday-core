# Friday — Long-Term Vision and Boundaries

**Status:** Directional draft; not an implementation specification  
**Version:** 0.4.2-draft  
**Last updated:** 2026-11-02

## 1. North star

Friday is the long-term personal AI environment the owner hopes to build: an assistant that can understand relevant user-approved preferences and goals, maintain useful continuity across projects, select specialized capabilities, work with permitted tools, and help turn ideas into completed work.

The inspiration is a practical real-world personal assistant with the continuity and usefulness associated with fictional assistants such as JARVIS or FRIDAY. The engineering objective is not to reproduce fiction or promise human-like understanding. It is to build an inspectable, secure, useful system grounded in provenance, user-approved context, explicit permissions, and measurable performance.

## 2. Manager destination and current implementation

Friday is intended to manage reusable skills, harnesses, workflows, agents and toolsets for public users across supported hosts. ADR-046 in [current decisions](../architecture/DECISIONS.md) supersedes the earlier optional-manager/private-owner direction.

Today Friday provides repository governance, a capability catalog, generated adapters and validation. Stage 2 adds the read-only explicit selector/intake helper and FRIDAY.md instructions; actual host/model behavior remains unverified. It should check scope, prerequisites, dependencies, permissions and handoff needs, loading only the selected capability. Host-native discovery remains useful; an autonomous routing loop is not required.

Peanuts is the first independent capability and must remain extractable. Future capabilities need real packages, bounded contracts and evaluation before registration. Fixture capabilities used for tests are not production offerings. Higher autonomy requires demonstrated benefit and failure/permission controls, rather than a growing catalog alone.

## 3. Capability growth and routing

The capability catalog is the source for what exists and where its canonical package lives. The portable package owns capability logic; host adapters define discovery paths and runtime-specific behavior. Friday should not activate every capability by default. Use progressive disclosure, curated installation profiles, explicit capability contracts, and one primary capability unless a declared dependency requires another. Avoid uncontrolled recursive routing or multi-agent orchestration unless measured benefit justifies its cost and maintenance.

## 4. Repository versus runtime

The manager maturity ladder in `docs/architecture/CAPABILITY_SYSTEM_AND_ROUTING.md` governs any future move from repository umbrella to active coordination.

The Friday repository is the version-controlled source for reusable instructions, methods, templates, schemas, scripts, evaluations, and adapters. It is not automatically a running assistant, memory service, orchestrator, or application.

The eventual runtime may combine AI products, local tools, connectors, and private data stores. Decide those components from validated use cases, actual platform capabilities, costs, permissions, and evaluation—not from fictional expectations.

## 5. Long-term capability areas

| Capability | Intended responsibility | Boundary |
|---|---|---|
| Identity/preferences | Store user-approved stable preferences and working context. | Do not casually infer sensitive or permanent facts. |
| Project continuity | Track active projects, decisions, blockers, and next actions. | Do not confuse project state with general personal memory. |
| Capability registry | Know what skills exist and when they fit. | Do not create a skill for every small task. |
| Routing/orchestration | Select capabilities and coordinate handoffs. | Routing must be explainable and evaluated. |
| Tool integrations | Access permitted systems and perform authorized actions. | Least privilege and approval for consequential actions. |
| Evaluation/observability | Detect failures, regressions, cost and quality changes. | Model confidence is not proof. |
| Privacy/security | Govern access, retention, sharing, and sensitive data. | Private context must not leak into public/shared artifacts. |

## 6. Personalization principles

Prefer explicit user instructions and approved records. Distinguish an explicit fact, stated preference, temporary project constraint, AI inference, and unverified assumption. Memory should have provenance, date, scope, confidence where meaningful, and review/expiry behavior. Sensitive data receives stricter controls and is not stored merely because it might be useful.

## 7. Trust and autonomy

Friday should earn additional permissions gradually. Greater autonomy requires a bounded repeatable task, narrow permissions, understood failure/recovery paths, adequate evaluation, inspectable action history, and a revocation path. Financial, legal, reputational, privacy-sensitive, or irreversible actions require explicit authorization unless a separately reviewed policy defines a narrow safe exception.

## 8. What this vision does not authorize now

This document does not authorize a general autonomous agent, personal database, vector memory, multi-agent platform, dashboard, or broad integration layer. These remain future architecture questions. The near-term revision sequence is a verified baseline, minimal explicit manager, simpler Peanuts handoff and real host evaluation. Optional profile import follows with explicit user review; a public release remains gated by licensing, privacy and evidence.
