# Peanuts Four-Council Review Protocol

**Status:** Experimental Peanuts method; calibration required before routine approval  
**Version:** 0.3.0-draft  
**Last reviewed:** 2026-10-31

## 1. Purpose and limits

The Four-Council Review challenges a project concept through four distinct review lenses. It is a Peanuts-designed structured critique, not a universal industry standard, prediction of competition results, or evidence that four statistically independent experts assessed the concept.

One model can simulate four lenses, but shared model, context, and source limitations remain. Use it to organize criticism, not manufacture consensus. When stakes justify it, add actual users, human domain specialists, or separate reviewers and describe their independence accurately.

## 2. Four review lenses and ownership

### Council I — Human Value and User Evidence

**Core question:** Does this address a meaningful problem for identifiable people?

Primary ownership: problem evidence, target-user fit, job/need, outcome relevance, usability and accessibility, user research quality, and whether claims about demand match the evidence. Challenge invented personas, leading interviews, solution-first framing, and unsupported adoption claims.

### Council II — Strategic Value and Differentiation

**Core question:** Why should this solution exist instead of the alternatives?

Primary ownership: value proposition, alternatives/prior art, differentiation, adoption barriers, distribution, operating model, sustainability where relevant, and fit with the user's desired outcome. Do not claim uniqueness from a shallow search.

### Council III — Technical Feasibility and Product Quality

**Core question:** Can the team build and demonstrate this reliably within its constraints?

Primary ownership: technical mechanism, architecture, dependencies, data and API feasibility, integrations, platform compatibility, performance, reliability, maintainability, accessibility, technical privacy/security design, and team skills. Distinguish documented capability, tested feasibility, and assumption.

### Council IV — Red Team, Risk, and Delivery

**Core question:** What can invalidate, harm, derail, or prevent successful delivery?

Primary ownership: adversarial scenarios, failure modes, hidden assumptions, material safety/privacy/legal/IP risks, schedule, budget, team capacity, dependency risk, operational resilience, demo reliability, and fallback strategy. It must make the strongest credible case against proceeding.

### Issue ownership and overlap

Other councils may challenge any issue, but assign one primary owner to prevent double counting:

| Issue | Primary owner | Secondary challenge allowed |
|---|---|---|
| User need, user research integrity | Council I | Council II/IV |
| Differentiation, alternatives, adoption | Council II | Council I/IV |
| Architecture, technical controls, maintainability | Council III | Council IV |
| Threat scenarios, harm, delivery failure | Council IV | Council I/III |
| Official event eligibility and judging | Separate Event Alignment Overlay | Council II/IV may comment |

## 3. Event Alignment Overlay (separate from council scores)

For event-first work, compare the concept to official eligibility, theme/track, deliverables, restrictions, deadlines, team requirements, technology rules, AI-use policy, IP terms, submission format, and published judging criteria. Use official weights where available and cite the applicable version. If none are published, provide qualitative alignment; never invent weights. Do not blend event fit into product-merit scores.

## 4. Adaptive review depth

Review depth changes the amount of evidence and scrutiny, not the dimensions or score anchors.

### Quick screen

For early candidates and low-commitment decisions. Each council records one strongest point, one strongest objection, one key unknown, and one next question/test. Every lens must cover its core question and disclose material blockers. Quick screen cannot label an idea validated or grant deep-review clearance.

### Standard review (default for leading concepts)

Assess all relevant dimensions using the rubric. Record evidence status, strongest case, strongest objection, assumptions, risk severity, and next test. Run the Event Alignment Overlay if applicable.

### Deep review

Trigger when any of the following applies: significant safety/privacy/legal/financial/reputational consequence; vulnerable users or sensitive data; novel/complex unproven dependencies; high cost or hard-to-reverse commitment; major event-compliance uncertainty; conflicting evidence on a decisive assumption; or conversion to an implementation baseline.

Deep review adds focused source research, alternative comparisons, threat/failure scenarios, requirements/quality review, and human domain or user review where practical. It does not require all possible tests or four separate AI agents.

## 5. Scoring rules

Score each applicable dimension from 1–5. Use `N/A` only when genuinely irrelevant and `UNKNOWN` when evidence is insufficient. Scores 2 and 4 fall between the anchors for 1/3 and 3/5. Every score needs a concise rationale and evidence status. Do not substitute 3 for missing evidence.

