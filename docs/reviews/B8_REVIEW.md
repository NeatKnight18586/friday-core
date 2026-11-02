# B8 — PRD, Technical Design, and Delivery Handoff Review

**Review date:** 2026-11-01  
**Status:** PASS WITH BOUNDED LIMITATIONS — local structural, deterministic, and integration milestone  
**Scope:** B8 schemas and record contracts; project templates and initialization; Peanuts P7–P9 references; requirement, acceptance-test, build-task, artifact and demo-plan validation; cross-document traceability; EVAL-062–087; regression and package verification.

> This is a structured review using four professional perspectives. It is not four independent human reviewers, a live expert sign-off, or evidence that a product is desirable, feasible in the field, secure, or commercially viable. Scores are qualitative judgments about the implemented specification and deterministic checks, not benchmark measurements.

## 1. Consolidated verdict

**B8 is accepted as a local PRD, technical-design, and delivery-handoff foundation.** It adds explicit, inspectable contracts from evidence and decisions through requirements, acceptance tests, architecture, build tasks, artifacts, and demo claims. The implementation is additive to B1–B7 and preserves legacy workspace readability.

B8 deliberately does not convert Peanuts into an autonomous project manager, create a database or orchestration service, approve external actions, or make a weak requirement look proven. A completed P9 handoff is not permission to spend, publish, deploy, contact participants, alter permissions, or submit a project.

The deterministic checks establish data integrity and enforceable process boundaries. They do not establish that the input evidence is true, that the requirements capture actual user needs, that a design will work under real conditions, or that an LLM will follow the methods consistently.

## 2. Four-Council review

### Council 1 — Product management, requirements, and user-value quality

**Assessment: 8.8/10 — Pass with bounded limitations**

**Strengths**
- Separates requirement priority, evidence state, approval, risk, and release scope instead of collapsing them into one field.
- Requires material requirements to link to traceable origins such as claims, assumptions, decisions, findings, opportunities, council findings, artifacts, or externally sourced constraints.
- Keeps the PRD's human-readable summary distinct from the structured requirement ledger.
- Requires approved requirements to have acceptance criteria and linked active acceptance-test specifications.
- Makes unresolved assumptions, conflicting requirements, supersession, and provisional status visible rather than silently resolving them.
- Defines a P7 exit gate that requires owner approval and traceability while preserving open risks.

**Limitations**
- A traceable requirement can still be the wrong requirement if the underlying research or interpretation is weak.
- The schema cannot judge whether a metric is meaningful, a threshold is appropriate, or a requirement reflects a representative user population.
- Real user validation, baseline measurement, and outcome selection remain project-specific work.

**Recommendation**
Keep the evidence/approval separation. For consequential projects, require human review of the problem framing, user outcome measures, and any mandatory or regulated requirement. Do not treat a complete PRD as proof of product-market fit.

### Council 2 — Principal systems architecture, security, and technical feasibility

**Assessment: 8.7/10 — Pass with bounded limitations**

**Strengths**
- Technical design begins with system context, external systems, trust boundaries, data lifecycle, failure behavior, non-goals, and operational ownership.
- Architecture selection is decision-led and requires alternatives and rationale; the simplest adequate solution is preferred over fashionable infrastructure.
- Requires explicit treatment of security, privacy, abuse/misuse, accessibility, recovery, rollback, observability, cost, and maintenance where relevant.
- Keeps major technical assumptions visible and ties them to spikes/prototypes and verification methods.
- Artifact records require safe relative paths, existing files, path containment, case-insensitive uniqueness, and optional SHA-256 integrity. Symlink escapes and stale hashes are rejected.
- Legacy project workspaces without B8 records remain readable; B8 adds no mandatory database, remote service, or provider-specific runtime dependency.

**Limitations**
- A technical-design document is not a threat model review by a security specialist, penetration test, safety assessment, or production architecture sign-off.
- The validator cannot establish that a selected technology, external API, or cost estimate is current; those claims require current source inspection and runtime evidence.
- Current single-owner JSONL workflows do not provide concurrent multi-writer locking or transaction guarantees.

**Recommendation**
Keep B8 as a file-centered handoff. Add infrastructure only when a validated requirement demonstrates that the current design is inadequate. Escalate regulated, safety-critical, privacy-sensitive, or high-impact technical decisions to qualified reviewers.

### Council 3 — Engineering delivery, operations, and developer experience

**Assessment: 8.8/10 — Pass with bounded limitations**

