# B10 Paired Baseline Comparison — Generic Critique vs Four-Council

**Date:** 2026-11-02  
**Runtime:** ChatGPT GPT-6 conversation; one same-model session.  
**Fixture:** Synthetic Campus Service Access Challenge; no real user or service data.

## Purpose

B8/B9 review recommendations called for comparing Four-Council against a simpler generic-critique baseline. This is an exploratory paired comparison on one fixed case. It is not a benchmark, statistical study, or independent human evaluation.

## Fixed input supplied to both methods

> Evaluate a proposed one-service campus status page. The fictional challenge says students may need help planning counter visits. No student interviews, staff owner, existing-channel audit, API access, budget, user permission, or service data is confirmed. The prototype must not expose student personal records. Identify the most important problems and recommend the next step.

## Baseline A — simple generic critique prompt

> Give a concise list of the idea's pros, cons, risks and next steps.

**Observed output summary:**

- Potentially useful if students currently lack reliable service information, but demand is unvalidated.
- Staff ownership and update burden are unresolved.
- Stale status can mislead students.
- No API is confirmed; a manual update process may be required.
- Avoid student IDs/accounts and conduct exploratory interviews before building.

This output was concise and surfaced several core risks. It did not explicitly separate strategic differentiation from existing official channels, accessibility, and consent/permission requirements for field observation/interviews.

## Method B — Peanuts Four-Council prompt

> Review the same idea through Human Value, Strategic Value/Differentiation, Technical Feasibility/Quality and Red-Team/Risk/Delivery. State evidence/confidence, severity and blockers. Disclose reviewer setup. Do not average away critical findings. Separate product merit from event alignment.

**Observed output summary:**

- **Human value:** possible service-visit uncertainty, but no direct user evidence; investigate recent actual behavior.
- **Strategic value:** differentiation unknown; audit official service channels and workarounds before claiming novelty.
- **Technical feasibility:** no API; consider a reversible manual single-service prototype only after staff ownership, update cadence, stale-state behavior and accessibility language are clarified.
- **Red-team/delivery:** stale information may be worse than no information; avoid student identifiers/case details; obtain service permission and informed consent for research/observation; identify a responsible updater and failure path.
- Explicitly disclosed that the four lenses are one model's perspectives, not independent reviewers.

## Issue-coverage coding

The issue set was fixed before comparing the two output summaries. “Detected” means the output explicitly named the issue or a direct operational equivalent; it does not mean the recommendation is correct or sufficient.

| Seeded issue | Generic critique | Four-Council |
|---|---:|---:|
| User need/demand not validated | Yes | Yes |
| Staff update owner/burden absent | Yes | Yes |
| Stale information/data freshness risk | Yes | Yes |
| API/integration not confirmed | Yes | Yes |
| Existing official channels/differentiation unknown | No | Yes |
| Accessibility of states/information | No | Yes |
| Privacy/data minimization | Yes | Yes |
| Consent/permission for participant research/observation | No | Yes |
| **Coverage in this single case** | **5/8** | **8/8** |

## Interpretation

On this one synthetic case, the structured Four-Council output surfaced more items from the predeclared issue set and made reviewer dependence, severity and blockers more explicit. The generic baseline was shorter and still found several important risks. The observed extra coverage came with additional structure and length.

This does **not** establish that Four-Council is generally better, more accurate, or worth its additional context cost. The issue coding was performed by the same model family that generated the outputs; there was one case, one session, no blind human adjudication and no repeatability run. The comparison is a useful test design and a provisional signal only.

## Next evaluation needed

Run a larger fixed set including strong, weak, technically infeasible, low-value, compliance-constrained and ambiguous concepts. Randomize method order, keep evidence and model/runtime identical, use a blinded human issue rubric, record false positives and missed issues, and repeat in fresh Project sessions. Only then consider a comparative quality claim.
