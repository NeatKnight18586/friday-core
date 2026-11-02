# NUTS — Cross-Domain Innovation Method

**Status:** Experimental Peanuts method; B6 operational specification  
**Version:** 0.4.0-draft  
**Guiding phrase:** Nothing New Under the Sun

## 1. Purpose and limits

NUTS studies existing systems, identifies useful mechanisms and relationships, and tests whether those principles can be transferred or recombined to address a different problem. It draws on cross-domain design, structure-mapping research, biomimicry, historical source criticism, engineering analysis, and the creative practice inspired by Austin Kleon's *Steal Like an Artist*.

NUTS is Peanuts' experimental synthesis, not an industry standard or proof of effectiveness. It does not certify originality, patentability, novelty, copyright clearance, or freedom to operate. A search can reduce uncertainty but cannot establish that something has never existed.

## 2. Core principle: relationship before resemblance

A weak analogy notices that two objects look alike or share a label. A stronger analogy identifies relations among actors/components, functions, constraints, process, feedback, resource flows, and failure handling.

Gentner's Structure-Mapping Theory describes mapping relational structure from a base domain to a target domain. Relations and connected systems of relations matter more than surface attributes. This is a theoretical basis for disciplined analogy, not a guarantee that a transfer will succeed.

## 3. Creative Influence System

Inspired by the broad creative practice in Austin Kleon's *Steal Like an Artist*, without reproducing the book's expression or treating it as empirical proof:

1. **Collect influences:** maintain a small, attributed collection of systems, inventions, research, processes, art, history, nature, and products that raise useful questions.
2. **Study the source:** understand original context, constraints, function, mechanism, choices, and limitations; do not copy appearance alone.
3. **Cross-pollinate:** combine influences only when each contributes a distinct function or principle and their interaction is plausible.
4. **Transform and contribute:** document what was retained, abstracted, changed, combined, rejected, and newly proposed. State the team's contribution.
5. **Credit and respect rights:** attribute sources; respect copyright, patents, trademarks, licenses, confidentiality, cultural protocols, and community knowledge rights.

An influence collection is a research aid, not an idea quota. “No useful influence found” is a valid result.

## 4. Source-domain pathways

Choose one to three source domains according to the target function and context. Do not search all domains by default.

| Domain | Appropriate practice | Key caution |
|---|---|---|
| Nature/biology | Biomimicry Design Spiral; biological function/context analysis; scientific mechanism verification | Understand organism/ecosystem context; do not turn a trait into a metaphor |
| History/civilization | Primary-source criticism, chronology, institutions, actors, incentives, logistics, materials, failure analysis | Distinguish primary evidence from later retellings; avoid anachronism and romanticized stories |
| Engineering/physical systems | Functional decomposition, failure analysis, feedback/control, reliability, constraints; TRIZ for genuine contradictions | Do not invoke TRIZ as decoration; verify method fit |
| Culture/social systems | Contextual research into norms, trust, incentives, institutions, governance, power, and local practices | Avoid stereotypes; respect Indigenous/community knowledge protocols and rights |
| Economics/operations | Queues, routing, allocation, matching, inventory, markets, incentives, bottlenecks | Make actor and institutional assumptions explicit |
| Existing products/processes | Permitted workflow analysis, service blueprinting, feature/mechanism comparison, architecture and business-model analysis | Respect licenses, terms, confidentiality, and IP boundaries |

Detailed instructions: [`NUTS_SOURCE_DOMAIN_PLAYBOOK.md`](NUTS_SOURCE_DOMAIN_PLAYBOOK.md).

### Biological pathway

When appropriate, use the Biomimicry Institute's Design Spiral: Define, Biologize, Discover, Abstract, Emulate, Evaluate. It is iterative; revisit earlier steps when evidence changes. It is biology-specific, not the whole NUTS method.

### Historical pathway

Prefer contemporary/primary records for claims about how a historical system operated, and corroborate consequential claims with reputable scholarship. Evaluate creator, purpose, audience, provenance, bias, editing/translation, completeness, and context. A primary source can itself be partial or biased.

### Engineering pathway

Use functional decomposition and failure analysis. Apply TRIZ only after stating a genuine technical or physical contradiction. Treat suggested principles as hypotheses, not guaranteed solutions.

