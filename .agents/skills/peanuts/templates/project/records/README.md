# Project record files

The initializer creates empty JSONL ledgers. Append one JSON object per line when a record is needed. Validate each record against its matching schema and preserve stable IDs.

Core evidence/decision records:
- `sources.jsonl` — source provenance and source quality assessment.
- `claims.jsonl` — decision-relevant factual or interpretive claims and evidence status.
- `assumptions.jsonl` — uncertain beliefs and planned tests.
- `decisions.jsonl` — choices, alternatives, evidence and approval status.

Research/discovery records:
- `research-questions.jsonl` — questions that the research plan must answer.
- `research-rounds.jsonl` — planned/conducted user or field research rounds. Use pseudonymous participant references only.
- `research-findings.jsonl` — de-identified findings linked to sources, claims, questions and rounds.
- `opportunities.jsonl` — solution-neutral user opportunities linked to findings and claims.

Never put names, contact details, raw recordings, signed consent forms, or unnecessary sensitive data in this repository. Store identifiable research material only in appropriately protected storage under applicable consent, retention, and access rules.

NUTS innovation records:
- `analogies.jsonl` — sourced analogy cards with source/claim links, relational mappings, mismatches, test plans, attribution and disposition.
- `nuts-runs.jsonl` — run-level target function, source domains actually searched, method components, coverage and conclusion (including a documented no-useful-analogy outcome).

Do not add a real analogy to `analogies.jsonl` without linked project source and claim records. A NUTS run may conclude that no useful analogy was found.


B7 review and validation records:
- `council-reviews.jsonl` — versioned Four-Council reviews, dimension scores, evidence pack, findings, reviewer setup, event overlay, verdict, and gate disposition.
- `assumption-tests.jsonl` — planned/executed tests linked to assumptions, with preregistered signals, participant controls, outcomes, and evidence.

A review record is not a human approval. A model-simulated four-lens review must explicitly disclose its reviewer setup and must not claim statistical independence. An unresolved critical/high finding blocks ADVANCE. Legal, safety, and mandatory compliance duties cannot be waived by recording an accepted risk.

Assumption tests must be planned before execution. A completed test requires a result summary and at least one traceable evidence reference. When people participate, obtain appropriate consent, minimize data, de-identify records, and assess whether institutional/ethics review is required. Keep identifying data and raw recordings outside this repository.


B8 product and delivery records:
- `requirements.jsonl` — atomic, prioritized requirements with evidence origins, approval status, acceptance criteria, dependencies and conflicts.
- `acceptance-tests.jsonl` — test specifications linked to requirement criteria; planned tests are not test passes. Executed human-participant tests require consent and an appropriate review disposition.
- `build-tasks.jsonl` — owned work packages, dependency graph, exit criteria, estimates with confidence, and completion evidence.
- `artifacts.jsonl` — stable artifact IDs and safe relative paths; the validator checks that referenced files exist inside the project.

The project root also contains `PRD.md`, `TECHNICAL_DESIGN.md`, `BUILD_PLAN.md`, `DEMO_PLAN.md`, and structured `demo-plan.json`. Approval remains an explicit owner decision.