### Common anchor

| Score | General interpretation |
|---:|---|
| 1 | Serious deficiency; contradicted, unsafe, non-compliant, or presently unworkable. |
| 2 | Weak; major gaps or unsupported assumptions. |
| 3 | Plausible/mixed; significant uncertainties or trade-offs remain. |
| 4 | Strong; relevant evidence and reasoning support the direction; gaps are manageable. |
| 5 | Exceptionally well-supported for this context; material alternatives and limitations addressed. |

A 5 does not mean perfect or guaranteed success. Evidence status and judgement score are separate variables.

### Council I — dimension anchors

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Problem evidence | No credible evidence or contradicted framing. | Plausible evidence but limited/context-bound. | Multiple appropriate evidence sources support a clear, consequential problem. |
| User fit | Users are vague or mismatched. | Target group identified; segment/context gaps remain. | Relevant user groups and contexts are clearly supported. |
| Outcome relevance | Proposed outcome is unclear or low-value. | Outcome is plausible but significance is uncertain. | Outcome is concrete, meaningful, and tied to a demonstrated need. |
| Usability/accessibility | Major barriers ignored. | Key paths considered; notable gaps remain. | Relevant needs, access barriers, and evaluation plans are addressed. |

### Council II — dimension anchors

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Differentiation | Close alternatives exist and no credible advantage is shown. | Some distinction, but value over alternatives is uncertain. | Search-backed, specific advantage against relevant alternatives. |
| Value proposition | Benefit is vague or unsupported. | Benefit is plausible but weakly evidenced. | Clear, important benefit linked to user/job evidence. |
| Adoption/operating model | No plausible route to adoption or operation where required. | Route exists but major dependencies remain. | Credible access, adoption, ownership, maintenance, and cost assumptions for this context. |
| Strategic fit | Conflicts with stated outcome or scope. | Partial fit with trade-offs. | Strong fit with objectives, constraints, and intended direction. |

### Council III — dimension anchors

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Technical plausibility | Core mechanism impossible or contradicted. | Plausible but critical assumptions untested. | Core mechanism demonstrated or strongly supported within stated limits. |
| Integration/data | Critical APIs/data/permissions unavailable or unexamined. | Dependencies identified but some access or integration unknowns remain. | Dependencies, access, data, interfaces, and limitations verified appropriately. |
| Product quality | Material reliability, accessibility, security, or maintainability needs are ignored. | Relevant quality needs identified; test/mitigation gaps remain. | Context-appropriate quality requirements and verification plan are credible. |
| Resource fit | Skills/time/budget materially insufficient. | Feasible only with trade-offs or help. | Scope matches team capacity, time, budget, and available assets. |

### Council IV — dimension anchors

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Risk/harm controls | Critical harm/compliance issue unmanaged. | Risks identified but some mitigations or evidence remain open. | Material risks, owners, mitigations, and residual risks are explicit and proportionate. |
| Delivery readiness | Timeline/demo/dependencies make delivery implausible. | Plausible with significant schedule or dependency risk. | Milestones, dependencies, demonstration, and fallback are credible. |
| Resilience/failure handling | No credible response to likely failure. | Some failure paths handled. | Critical failure modes have tested or plausible fallback and recovery plans. |
| Assumption challenge | Major assumptions remain hidden or unchallenged. | Main assumptions visible, but counterevidence limited. | High-impact assumptions, contrary cases, and disconfirming tests are addressed. |

Use 2/4 when evidence lies between anchor descriptions. Add project-specific dimensions only with a documented reason; preserve core dimensions for comparability.

## 6. Evidence status

Use one status per material finding:

- `VERIFIED` — directly supported by an authoritative source, primary evidence, or test appropriate to the claim.
- `SUPPORTED` — credible support with stated limitations.
- `PRELIMINARY` — early or narrow evidence.
- `ASSUMPTION` — temporarily accepted, not verified.
- `UNKNOWN` — insufficient evidence.
- `CONTESTED` — credible evidence conflicts.

## 7. Risk severity and progression rules