## 5. Operational workflow

1. Define target problem/function, users/stakeholders, context, constraints, desired outcome, and failure conditions without embedding a preferred solution.
2. Choose one to three relevant source domains and explain why each may inform the decision.
3. Set bounded search terms, source types, timebox, minimum source-quality threshold, and stopping criteria.
4. Find and inspect credible sources; record access dates and project source/claim IDs. Search snippets are leads, not verified evidence.
5. Reconstruct source context, function, actors/components, inputs/outputs, resources, constraints, feedback, failures, and limitations.
6. Map source relationships to target relationships. Separate strong, partial, weak, and unmapped correspondences.
7. Abstract the principle into domain-neutral language; do not transfer unjustified surface attributes.
8. Analyze mismatch: scale, incentives, environment, physics, governance, users, cost, safety, and maintenance as relevant.
9. Recombine only mechanisms with distinct contributions; document interface conflicts and added failure modes.
10. Compare simpler alternatives, prior art, research, products, and open-source approaches within lawful access.
11. State a transfer hypothesis and smallest practical test, with observable measures and success/failure signals.
12. Challenge and reject weak analogies. Record either retained cards or a run-level “no useful analogy” result.
13. Preserve attribution, source provenance, uncertainty, and decision relevance.

## 6. Analogy record and run record

B6 introduces machine-readable Draft 2020-12 schemas:

- `schemas/analogy-card.schema.json` — sourced analogy candidate, structural mappings, context mismatches, alternatives, test plan, rights/attribution, and disposition.
- `schemas/nuts-run.schema.json` — target function, domains actually searched, methods used, candidate cards, coverage, conclusion, and next action.

Use `templates/records/analogy-card.json` and `templates/records/nuts-run.json` as synthetic structural templates. Project workspaces store append-oriented `analogies.jsonl` and `nuts-runs.jsonl`. The records must link to real project source and claim IDs. A synthetic example must never be represented as real research.

## 7. Candidate assessment and rejection

Assess source accuracy, functional relevance, relational mapping, context fit, incremental value over alternatives, testability, and attribution/rights. Do not convert these qualitative dimensions into a fake novelty score.

Dispositions: `PROMISING`, `PLAUSIBLE-NEEDS-TEST`, `WEAK-TRANSFER`, `REJECTED`, `NO-USEFUL-ANALOGY`.

A `retained_for_test` card requires source and claim references, source accuracy `verified` or `partially_verified`, at least adequate functional relevance and relational mapping, and a testable hypothesis. Otherwise keep it as a candidate/researching record or reject it. A no-analogy outcome belongs in the NUTS run record and must explain the bounded search performed.

Reject candidates that rely on unsupported stories, superficial similarity, misunderstood mechanisms, incompatible context, no incremental value, untestable transfer, or unresolved rights concerns. Do not claim originality or legal clearance.

## 8. Evaluation of NUTS

Pilot cases should include strong relational mapping, surface resemblance, inaccurate biology, disputed historical claims, context mismatch, false TRIZ invocation, weak combinations, prior-art discovery, and a valid no-analogy outcome. Compare NUTS with a simpler ideation baseline. Assess source accuracy, mapping quality, mismatch detection, actionable tests, useful rejection, false-positive analogies, unsupported claims, human usefulness, and time/cost. No effectiveness claim is warranted until representative runs and human evaluation exist.

## 9. References

- Gentner, D. (1983), “Structure-Mapping: A Theoretical Framework for Analogy,” *Cognitive Science*, 7(2), 155–170. https://doi.org/10.1207/s15516709cog0702_3
- Biomimicry Institute, Design Process: https://toolbox.biomimicry.org/methods/process/
- AskNature, Biological Strategies: https://asknature.org/biological-strategies/
- ALA/RUSA, Using Primary Sources Online: https://www.ala.org/rusa/sections/history/resources/primarysources/using
- Library of Congress, Getting Started with Primary Sources: https://www.loc.gov/programs/teachers/getting-started-with-primary-sources/
- MATRIZ methodology: https://matriz.org/methodology/
- Austin Kleon, *Steal Like an Artist*: https://austinkleon.com/steal/
