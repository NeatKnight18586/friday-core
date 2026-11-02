# Evidence boundaries for the Peanuts vertical slice

## Keep these categories separate

| Category | Meaning | Example label |
|---|---|---|
| External fact | A claim directly supported by an inspected source | `VERIFIED — PRIMARY SOURCE` |
| Secondary evidence | A claim supported by a credible secondary source | `SUPPORTED — SECONDARY SOURCE` |
| User-reported | What the user or participant says | `USER-REPORTED` |
| Observed | What was directly observed | `OBSERVED` |
| Measured | Result of a described measurement or test | `MEASURED` |
| Inference | A reasoned interpretation of available evidence | `INFERRED` |
| Assumption | A proposition not yet established | `ASSUMPTION — UNTESTED` |
| Synthetic | Fictional test data used to exercise the workflow | `SYNTHETIC TEST DATA` |
| Unknown | Not inspected, inaccessible, stale, or unresolved | `UNKNOWN / NOT CHECKED` |

## Source handling

- Prefer the source closest to the claim: official event rules for eligibility, official API docs for an API, a standard's publisher for standard status, and primary research where available.
- Record title, publisher/author when known, URL/identifier, publication/version date, access date, source type, access status, validity status, and limitations.
- Search-result snippets are discovery aids, not sufficient support for consequential claims. Open and inspect the source.
- A source can be authoritative but irrelevant, current but indirect, or primary but incomplete. Assess authority, directness, recency, and context fit separately.
- When sources conflict, record the conflict and explain why one source is preferred. Do not silently discard counterevidence.
- Never create a citation, quote, interview, observation, statistic, or user-validation claim that did not occur.

## User research boundaries

Desk research, synthetic personas, hypothetical journeys, and AI-generated interviews are not direct user validation. Before interviews or tests, explain purpose, recording, data use, sharing, retention, and voluntary participation; obtain appropriate consent. Recruit participants who are relevant to the decision and describe sampling limitations. Avoid collecting unnecessary personal or sensitive data. Use additional safeguards for minors or vulnerable groups and seek institutional/professional guidance where required.

## Research sufficiency

Stop when additional search is unlikely to change the decision, the decision's evidence threshold is met, or remaining uncertainty is explicitly accepted as a blocker/assumption. State scope, date, sources searched, important gaps, and what would change the conclusion. There is no universal source-count threshold.
