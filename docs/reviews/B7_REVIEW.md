# B7 — Four-Council and Assumption Validation: Four-Council Review

**Review date:** 2026-11-01  
**Status:** Passed as a local structural and deterministic-validation milestone; live model calibration and host runtime remain pending.  
**Scope:** Four-Council review schema/template, assumption-test schema/template, B7 semantic cross-record rules, project initializer and validator integration, B7 Peanuts references, evaluation cases EVAL-051–061, and regression results.

This is a structured review using four perspectives. It is not four independent human experts. The implementation's schema and tests are evidence of structural behavior only; they do not prove that an AI model will apply the rubric correctly or that project conclusions are true.

## Council 1 — Product Decision Quality and Governance

**Assessment: 8.8/10 — Pass with bounded limitations**

Strengths:
- Preserves all 16 core dimensions at every review depth. Quick mode uses `UNKNOWN`/`N_A` instead of silently deleting dimensions.
- Separates product-merit review from the Event Alignment Overlay.
- Keeps council recommendations separate from the user's decision/approval.
- Does not average scores; critical/high open findings are non-compensatory blockers.
- Uses stable IDs and records concept version, review depth, evidence-pack scope, verdict, gate and limitations.

Limitations:
- Dimension scores remain judgments requiring calibrated examples and human-labelled review cases.
- A structured report can still be biased, incomplete or overly confident if the model does not follow the procedure.
- Event criteria can be structurally recorded, but their factual compliance requires inspected organizer evidence and sometimes human/legal review.

Recommendation: Keep the fixed core dimensions and non-compensatory gate. Calibrate the rubric using known-answer and blind cases before making performance claims.

## Council 2 — Assumption Testing, UX Research and Ethics

**Assessment: 8.9/10 — Pass with bounded limitations**

Strengths:
- Separates the assumption from the test designed to investigate it.
- Requires a falsifiable hypothesis, steps, success/failure signals, decision threshold, scope and known limitations.
- Completed tests need an outcome, completion date, evidence reference, limitations and protocol deviations.
- Human interview/observation/usability methods must declare human participation.
- Test planning may precede consent, but approval/execution/completion requires obtained consent, de-identification and an appropriate ethics-review disposition.
- Consent withdrawal forces the test into a cancelled state with no completed result.
- A `supported` or `invalidated` assumption requires a corresponding completed test outcome.

Limitations:
- The schema cannot determine whether a consent process is genuinely informed or whether an ethics review is legally/institutionally sufficient.
- Project records intentionally exclude direct identifiers; secure handling of consent forms, recordings and identity mappings remains an operational responsibility outside this repository.
- The method does not automatically establish sample representativeness, causal validity, saturation or generalizability.

Recommendation: Retain the lifecycle-sensitive safeguards. Use local institutional and jurisdiction-specific requirements when conducting real human research; do not treat the schema as legal or ethics approval.

## Council 3 — Principal Systems Architect and Software Engineer

**Assessment: 8.7/10 — Pass**

Strengths:
- Introduces two bounded append-oriented ledgers rather than a new database or orchestration service.
- Reuses existing source, claim, assumption, decision, research and NUTS records for provenance.
- Adds semantic validation for dangling references, duplicate review/finding IDs, reviewer-setup disclosure, event-criterion evidence, assumption/test state consistency, and progression-gate invariants.
- New project initialization creates the B7 ledgers; older workspaces without them remain readable with a migration warning and are not silently modified.
- `validate_project.py` supports both package import and direct script execution, preserving the B2 subprocess workflow.
- Friday remains an umbrella; B7 does not introduce a multi-agent manager or provider-specific runtime dependency.

Limitations:
- JSONL is suitable for the current single-owner sequential workflow, but concurrent writers would need locking or a controlled write service.
- There is no automated migration tool because the new ledgers are additive; future breaking schema changes still require explicit migration design.
- A review can reference artifact IDs, but artifact-path existence is not yet verified by the project validator.

Recommendation: Keep JSONL for the current project scale. Revisit concurrency controls only when actual multi-writer/runtime usage exists. Consider artifact-path verification when artifact linking becomes a routine workflow.

## Council 4 — AI Quality, Evaluation and Assurance

**Assessment: 8.6/10 — Pass with bounded limitations**

Strengths:
- Adds EVAL-051–061 for critical blockers, reviewer-independence disclosure, unknown scoring, event-overlay separation, accepted-risk conditions, non-waivable critical compliance, human-participant controls, completed-test evidence, assumption/test consistency, quick-depth comparability, and mandatory event-rule blockers.
- Adds schema and semantic negative tests, not only happy-path checks.
- Adds an operational reference and rubric for future live review runs.
- Explicitly prevents the four lenses from claiming statistical independence.
- The one-command verifier now includes the B7 structural validator.

Limitations:
- EVAL-051–061 are synthetic cases marked `ready`; no live Peanuts model has passed them.
- No comparison against a simple-critique baseline has been performed.
- No human-labelled calibration set or repeatability study exists yet.
- Ruff was not run in the managed environment; remote GitHub Actions, Codespaces, Claude Code, Codex and ChatGPT runtime tests remain pending.

Recommendation: Keep the tests as a versioned starter set. At B10, run the same cases against actual supported hosts and compare against a simpler critique baseline before claiming improved decision quality.

## Consolidated verdict

**PASS WITH BOUNDED LIMITATIONS.** B7 is accepted as a local structural, record, and deterministic-validation milestone. It makes the review process persistent and its most important gate rules machine-checkable. It does not prove model-quality calibration, independent expertise, legal/ethics compliance, or improved real-world decisions.

## Verification evidence

- `python tools/validate_b7.py` — passed.
- `python tools/validate_b2.py` — passed after fixing the direct-execution import path for `tools/b7_rules.py`.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q` — 84 tests passed in the managed Linux/Python 3.13.5 environment.
- Full repository verifier and package extraction checks are recorded in the B7 delivery report/package; Ruff, remote CI and runtime checks are explicitly not run where unavailable.

## Follow-up and release gates

1. Run Ruff and full CI in a network-enabled environment.
2. Execute GitHub Actions and Codespaces after private upload.
3. Run live Claude/Codex/ChatGPT evaluations where account and host support allow.
4. Calibrate Four-Council against a simpler critique baseline using fixed cases, human-labelled findings and repeated runs where practical.
5. Add concurrent-write protection only when multiple writers are introduced.
