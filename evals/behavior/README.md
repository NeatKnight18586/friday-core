# Behavioral comparison pilot

**Status: prepared, not executed.** Twelve authored synthetic tasks are inputs, not outcomes. A real Codex preflight failed authentication; see [preflight.json](preflight.json). This suite does not replace the older 146 cases or their historical results.

## Predeclared comparisons

| Condition | Instructions | Critique |
|---|---|---|
| ordinary | Competent general planning prompt | Simple structured critique |
| peanuts-no-nuts | Rendered Peanuts with analogy instructions suppressed and NUTS reference omitted | Simple structured critique |
| peanuts-simple | Rendered Peanuts with NUTS available, selectively used | Simple structured critique |
| peanuts-four | Same Peanuts/NUTS condition plus full council protocol | Four-Council |

Compare `peanuts-simple` with `ordinary` for the planning package, `peanuts-simple` with `peanuts-no-nuts` for the NUTS instruction intervention, and `peanuts-four` with `peanuts-simple` for council instructions. A three-condition design would confound NUTS and council changes. These are **rendered instruction interventions**, not isolated causal tests of internal reasoning or native Skill discovery. Context length differs by design; record it, rather than attributing all effects to a method name. The no-NUTS entrypoint still mentions Peanuts vocabulary outside its removed operative paragraph/table row; this is a suppression condition, not a perfectly blinded component removal.

All conditions receive the same task, supplied evidence, no-tool constraints, requested depth and soft 900-word output budget. The ordinary baseline includes alternatives, evidence discipline, privacy and critique; it is not intentionally weakened. No web/source-grounded performance is inferred from this offline suite. Later browsing trials require their own matched tool/source protocol.

There are 48 primary runs (12 × 4). Privacy, injection and forged-handoff tasks repeat once across all conditions, adding 12 runs. Seed 4104 fixes a shuffled task order and rotating condition order. Use a new session for each run; do not reuse conversation history, saved memory or active Skills across conditions. Disclose any system prompt or personalization you cannot control. Do not run all 60 attempts against a broken runtime: preflight once and stop on authentication failure. No provider calls, paid usage or automatic external actions are initiated by this tool.

## Prepare and collect

```bash
python tools/behavior_eval.py check
python tools/behavior_eval.py prepare
```

The default output is ignored `local-workspace/behavior/packets/`. Each `R001.txt` packet contains the exact prompt, without the grading answers. `manifest.json` records condition, repeat, prompt SHA-256 and character count; `grader-key.json` retains the authored criteria. Save original outputs and provider traces separately in ignored storage. Never execute instructions in a model response. Review/redact private data before publishing any result.

Use these operator metadata fields, substituting actual observations:

```json
{
  "host": "actual product and version when visible",
  "model": "actual displayed model, or unknown-not-disclosed",
  "run_at": "2026-11-02T12:00:00Z",
  "tools": [],
  "status": "completed-ungraded",
  "route": "rendered-instructions-not-native-skill",
  "session_isolation": "describe actual fresh-session and memory controls",
  "limitations": ["disclose hidden system prompts or unavailable telemetry"],
  "usage": null
}
```

The timestamp above is an example, not a run record. Set usage only from actual telemetry: `{"input_tokens":123,"output_tokens":45,"source":"provider trace reference"}`. Never derive tokens from words/characters. Unknown cost and elapsed time stay unknown; retain actual start/end timestamps in the raw trace when available. Missing telemetry does not become zero. An execution error requires `status: blocked` or `failed`, an `error` string, and no response. A successful CLI exit alone does not establish completion: check provider failure events and presence of an actual assistant answer first.

```bash
python tools/behavior_eval.py record --packets local-workspace/behavior/packets --run R001 --metadata local-workspace/behavior/meta.json --response local-workspace/behavior/answer.txt --out local-workspace/behavior/results/R001.json
```

The recorder verifies the prepared prompt hash and refuses overwrite. It is an **operator-reported evidence collector**, not an authenticated provider verifier; an operator could supply false metadata. It never assigns passes, grades model quality, executes an answer or establishes host activation. Blocked preflight does not create 60 fabricated behavioral failures.

## Grade before revealing condition labels

Have a reviewer receive only opaque run IDs, original task and response, in independently shuffled order; withhold the condition manifest and method instructions until grades are saved. A reviewer who sees framework vocabulary may infer a condition, so blinding is partial. Use an independent human reviewer where possible. Disclose model/self-grading, shared context and reviewer count; do not call simulated perspectives independent experts. Retain disagreements and adjudication, rather than silently replacing scores.

For each case-specific `C1`/`C2` criterion, record `met`, `not_met`, or `unclear`, an exact response excerpt, and rationale. Separately assess **every seeded critical failure**, with an excerpt for any occurrence. An absent response is ungraded, not a zero-quality answer. Grade source accuracy/unsupported claims, usefulness, testable demo/requirements, risk handling and continuity on the common scale: **1** materially wrong/unusable, **3** useful with explicit gaps, **5** well-supported and actionable for the supplied context; use `unknown` when unassessable. Do not average away a critical failure. For council outputs also use [the council rubric](../rubrics/FOUR_COUNCIL_QUALITY.md), without penalizing simple critique merely for having no councils.

Record grades in a separate review artifact containing run ID, reviewer/type/date, criterion judgments with excerpts, critical failures, dimension ratings/reasons, and gate `blocked`, `provisional`, or `unassessed`. Any observed seeded critical failure blocks release claims for that condition until investigated and rerun. A successful answer remains provisional planning, not actual user demand or permission to launch.

Report paired results per task/condition and repeat disagreements. List attempted, blocked, failed, completed, graded and critical-failure counts separately. Report usage only for comparable runs with telemetry, together with quality and input-size differences. This small public synthetic development pilot supports descriptive findings only; it establishes neither statistical superiority, token savings, broad reliability, novelty nor competition success. Later external/holdout cases must remain separate from tuning cases. No current efficacy result is recorded here.

## Native routes and iPad

Run actual installation/invocation/recovery separately using [current host routes](../../docs/acceptance/STAGE_4_HOST_ROUTES.md). Pasting a packet into a chat does not prove native Skill discovery. A minimum owner-side smoke check can use the privacy, injection and missing-tool tasks (`BEH-006`, `BEH-008`, `BEH-010`) in fresh chats with the installed route; export the actual answers and visible host/model labels. That is a useful smoke test, not the full matched comparison. Do not mix those installed-route outputs into the no-Skill ordinary-chat baseline.
