# Method Governance and Evidence Standard

**Status:** Initial governance specification  
**Version:** 0.3.0-draft

## 1. Purpose

Peanuts should use professional methods deliberately, not decorate outputs with framework names. Every significant method needs a clear job, evidence appropriate to the claim, prerequisites, application boundary, known limitations, and an evaluation plan.

Distinguish:

- Evidence supporting a method in its original context.
- Evidence that Peanuts' adaptation is faithful and useful.
- Evidence that the adapted method improves an actual project decision or outcome.

## 2. Evidence types

| Evidence type | Meaning |
|---|---|
| Normative/official | Standards, regulations, official policy, or technical specifications. |
| Empirical research | Published research with method, data, results, and limitations. |
| Field/case evidence | Documented use in a real setting; generalizability may be limited. |
| Expert/vendor guidance | Official technical or professional guidance from a relevant provider. |
| Practitioner framework | Named methodology used by practitioners; not automatically empirically proven. |
| Internal evaluation | Peanuts' own pilot, test suite, comparison, or user feedback. |
| Inference/hypothesis | Reasoned interpretation not directly established. |

Evidence types may coexist. Do not rank a standard, empirical paper, and practitioner framework on one simplistic scale; they support different claims.

## 3. Method maturity lifecycle

1. `PROPOSED` — candidate only.
2. `RESEARCHED` — purpose, origin, alternatives, evidence, limitations, and fit reviewed.
3. `PILOT` — used in limited realistic cases.
4. `EVALUATED` — results compared with criteria or a baseline.
5. `APPROVED-SCOPED` — accepted for a specific use and context.
6. `UNDER-REVIEW` — new evidence, failures, or platform changes require reconsideration.
7. `DEPRECATED` — no longer recommended; replacement/migration noted where useful.

A method may be approved for early ideation and not for high-stakes decisions.

## 4. Method contract

Use the contract in `../governance/PROFESSIONAL_PRACTICE_ARCHITECTURE.md`. Every recurring/core method should record its ID, purpose, discipline, evidence/maturity, suitable and unsuitable contexts, prerequisites, inputs, procedure, tools/sources, outputs, limitations, quality checks, evaluation cases, version, and review date.

## 5. Selecting a method

1. Identify the specific decision or failure it should improve.
2. Check whether an existing method already covers the need.
3. Find an original/authoritative source and credible critique or limitation.
4. Verify prerequisites and applicability.
5. Compare a simpler alternative if complexity is affected.
6. Select only the components relevant to Peanuts.
7. Define what better performance would look like.
8. Pilot and evaluate on representative cases.
9. Keep, modify, or reject based on results.

Do not add a method merely because it is popular, sophisticated, or associated with a respected organization.

## 6. Evaluation

Use deterministic checks, rubric-based review, human evaluation, and outcome evaluation as appropriate. Maintain versioned test cases with ordinary, edge, ambiguous, conflicting, and adversarial inputs. Compare against a baseline when claiming added value. Calibrate model graders against human-labelled examples. Do not report statistical reliability or significance without suitable samples and analysis.

See `../governance/QUALITY_ASSURANCE.md` for the quality-gate and evaluation standard.

## 7. Current method register (initial)

| Method/reference | Intended use | Evidence posture / caution |
|---|---|---|
| Double Diamond | Flexible discover/define/develop/deliver map. | Practitioner framework; not a guarantee or rigid waterfall. |
| Jobs to Be Done | Understand progress, context, and motivation. | Practitioner/research tradition; use actual context, not invented personas. |
| Opportunity Solution Tree | Connect outcome, opportunities, solutions, and assumption tests. | Practitioner method; formal version has prerequisites; label adaptations. |
| User interview/observation | Understand actual experience and behavior. | Research method; requires appropriate recruitment, ethics, consent, and synthesis. |
| Triangulation | Compare findings from different evidence types/sources. | Evidence strategy; sources may share bias/dependency. |
| Test Card/hypothesis testing | Make assumptions and experiments explicit. | Practitioner tool; define observable success/failure signals. |
| Structure-Mapping Theory | Relational analogy and mechanism transfer. | Published cognitive-science theory; does not guarantee transfer. |
| NUTS (Peanuts synthesis) | Bounded cross-domain search, mechanism abstraction, transfer challenge, and useful rejection. | Experimental Peanuts synthesis; must be piloted against a simpler ideation baseline. |
| Biomimicry Design Spiral | Biological function discovery and abstraction. | Established domain-specific design process; not all cross-domain ideation. |
| TRIZ | Investigate and resolve technical/physical contradictions. | Established practitioner methodology; use only when a real contradiction is formulated. |
| ISO/IEC/IEEE 29148 | Requirements processes and information items. | Formal standard; 2018 edition remains published/current on 2026-10-31 while DIS successor is under development. Recheck. |
| ISO/IEC 25010:2023 | Select product quality characteristics. | Formal quality model with nine characteristics; tailor to context. |
| NIST AI RMF / GenAI Profile | AI risk governance. | Voluntary frameworks; tailor to use case. The AI RMF 1.0 is under revision. |
| OWASP GenAI/agent guidance | AI/security threat discovery. | Security guidance; map threats to actual architecture and permissions. |

## 8. Change control

Method changes affecting outputs, decisions, safety, or expectations must update the registry, relevant docs, affected tests, and decision/release record. Do not change a core method because one response feels better; identify the failure, compare alternatives, and evaluate representative cases.
