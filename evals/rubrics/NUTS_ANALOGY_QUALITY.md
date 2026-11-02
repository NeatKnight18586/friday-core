# NUTS Analogy Quality Rubric

Use this rubric to assess an analogy card or NUTS output. Score each dimension only where evidence is sufficient; otherwise mark `UNKNOWN / NOT ASSESSED`. A high score requires demonstrated reasoning, not terminology.

| Dimension | 1 — Poor | 3 — Adequate | 5 — Strong |
|---|---|---|---|
| Source accuracy | Source absent, misrepresented, or unsupported | Relevant source inspected; some limits remain | Appropriate primary/authoritative evidence inspected and accurately contextualized |
| Functional relevance | Source function unrelated to target | Partial functional relationship | Clear function match under relevant conditions |
| Relational mapping | Surface resemblance only | Some relationships map; gaps are described | Connected source relations map coherently to target relationships |
| Context and mismatch analysis | Ignores major differences | Names relevant differences | Explains how differences constrain or alter transfer, including failure conditions |
| Incremental value | No comparison to simpler alternatives | Some alternatives considered | Shows a plausible advantage over credible baselines without claiming proof |
| Testability | No observable test | Test proposed but weakly operationalized | Small, feasible test with measurable success/failure signals |
| Attribution and rights | No source credit or rights consideration | Basic attribution | Provenance and copyright/license, patent/prior-art, and cultural-knowledge issues are considered appropriately |
| Useful rejection | Forces an analogy or protects a weak candidate | Rejects obvious weak analogies | Actively tests counterexamples and accepts “no useful analogy” when warranted |

## Disposition guidance

- `PROMISING`: source sufficiently verified and structural/context fit is strong; still not proof of transfer.
- `PLAUSIBLE-NEEDS-TEST`: meaningful mapping exists, but critical assumptions need an experiment.
- `WEAK-TRANSFER`: partial mapping or context mismatch undermines usefulness.
- `REJECTED`: source is inaccurate, analogy is superficial, transfer is unsafe/unhelpful, or a better baseline exists.
- `NO-USEFUL-ANALOGY`: bounded search did not identify a useful source; this is a valid result.

Do not average dimensions into a novelty score. Report confidence separately from quality. A low source-accuracy result blocks retaining the analogy for testing even when the concept sounds attractive.
