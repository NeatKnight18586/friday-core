# User and Problem Discovery Playbook

Use this reference when a project depends on understanding people, their needs, behavior, context, workarounds, access, or adoption.

## 1. Start with a decision

State what decision the research should inform. Convert opinions into questions. Identify what evidence would change the decision. Do not begin by testing whether people like the proposed solution.

## 2. Select the least-cost credible method

| Question | Candidate method | What it can support |
|---|---|---|
| What are users trying to accomplish? | Story-based interview, contextual inquiry | Needs, jobs, context, workarounds, vocabulary |
| What do users actually do? | Observation, artifact walk-through, diary study | Observed behavior in a particular context |
| Can users complete a task? | Moderated usability test, prototype test | Task success, friction, comprehension in the tested prototype/context |
| How common is a behavior? | Properly designed survey or behavioral dataset | Prevalence estimates only when sampling/design support them |
| Will a change improve outcomes? | Controlled/appropriate experiment or longitudinal measurement | Effect estimate under the design's assumptions |
| Can the system work? | Technical spike, integration test, field trial | Demonstrated technical behavior within tested conditions |

Do not use an interview to estimate population prevalence or a prototype preference question as proof of adoption.

## 3. Participant planning

Define target groups by experience relevant to the question, not merely easy-to-reach demographics. Record inclusion/exclusion criteria, recruitment channel, sample rationale, likely selection bias, underrepresented perspectives, accessibility/language requirements, and whether the group includes minors or vulnerable people.

A convenience sample is acceptable for exploratory learning when disclosed. It is not representative by default. There is no universal sample count. Choose a method-appropriate sample and iterate when findings are unclear or segments differ.

## 4. Interview practice

Start with recent concrete events:

- “Tell me about the last time this happened.”
- “What were you trying to do?”
- “What did you do first?”
- “What happened next?”
- “What tools, people, or workarounds did you use?”
- “What was difficult or costly?”
- “What did you do when the normal process failed?”
- “Can you show me an example or artifact, if comfortable?”

Avoid leading or hypothetical questions such as “Would you use our app?” or “Don't you think this would be useful?” Ask about actual past behavior before showing a concept. Separate direct quotes from interviewer interpretation.

## 5. Consent, accessibility and privacy gate

Before recruitment, prepare participant information in understandable language. Explain purpose, activities, data, recording, observers, sharing, retention, withdrawal, and contact/responsible organization. Obtain and retain appropriate informed consent before participation/recording. Participation is voluntary.

Use pseudonymous participant codes in project records. Store signed consent, contact information, raw recordings, identifiable notes, and sensitive materials only in a properly authorized, access-controlled location outside the Git repository. Collect the minimum necessary. Define retention/deletion and withdrawal handling.

If participants are minors, vulnerable, or asked about sensitive topics, or if the study may require institutional/legal approval, pause and obtain appropriate supervision/review. This playbook is not legal or ethics-board advice.

## 6. Synthesis

For each note, distinguish:

- Observation: what the researcher directly saw.
- Participant statement: what the participant said.
- Interpretation: what the team thinks it may mean.
- Recommendation: what the team proposes to do.

Code/group patterns, preserve contrary cases, compare segments, and link findings to research questions, claims, and opportunities. Do not fabricate quotes or use AI-generated personas as participants. AI may help organize de-identified notes, but a human researcher must inspect the synthesis and protect the raw data.

## 7. Opportunity mapping

Use JTBD to articulate progress in a circumstance, not to force a rigid sentence. Use an Opportunity Solution Tree only when a meaningful outcome and target-customer theory exist and the appropriate discovery inputs are available. Product Talk describes three to four story-based interviews as a prerequisite in its formal method. Without those prerequisites, label the artifact `PROVISIONAL OPPORTUNITY MAP` and include the missing evidence.

Keep opportunity statements solution-neutral. Link them to supporting and contradictory finding/claim IDs. Preserve different user segments rather than averaging their needs together.

## 8. Output and stop criteria

Produce a problem brief or synthesis that shows: target segment/context, desired progress, current behavior/workarounds, findings, contradictions, opportunity hypotheses, evidence strength, unrepresented groups, assumptions, and next tests.

Stop when the decision can be made responsibly, or make the remaining uncertainty explicit and classify the output as provisional/blocked. Do not claim validated demand when direct evidence is absent.
