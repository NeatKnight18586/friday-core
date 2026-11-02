# Method Governance and Evidence Standard

**Document status:** Draft for owner review  
**Version:** 0.1.0-draft  
**Date:** 2026-10-31

## 1. Purpose

Peanuts should use professional methods deliberately, not decorate its outputs with methodology names. Every significant method must have a defined purpose, credible support appropriate to its claims, known limitations, and a way to evaluate whether it helps.

This document distinguishes **evidence type** from **Peanuts adoption status**. A method can be widely used but weakly evaluated for a particular outcome. A formal standard may define quality requirements without proving that one workflow is universally superior. A promising internal technique remains experimental until tested.

## 2. Evidence types

Use one or more of these labels for the evidence supporting a method or claim:

| Evidence type | Meaning | Example of appropriate use |
|---|---|---|
| Normative / official | A formal standard, regulation, official policy, or specification. | Establishing required quality characteristics, compliance, or interface constraints. |
| Empirical research | Published research with a stated method, sample, and findings. | Supporting a claim about user behavior or intervention effectiveness within the study's limits. |
| Field / case evidence | Documented real-world use, operational results, or case studies. | Understanding how a practice performed in a particular organization or environment. |
| Expert / vendor guidance | Official technical documentation or professional guidance from a relevant provider. | Understanding supported APIs, platform behavior, recommended configuration, or known limitations. |
| Practitioner framework | A named methodology or framework used by professionals. | Providing a structured process, while avoiding claims of universal effectiveness. |
| Internal experiment | A Peanuts test, pilot, or comparison. | Determining whether a method improves Peanuts' own outputs. |
| Inference / hypothesis | Reasoned interpretation not yet directly established. | Generating a testable proposition or explaining a tentative recommendation. |

Do not treat source prestige as a substitute for relevance. Evaluate whether the evidence actually supports the particular claim being made.

## 3. Method lifecycle

A method moves through explicit maturity states:

1. **Proposed:** Identified as a candidate; not yet accepted for routine use.
2. **Researched:** Purpose, origin, evidence, alternatives, and limitations have been examined.
3. **Pilot:** Used in a limited set of realistic cases.
4. **Evaluated:** Results have been compared against defined criteria; failures and tradeoffs documented.
5. **Approved:** Accepted for use within a stated scope and version.
6. **Under review:** New evidence, failures, or platform changes may require revision.
7. **Deprecated:** No longer recommended; replacement or migration guidance is recorded where needed.

Approval is scope-specific. A method may be approved for early ideation but not for high-stakes decisions.

## 4. Method Registry record

Each significant method should have a record with these fields:

- `method_id`
- `name`
- `purpose`
- `problem_addressed`
- `origin_and_attribution`
- `evidence_types`
- `supporting_sources`
- `claims_supported`
- `known_limitations`
- `alternatives`
- `peanuts_application`
- `success_criteria`
- `evaluation_cases`
- `maturity_status`
- `scope_of_approval`
- `last_reviewed`
- `owner_or_reviewer`

Stage 2 will select a machine-readable representation if it is useful. Do not introduce a database for the registry at this stage.

## 5. Research protocol for adopting a method

Before adopting a significant method:

1. State the problem it is intended to solve.
2. Find the original or authoritative source where possible.
3. Search for relevant empirical findings, credible case evidence, and documented criticism or limitations.
4. Compare at least one plausible alternative when the choice materially affects outcomes.
5. Identify what the method does not establish.
6. Define how Peanuts will apply it; do not assume the original method's entire process is necessary.
7. Define realistic test cases and success/failure signals.
8. Pilot it before treating it as a core practice.
9. Record the decision, version, and review date.

For current standards, APIs, event rules, regulations, and platform features, verify the latest primary source at the time of use. A static registry entry is not proof that a time-sensitive claim remains current.

## 6. Evaluation standard

Use a mixture of:

