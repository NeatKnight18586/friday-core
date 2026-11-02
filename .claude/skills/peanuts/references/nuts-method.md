# NUTS Method — Operational Instructions

Read this file when the target project would materially benefit from cross-domain inspiration. The user selected broad cross-domain innovation; this does not mean every domain must be searched every time.

## 1. Entry conditions

Do not begin source analogies until the target problem/function is sufficiently clear. If the problem is framed as a preferred solution (“build an app like X”), rewrite it neutrally and confirm that the user accepts the framing when consequential. If the target function is unknown, ask a focused question or return a research-insufficient result.

## 2. Procedure

1. State target problem, target function, context, users/stakeholders, constraints, and failure conditions.
2. Choose one to three relevant source domains. State why each is relevant and which decision it may inform.
3. Create a bounded search plan with source types, search terms, timebox, source-quality threshold, and stop criteria.
4. Find and inspect credible source material. Record actual source IDs and decision-relevant claim IDs. Search-result snippets are leads, not verified evidence.
5. Reconstruct the base system: original context, function, actors/components, resources, relationships, inputs/outputs, constraints, feedback, failure modes, and limitations.
6. Map relationships from source to target. Prioritize relational structure and connected systems of relations over shared appearance or labels (Gentner, 1983). Record strong, partial, weak, and unmapped correspondences separately.
7. Abstract the mechanism into neutral language. Do not transfer attributes that are not functionally justified.
8. Identify context mismatches and what would have to change. Include scale, incentives, environment, physics, users, governance, cost, safety, and maintenance when relevant.
9. Compare simpler and existing alternatives. Check relevant products, research, patents, and open-source solutions within lawful access. Do not claim legal novelty or freedom to operate.
10. Define a smallest practical test with observable measures, success/failure signals, and limits.
11. Apply the analogy rejection procedure. Keep `candidate` separate from `retained_for_test`; a promising-sounding concept is not evidence.
12. Record the analogy card and the NUTS run. If none is useful, record `no_useful_analogy` with the domains searched, coverage, rationale, and next action—do not invent an analogy to fill the document.

## 3. Source-specific routing

- Nature/biology: read the Biomimicry Design Spiral; biologize function, discover strategies, verify biology, abstract, emulate, evaluate.
- History: read primary/secondary sources with source criticism, chronology, context, corroboration, bias, and anachronism checks.
- Engineering/physical: use functional decomposition and failure analysis; use TRIZ only when a real contradiction has been stated.
- Culture/social systems: investigate context, power, incentives, governance, and knowledge rights; seek appropriate consultation.
- Economics/operations: analyze resources, capacities, queues, routing, matching, incentives, and costs.
- Existing products/processes: analyze permitted workflows and mechanisms; respect access controls, licenses, and confidentiality.

Use `references/nuts-source-domain-playbook.md` for detailed pathways and `docs/methods/NUTS_METHOD.md` for the governing method, limits, and creative-influence practice.

## 4. Analogy quality checks

Before retaining a candidate, answer:

- Is the source system and mechanism actually supported by inspected sources?
- Does the source perform a relevant function?
- Are meaningful relationships mapped rather than surface attributes?
- Are important mismatches explicit?
- Does transfer add value compared with the simplest credible alternative?
- Is there a practical test?
- Are attribution, IP, license, and cultural-knowledge issues handled?

A retained-for-test card must have at least one source and claim record, source accuracy `verified` or `partially_verified`, acceptable functional relevance, at least adequate relational mapping, and a testable hypothesis. Otherwise keep it as a candidate/researching item or reject it.

## 5. Output discipline

Use `templates/records/analogy-card.json` as the machine-readable record and `assets/templates/analogy-card.md` for a human-readable summary. Use `templates/records/nuts-run.json` for the run-level summary. Link sources and claims using their stable project IDs. Do not put sensitive participant data in analogy cards.

Never assert that an idea is original, patentable, legally clear, or “never done before” based on analogy research. State the scope of prior-art search and recommend qualified IP counsel for consequential decisions.
