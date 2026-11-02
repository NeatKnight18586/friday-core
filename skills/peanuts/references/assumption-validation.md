# Assumption Validation — Operational Reference (B7)

Load this reference when a decision depends on an uncertain belief that can be tested. The canonical record format is `schemas/assumption-test.schema.json`; the assumption itself uses `schemas/assumption-record.schema.json`.

## 1. Select the assumption worth testing

Prioritize assumptions by consequence if wrong, uncertainty, and how cheaply a useful test can reduce uncertainty. Test assumptions that could invalidate the concept before optimizing secondary details. Do not prioritize solely by how easy an assumption is to test.

## 2. Write a falsifiable hypothesis

Every test plan must specify:
- The assumption being tested and the decision it affects.
- A specific hypothesis.
- The method and target/system.
- Steps and scope/sample where relevant.
- A success signal and a failure signal.
- A decision threshold written before execution.
- Known limitations and ethical/data controls.

Avoid vague tests such as "ask people whether they like it." Prefer observable behavior, realistic tasks, current workarounds, technical demonstrations, or authoritative checks appropriate to the assumption.

## 3. Choose a proportionate method

Examples include user interviews, observation, usability tests, prototype tests, technical spikes, benchmarks, experiments, simulations, expert review, official-source checks and literature review. Method choice must match the claim. Desk research cannot by itself prove local user demand; a tiny convenience sample cannot establish population prevalence; a prototype demonstration cannot prove sustained adoption.

## 4. Human-participant safeguards

When people participate, obtain appropriate informed consent before collecting data, explain purpose and use, minimize collection, use pseudonymous references in project records, confirm de-identification, and assess whether institutional/ethics or local review is required. Store names, contact information, raw recordings and signed consent outside the project repository in appropriately protected storage. If consent is withdrawn, stop the affected activity and follow the applicable deletion/retention commitments. Do not treat `not_required` as a casual default: record the rationale.

This reference is operational guidance, not legal or institutional ethics advice. Requirements vary by jurisdiction, institution, population and data type.

## 5. Record results honestly

A completed test requires a completion date, outcome (`supports`, `invalidates`, `mixed`, or `inconclusive`), result summary, at least one traceable evidence reference, limitations and protocol deviations. Never invent a sample size or test outcome. A planned test is not completed evidence.

Update the linked assumption status only when the evidence warrants it. `supported` requires a completed supporting test; `invalidated` requires a completed invalidating test. Mixed/inconclusive results usually leave the assumption under investigation or lead to a revised hypothesis.

## 6. Decide and learn

Compare the result with the predeclared threshold. State whether to proceed, revise, test again, pivot or stop. Record what the test did not establish. A test can reduce uncertainty without proving universal truth.