- **Deterministic checks** for format, required fields, source metadata, schema validity, and traceability.
- **Rubric-based review** for relevance, reasoning quality, completeness, clarity, and usefulness.
- **Human evaluation** for user value, originality, acceptability, and consequential decisions.
- **Outcome evaluation** where possible, such as user interviews, prototype behavior, task completion, event compliance, or implementation results.

Evaluation cases should include ordinary, edge, ambiguous, conflicting, and adversarial examples where relevant. Keep a stable regression set so changes can be compared with earlier versions.

Record the model/runtime, skill version, test inputs, expected behavior, observed output, grader or reviewer, and known limitations. Do not infer causality from a small number of examples.

## 7. NUTS method governance

The NUTS procedure is an experimental synthesis inspired by cross-domain learning, analogical reasoning, biomimicry, and the creative philosophy in Austin Kleon’s *Steal Like an Artist*: study influences, collect ideas, and recombine them into work with a distinct purpose. The book is a creative influence, not empirical validation of the Peanuts procedure. Do not reproduce its protected text or illustrations.

It must be evaluated on more than novelty. Useful criteria include:

- Relevance to the actual problem.
- Accuracy of the source explanation.
- Quality of mechanism abstraction.
- Plausibility of cross-domain transfer.
- Awareness of transfer limitations.
- Distinction from existing approaches.
- Potential user value and feasibility.
- Attribution and intellectual-property awareness.

A strange analogy is not automatically a useful analogy. Peanuts should be allowed to conclude that no cross-domain inspiration materially improves a particular project.

## 8. Four-Council method governance

The Four-Council Review is an internal Peanuts protocol, not a recognized universal standard. Its four perspectives are Human Value, Strategic Innovation, Technical Feasibility, and Red-Team/Delivery.

Its evaluation should test whether it:

- Identifies meaningful weaknesses that a generic review misses.
- Avoids ungrounded praise and invented evidence.
- Distinguishes independent dimensions rather than double-counting them.
- Surfaces uncertainty and disagreement.
- Produces useful next tests and actionable recommendations.
- Helps users make better decisions without falsely implying statistical independence.

A single model simulating four perspectives may share the same blind spots. Where stakes justify it, use separate models, external experts, or actual users as additional reviewers and compare whether this improves decision quality.

## 9. Source quality and citation rules

Prefer primary sources for facts about an event, standard, law, API, or product. Use original research for empirical claims. Use secondary sources to discover context and counterarguments, not as a substitute for authoritative evidence where available.

For each important source, capture title, author/publisher, publication/update date if available, access date, URL, relevant claim, and limitations. Distinguish a source's reported fact from Peanuts' interpretation. Report conflicting sources rather than silently choosing the convenient one.

## 10. Initial method candidates

These are candidates for research and appropriate use, not blanket endorsements:

| Candidate | Potential role in Peanuts | Caution |
|---|---|---|
| Design Council Double Diamond | Problem discovery and iterative development. | A process framework, not a guarantee of successful innovation. |
| Human-centered design | Grounding concepts in user needs and context. | Desk research alone is not direct user validation. |
| Biomimicry Design Spiral | Discovering and abstracting mechanisms from nature. | Biological analogies can be superficial or invalid when constraints differ. |
| Hypothesis-driven experimentation | Testing assumptions before committing to a solution. | Tests must be ethical, measurable, and appropriate to the decision. |
| ISO/IEC 25010 quality model | Selecting relevant software product quality characteristics. | Use as a tailored quality reference, not a mandatory checklist for every prototype. |
| Threat modeling / OWASP guidance | Identifying software and AI-related security risks. | Apply based on product architecture and actual exposure; keep references current. |

## 11. Change control

A method change that affects outputs, decisions, safety, or user expectations must update:

- Its registry entry.
- The relevant skill/reference file.
- Relevant test cases and evaluation criteria.
- Release notes or decision records where appropriate.

Do not change a core methodology solely because one output felt better. Record the problem, compare alternatives, evaluate representative cases, and retain known tradeoffs.
