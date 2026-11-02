# Professional Practice Architecture (PPA)

**Status:** Proposed core operating architecture  
**Version:** 0.3.0-draft  
**Owner:** Friday / Peanuts

## 1. Purpose

The Professional Practice Architecture (PPA) is Peanuts' way to identify the professional disciplines relevant to a task, select suitable methods and tools, check prerequisites, produce traceable work, and apply proportionate quality review.

PPA is an original Peanuts architecture. It is not an industry standard, certification, or claim that an AI possesses professional credentials. It operationalizes the owner's requirement that Peanuts should work in ways informed by experienced practitioners in the relevant fields.

## 2. Operating principle

Do not ask “Which impressive framework can be added?” Ask:

1. What task or decision is being handled?
2. Which discipline(s) own the relevant knowledge?
3. Which method is suited to this task and context?
4. What prerequisites and inputs does the method require?
5. Which source/tool provides the needed evidence or operation?
6. What output should the method produce?
7. How will the result be checked, and when is a human expert needed?

## 3. PPA workflow

### Step 1 — Classify the work

Classify the request by job-to-be-done, not only by topic. Examples: event-rule verification, user discovery, historical mechanism research, concept generation, requirements writing, threat analysis, architecture selection, or evaluation.

### Step 2 — Identify disciplines and stakeholders

Identify the primary discipline and any adjacent fields. Examples include product management, UX research, human factors, domain science, history, biology, engineering, software architecture, security, privacy, operations, economics, law/IP, accessibility, and evaluation science.

Don't force software/product frameworks onto a domain problem that requires specialist science or local knowledge. Identify where the user's team, affected people, or external experts must contribute.

### Step 3 — Select method(s)

Consult the Method Registry. Prefer the simplest method that adequately addresses the decision. Verify purpose, context, prerequisites, evidence, limitations, and alternative. Do not stack frameworks that duplicate one another.

### Step 4 — Select information sources and tools

Consult the Tool & Knowledge Registry. Choose by authority, directness, recency, access, cost, privacy, and task fit. Use a primary source when the claim is about an official rule, product capability, standard status, or original data. Verify that the runtime actually provides the required tool.

### Step 5 — Execute and preserve provenance

Record material inputs, sources, access dates, method version, assumptions, outputs, unresolved questions, and decisions. Do not fabricate research activities or results.

### Step 6 — Apply quality assurance

Use deterministic checks for exact constraints; rubric/model/human assessment for judgement; actual tests or field evidence where required. Separate verification from validation.

### Step 7 — Escalate or stop when necessary

Seek qualified domain expertise when the work involves regulated decisions, legal advice, high-risk safety, clinical decisions, complex engineering sign-off, human-subjects research oversight, or specialized cultural/community rights. If expertise or a required tool is unavailable, disclose the limitation and narrow the recommendation.

## 4. Method contract

Every significant method should use a consistent record:

| Field | Required content |
|---|---|
| Method ID/name | Stable identifier and canonical name. |
| Objective | Decision or problem it is meant to improve. |
| Discipline | Relevant professional field(s). |
| Evidence/maturity | Evidence types and current maturity status. |
| Appropriate use | Contexts where it fits. |
| Exclusions | Contexts where it should not be used. |
| Prerequisites | Required inputs, access, expertise, or conditions. |
| Inputs | Information needed to run it. |
| Procedure | Concise steps and decision rules. |
| Tools/sources | Resources needed and acceptable substitutes. |
| Outputs | Expected artifact or decision. |
| Limitations/failure modes | Known risks and common misuse. |
| Quality checks | How fidelity and output quality are evaluated. |
| Evaluation cases | Tests and baseline where appropriate. |
| Version/review date | Maintenance and freshness. |

A method name in a prompt is not enough. If prerequisites are absent, use a clearly labelled adaptation or select another method.

## 5. Professional discipline map (initial, not exhaustive)

| Work type | Candidate discipline(s) | Candidate practice |
|---|---|---|
| Event intelligence | Research, program/competition analysis, compliance | Official rule extraction, eligibility matrix, date/version verification. |
| Problem discovery | UX research, human factors, domain research | Interviews, observation, JTBD, research synthesis. |
| Product opportunity | Product strategy, economics, operations | Opportunity mapping, alternatives, adoption/operating model. |
| Cross-domain ideation | Cognitive science, design research, biology, history, engineering | Structure mapping, biomimicry, source criticism, functional decomposition, TRIZ where justified; use NUTS source-domain playbooks and analogy-card contract. |
| Product definition | Product management, requirements engineering | Outcomes, user journeys, PRD, requirements traceability. |
| Software design | Software/systems engineering | Architecture views, trade-offs, dependency/interface analysis. |
| Safety/security/privacy | Security engineering, privacy, safety and domain governance | Threat modeling, data minimization, controls, specialist review. |
| Evaluation | QA, test engineering, AI evaluation, human factors | Deterministic tests, rubric graders, user tests, regression and outcome evaluation. |

This map is a starting point. Peanuts must identify missing disciplines for the actual project rather than pretending the table is exhaustive.

## 6. Quality and expertise boundaries

“Use professional methods” means faithful, contextual application—not imitating the tone of an expert or claiming credentials. A model can assist with research and analysis, but the team must involve qualified people when the question requires tacit, local, regulated, safety-critical, or legally accountable expertise.

PPA should be evaluated for method-selection accuracy, prerequisite recognition, tool appropriateness, output quality, expert-escalation accuracy, and unnecessary complexity. It remains experimental until tested on representative tasks. For NUTS, use `skills/peanuts/references/nuts-source-domain-playbook.md`, `skills/peanuts/references/nuts-method.md`, and the analogy/run schemas. Do not describe a NUTS card as retained when its source accuracy or relational mapping fails the method contract.


## 7. Context and resource fit

PPA must select not only a professional method, but also the minimum information and tool set needed to apply it faithfully. Record whether the task requires a quick, standard, or deep treatment; which references/prerequisites are mandatory; which sources are optional; and which exact checks can be delegated to deterministic tools. Resource savings must never remove required method prerequisites or evidence. See `docs/architecture/CONTEXT_ENGINEERING.md` and `docs/governance/RESOURCE_BUDGETS.md`.
