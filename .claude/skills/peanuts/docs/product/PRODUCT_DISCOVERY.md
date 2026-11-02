# Product Discovery and User Validation Protocol

**Status:** Method specification for first Peanuts implementation  
**Version:** 0.4.0-draft  
**Last reviewed:** 2026-11-01

## 1. Purpose

Prevent Peanuts from jumping from an event theme or interesting idea directly to a solution. Discovery should establish the desired outcome, understand relevant people and contexts, identify opportunities, compare alternatives, and reduce decision-critical uncertainty. This is a selective protocol, not a heavyweight ritual for every project.

## 2. Project modes and stable identifiers

These identifiers name entry modes only. They are not build milestones (`B0–B10`) or user workflow phases (`P1–P10`).

| Mode ID | Mode | Entry point | Main emphasis |
|---|---|---|---|
| `MODE-EVENT` | Event-first | Hackathon, competition, challenge, grant, or accelerator | Official rules, judging, eligibility, deadline, deliverables, problem and event fit. |
| `MODE-PROBLEM` | Problem-first | User group, stakeholder, or observed problem | Context, jobs/needs, current behavior, workarounds, opportunity. |
| `MODE-IDEA` | Idea-first | Rough solution or invention | Preserve intent, identify assumed problem, prior art, users and alternatives. |
| `MODE-EXISTING` | Existing-project | Prototype, codebase, or partially built product | Current behavior, evidence, gaps, technical debt, user feedback and constraints. |
| `MODE-RESEARCH` | Research/prototype | Technical or exploratory question | Research gap, mechanism, feasibility, hypothesis and learning objective. |

The first release prioritizes `MODE-EVENT` and `MODE-IDEA`. Other modes may use the same core methods to the extent practical.

## 3. Discovery principles

- Separate event requirements, desired outcomes, user problems, and proposed solutions.
- Start with the smallest useful research effort; deepen it when uncertainty, risk, or decision impact warrants it.
- Do not treat AI-generated personas, desk research, market reports, or hypothetical journeys as direct user evidence.
- Preserve competing problem framings until evidence supports narrowing.
- Give observed behavior and concrete past examples appropriate weight; do not rely solely on stated future intent.
- Distinguish product merit from event alignment.
- Capture team capabilities and constraints progressively rather than forcing a long questionnaire.
- Make recruitment, consent, privacy, accessibility, and data handling proportionate to the research.

## 4. Discovery sequence

### 4.1 Define the decision and desired outcome

First identify what decision the research must support. Define a meaningful outcome separately from a feature or deliverable. “Build a mobile app” is a deliverable; “help a field team coordinate safely when cellular service is unavailable” is an outcome direction.

When the user does not know the outcome, present a small number of plausible interpretations and ask one high-value question.

### 4.2 Understand people, context, and stakeholders

Investigate as relevant:

- Who experiences the situation and who else is affected?
- What are they trying to accomplish (functional, emotional, or social progress)?
- In what context does the situation occur?
- What happened the last time the problem occurred?
- What do people currently do, use, avoid, or work around?
- What is difficult, risky, slow, costly, inaccessible, or frustrating?
- How frequent or consequential is it, and what supports that estimate?
- Who influences, pays for, operates, maintains, or regulates the solution?
- What constraints shape the current behavior?

Public sources may answer some context questions, but not necessarily the lived experience of a target user.

### 4.3 Use Jobs to Be Done when useful

Use JTBD to understand progress a person seeks in a particular circumstance. Consider functional, emotional, and social dimensions when relevant. A job statement may use:

> When [situation], I want to [progress/job], so I can [desired outcome].

This is a synthesis aid, not a rigid formula or proof of a market. Do not invent quotes or turn an AI persona into a real participant.

### 4.4 Use Opportunity Solution Trees selectively

Use an Opportunity Solution Tree (OST) when multiple user opportunities and solution directions need to be explored against a clear outcome:

- Desired outcome.
- User opportunities (needs, pain points, desires, or barriers).
- Candidate solutions linked to specific opportunities.
- Assumptions and tests beneath candidate solutions.

