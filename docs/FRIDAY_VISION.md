# Friday — Long-Term Vision and Boundaries

**Status:** Directional draft; not an implementation specification  
**Version:** 0.2.0-draft  
**Last updated:** 2026-10-31

## 1. North star

Friday is the long-term personal AI environment the owner hopes to build: an assistant that can understand relevant preferences and goals, maintain useful continuity across projects, bring specialized capabilities to the right tasks, work with permitted tools, and help turn ideas into completed work.

The inspiration is a real-world personal assistant with the continuity and usefulness associated with fictional assistants such as JARVIS or FRIDAY. The engineering objective is not to reproduce fiction or promise human-like understanding. It is to build a practical, inspectable, secure, and increasingly capable system whose behavior is grounded in user-approved context, clear permissions, and measurable performance.

## 2. Friday is not one giant skill

Friday should eventually coordinate multiple capabilities. Examples may include research, writing, project planning, learning support, software development, content production, and personal productivity. These are future possibilities, not approved build commitments.

Each capability should:

- Have a clearly defined job and boundary.
- Be independently understandable and testable.
- Declare inputs, outputs, dependencies, and permissions.
- Reuse common Friday standards without duplicating them.
- Be removable or replaceable without breaking unrelated capabilities.

Peanuts is the first capability because it is a bounded, useful project that can teach us how to create and maintain skills. It must remain useful on its own and extractable from Friday if needed.

## 3. The repository is not the assistant

The Friday Git repository is the version-controlled source for reusable instructions, methods, templates, schemas, scripts, evaluations, and adapters. It is not automatically a running assistant, memory service, orchestrator, or application.

The eventual runtime may consist of one or more AI products, local tools, connectors, and private data stores. That design must be decided from real use cases and verified constraints rather than assumed now.

## 4. Long-term capability areas to investigate

| Capability area | Intended responsibility | Important boundary |
|---|---|---|
| Identity and preferences | Store user-approved stable preferences and working context. | Do not infer sensitive or permanent facts casually. |
| Project continuity | Track active projects, decisions, blockers, and next actions. | Project state must not be confused with general personal memory. |
| Skill registry | Know what capabilities exist and when they are appropriate. | Do not create a skill for every small task. |
| Routing and orchestration | Select an appropriate capability and coordinate handoffs. | Routing must be testable and explainable. |
| Tool integrations | Access permitted external systems and perform authorized actions. | Least privilege and explicit approval for consequential actions. |
| Evaluation and observability | Detect failures, regressions, cost, and quality changes. | Do not treat model confidence as proof. |
| Privacy and security | Control access, retention, sharing, and sensitive information. | Private information must not leak into public repository artifacts. |

## 5. Personalization principles

Friday should learn from explicit user instructions and approved records first. It may suggest that a preference or recurring pattern be saved, but should distinguish:

- A fact explicitly supplied by the user.
- A preference explicitly stated by the user.
- A temporary project constraint.
- An AI-generated inference.
- An unverified assumption.

Memory should carry provenance, date, scope, confidence where meaningful, and review or expiry behavior. Sensitive personal information requires stricter handling and should not be stored merely because it might be useful.

## 6. Trust and autonomy direction

Friday should earn additional permissions gradually. The initial operating model is assistive and human-directed. Greater autonomy may be considered only when:

1. The task is well-bounded and repeatable.
2. The action permissions are narrow and explicit.
3. Failure modes and recovery are understood.
4. Evaluation demonstrates adequate performance.
5. The user can inspect what happened and revoke access.

External actions with financial, legal, reputational, privacy, or irreversible consequences require explicit authorization unless a future, separately reviewed policy defines a safe bounded exception.

## 7. What this vision does not authorize now

This document does not authorize building a general autonomous agent, long-term personal database, vector memory system, multi-agent platform, dashboard, or broad integration layer. Those remain future architecture questions. The near-term goal is to make Peanuts work well and teach us which shared Friday foundations are genuinely needed.
