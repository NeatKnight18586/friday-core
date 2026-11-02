# Peanuts Research Engine — Routing and Execution

Use this reference to orchestrate B5 research methods. Detailed procedures live in the linked references; do not load all research guidance for every task.

## 1. Select the research mode

- Event/competition/grant named: load `event-intelligence.md` first.
- People or problem named: load `user-discovery.md`.
- Existing claims/findings from mixed sources: load `evidence-synthesis.md`.
- Technical, market, historical or academic question: load `../evidence-boundaries.md` and the relevant entry in the Tool & Knowledge Registry; apply the Research Protocol.
- Mixed project: combine only the relevant branches.

## 2. Create a decision-led plan

Identify the decision, desired outcome, high-impact research questions, critical assumptions, source targets, available tools, timebox, ethical constraints, and stop criteria. Use `research-plan.json` and `research-questions.jsonl` in the project workspace. Ask only the most important missing question after making useful progress.

## 3. Research using host capabilities

Use the current host's web search, page opening/fetching, document reading, academic search, or permitted connectors where available. Tool names differ by host. Do not assume a tool exists because it appears in the registry. If no browsing/search capability is available, request source material or provide a research plan marked `not_checked`; never fabricate results.

Preferred sequence:

1. Official/primary sources for event requirements, laws, standards, vendor documentation and release facts.
2. Original research and high-quality datasets for empirical claims.
3. Credible syntheses and practitioner sources for context.
4. Direct user or field research where behavior/needs/adoption cannot be established from desk research.
5. Technical spikes, prototypes or tests for actual feasibility/performance.

Use discovery indexes to find sources, not as a substitute for inspecting the underlying source. Crossref provides metadata deposited by publishers/members and trusted sources; metadata availability does not mean full-text availability, peer review, or study quality. See https://www.crossref.org/documentation/retrieve-metadata/rest-api/. Do not infer a paper's methods or findings from metadata alone.

## 4. Preserve the evidence chain

Create source records for inspected sources, claim records for material statements, question records for research questions, and finding records for synthesized results. Link every claim/finding to source IDs and question IDs where possible. Preserve counterevidence. Use `research-rounds.jsonl` only for actual planned/conducted direct research, with pseudonymous participant references and consent/data safeguards.

## 5. Event-first sequence

Run the Event Intelligence Protocol. Inspect the current official edition, identify eligibility, deadline/timezone, challenge, deliverables, judging, technology, AI-use, IP and submission rules. Record each requirement as confirmed, interpreted, conflicting, not_found or not_checked. Do not claim event eligibility is confirmed if a material rule is unknown.

## 6. User/problem discovery sequence

Start from actual context and the desired progress. Identify target groups, current behavior, workarounds and stakeholders. Use JTBD when it clarifies the job. Use an Opportunity Solution Tree only when its method prerequisites are satisfied; otherwise make a provisional opportunity map. Plan interviews/observation only when needed and ethically feasible. Do not describe desk research or generated personas as user validation.

## 7. Synthesis and decision gate

Load `evidence-synthesis.md`. Summarize support, counterevidence, gaps, source dependence, participant/context limitations and the decision implication. Ask for direct user evidence or expert/organizer clarification when needed. A draft opportunity brief may proceed with explicit unknowns; claims about validated demand, prevalence, adoption, novelty or technical performance require appropriate evidence.

## 8. Quality gate

Before marking research complete, verify:

- The decision and questions were explicit.
- Sources were inspected and date/version checked where material.
- Primary sources were prioritized where appropriate.
- Claims and findings have traceable IDs.
- Conflicts, counterevidence and unknowns are visible.
- User research has consent, recruitment, accessibility and privacy safeguards.
- Sample limitations are not overstated.
- Stop criteria are met, or the report is clearly time-boxed/incomplete.

A structurally valid research plan is not proof that research actually occurred. An AI-generated synthesis is not direct user evidence.
