# Four-Council Review — Operational Reference (B7)

Load this reference when a concept requires a structured critical review. The canonical rubric and data contract are in `docs/methods/FOUR_COUNCIL_PROTOCOL.md` and `schemas/council-review.schema.json`.

## Select depth

- **Quick:** early, low-commitment screening. Keep every core dimension visible; use `UNKNOWN` or `N_A` rather than silently omitting a dimension. Never call a quick screen validated or final clearance.
- **Standard:** default for a leading concept or before committing meaningful effort. Apply all applicable dimensions, record evidence, findings, assumptions and next tests.
- **Deep:** use for material safety, privacy, legal, financial, reputational, delivery or event-compliance consequences; novel dependencies; expensive/irreversible commitments; conflicting decisive evidence; or a proposed implementation baseline. Add focused research, counterexamples, failure scenarios and human/domain review where warranted.

Depth changes evidence-gathering effort, not the core scoring dimensions or the 1–5 anchors.

## Four lenses and ownership

1. **C1 Human Value:** problem evidence, user fit, outcome relevance, usability/accessibility.
2. **C2 Strategic Value:** differentiation, value proposition, adoption/operating model, strategic fit.
3. **C3 Technical Feasibility:** technical plausibility, integration/data, product quality, resource fit.
4. **C4 Red Team/Delivery:** risk/harm controls, delivery readiness, resilience/failure handling, assumption challenge.

Use the dimension-specific anchors in the canonical protocol. Scores are judgments; evidence status is separate. `UNKNOWN` is not a score of 3. `N_A` needs a reason. A `VERIFIED` rating must link to evidence.

## Findings and progression gate

For every material issue, assign one primary owner, a severity, status, evidence status, and evidence links. Other councils may challenge but must not double-count the same issue.

- Critical or high **open** findings block progression and must appear in `gate.blocking_finding_ids`.
- `ADVANCE` requires a passing gate and no unresolved critical/high findings.
- Accepted high residual risks require explicit rationale, named acceptor and revisit trigger; the gate must be `pass_with_conditions`, not `pass`.
- Critical risks cannot be marked `accepted_with_rationale`.
- Safety, legal/regulatory and mandatory-compliance findings cannot be waived through this acceptance status.
- Mitigation requires a resolution summary and evidence. Do not mark a risk mitigated merely because a mitigation was proposed.

A council review is a recommendation, not the user's approval. Record the user's decision separately.

## Reviewer independence

Record the actual execution pattern. Four sequential perspectives from one model are not independent experts. Blind passes can reduce anchoring but do not establish statistical independence. For deep reviews, add distinct models, human domain reviewers or user evidence where the stakes justify it, and disclose what was actually used.

## Event Alignment Overlay

Keep eligibility, official event rules and judging alignment separate from product-merit scores. Use official weights only when the organizer publishes them. Assessed criteria need evidence references; unknown criteria stay unknown.

## Required output

Include: concept/version, depth and reason; evidence pack and as-of date; all four council findings; dimension scores and rationales; critical assumptions; severity-ranked issues; event overlay when relevant; gate status; verdict; limitations; and user decision status.

## Context efficiency

Read the canonical protocol and this reference. Retrieve only the evidence pack and records relevant to the concept. Do not load all project ledgers or unrelated Peanuts references. Use scripts to validate IDs and links; report concise findings rather than dumping full records.