**Strengths**
- Converts approved in-scope requirements into sequenced build tasks with owners, deliverables, exit criteria, and dependency ordering.
- Rejects missing task dependencies, dependency cycles, out-of-order prerequisites, implementation progress against unapproved requirements, and completion without evidence.
- Requires coverage of approved in-scope requirements by active tasks.
- Keeps a structured demo plan as the source of truth and a separate presenter-facing script for actual delivery.
- Distinguishes demonstrated, measured, illustrative, and hypothetical claims. Quantitative claims cannot be supported by an ordinary functional pass alone; measurement requires measured evidence or an appropriate executed measurement/performance test with inspectable reviewed evidence.
- P7, P8, and P9 stage gates are connected: P8 cannot bypass P7; P9 cannot bypass P7/P8 approval prerequisites. A non-applicable demo is allowed only with a rationale and without a fake walkthrough or claims.
- Project initialization creates valid blank B8 ledgers and templates without inventing requirement IDs or sample completion evidence.

**Limitations**
- Effort estimates and delivery dates are still judgments; the schema can require a basis/confidence note but cannot make estimates accurate.
- Real integration, deployment, operational readiness, rollback, and team-capacity constraints must be tested in the target environment.
- The build plan is a handoff artifact, not an execution engine or authorization to perform external actions.

**Recommendation**
Use the handoff to reduce ambiguity, not to manufacture precision. Keep estimates explicitly uncertain until supported by team capacity, prototypes, and delivery history. Treat production deployment and external submissions as separate approval gates.

### Council 4 — AI quality assurance, evaluation, and governance

**Assessment: 8.9/10 — Pass with bounded limitations**

**Strengths**
- Adds 26 structured B8 evaluation cases, EVAL-062–087, covering requirement provenance, acceptance-test coverage, task ordering, artifacts, privacy safeguards, demo-claim evidence, traceability, and stage gates.
- Includes schema-level checks and semantic negative tests; the tests do not rely solely on happy-path examples.
- Adds end-to-end positive and intentionally broken project-handoff fixtures.
- Tests identifier boundaries so `REQ-0010` cannot falsely satisfy a reference to `REQ-001`.
- Tests missing rubric references, duplicate demo-step IDs, misleading quantitative claims, and P9 gate bypass attempts.
- Adds rubric-reference validation so an evaluation case cannot silently point to a nonexistent rubric.
- Preserves the distinction between a case marked `ready` and an actual model evaluation result.

**Limitations**
- EVAL-062–087 are structurally valid and ready for later runtime evaluation; no live Claude, Codex, or ChatGPT Peanuts model has passed them as part of B8.
- No human-labelled calibration set, repeated-run consistency study, or comparison against a simple baseline has been completed for B8.
- Deterministic validation can reject known failure patterns but cannot prove that all relevant failure modes have been anticipated.
- Ruff was not run in this environment. The pinned Ruff package was unavailable and package installation could not reach the package index.

**Recommendation**
At B9/B10, run fixed B8 cases against actual supported hosts, repeat runs where practical, and compare with a simpler critique baseline. Record false positives, missed issues, model/version/runtime details, and human adjudication. Do not claim improved model quality based on schema or synthetic-fixture tests alone.

## 3. Defect-driven improvements made during B8

The build process exposed several concrete holes that were fixed and given regression tests:

1. **Invalid fresh-project demo reference.** The initial demo template referenced a placeholder requirement that did not exist. The template now starts with empty steps and claims, and a freshly initialized workspace is tested.
2. **Identifier substring collision.** A raw substring check could mistake `REQ-0010` for `REQ-001`. Cross-document traceability now checks identifier boundaries.
3. **Missing evaluation rubric.** Several cases referenced a rubric filename that did not exist. Those references were corrected, and the B8 validator now verifies that every referenced rubric exists.
4. **Unsupported quantitative demo claim.** A generic passing functional test could previously support a “measured” claim. Measured claims now require a measured research finding or suitable executed measurement/performance evidence with inspectable reviewed results.
5. **P9 gate bypass.** A handoff could previously appear complete while PRD and technical design were not approved. P8 now requires P7 completion; P9 requires P7/P8 approval artifacts and completed upstream stages, in addition to build/demo handoff artifacts.
6. **Demo inconsistency.** Duplicate step IDs and `not_applicable` demos containing live walkthroughs or claims are now rejected.
7. **P8 stage-order bypass.** P8 could be marked complete before P7. P8 now requires P7 completion, with a dedicated negative test and EVAL-087.

