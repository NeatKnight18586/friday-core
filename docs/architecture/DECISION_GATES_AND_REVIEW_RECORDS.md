# Decision Gates and Review Records

**Status:** B7 implementation specification, draft 1.0.0

## Purpose

Make Peanuts' critical reviews and assumption tests persistent, traceable and machine-checkable. A review document is not an approval, and a proposed experiment is not evidence that it occurred.

## Records

- `records/council-reviews.jsonl` — one versioned review per concept version and review pass. Uses `council-review.schema.json`.
- `records/assumption-tests.jsonl` — one planned or executed test linked to an assumption. Uses `assumption-test.schema.json`.
- `records/assumptions.jsonl` remains the canonical assumption ledger. `supported` and `invalidated` require matching completed test outcomes; accepted-with-rationale requires a rationale, acceptor and revisit trigger.

New projects receive the ledgers. Older workspaces without them remain compatible and are treated as empty until initialized; validation reports a migration warning rather than silently creating files.

## Review contract

A review preserves all 16 core dimensions across quick, standard and deep depth. In quick mode, unknowns are explicit; depth never removes a dimension or weakens a safety rule. The four lenses have stable ownership. Event Alignment remains a separate overlay.

Reviewer setup records whether the review used one model sequentially, blind passes, multiple models, human reviewers or a mixed setup. Same-model sequential review cannot claim independence.

## Gate invariants

1. Critical/high open findings are blockers and must appear in the gate's blocker list.
2. `ADVANCE` requires `pass` or `pass_with_conditions` and no unresolved critical/high finding.
3. A `pass` gate cannot retain blockers.
4. Accepted high residual risk requires explicit rationale, acceptor and revisit trigger, and must use `pass_with_conditions`.
5. Critical findings cannot be accepted with rationale. Safety, legal/regulatory and mandatory-compliance findings cannot use that waiver status.
6. Mitigated findings require a resolution summary and traceable evidence.
7. The user's decision is recorded separately from the council verdict.

These are minimum structural rules. A schema-valid record still needs human judgment and appropriate evidence.

## Assumption-test invariants

A test is designed before execution: hypothesis, steps, success/failure signals and decision threshold are recorded. A completed test requires a result, completion timestamp, evidence references and limitations. Human-participant methods require participant safeguards. Project ledgers contain only pseudonymous, de-identified findings; do not store direct identifiers or raw recordings.

## Validation

`tools/validate_project.py` checks record schemas and cross-links. `tools/validate_b7.py` checks B7 schemas, templates and evaluation cases. `tools/verify.py` runs all milestone validators and the Python regression suite. Structural checks do not prove that a model follows the protocol or that a finding is true; live model evaluations remain separate.
