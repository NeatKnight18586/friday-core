# Context, Token and Resource Budgets

**Status:** B6.5 operating policy; hard enforcement depends on host/runtime  
**Version:** 0.2.0-draft  
**Last reviewed:** 2026-11-01

## 1. Objective

Use the smallest amount of context, research, tool activity, and output that can reliably meet the task's quality and safety requirements. Efficiency must not conceal uncertainty, skip required evidence, weaken safety, or misrepresent work as validated.

Friday cannot guarantee a fixed percentage of token or subscription-credit savings across consumer AI products. It controls repository-owned instructions and its own retrieval/tool behavior; providers control hidden prompts, tokenization, model usage accounting, caching, context limits, and subscription quotas.

## 2. Resource dimensions

Budget the resources relevant to the task:

- Model input/output tokens (only when the host exposes actual counts).
- Context sources/files and approximate words/characters loaded.
- Web/search/API/tool calls and repeated requests.
- Number of research or review iterations.
- External API cost, service quotas, latency, and compute.
- Human attention and project time.

Word/character counts are maintainability proxies, not token measurements. Do not convert characters to a claimed token count. Do not compare raw token totals across model providers as if tokenizers and hidden context were identical.

## 3. Operating modes

Use `standard` by default. The user may request `quick` or `deep`. Modes change depth and resource planning, not truthfulness or mandatory safeguards.

| Mode | Typical use | Context/retrieval behavior | Review/research behavior | Output |
|---|---|---|---|---|
| `quick` | Exploration, simple questions, low-consequence choices | Selected capability only; normally 0–1 supporting references; use current project summary, not full history | One concise pass; no full Four-Council unless requested or risk requires it | Brief, clearly preliminary when evidence is limited |
| `standard` | Normal Peanuts work; default | One primary capability; add at most one supporting capability initially; retrieve references as needed, normally 1–3 to start | Decision-led research with explicit stopping criteria; targeted critique; validate material claims | Complete practical output with evidence, assumptions and next steps |
| `deep` | High-consequence decisions, major submissions, final reviews | Load all task-relevant references and evidence; still exclude unrelated capability files | Plan the research/evaluation budget; full Four-Council when appropriate; use adversarial checks and repeat tests | Detailed report, traceability and limitations |

The reference counts are starting targets, not hard limits. A high-risk task may require escalation beyond a mode's usual depth. A low-risk task should not be expanded merely to consume the budget.

## 4. Escalation rules

Escalate from quick to standard/deep when:

- The decision is consequential, difficult to reverse, or safety/privacy/legal sensitive.
- Official rules, deadlines, standards, prices, APIs, or other time-sensitive facts must be verified.
- Evidence conflicts or material claims remain unsupported.
- A method's prerequisites are not met.
- A critical assumption could invalidate the result.
- The user explicitly requests deeper review.

If available resources cannot support the required work, stop at a provisional result, disclose what is missing, and provide the next validation step. Do not relabel a shallow pass as deep.

## 5. Default resource controls

- Do not load all capabilities or all references by default.
- Do not reread a complete project history when a current status/handoff plus linked records is sufficient.
- Do not run all four councils on every minor task; use risk-adaptive review while preserving core criteria.
- Do not create multiple agents/subagents by default. Require a specific benefit such as parallel independent research or isolated long-context review, and compare the benefit with coordination/token cost.
- Avoid repeated searches that return the same evidence. Search to resolve a decision question and stop when additional coverage is unlikely to change the decision, while retaining unresolved gaps.
- Prefer compact summaries with source/record IDs and paths over unbounded raw output.
- Use deterministic scripts for exact, repeated processing; return concise summaries and traceability.
- Keep output proportional to the requested decision and user preference.

## 6. Hard versus soft budgets

| Runtime | What can be controlled | What cannot be guaranteed by a portable skill |
|---|---|---|
| Claude Code / consumer UI | Instructions, selected files, tool behavior, user-visible workflow | Provider hidden context, subscription limits, exact credit usage, all internal tool accounting |
| ChatGPT consumer UI/Projects | Instructions/files supplied, response scope, workflow and manual retrieval | Universal token cap, exact internal usage, automatic filesystem access on every surface |
| Codex/agent runtime | Skill selection and accessible context; host-supported tool policies | Identical behavior to Claude or ChatGPT; all hidden provider overhead |
| Custom API/orchestrator | Where APIs expose them: max output tokens, model choice, tool-call caps, timeouts, spend limits, retrieval limits, tracing | Complete cost/quality guarantees; all provider-specific overhead or external service charges |

Only a custom runtime can reliably enforce hard request-level limits such as API `max_output_tokens`, tool-call ceilings, timeouts, and spend controls—where the provider exposes those controls. A portable `SKILL.md` expresses policy but does not enforce hidden platform quotas.

## 7. Usage measurement

Record exact token/cost usage only from actual host/API telemetry. If unavailable, mark `not_available`. Optional proxy metrics may include:

- Number of files/references explicitly loaded.
- Number of search/tool calls.
- Number of review/repair iterations.
- Output size in words/characters.
- Whether the task needed a fresh-session reload.

Do not label proxy metrics as tokens or credits. Use the same host/model/task test setup for before/after comparison. Evaluate output quality alongside usage; a cheaper answer that misses critical evidence is not an improvement.

## 8. Cache policy

Prompt caching is provider-specific and may reduce repeated processing cost/latency for eligible stable prefixes. It does not make cached content disappear from the context window and is not a portable guarantee. Do not make Friday depend on cache availability. Prefer concise stable prefixes and host-native caching only after checking current documentation and measuring actual usage.

## 9. Per-task resource plan

Before a material research or multi-step task, record a short resource plan proportionate to the task:

- **Decision:** what decision or output must this work support?
- **Mode:** quick, standard, or deep, including why the mode fits.
- **Required methods/evidence:** mandatory prerequisites and evidence types.
- **Retrieval plan:** which capability, project state, references, and sources are expected to be needed.
- **Tool plan:** which tools are available and why they are needed.
- **Stopping conditions:** what would be sufficient to answer, and what unresolved gap would trigger escalation?
- **Escalation:** what additional work requires more time, tool calls, provider/API cost, or user permission?

For an ordinary low-consequence request, this plan can be an internal brief rather than a separate document. For a deep or consequential task, preserve it in the project record. Do not create a plan document for every trivial interaction.

## 10. Provider-specific enforcement boundary

A skill can request economical behavior but cannot reliably enforce consumer-product credit limits, hidden prompt size, or provider usage accounting. Where a custom API runtime is later justified, enforce supported limits at the orchestrator boundary (for example output-token ceilings, tool-call ceilings, timeouts, retrieval limits, and spend limits). Keep secrets and billing controls outside the portable skill. Provider-specific limits and pricing must be checked at the time of implementation.

## 11. Default mode for Peanuts

`standard` is the default. `quick` is appropriate for early exploration, but it must label weakly evidenced results as preliminary. `deep` is for consequential decisions or explicit requests. Four-Council depth remains adaptive; no mode silently drops critical-risk checks.
