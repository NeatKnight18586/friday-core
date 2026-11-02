# Vertical-slice workflow contract

This reference defines the minimum connected workflow. It is intentionally smaller than the full Peanuts roadmap.

## Stage contract

| Stage | Purpose | Required input | Output | Exit condition |
|---|---|---|---|---|
| P1 — Intake/intelligence | Understand the opportunity and rules | Event/idea name, URL, or brief | Event/Idea Dossier | Purpose, constraints, sources, unknowns recorded |
| P2 — Problem discovery | Understand people and the problem | P1 dossier and available evidence | Problem Brief | User/problem hypotheses and evidence gaps explicit |
| P3 — NUTS exploration | Search for useful cross-domain mechanisms | Defined target function/problem | Analogy Card or documented no-analogy decision | Transfer logic and limitations assessed; weak analogy rejected |
| P4 — Concept refinement | Form and compare candidate concepts | P1–P3 outputs | Concept Brief | A candidate is selected for review, with rationale and assumptions |
| P5 — Quick Four-Council | Challenge the candidate | Concept, evidence, constraints | Quick Council Review | Four lenses covered; critical risks and disposition recorded |
| P6 — Assumption validation | Test highest-risk unknowns | Council findings and assumption register | Validation Plan or report | Critical assumptions tested or explicitly left open |
| P7 — Product definition | Translate concept into requirements | P1–P6 evidence and decisions | Draft PRD | Requirements traceable and acceptance criteria testable |

P7 can be drafted provisionally while P6 is pending, but it cannot be approved as a product baseline until critical prerequisites are resolved or consciously accepted by the owner.

## Handoff fields

Every resumable handoff should state:

- Project ID and mode.
- Current stage and status.
- Completed stages and evidence for completion.
- Approved decisions versus proposals.
- Current source/claim/assumption/decision record IDs.
- Open risks, blockers, and validation gaps.
- Exact next action and who owns it.
- Files/artifacts that the next session must read.

## Tool unavailable behavior

If a stage requires a tool that the host does not provide, do not simulate the missing capability. State what is unavailable, identify what can still be done, and create a bounded next step (e.g., ask for an official rulebook, prepare search queries, or create a test plan).

## Stop / escalation conditions

Pause or escalate when:

- Event eligibility, legal terms, or critical judging requirements cannot be verified.
- A material source conflict affects a decision.
- A safety, privacy, security, or regulatory risk is critical or outside Peanuts' competence.
- Direct user evidence is necessary but unavailable.
- The proposed architecture depends on an untested external capability.
- The user has not approved a consequential decision.
