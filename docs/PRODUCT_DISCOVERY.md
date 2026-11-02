# Product Discovery and Validation Protocol

**Status:** Stage 0.5 methodology draft; owner approval pending  
**Version:** 0.2.0-draft  
**Applies to:** Peanuts project modes P1–P4

## 1. Purpose

This protocol prevents Peanuts from jumping from a theme or interesting idea directly to a solution. It combines a flexible discovery process with selected professional methods. It is not a mandatory heavyweight process for every project.

## 2. Discovery principles

- Separate event requirements, user problems, and proposed solutions.
- Start with the smallest useful research effort; expand when uncertainty or consequence warrants it.
- Do not treat AI-generated personas, market estimates, or desk research as direct user evidence.
- Preserve competing problem framings until evidence supports narrowing.
- Distinguish product merit from competition/event fit.
- Capture the user's capabilities and constraints progressively, not with a mandatory questionnaire.

## 3. Project modes

| Mode | Entry point | Discovery emphasis | Event overlay |
|---|---|---|---|
| Event-first | Event name, URL, track, or challenge | Rules, target problem, stakeholder needs, judging rubric, timeline, deliverables | Required |
| Problem-first | User group or observed problem | Jobs, current behavior, pain points, context, alternative solutions | Optional |
| Idea-first | Rough solution or invention | Preserve intent, identify assumed problem, compare prior art, discover users | Optional |
| Existing-project | Prototype, codebase, or partially built product | Current behavior, user evidence, gaps, constraints, technical debt | Optional |
| Research/prototype | Technical question or uncertain mechanism | Research question, feasibility, experiment, learning objective | Optional |

For the first release, prioritize Event-first and Idea-first technology-enabled projects. Other modes are supported only to the depth that can be handled without broadening the initial product excessively.

## 4. Discovery sequence

### 4.1 Identify the desired outcome

Ask what meaningful change the project should create. An outcome is not the same as a feature or deliverable. For example, “build a mobile app” is a deliverable; “help a field team coordinate safely when cellular service is unavailable” is an outcome direction.

When the user does not know, offer a small number of interpretations and ask one high-value clarifying question.

### 4.2 Understand the problem and context

Determine:

- Who experiences the situation?
- What are they trying to accomplish?
- In what context does the problem occur?
- What do they do today?
- What is frustrating, slow, costly, risky, or inaccessible?
- How frequent or consequential is it?
- Who else is affected or has influence?
- What constraints shape the situation?

Do not assume all answers can be obtained from public sources.

### 4.3 Use Jobs to Be Done (JTBD) when it helps

JTBD is useful when Peanuts needs to understand the progress a person is trying to make and the circumstances that cause them to seek a solution. Use functional, emotional, and social dimensions where relevant.

A concise job statement may follow this pattern:

> When [situation], I want to [progress/job], so I can [desired outcome].

This is a discovery aid, not a rigid formula or proof that a market exists. Avoid demographic stereotypes and avoid rewriting a user's observation into a fabricated “customer quote.”

### 4.4 Map opportunities and solutions

Use an Opportunity Solution Tree (OST) when a project has multiple possible user needs and solution directions:

- Desired outcome at the root.
- User opportunities beneath it (needs, pain points, desires, or barriers).
- Potential solutions beneath each opportunity.
- Assumption tests beneath candidate solutions.

**Important method-fidelity caveat:** Teresa Torres / Product Talk describes prerequisites for a formal OST: a theory of the target customer and value proposition, a clearly defined outcome, and several story-based customer interviews (the guide specifies three to four). If these inputs are not available, Peanuts may create a *provisional opportunity map* from desk research and explicit hypotheses, but must label it as an adaptation rather than implying that it is a properly evidence-grounded OST. Do not invent customer opportunities.

Do not create an elaborate tree for a tiny or time-critical project. A simple table may be enough. Ensure each candidate solution remains linked to the opportunity it is intended to address.

### 4.5 Investigate alternatives and prior art

Look for direct competitors, substitutes, workarounds, open-source projects, academic prototypes, existing products, and non-digital approaches. Compare the problem addressed, target user, mechanism, limitations, adoption barriers, and evidence of use.

Do not claim “first,” “unique,” or “no existing solution” based on a quick search. State the scope and limits of the prior-art search.

## 5. Balanced validation policy

“Balanced” is an adaptive evidence strategy, not a fixed ratio of desk research to interviews.

### Level 1 — Desk research and secondary evidence

Use official sources, relevant research, product documentation, credible reports, and existing case studies to map what is already known. This level can establish event requirements, technical constraints, known alternatives, and published evidence. It cannot, by itself, establish that the target users want the proposed product or will adopt it.

