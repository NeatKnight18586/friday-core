# Peanuts Quality Assurance and Evaluation Standard

**Status:** B2 evaluation foundation delivered; runtime and method performance evaluation remains in B3–B10  
**Version:** 0.4.0-draft

## 1. Purpose and honest quality claim

Peanuts cannot guarantee that every AI conclusion is correct. It can make quality expectations explicit, enforce checks where possible, evaluate judgement with anchored rubrics, preserve evidence, and disclose unresolved limitations.

Quality is fit-for-purpose and risk-proportionate. A short event fact sheet and a safety-sensitive technical plan do not need identical checks.

## 2. Five quality layers

1. **Method selection:** Was the relevant discipline/method chosen for the decision?
2. **Method fidelity:** Were prerequisites, steps, scope, and limitations respected?
3. **Evidence and provenance:** Are material claims supported and traceable to sources, observations, or tests?
4. **Independent challenge:** Were alternatives, counterevidence, uncertainty, contradictions, and failure modes examined?
5. **Acceptance:** Does the output meet defined criteria, and are residual gaps disclosed or escalated?

## 3. Verification versus validation

- **Verification:** Does the artifact/system meet its specified requirements? Examples: links resolve, JSON validates, required fields exist, acceptance tests pass.
- **Validation:** Does the concept/system solve the intended problem in its real context? Examples: user observation, task tests, field pilots, actual outcome evidence.

Passing structural checks is not proof of desirability. Positive interview feedback is not proof of technical security or reliability.

## 4. Evaluation methods

Use an appropriate combination:

- Deterministic checks: links, IDs, schemas, date formats, file presence, state transitions, source metadata, policy rules.
- Rubric-based/model grading: relevance, completeness, method fidelity, evidence quality, clarity, and actionability.
- Human evaluation: user value, originality, acceptability, risk judgement, and consequential decisions.
- Outcome evaluation: observed task success, prototype use, implementation outcomes, operational behavior, event results, and retrospective evidence.

Calibrate model graders against human-labelled examples before relying on them. Keep reference cases separate from evaluation cases where possible to reduce overfitting. Do not claim statistical significance, inter-rater reliability, or improved decision quality without suitable design and sample size.

## 5. Evaluation case design

For each core method, maintain a versioned case set with:

- Standard/straightforward case.
- Vague or incomplete input.
- Conflicting evidence.
- Misleading or stale source.
- Edge case and constraint-heavy case.
- Adversarial/untrusted content case where relevant.
- Known failure or deliberately invalid case.
- A case where the correct action is to ask, defer, reject, or report unknown.

Compare proposed method changes with a simpler baseline when claiming the method adds value.

## 6. Example metrics

Choose a small number relevant to the use case:

- Claim/source traceability rate.
- Unsupported factual claim count/severity.
- Required-constraint detection (recall on seeded constraints).
- Irrelevant/unsupported finding rate.
- Assumption and unknown identification.
- Method prerequisite compliance.
- Useful/actionable test recommendations.
- Critical-risk detection on known test cases.
- Human usefulness/decision-change rating.
- Regression pass rate, runtime, and cost where available.

Metrics must have a defined numerator, denominator, and interpretation. Avoid composite quality scores unless justified and calibrated.

## 7. Output status labels

Use descriptive statuses, not a single quality percentage:

- `DRAFT` — generated but not materially reviewed.
- `DESK-RESEARCHED` — relevant secondary/official research performed; not user validated.
- `USER-EVIDENCE-INFORMED` — direct user evidence informed the work; sample and limitations disclosed.
- `TECHNICALLY-SPIKED` — a limited technical proof/test was run; scope disclosed.
- `TESTED` — specified tests were run and results recorded.
- `VALIDATED-IN-CONTEXT` — a defined real-context validation test supports a stated outcome; not a universal success guarantee.
- `BLOCKED` — a critical prerequisite/risk prevents progression.

A document can combine several statuses by claim or section. Avoid applying one label to an entire project if its evidence varies.

## 8. Quality gates

- Method and discipline fit checked.
- Required method prerequisites checked or adaptation disclosed.
- Material facts traceable to sources with dates.
- Assumptions, unknowns, and counterevidence visible.
- Required constraints and acceptance criteria addressed.
- Privacy, security, legal, safety, accessibility, and participant protections considered where relevant.
- Four-Council or other review completed when warranted.
- Human/expert escalation made where required.
- Project state and limitations recorded.

## 9. AI-specific risk governance

Use NIST AI RMF and the Generative AI Profile as voluntary risk-management references, tailoring controls to actual model use, data, tools, and impacts. Use OWASP GenAI/agent guidance as threat-discovery input. Treat prompt injection, insecure output handling, sensitive information disclosure, supply-chain issues, excessive agency, overreliance, and unbounded consumption as relevant threat classes where applicable.

Do not assume that an instruction in a prompt enforces a permission. Use runtime permissions, restricted file scopes, confirmation for consequential actions, output validation, logging, and other deterministic controls as capabilities become available.

## 10. Release and change control

Every significant skill/method version change records: problem observed, proposed change, affected docs/tests, baseline comparison, risks/trade-offs, result, and disposition. Preserve regression cases. Do not release with hidden critical failures. A method's maturity and scope of approval are recorded separately from evidence supporting its theory or origin.

## 11. B2 evaluation starter set

The full Friday repository maintains synthetic cases under `evals/cases/`, human/model rubrics under `evals/rubrics/`, and JSON Schemas for actual run records. These are repository-level validation assets; the standalone skill package does not claim to execute or include the full evaluation harness. Cases specify expected behavior, not completed evaluation results. No pass rate or improvement claim is made until real executions are recorded.


## Context efficiency and capability routing (B6.5)

Quality review must check that only the selected capability and task-relevant references are loaded, but must also verify that mandatory evidence, prerequisites and safety controls remain present. Track actual token/cost metrics only where host telemetry exposes them; otherwise report observable proxies such as files loaded, tool calls, iterations and output length. Compare progressive disclosure against a controlled baseline before claiming savings. A reduction in context/tool usage that causes critical omissions is a failure, not an optimization. See `docs/governance/CONTEXT_EVALUATION.md`.


## Development incident and test-limit handling

For timeout, missing dependency, execution-limit, partial-run, or recovery reporting, follow `DEVELOPMENT_INCIDENT_PROTOCOL.md`. An aggregate pass must list skips; acceptance criteria must not be weakened to obtain a pass.