| Severity | Meaning | Expected disposition |
|---|---|---|
| Critical | Could cause serious harm, breach a mandatory rule, invalidate the core concept, or create an unacceptable consequence. | Blocks ADVANCE until resolved or appropriately reviewed/mitigated; user cannot waive legal or safety obligations. |
| High | Could materially invalidate value, feasibility, or delivery. | Must be tested, mitigated, or explicitly carried as a blocking uncertainty. |
| Medium | Important but not currently decisive. | Record owner and planned treatment. |
| Low | Minor improvement or manageable concern. | Record if useful; does not block by itself. |

A strong score in one dimension cannot compensate for a critical failure elsewhere. Do not calculate a default overall average. Report council-level dimensions, critical findings, evidence, and verdict separately.

## 8. Verdicts

- `ADVANCE` — enough is known for the next defined step; not a claim of market validation.
- `REVISE` — improve framing, concept, scope, mechanism, or evidence.
- `VALIDATE` — a decisive assumption must be tested first.
- `PIVOT` — current solution is weak but another opportunity/direction is supported.
- `STOP` — fundamental constraints, no meaningful value, unacceptable risk, or mandatory non-compliance make proceeding unjustified.

If a critical issue remains unresolved, do not issue ADVANCE. If the user chooses to continue despite a high/critical warning, record the unresolved issue and rationale without describing it as approved or resolved.

## 9. Review output

1. Concept/version and review depth/reason.
2. Evidence pack, sources, date, scope, and limitations.
3. Findings for each council: strongest case, strongest objection, dimension scores/unknowns, evidence status, critical assumptions, and next test.
4. Issue ownership and cross-council overlap/conflict check.
5. Event Alignment Overlay (if relevant).
6. Severity-ranked risk register and mitigations.
7. Verdict and rationale.
8. User decision and approval status.

## 10. Independence and anchoring

Where practical, conduct separate passes against the same concept and evidence pack before showing each pass the others' findings. A later synthesis should compare disagreements and duplicates. This may reduce anchoring but does not create statistical independence if the same model, prompt foundation, or sources are shared.

For deep reviews, consider separate models, human domain specialists, real users, or external expert review when the decision warrants the effort. Disclose reviewer type and limits.

## 11. Calibration and evaluation plan

Test representative cases: strong concept/evidence; weak user evidence; infeasible architecture; good product/poor event fit; compliant event fit/weak product; superficial analogy; close prior art; serious privacy/safety risk; vague concept; and conflicting sources.

Compare against a simpler structured critique baseline using the same cases. Assess:

- Recall of seeded critical issues (did it find known important problems?).
- Precision/relevance of findings (were claims supported and decision-relevant?).
- Unsupported praise and false-positive objections.
- Quality/actionability of suggested experiments.
- Correct use of UNKNOWN and evidence statuses.
- Reviewer agreement/disagreement where genuinely measurable.
- Human usefulness and decision impact.
- Runtime/cost where available.

Calibrate model-based graders against human-labelled examples. Do not claim inter-rater reliability, statistical significance, or improved decision quality without an appropriate sample, method, and analysis. Keep a stable versioned test set for regression.


## 12. B7 operational record contract

B7 implements the protocol with `schemas/council-review.schema.json` and `templates/records/council-review.json`. Each review records all 16 stable dimensions across every depth; unassessed items use `UNKNOWN`/`NOT_ASSESSED`, while `N_A` requires a reason. The review records the evidence pack, reviewer setup, event overlay, findings, gate, verdict, limitations, and the user's separate decision. A review is not user approval.

`statistical_independence_claim` must always be false for the four-lens review. The record may describe separate first passes or distinct reviewers, but multiple passes/models do not by themselves prove statistical independence.

The project validator enforces that critical/high open findings block progression, blocker IDs resolve, passing gates do not retain blockers, `ADVANCE` has a passing gate, and accepted high residual risks require a conditional gate. Mitigated findings require evidence. Critical findings and safety/legal/regulatory/mandatory-compliance obligations cannot be waived through `accepted_with_rationale`.

See `skills/peanuts/references/four-council.md` for concise operational instructions and `docs/architecture/DECISION_GATES_AND_REVIEW_RECORDS.md` for record and migration behavior. Structural checks do not determine whether the council's reasoning is correct.
