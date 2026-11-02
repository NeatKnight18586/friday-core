# Context and Resource Efficiency Evaluation

**Status:** B6.5 evaluation design; runtime comparisons not yet run  
**Version:** 0.2.0-draft  
**Last reviewed:** 2026-11-01

## 1. Purpose

Evaluate whether Friday's progressive-disclosure and resource policies reduce unnecessary context/tool work while preserving or improving task quality. This is a hypothesis to test, not an assumed benefit.

## 2. Evaluation questions

1. Does the correct capability get selected for the request?
2. Are only task-relevant references loaded?
3. Are mandatory methods, evidence, safety and output requirements still followed?
4. Can a fresh session resume from the saved handoff without reading the full conversation?
5. Does quick/standard/deep mode change depth as intended?
6. Does selective retrieval reduce measured usage or time on the same host/model/task without reducing quality?
7. Does adding capabilities increase routing errors or always-on metadata overhead?

## 3. Baselines

Use at least two comparison conditions when live runtime evaluation becomes available:

- **Baseline A — broad context:** a controlled version of the task where a defined, larger set of relevant repository documents is provided up front.
- **Candidate B — progressive disclosure:** a compact entry point and selected files loaded on demand.

Both conditions must receive the same user request, source availability, tool permissions and evaluation rubric. The baseline is not intentionally degraded and must not contain secret or irrelevant data.

Where useful, compare native host skill discovery with explicit invocation. Record differences rather than assuming identical triggering.

## 4. Quality dimensions

- Task correctness and completeness.
- Evidence coverage and provenance.
- Method fidelity/prerequisites.
- Safety and permission compliance.
- Handoff/resume accuracy.
- User usefulness/readability.
- Critical omission and false-confidence rate.

## 5. Resource dimensions

Measure actual input/output/cached tokens and cost only when available from host/API telemetry. Otherwise record observable proxies: files loaded, approximate words/characters, tool calls, search iterations, retries, latency, and output length. Never convert proxies into an invented token count.

## 6. Acceptance logic

- The candidate must pass all mandatory correctness, evidence, safety and handoff checks.
- A reduction in token/tool use is beneficial only if quality remains within the predeclared non-inferiority margin or improves. Define that margin per evaluation set before comparing outputs; do not invent a universal threshold.
- Critical failures are release-blocking regardless of average score.
- Report per-case results, failures, confidence, and sample size. Do not make statistical claims from a handful of synthetic examples.
- Re-run regression cases when skill metadata, references, registry/routing, budgets or host adapters change.

## 7. Experimental design and reporting

For a meaningful comparison of broad-context and progressive-disclosure approaches:

1. Use the same user task, model/version, host, tool permissions, source availability, and output requirements.
2. Define the quality rubric and any non-inferiority margin before inspecting results.
3. Use the same cases in both conditions; randomize or counterbalance run order where practical to reduce order effects.
4. Repeat cases when feasible because model outputs vary; record the number of runs and avoid significance claims from small samples.
5. Have outputs graded without exposing the condition label where practical. Keep graders' evidence and rationales.
6. Report quality failures and resource metrics together, including per-case results and critical omissions.
7. Preserve prompts, selected references, tool traces where available, host/model version, and evaluator version so a result can be reproduced.

A small synthetic test set is useful for debugging and early regression checks, but it cannot establish broad token savings, general task-quality equivalence, or statistical significance. A live evaluation must use realistic tasks and an explicitly scoped sample.

## 8. Current test status

EVAL-039–050 are synthetic readiness cases for future live model evaluation. Their JSON structure can be validated in CI. They are not passed by Claude, Codex, or ChatGPT merely because they are present or schema-valid. EVAL-047–050 additionally cover multi-capability context loading, no-forced-routing, safety escalation under a small requested budget, and deferring a custom Friday manager until there is evidence of need.

## 9. References

- OpenAI, Harness engineering (2026-02-11): https://openai.com/index/harness-engineering/
- Anthropic, Agent Skills overview: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- OpenAI, Skills guide: https://developers.openai.com/api/docs/guides/tools-skills
- OpenAI, Prompt caching guide: https://developers.openai.com/api/docs/guides/prompt-caching