### Level 2 — Direct discovery evidence

When user needs, behavior, severity, workflow, or adoption materially affects the decision, plan direct evidence such as interviews, contextual inquiry, observation, diary studies, or conversations with relevant practitioners. Use neutral questions; ask about actual past behavior and workarounds rather than leading respondents toward the proposed solution.

No universal interview count is prescribed. Sample size and participant selection depend on the decision, population diversity, access, time, and research method. A small convenience sample should be described as exploratory, not representative.

### Level 3 — Concept or prototype validation

Use a paper prototype, clickable prototype, demo, usability session, task test, landing-page test, or other suitable experiment to examine a specific hypothesis. Define the observable behavior and success/failure signal before running the test.

### Level 4 — Technical or operational validation

Use a feasibility spike, integration test, load test, field pilot, workflow simulation, or expert review to test technical and operational assumptions. Choose the smallest test that meaningfully reduces the relevant uncertainty.

### Rules

- Research first when it can answer questions efficiently and prevent unnecessary user burden.
- Seek direct evidence when a critical claim concerns real users or real-world behavior.
- If direct evidence is unavailable, record the access limitation and leave the claim unvalidated.
- Never say “users want,” “customers confirmed,” or “validated” unless actual evidence supports that wording.
- Time-box testing according to the deadline, but disclose which assumptions remain open.
- High-consequence, safety-sensitive, or hard-to-reverse decisions require stronger evidence and expert review than a low-risk hackathon concept.

## 6. Capability and constraint profile

Gather only details that materially affect the next decision. Ask conversationally and reuse known, current information where appropriate.

Potential variables:

- Team size and role availability.
- Relevant technical and domain skills.
- Time remaining and weekly capacity.
- Budget and recurring cost tolerance.
- Devices, hardware, datasets, and infrastructure available.
- API credentials, platform permissions, and service access.
- Access to intended users, practitioners, or field sites.
- Event restrictions, intellectual-property terms, and AI-use rules.
- Accessibility, language, connectivity, location, and operating constraints.

Unknown values remain unknown. Do not silently assume an expert team, unlimited budget, production access, or permission to use data.

## 7. Separate product merit from event fit

For event-first projects, produce two distinct views:

### Product merit

Does the concept address a meaningful problem, create value, differentiate from alternatives, and have a plausible path to implementation or adoption?

### Event fit

Does the concept comply with the official eligibility rules, track, theme, deliverables, technology requirements, intellectual-property terms, timeline, and published judging criteria?

Use official judging weights when available. If no weights are published, report a qualitative alignment analysis. Do not invent weights or merge the event score into product merit.

## 8. Assumption and experiment prioritization

Record important assumptions and assess them qualitatively by:

- **Impact if false:** Would the assumption invalidate the concept, create serious harm, or materially change the product?
- **Uncertainty:** How little reliable evidence currently exists?
- **Testability:** Is there a practical test that can reduce the uncertainty within the available time?

Prioritize assumptions that are both consequential and uncertain, especially when a low-cost test is available. Avoid a pseudo-precise multiplication score unless a later evaluation demonstrates that a defined scoring model improves decisions.

Each experiment record should include: hypothesis, rationale, target participant/system, method, success signal, failure signal, limitations, result, and decision changed.

## 9. Documentation strategy

The **Project Brief** is the primary user-facing summary. Supporting artifacts are created only when they add value.

Typical conditional outputs:

- Event Dossier for an event-first project.
- JTBD notes or opportunity map for complex discovery.
- Alternatives/prior-art comparison when differentiation matters.
- Assumption Register and Validation Plan when important unknowns remain.
- Concept Brief for a selected direction.

Avoid separate documents that repeat the same facts. Use links and identifiers to preserve traceability.

## 10. Exit criteria

Discovery is sufficient to move forward when:

1. The desired outcome and problem framing are explicit enough for concept development.
2. Relevant users or stakeholders are identified.
3. Current alternatives and known workarounds have been examined to an appropriate depth.
4. Critical constraints and unknowns are recorded.
5. Product merit and event fit (where relevant) are clearly separated.
6. The highest-impact assumptions are identified with a plan to test or knowingly carry them.

This is an exit-to-next-step criterion, not a claim that the product has been validated.

## 11. Key references

- Design Council, Double Diamond: https://www.designcouncil.org.uk/resources/the-double-diamond/
- Christensen Institute, Jobs to Be Done theory: https://www.christenseninstitute.org/theory/jobs-to-be-done/
- Product Talk, Opportunity Solution Trees: https://www.producttalk.org/opportunity-solution-trees/
- Strategyzer, Test Card: https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card
