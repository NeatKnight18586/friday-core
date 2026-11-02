# Peanuts JSON Schemas

Schemas use JSON Schema Draft 2020-12. They validate record structure and selected field constraints, not factual correctness or business logic. Cross-record integrity and state invariants are checked by `tools/validate_project.py`.

| Schema | Validates |
|---|---|
| `project.schema.json` | Project identity, mode, status, desired outcome and constraints |
| `project-state.schema.json` | Current stage, blockers, pending decisions and next action |
| `source-record.schema.json` | Provenance and source assessment |
| `claim-record.schema.json` | Claim class, origin, evidence status and source references |
| `assumption-record.schema.json` | Uncertainty, criticality, test plan, and controlled acceptance rationale |
| `assumption-test.schema.json` | Pre-registered test protocol, human-participant safeguards, result, and evidence |
| `council-review.schema.json` | Four-Council dimensions, findings, reviewer setup, event overlay, and progression gate |
| `decision-record.schema.json` | Options, status, approval and evidence rationale |
| `evaluation-case.schema.json` | Synthetic test scenario and expected behavior |
| `evaluation-result.schema.json` (actual executed runs only; do not store hypothetical `not_run` results) | Actual evaluation run record |

Schema changes require a schema version/migration decision and regression examples. The project currently uses schema version `1.0.0`.

## B6 NUTS records

- `analogy-card.schema.json` — source/claim-linked analogy candidate, mapping, mismatch, test, rights, and assessment record.
- `nuts-run.schema.json` — target function, searched domains, coverage, analogy references, conclusion, and next action.

Templates: `templates/records/analogy-card.json` and `templates/records/nuts-run.json`. Project JSONL ledgers: `analogies.jsonl` and `nuts-runs.jsonl`.


## B7 review and validation records

Project ledgers: `council-reviews.jsonl` and `assumption-tests.jsonl`. Templates: `templates/records/council-review.json` and `templates/records/assumption-test.json`. Cross-record and progression-gate invariants are checked by `tools/validate_project.py` and `tools/b7_rules.py`. Older workspaces may omit these B7 ledgers and remain compatible; the validator reports a migration warning.


## B8 product and delivery records

- `requirement-record.schema.json` — atomic product requirements with provenance, approval, priority, scope, conflicts/dependencies, and measurable acceptance criteria.
- `acceptance-test.schema.json` — planned/ready/executed/not-applicable/blocked/cancelled test specifications, linked to requirement criteria and guarded for consent, privacy, and execution evidence.
- `build-task.schema.json` — owned delivery tasks, sequencing/dependencies, exit criteria, status reasons, and completion evidence.
- `artifact-record.schema.json` — stable metadata for project deliverables and safe workspace-relative paths. File existence, symlink/path safety, path collisions, and optional SHA-256 integrity are semantic checks.
- `demo-plan.schema.json` — structured walkthrough, requirement links, demo-claim strength/evidence, data controls, failure fallback, and limitations.

Project JSONL ledgers: `requirements.jsonl`, `acceptance-tests.jsonl`, `build-tasks.jsonl`, and `artifacts.jsonl`; the project root also contains `demo-plan.json`. `tools/validate_project.py` runs B8 semantic checks after schema checks, including cross-document traceability and P7–P9 completion gates.