These fixes are evidence that adversarial and cross-file tests found issues that schema validation alone did not catch. An additional regression sweep found the older B6 validator was asserting on obsolete legacy-warning wording; its assertion now checks the actual optional-ledger warnings while retaining the same pass/fail contract. The test set is still not exhaustive.

## 4. Verification evidence

**Environment:** managed Linux container, Python 3.13.5. The project is a local workspace; no remote GitHub repository is configured.

| Check | Result | Interpretation |
|---|---|---|
| B8 Python compilation (`tools/b8_rules.py`, `tools/validate_b8.py`, `tests/test_b8_delivery.py`) | PASS | Changed Python files compile. |
| B8 focused test module | PASS — 54 tests | B8 schema, semantic, negative, integration, lifecycle, traceability, artifact, and stage-gate tests passed. |
| Pre-B8 regression test set | PASS — 84 tests |
| B8 validator | PASS | Five B8 record schemas/templates, 26 EVAL-062–087 cases, and rubric references validate; cases are marked ready, not model-passed. |
| B4, B5, B6, B6.5, and B7 stage validators | PASS | Individual validators passed after repairing a stale B6 legacy-warning text assertion; no B6 behavior or acceptance rule was weakened. |
| B2 validator workflow | PASS — in-process `main()` returned 0 in 28.50 seconds | All 8 B2 schemas, 87 evaluation cases, and temporary-workspace lifecycle checks passed. Direct child-process execution did not return reliably in this container, so the repository verifier's in-process route is the accepted local evidence. |
| Consolidated `verify.py --skip-lint` sequence | NOT COMPLETED | Repository integrity, B2, and B4 passed; the chained in-process run became unresponsive upon entering B5 after B2. B5 passes on its own, and all milestone validators pass individually. The cause of this same-process interaction is unresolved; it is not reported as a pass or as a functional test failure. |
| Fresh project initialization | PASS within B8 integration tests | New workspace starts with valid empty B8 structures. |
| Legacy workspace compatibility | PASS within B8 tests | A workspace without B8 ledgers remains readable. |
| Artifact security/integrity | PASS within B8 tests | Path traversal, missing files, symlink escape, case collision, and hash mismatch cases are rejected. |
| End-to-end handoff | PASS within B8 tests | Fully linked handoff passes; deliberately dangling traceability fails. |
| Repository manifest and link validation | PASS | Manifest regenerated with 323 source files; required files, Markdown links/fences, configuration contracts, heuristic secret scan, and full manifest coverage pass. |
| Full combined pytest suite | PASS — 138 tests in one run | 84 pre-B8 tests and 54 B8 tests passed together in 29.59 seconds. |
| Ruff | NOT RUN | Ruff was not installed; package index access was unavailable. |
| GitHub Actions / Codespaces | NOT RUN | No remote repository or cloud execution was available. |
| Claude Code / Codex / ChatGPT live skill runtime | NOT RUN | No live host-runtime evaluation was executed in this milestone. |

The full combined pytest run completed successfully: **138 passed in 28.34 seconds** in the working copy and **138 passed in 23.97 seconds** from the final clean ZIP extraction. This comprises the 84 pre-B8 regression tests and 54 B8-focused tests. B2 also completed through the in-process validator route. The separate consolidated verifier sequence did not complete because of the documented B2→B5 same-process interaction; individual stage validators and the complete pytest suite passed.

## 5. Residual risks and release conditions

- **Model behavior:** Run EVAL-062–087 on supported model hosts; distinguish runtime compliance from structural validity.
- **Calibration:** Compare Four-Council/B8 outputs with a simple baseline and human-labelled cases; measure false positives, false negatives, repeatability, and review effort.
- **Real-world validity:** Test user needs, usability, feasibility, performance, security, and operational readiness with actual evidence appropriate to the project.
- **Security and privacy:** Obtain specialist review for material threat, privacy, safety, and regulated-data concerns. The schemas are safeguards, not legal or security certification.
- **Cross-platform and host compatibility:** Run configured GitHub Actions, Codespaces, Claude Code, Codex, and ChatGPT routes where supported.
- **Concurrency:** Add controlled writes/locking only if multiple simultaneous writers become a demonstrated need.
- **Publication:** A release archive is not a public release. The owner separately approves repository visibility, publication, deployment, spending, and external submissions.

## 6. B8 disposition

**PASS WITH BOUNDED LIMITATIONS** as a local structural and deterministic-validation milestone, conditional on the final repository-integrity, full-regression, and clean-extraction checks recorded in the delivery evidence. B9 may proceed after those local checks pass. B10 remains responsible for full release verification and actual host-runtime evaluation.
