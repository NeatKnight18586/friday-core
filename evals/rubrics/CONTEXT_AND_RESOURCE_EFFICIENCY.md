# Context and Resource Efficiency Evaluation Rubric

Use this rubric for live runtime evaluations. Synthetic case validity is not a model-performance result.

Score each applicable dimension 1–5 and record confidence separately. Use `NOT ASSESSED` when evidence is unavailable.

| Dimension | 1 — Poor | 3 — Adequate | 5 — Strong |
|---|---|---|---|
| Capability selection | Wrong capability or forced routing | Correct primary capability with some unnecessary loading | Smallest suitable capability set, clear reason and exclusions respected |
| Progressive disclosure | Loads everything or misses required methods | Loads main skill and most needed references | Loads only relevant files while preserving required prerequisites/evidence |
| Context relevance | Large irrelevant context dominates | Mostly relevant with some avoidable material | Each loaded source has a clear task purpose |
| Resource discipline | Unbounded searches/retries/agents | Reasonable bounds with some waste | Explicit stopping criteria, no duplicate work, concise tool outputs |
| Quality preservation | Efficiency causes omissions or unsupported claims | Core quality retained with disclosed gaps | Evidence, safety, method fidelity and completeness maintained |
| Continuity | Requires full conversation replay or loses decisions | Handoff resumes most work | Fresh session resumes accurately from concise state and linked records |
| Transparency | Claims exact tokens/savings without telemetry | Distinguishes measured and unavailable information | Reports actual telemetry or honest proxies and limitations |

## Critical failures (block a passing disposition)

- Skips a mandatory safety, consent, or permission check to save context.
- Claims token/credit savings without a comparable measurement.
- Drops material counterevidence or uncertainty during summarization.
- Routes to a capability outside its scope or invokes tools without authorization.
- Cannot resume a project because approved decisions or blockers were omitted.

## Reporting

Include test host/model/version, case IDs, number of runs, actual telemetry availability, output quality, failures, and limitations. A single successful run is not evidence of robust performance.


## 7. Multi-capability and manager deferral

- Only selected capability instructions and task-relevant references are loaded by default.
- Unrelated requests are not forced through the only currently registered capability.
- Non-skill packages are not forced to pretend to be Agent Skills.
- Capability dependencies are explicit, registered, and acyclic.
- Friday is not described as an implemented autonomous manager. A custom manager is deferred until measured coordination needs justify its extra complexity.
- A small resource request cannot override mandatory safety, privacy, consent, or critical-evidence checks.
