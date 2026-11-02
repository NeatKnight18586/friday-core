# Quick Four-Council review contract

The quick screen is a triage tool, not a substitute for a deep review or qualified professional sign-off.

## Four required lenses

1. **Human Value:** Is there a meaningful user problem or job? What evidence supports it? Who might be excluded or harmed?
2. **Strategic Value:** Does this fit the opportunity? Is the proposed value meaningfully different from existing alternatives? Is adoption/operation plausible where relevant?
3. **Technical Feasibility:** Can a credible prototype be built with available skills, time, budget, data, APIs, equipment, and dependencies?
4. **Red-Team / Risk / Delivery:** What could invalidate or harm the proposal? What can fail in the demo or operation? What fallback exists?

## Score anchors

Use 1–5 only when there is enough evidence for a judgment:

- **1 — Deficient:** Evidence or constraints strongly contradict the proposal.
- **2 — Weak:** Major gaps or risks; no credible mitigation yet.
- **3 — Plausible:** A reasonable hypothesis, but meaningful evidence or design gaps remain.
- **4 — Strong:** Good supporting evidence; remaining gaps are manageable and understood.
- **5 — Exceptional:** Strong, relevant evidence and a robust design; material alternatives and failure modes have been examined.
- **Unknown / not assessed:** Insufficient information. Do not convert unknown into 3.

Record a separate confidence (`low`, `medium`, `high`) and rationale for every score. A score without evidence or a stated reasoning basis is not useful.

## Critical finding severity

- `CRITICAL`: Progression blocked until resolved or formally accepted through an appropriate risk process.
- `HIGH`: Could materially invalidate the concept or delivery.
- `MEDIUM`: Needs attention but does not currently block progression.
- `LOW`: Improvement opportunity.

Each finding has one primary owner. Other councils may challenge it, but avoid double counting the same underlying issue.

## Disposition

- `ADVANCE`: Sufficiently supported to proceed to the next planned gate.
- `REVISE`: Improve scope/design and return for review.
- `VALIDATE`: Test one or more critical assumptions before commitment.
- `PIVOT`: Change the problem framing or solution direction.
- `STOP`: Fundamental constraints or unacceptable risks make the concept unsuitable.

Do not average scores into a single pass mark. A critical risk cannot be cancelled by high scores elsewhere. Event-rule alignment is a separate overlay based on official criteria; it is not a fifth council and must not be confused with general product merit.


## B7 structured-record rule

A quick screen must still represent all 16 core dimensions. Use `UNKNOWN`/`NOT_ASSESSED` when evidence is insufficient and `N_A` only with a reason. Read `four-council.md` and create a record from `templates/records/council-review.json` when the review must persist. Critical/high open findings block progression; quick depth never removes this gate.
