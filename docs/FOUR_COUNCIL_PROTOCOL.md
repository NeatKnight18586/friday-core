# Peanuts Four-Council Review Protocol

**Status:** Experimental Peanuts method; Stage 0.5 specification draft  
**Version:** 0.2.0-draft

## 1. Purpose and limits

The Four-Council Review is a structured way to challenge a project concept from four professional perspectives. It is not a recognized universal standard, a prediction of competition results, or evidence that four statistically independent experts have reviewed the idea.

A single model can simulate four review lenses, but those lenses may share the same model limitations, context, and blind spots. Use the method as structured critique, not independent consensus. When stakes justify it, add real users, human domain experts, or separately run reviewers and disclose their independence limitations.

## 2. Four review lenses

### Council I — Human Value and User Evidence

**Core question:** Does this address a meaningful problem for identifiable people?

Review problem clarity, target users, job/need, frequency or severity where known, existing workarounds, accessibility, evidence quality, and whether the proposed outcome matters. Challenge invented personas, unsupported demand claims, and solution-first framing.

### Council II — Strategic Value and Differentiation

**Core question:** Why should this solution exist instead of the alternatives?

Review value proposition, differentiation, existing solutions, adoption barriers, distribution, operating model, sustainability where relevant, and alignment with the project's desired outcome. Do not claim uniqueness from a shallow prior-art search.

### Council III — Technical Feasibility and Quality

**Core question:** Can the team build and demonstrate this reliably within the constraints?

Review technical mechanism, architecture, dependencies, data, APIs, integration, platform compatibility, performance, reliability, accessibility, security, privacy, maintainability, and team skills. Distinguish demonstrated feasibility from plausible assumptions.

### Council IV — Red Team, Risk, and Delivery

**Core question:** What can invalidate, harm, derail, or prevent successful delivery?

Review failure modes, hidden assumptions, event compliance, schedule, budget, team capacity, dependency risks, legal/IP concerns, safety, privacy, abuse cases, demo reliability, and fallback strategy. It should make the strongest case against proceeding, not merely list generic risks.

## 3. Keep event fit separate

For event-first work, run an **Event Alignment Overlay** separately from the four product-review lenses. Compare the concept to official eligibility, theme, track, deliverables, restrictions, timeline, and published judging criteria. Use official weights where available. Do not merge event alignment into product-merit scores or invent judging weights.

## 4. Adaptive review depth

The owner selected adaptive depth. Depth changes the amount of evidence and analysis, not the core criteria or score definitions.

### Quick screen

Use for early candidate ideas, low-consequence decisions, or rapid narrowing. Each council gives a concise strongest point, strongest objection, key unknown, and next question/test. Perform a minimum check for user value, differentiation, feasibility, and material risk. Do not issue a “validated” verdict.

### Standard review (default for leading concepts)

Use when comparing or selecting a leading concept. Each council examines relevant evidence, records major strengths and weaknesses, uses the common rubric, identifies critical assumptions, and recommends next tests. Include the Event Alignment Overlay when applicable.

### Deep review

Escalate when one or more triggers apply:

- Significant safety, privacy, legal, financial, or reputational consequence.
- Sensitive data, vulnerable users, or high-impact decisions.
- Novel or technically complex architecture with unproven dependencies.
- High cost, difficult reversibility, or major resource commitment.
- Important event eligibility or compliance uncertainty.
- Weak/conflicting evidence on a decisive assumption.
- A concept is about to be converted into an implementation baseline.

Deep review adds targeted source research, adversarial scenarios, failure analysis, alternative architectures, and, where practical, real user/expert input or separate reviewers. It is not automatically required for every hackathon idea.

## 5. Common scoring rubric

Score each applicable dimension from 1 to 5. Use `N/A` when genuinely irrelevant and `Unknown` when evidence is insufficient. Do not substitute 3 for unknown.

| Score | Anchor |
|---:|---|
| 1 | Serious deficiency; contradicted by evidence or currently unworkable. |
| 2 | Weak; major gaps or unsupported assumptions remain. |
| 3 | Plausible but mixed; important uncertainties or trade-offs remain. |
| 4 | Strong; evidence and reasoning support the direction, with manageable gaps. |
| 5 | Exceptionally well-supported for this context; important alternatives and limitations addressed. |

A 5 is not a claim of perfection or guaranteed success. Explain the evidence behind every material score.

### Separate evidence status from judgment score

For each finding, record an evidence status such as:

- `VERIFIED` — directly supported by authoritative source or test.
- `SUPPORTED` — credible support with stated limitations.
- `PRELIMINARY` — early evidence, not yet robust.
- `ASSUMPTION` — accepted temporarily, unverified.
- `UNKNOWN` — insufficient evidence.
- `CONTESTED` — credible evidence conflicts.

A score describes the council's judgment against the rubric. Evidence status describes what supports that judgment. They are not the same variable.

## 6. No default overall average

Do not average all council scores into a single “idea score.” The dimensions are not necessarily commensurate, and critical safety, compliance, or feasibility failures cannot be compensated for by high novelty or presentation quality.

Report:

- Council-level scores and rationale.
- Evidence quality and uncertainty.
- Critical blockers or veto conditions.
- Event alignment separately, where relevant.
- Recommended disposition and next test.

If official competition criteria contain numerical weights, calculate event fit separately using those published weights and preserve the source. Do not blend the result with product merit.

## 7. Review output template

1. Concept and version reviewed.
2. Review depth and reason selected.
3. Evidence set and scope limitations.
4. Four council findings: strongest case, strongest objection, evidence, score/unknowns, critical assumptions, next test.
5. Cross-council conflicts and double-counting check.
6. Event Alignment Overlay if applicable.
7. Fatal/critical risks and mitigations.
8. Verdict: `ADVANCE`, `REVISE`, `VALIDATE`, `PIVOT`, or `STOP`.
9. User decision and approval status.

## 8. Verdict definitions

- **ADVANCE:** The concept is sufficiently understood for the next defined stage; this is not a claim of market validation.
- **REVISE:** The core opportunity may be sound, but the concept, scope, or mechanism needs improvement.
- **VALIDATE:** A decisive assumption must be tested before a stronger commitment.
- **PIVOT:** The current solution is weak, but evidence suggests a different direction may address the opportunity.
- **STOP:** Fundamental constraints, lack of value, unacceptable risk, or event non-compliance make proceeding unjustified.

The user retains the final decision. If the user proceeds against a critical warning, document the unresolved risk and rationale.

## 9. Independence and anchoring safeguards

When practical, each review pass should first receive the same concept brief and evidence pack, without seeing other councils' scores or conclusions. A later synthesis should compare disagreements and overlaps. This reduces some anchoring but does not create statistical independence if the same model, context, or underlying sources are shared.

For deep reviews, consider a separate model, a human domain expert, or actual target-user input when the added effort is justified. Disclose reviewer identity/type and whether reviews were truly separate.

## 10. Calibration and evaluation

Before the method is treated as approved, test it on representative cases:

- Strong concept with strong evidence.
- Attractive concept with weak user evidence.
- Technically infeasible concept.
- Useful product with poor event fit.
- Event-compliant concept with weak product merit.
- Novel-looking concept with close existing alternatives.
- Concept with serious privacy/safety risks.
- Vague concept with insufficient evidence.

Compare the Four-Council method with a simpler generic structured critique. Evaluate whether it finds more decision-relevant issues, avoids unsupported praise, reduces missed risks, produces useful tests, and improves human decisions. Keep the same case set for regression testing. Calibrate rubric examples with human review; do not claim inter-rater reliability unless it is actually measured.
