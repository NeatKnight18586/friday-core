# Technical Design and Feasibility (B8 / P8)

## Purpose

Translate the approved or explicitly provisional PRD into a feasible, secure, maintainable design and expose what still needs a prototype, expert review, or evidence. The goal is the simplest adequate design—not an impressive technology stack.

## Entry and scope

Read the approved PRD (or clearly provisional draft), relevant requirements, decisions, assumptions, constraints, and unresolved Four-Council findings. Identify project type: software, hardware, service, event/operations, mixed, or not applicable. Adapt the document accordingly; do not force software architecture onto a non-software problem.

## Design procedure

1. Define system context, users, external systems, environment, trust boundaries, ownership, and explicit non-goals.
2. Derive components and responsibilities from requirements. Describe inputs, outputs, state, and failure boundaries.
3. Select architecture patterns only when they solve a demonstrated problem. Compare credible alternatives and the simplest adequate option.
4. Specify interfaces and contracts: data formats, API assumptions, events, permissions, error behavior, timeouts, retries, idempotency, and human handoffs.
5. Model data lifecycle and sensitivity: collection, purpose, minimization, validation, ownership, access, retention, deletion, backup, and migration.
6. Analyze security, privacy, safety, abuse/misuse, accessibility, and operational risks. Include attacker/operator failure paths where relevant.
7. Define degraded modes, recovery, rollback, observability, support, maintenance, and resource/cost boundaries.
8. Map requirements to verification methods and test IDs. Separate proposed tests from executed evidence.
9. Record technology choices as decisions with context, alternatives, rationale, consequences, evidence, and revisit triggers.
10. Identify technical assumptions that can invalidate the design and design the smallest useful spike/prototype to test them.

## Technical honesty

Never claim a vendor API, platform, device, library, model, pricing tier, or standard has a capability without current evidence. Mark external dependencies as `verified`, `supported`, `preliminary`, or `unknown`; record versions and access dates. A prototype proves only what was actually tested in its environment. A design review is not a security audit, certification, or specialist sign-off.

## Proportionate architecture

Do not add databases, cloud infrastructure, vector search, multi-agent orchestration, event buses, queues, microservices, custom authentication, or custom APIs by default. State the concrete requirement that makes an added component necessary, the simpler alternatives considered, operational costs, credential/security implications, and rollback path. Friday remains an umbrella; a Friday manager/control plane remains optional and evidence-dependent.

## Exit gate for P8

P8 can be marked complete only when the technical-design artifact is owner-approved (or explicitly marked N/A with rationale), every selected major design choice has a traceable rationale, relevant security/privacy/reliability/operations constraints are addressed, unresolved feasibility assumptions have owners and test/spike plans, and the verification strategy maps back to requirements. Missing specialist expertise is recorded as an escalation, not simulated approval.
