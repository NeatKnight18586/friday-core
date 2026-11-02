# PRD and Requirement Engineering (B8 / P7)

## Purpose

Turn the approved problem/concept direction and evidence into a product definition that a team can inspect, challenge, estimate, build, and verify. The PRD is a decision artifact—not a persuasive pitch and not proof that the product should exist.

## Entry conditions

Before drafting, load only the relevant project brief, current state/handoff, approved decisions, high-impact findings, open Four-Council findings, critical assumptions/tests, and event or external constraints. Confirm that the current concept version is the one being specified.

A draft can proceed while evidence is incomplete. The document and requirement records must make that incompleteness visible. Do not convert an assumption into a user need or a recommendation into an approved decision.

## Requirement-writing method

For each material requirement:

1. Express one behavior, quality attribute, boundary, or obligation. Avoid bundling unrelated outcomes.
2. Identify the intended actor and context where useful.
3. Give it a stable `REQ-###` ID, type, priority, release scope, owner, and status.
4. Link the actual origin: source, claim, assumption, research finding, opportunity, decision, council finding, artifact, or an inspectable external requirement. A free-floating assertion is not traceability.
5. Label the evidence state separately from approval. `verified`, `supported`, `preliminary`, `assumption`, `unknown`, and `constraint` are not priority labels.
6. Write one or more observable acceptance criteria using `AC-###`. State the pass condition and how it will be verified.
7. Record dependencies and conflicts. Resolve contradictions; do not quietly choose whichever requirement is convenient.
8. Identify MVP, post-MVP, or out-of-scope disposition. Keep must-have scope small enough to be delivered and tested.
9. Add a linked acceptance-test specification for every criterion before approving a material requirement.

Use `records/requirements.jsonl` as the machine-checkable source of truth. The PRD's table is a human-readable summary. Use `records/acceptance-tests.jsonl` for test designs. A test marked planned/ready has not passed.

## Acceptance-criteria quality

A criterion should make it possible for two competent reviewers to agree whether it passed. Prefer observable outcomes, bounded thresholds, explicit conditions, and failure behavior. Avoid phrases such as “fast,” “easy,” “secure,” “intuitive,” “robust,” or “high quality” unless operationalized.

Use verification methods deliberately:

- `test`: observable behavior under stated conditions.
- `inspection`: inspect an artifact, configuration, or implementation.
- `analysis`: reason from an explicit model or evidence set.
- `demonstration`: show the implemented behavior; do not substitute a mockup for a real capability without labeling it.
- `measurement`: compare a measured result with a declared threshold and environment.
- `usability_test`: task-based evaluation with appropriate participants and consent.
- `security_test`: threat-informed security check; a checklist alone is not a penetration test.
- `review`: qualified human review when judgment, policy, or domain expertise is needed.

## Priority, evidence, and approval

Keep priority, evidence quality, uncertainty, risk, and approval separate. A high-priority requirement can be weakly evidenced; it should then remain provisional or carry an explicit owner-approved risk and revisit trigger. Mandatory legal, safety, privacy, security, accessibility, and event requirements cannot be waived by averaging or a general owner preference. Verify the actual applicable authority and jurisdiction.

An approved requirement needs an approval identity/date, at least one acceptance criterion, and a linked active acceptance-test specification. Mandatory/compliance requirements need current supporting evidence before approval. Conflicting approved requirements are invalid.

## User-value and outcome measures

Prefer measures tied to the user outcome, baseline, target, population, timeframe, and collection method. Separate product output metrics from user outcomes and guardrails. If no baseline exists, state that and plan how to establish one; do not invent a number to make the PRD look complete.

## Change control

Do not silently overwrite a requirement's meaning. Create a new ID or record an explicit supersession, explain the reason and impact, update dependent criteria/tests/tasks, and preserve the historical reference. Revisit a requirement when its evidence, assumptions, constraints, or context changes.

## Exit gate for P7

P7 can be marked complete only when the PRD artifact is explicitly approved by the owner, in-scope material requirements trace to origins, approved requirements are testable and linked to test specifications, contradictions are resolved or visibly blocked, and unresolved assumptions/risks remain visible. Approval of a document is not approval to spend, publish, or execute external actions.
