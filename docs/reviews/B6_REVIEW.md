# B6 — NUTS Innovation Engine: Four-Council Review

**Milestone:** B6  
**Review date:** 2026-11-01  
**Status:** Passed as a structural/method-specification milestone; live-model efficacy not established.

## Review scope

Reviewed `NUTS_METHOD.md`, `NUTS_SOURCE_DOMAIN_PLAYBOOK.md`, the operational skill reference, PPA and Tool & Knowledge Registry updates, analogy/run schemas, project record integration, evaluation cases EVAL-031–038, and deterministic tests.

This is a structured four-perspective review, not four independent human auditors or a statistical assessment.

## Council 1 — Analogical Reasoning and Cognitive Science

**Assessment: 8.8/10 — Pass with limitations**

Strengths:
- Function-first framing reduces solution anchoring.
- Gentner's Structure-Mapping Theory is used to emphasize relationships and systematicity rather than surface resemblance.
- Transfer mismatches and counterexamples are explicit.
- Analogy disposition is not reduced to an unsupported novelty score.

Limitations:
- A language model can still invent correspondences or overstate a relation.
- The proposed NUTS synthesis has not been benchmarked against a human-coded analogy dataset or a simple ideation baseline.
- The record contract captures mapping judgments but does not mechanically prove that the mapped relations are logically equivalent.

Recommendation: retain the relational mapping contract; develop human-labelled calibration cases during later evaluation. Do not claim NUTS is empirically validated.

## Council 2 — Domain Research and Source Integrity

**Assessment: 8.7/10 — Pass with limitations**

Strengths:
- Distinct pathways for biology, history, engineering, culture/social systems, economics/operations, and existing products.
- Biomimicry Design Spiral is restricted to biological inspiration.
- Historical source criticism distinguishes primary from secondary material and notes that primary does not mean unbiased.
- AskNature and other indexes are treated as discovery aids; important claims require source inspection/corroboration.
- Cultural knowledge, copyright, patents, and confidentiality are explicit concerns.

Limitations:
- No actual biological, historical, or engineering example was researched as part of B6.
- The registry lists candidate tools, not installed or guaranteed tools.
- Patent/prior-art searches cannot establish legal novelty or freedom to operate.

Recommendation: require source/claim records for every retained-for-test card and qualified human/legal/domain review for consequential issues.

## Council 3 — Innovation and Product Design

**Assessment: 8.6/10 — Pass with limitations**

Strengths:
- Creative Influence System operationalizes collecting, studying, cross-pollinating, transforming, and crediting influences.
- The process allows “no useful analogy found.”
- A testable transfer hypothesis and baseline comparison are required.
- Combining mechanisms requires distinct contributions and a plausible interface.

Limitations:
- More influences can create noise and overcomplication; domain selection needs to stay bounded.
- NUTS may be unnecessary when the project problem is already clear and a conventional solution is sufficient.
- No evidence yet demonstrates that NUTS produces better concepts than baseline ideation.

Recommendation: keep NUTS optional and decision-led. Evaluate whether it adds useful transfer, not just novelty or longer outputs.

## Council 4 — Software Architecture and AI Quality Assurance

**Assessment: 8.8/10 — Pass with limitations**

Strengths:
- Draft 2020-12 schemas for analogy cards and NUTS runs.
- Project ledgers link analogy cards to source and claim IDs.
- A retained-for-test card requires verified/partially verified source accuracy, adequate relevance/mapping, and a testable hypothesis.
- A NUTS run can record no useful analogy without fabricating a candidate.
- Legacy project workspaces without the new optional ledgers are not destructively modified; the validator reports a warning.
- EVAL-031–038 cover surface resemblance, source accuracy, history, TRIZ applicability, no-analogy outcome, and IP overclaim.

Limitations:
- Schema and traceability tests establish structure, not truth.
- Runtime instruction adherence and model quality have not been tested.
- Ruff and remote CI/Codespaces remain separate verification items.

Recommendation: preserve schemas and validators; run model-based and human calibration during later release evaluation. Keep the no-fabrication and no-legal-certification boundaries.

## Consolidated findings

| Finding | Severity | Disposition |
|---|---|---|
| Analogies can be superficially plausible despite weak evidence | High | Mitigated by source and mapping gates; runtime evaluation remains |
| NUTS may be applied when not useful | Medium | Mitigated by optional, decision-led routing |
| Source discovery tool may be mistaken for final evidence | High | Mitigated by registry and source-inspection rules |
| Prior-art search may be overclaimed | High | Explicitly prohibited; expert review required for legal conclusions |
| Cross-record references may dangle | High | Deterministic validator added |
| Model may invent a source/analogy | Critical if used as fact | No-fabrication instructions, source IDs and runtime evaluation required; not fully proven |

## Acceptance evidence

- Analogy Card and NUTS Run schemas validated.
- Templates validated.
- EVAL-031–038 validated and marked `ready` for future runtime evaluation.
- Project initializer creates `analogies.jsonl` and `nuts-runs.jsonl`.
- Project validator checks source/claim/analogy references and run conclusion invariants.
- Negative tests reject dangling references and retained cards with unverified source accuracy.
- Recovery to valid project state passes.
- Added a deterministic release-archive builder that places repository contents at ZIP root, checks for manifest drift and unsafe paths, verifies archive CRC and SHA-256, and replaces output atomically.
- Packaging tests cover flat extraction layout, stale-manifest refusal, unmanifested-file refusal, unsafe paths, deterministic output, and embedded hashes.
- The final B6 ZIP was extracted into a fresh directory. Repository integrity, B2, B4, B5, B6, and the complete verifier then passed from that extracted root with Ruff explicitly skipped.

## Limitations and non-claims

B6 does not prove source truth, analogy correctness, novelty, patentability, transfer feasibility, better innovation outcomes, or live-model performance. The method is experimental. The example analogy card is synthetic and exists only to validate the record contract.

## Verdict

**PASS WITH BOUNDED LIMITATIONS** as a structural and method-specification milestone. Proceeding to B7 is reasonable after the B6 deterministic checks and repository regression suite pass. No claim of empirically validated NUTS effectiveness is authorized.

## Release/package verification note

The cumulative ZIP uses repository-root layout (no enclosing `Friday/` folder) to simplify the owner’s iPad-to-GitHub upload. The archive was extracted into a fresh directory and the consolidated verifier completed successfully there. This is a local reproducibility check; remote GitHub Actions, Codespaces, and model-host runtime tests remain pending.