**Method-fidelity note:** Product Talk's formal OST guidance describes prerequisites including a target-customer/value-proposition theory, a defined outcome, and several story-based customer interviews (its guidance specifies three to four). This is a method-specific recommendation, not a universal sample-size rule for all research. If the prerequisites are missing, Peanuts may create a clearly labelled *provisional opportunity map* based on desk research and hypotheses; it must not present that map as a fully evidence-grounded OST.

Do not build a tree for a small or time-critical project when a simple opportunity table is sufficient.

### 4.5 Investigate alternatives and prior art

Look for direct competitors, substitutes, manual workarounds, open-source projects, academic prototypes, patents where relevant, and non-digital approaches. Compare the target problem, users, mechanism, limitations, adoption, evidence of use, and relevant rights/licensing.

Never claim “first,” “unique,” “no competitor,” or “novel” based on a shallow search. Describe the search scope, terms, databases, dates, and limits. Legal novelty, patentability, and freedom to operate require qualified legal review.

## 5. Balanced evidence and validation strategy

“Balanced” means selecting the evidence type that can best reduce the uncertainty behind the current decision. It is not a fixed ratio of secondary research and interviews.

### Level A — Desk and secondary research

Use official rules, primary research, standards, technical documentation, credible reports, product evidence, and published datasets to establish what is already known. This can verify many event facts and technical constraints. It cannot, by itself, establish that target users want a proposed product or will adopt it.

### Level B — Direct discovery evidence

When user behavior, needs, severity, workflow, access, or adoption materially affects a decision, consider interviews, contextual inquiry, observation, diary studies, participatory methods, or practitioner conversations. Ask about concrete past situations, actions, workarounds, and artifacts before presenting a proposed solution. Avoid leading or sales-oriented prompts.

### Level C — Concept and usability evidence

Use a paper or clickable prototype, task-based usability session, workflow simulation, smoke test, or appropriate experiment. Define the hypothesis, target group, observable behavior, success/failure signals, and limitations before testing.

### Level D — Technical and operational evidence

Use a feasibility spike, API proof, integration test, load/reliability test, field pilot, safety analysis, or expert review. Select the smallest test that meaningfully reduces the uncertainty.

No universal interview or test count is prescribed. Sample size and recruitment depend on the decision, method, population, diversity, time, and consequence. A small convenience sample is exploratory and must not be described as representative of a population.

## 6. User research ethics and participant integrity

Before direct research, define the research objective and what decision the result will influence. Then:

1. Define the target participant groups and the experience required to answer the research question.
2. Set inclusion/exclusion criteria and a practical recruitment approach; record likely selection bias.
3. Consider accessibility, language, accommodations, and power imbalances.
4. Explain who is conducting the research, its purpose, activities, data collected, recording, use/sharing, retention, voluntary nature, and withdrawal process.
5. Obtain appropriate informed consent before participation or recording.
6. Collect only necessary information; anonymize or pseudonymize notes where appropriate; restrict access and set a retention/deletion plan.
7. Follow applicable local laws, institutional rules, school/event policies, and ethics-review requirements. GOV.UK guidance is a useful operational reference, not a substitute for local legal advice.
8. Apply additional safeguards and seek appropriate oversight when involving minors, vulnerable people, sensitive data/topics, or regulated research.

Do not record people or collect personal data simply because the tool makes it easy. Do not treat consent as automatically resolving every legal/privacy obligation.

## 7. Research synthesis and triangulation

Do not stop after collecting notes. Synthesize evidence systematically:

- Separate observations, participant statements, interpretations, and recommendations.
- Code or group recurring patterns without erasing context or dissenting cases.
- Compare accounts with observed behavior, artifacts, analytics, secondary research, and prototype evidence where available.
- Record supporting and contradictory evidence.
- Distinguish an individual anecdote, a repeated qualitative pattern, and a population-level prevalence claim.
- Preserve segment/context differences rather than forcing one average user narrative.
- Link each decision-relevant finding to source/participant IDs and the relevant assumptions or opportunities.

Triangulation can increase confidence when independent evidence converges, but convergent sources may share the same underlying source or bias. Explain source dependence and limitations.

## 8. Capability, constraints, and operating model

Gather only information that affects the next decision. Potential variables include team size/roles, skills, time remaining, weekly capacity, budget and recurring costs, devices/hardware, datasets, infrastructure, API/platform access, target-user access, accessibility, language, connectivity, event restrictions, IP terms, AI-use policy, and relevant domain expertise.

For projects that need ongoing operation, assess who operates, pays for, supports, updates, distributes, and maintains the solution. A business model is not mandatory for every project; a credible operating model is required where the solution depends on sustained service.

Unknown values remain unknown. Do not silently assume expert skills, unlimited time/budget, legal access to data, or production credentials.

## 9. Separate product merit from event fit

### Product merit

Assess whether the concept addresses a meaningful problem, creates a credible benefit, compares favorably with alternatives, is technically plausible, and has a realistic path to adoption or continued operation where relevant.

### Event alignment overlay

For `MODE-EVENT`, separately check official eligibility, theme/track, deliverables, deadline, team restrictions, technology requirements, AI-use rules, IP terms, judging criteria, and submission format. Prefer official organizer sources. Use published judging weights when available; otherwise report qualitative alignment. Never invent weights or merge event fit into product-merit scores.

A project can be a good product but weak event fit, or strong event fit but weak product merit.

## 10. Assumptions and experiment prioritization

For each material assumption, record its owner/source, impact if false, current uncertainty, affected decision, and a feasible test. Prioritize assumptions that are both consequential and poorly evidenced, especially when an inexpensive test can resolve them. Do not multiply subjective ratings into pseudo-precise risk scores unless a defined model is empirically shown to improve decisions.

An experiment record includes hypothesis, rationale, method, target participant/system, recruitment or test conditions, success and failure signals, ethical/data controls, limitations, result, and decision changed.

## 11. Discovery exit criteria

Move to concept development when the desired outcome and problem framing are explicit enough, relevant users/stakeholders are identified, meaningful alternatives are inspected, key constraints and unknowns are recorded, and decision-critical assumptions have an evidence or test plan.

Move to a stronger product commitment only when the level of validation matches the risk and decision. If direct evidence is not available, mark the concept and PRD provisional and record what remains unvalidated.

## 12. Documentation strategy

The Project Brief is the primary summary. Create supporting artifacts only when they add decision value: Event Dossier, opportunity map/OST, recruitment and research plan, synthesis, alternatives comparison, assumption register, validation plan/report, or concept brief. Avoid duplicating facts. Use stable identifiers and links when traceability is useful.

## 13. Operational playbooks and records

Use the following B5 playbooks when the selected method requires them:

- `docs/methods/EVENT_INTELLIGENCE_PROTOCOL.md` for current event rules, eligibility, deadlines, deliverables, judging, technology, AI-use and IP requirements.
- `docs/methods/USER_RESEARCH_PROTOCOL.md` for recruitment, participant selection, consent, accessibility, privacy, session methods and safeguarding.
- `docs/methods/EVIDENCE_SYNTHESIS_PROTOCOL.md` for de-identified synthesis, triangulation, source independence, coverage and decision handoff.
- `docs/methods/RESEARCH_PROTOCOL.md` for end-to-end research planning, source quality, conflicts and stop criteria.

Project workspaces now provide `research-plan.json` and stable JSONL records for research questions, research rounds, findings, and opportunities. Use pseudonymous participant references only. Store identifiable consent records and raw materials outside Git in suitably protected storage.

Method artifacts are conditional: generate an event dossier, user research plan, interview guide, evidence matrix, synthesis, or opportunity map only when it advances the decision. The Project Brief remains the main human-readable summary.

## 14. Key references

- Design Council, Double Diamond: https://www.designcouncil.org.uk/resources/the-double-diamond/
- Christensen Institute, Jobs to Be Done: https://www.christenseninstitute.org/theory/jobs-to-be-done/
- Product Talk, Opportunity Solution Trees: https://www.producttalk.org/opportunity-solution-trees/
- Strategyzer, Test Card: https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card
- GOV.UK, Plan user research: https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service
- GOV.UK, Recruit participants: https://www.gov.uk/service-manual/user-research/find-user-research-participants
- GOV.UK, Informed consent: https://www.gov.uk/service-manual/user-research/getting-users-consent-for-research
- GOV.UK, Analyse a research session: https://www.gov.uk/service-manual/user-research/analyse-a-research-session
- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
