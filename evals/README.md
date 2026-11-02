# Peanuts Evaluation Starter Set

**Status:** 134 synthetic evaluation cases across B2–B10; structurally validated. B10 includes one live ChatGPT conversation run record set, four deterministic Codex/Claude Code install/package checks plus three malicious-archive rejection checks, and blocked real-host runtime cases; self-evaluation is not independent human adjudication.
**Version:** 1.6.1-rc.1

## Purpose

This directory holds version-controlled cases, rubrics, baselines, and (when real runs occur) actual evaluation results. A case marked `ready` or passing JSON Schema validation has **not** passed an AI behavior evaluation. Do not invent run results.

## Structure

- `cases/` — one JSON case per file, validated against `schemas/evaluation-case.schema.json`.
- `rubrics/` — anchored review criteria for specialist methods.
- `results/` — actual run results; append-only JSONL when a real execution is performed.
- `baselines/` — baseline definitions and later comparison results.

## Coverage by milestone

- **B2:** project continuity, conflicting/stale sources, record integrity, desk-research limits, method prerequisites, superficial analogy, critical risks, prompt injection, assumption prioritization, provenance, handoff integrity, PPA/tool selection, research ethics, historical source criticism, and event-alignment separation.
- **B4 / EVAL-019:** fictional end-to-end event-to-draft-PRD vertical-slice handoff. It is synthetic and is not real research, user validation, or model-performance evidence.
- **B5 / EVAL-020–030:** stale/conflicting event rules, inaccessible sources, synthetic-persona overclaims, missing consent, convenience-sample overclaims, missing formal-method prerequisites, provisional PRDs, false triangulation, time-boxed research, and escalation for sensitive contexts.
- **B6 / EVAL-031–038:** relational versus surface analogy, source accuracy, historical source criticism, appropriate TRIZ use, no-useful-analogy outcomes, and IP/novelty overclaim prevention.
- **B6.5 / EVAL-039–050:** capability boundaries, progressive disclosure, continuity, resource-mode escalation, measurement honesty, deterministic processing, capability growth, no-forced-routing, safety escalation under a constrained budget, and deferring an unjustified Friday manager.

- **B7 / EVAL-051–061:** unresolved critical/high blockers, reviewer-independence disclosure, UNKNOWN scoring, event-overlay separation, accepted-risk conditions, non-waivable critical compliance, participant safeguards, completed-test evidence, assumption/test consistency, quick-depth dimension comparability, and mandatory event-rule blockers.
- **B8 / EVAL-062–087:** requirement provenance and evidence maturity, untestable/ambiguous criteria, approval and legal/compliance constraints, conflicting/dependent/superseded requirements, acceptance-test lifecycle, participant consent and privacy, task sequencing and completion evidence, artifact tampering/path traversal, cross-document traceability, demo overclaiming, non-applicable demo handling, and P7–P9 stage gates. These cases are structurally validated and marked ready, not live-model passes.
- **B9 / EVAL-088–102:** Agent Skills metadata/directory alignment, description limits, reference integrity, canonical-source drift, Claude Code/Codex discovery paths, ChatGPT five-file/manual adapter constraints, actual schema/record-template inclusion, complete standalone support-resource closure, concise Project instructions, reproducible package builds, ZIP/path/symlink safety, tool-availability honesty, continuity and prompt-injection boundaries. Cases are structurally validated; live host runtime remained separate.
- **B10 / EVAL-103–122:** ChatGPT-primary continuity, progressive disclosure, current product facts, tool boundaries, prompt injection, unknowns, NUTS selectivity, Four-Council disclosure, assumption/consent safeguards, PRD/P8/P9 gates, handoff, five-file Project route, actual Project UI acceptance, repeated-run calibration, no-fabrication external-action approval, paired-baseline comparison and repeatability/human review. One live ChatGPT conversation run is recorded for 16 cases, one exploratory baseline comparison is partial, and EVAL-117/118/122 are explicitly blocked pending target Project UI and independent/repeated evaluation.
- **B10 cross-host / EVAL-123–134:** Codex and Claude Code install-path simulations, root guidance presence, canonical package parity, resource/link closure and least-privilege package checks; then separate blocked actual CLI discovery/invocation, method fidelity, fresh-session recovery, and claude.ai/Cowork upload runtime acceptance. Seven deterministic package/install/security cases passed; live host cases remain blocked until executed in actual eligible accounts and host sessions.

## Deterministic validation

Run the consolidated suite with:

```bash
python tools/verify.py
```

For a local environment where Ruff is unavailable, `python tools/verify.py --skip-lint` skips only lint and must be reported as **PASS WITH SKIPS**, not as a fully passed suite. Individual milestone validators are available as `python tools/validate_b2.py`, `python tools/validate_vertical_slice.py`, `python tools/validate_b5.py`, `python tools/validate_b6.py`, and `python tools/validate_capabilities.py`, `python tools/validate_b7.py`, and `python tools/validate_b8.py`, and `python tools/validate_b9.py`, and `python tools/validate_b10.py`, plus `python tools/validate_host_adapters.py`.

These validators check schemas, record relationships, fixtures, and deterministic constraints. They do not evaluate whether a model actually follows instructions or whether a real-world claim is true.

## Running live evaluations later

For each actual run, record: case ID/version, host, model/system version where visible, skill/repository version, selected resource mode, tool permissions, evaluator type, output/evidence, disposition, scores, critical failures, limitations, and run date. Use `schemas/evaluation-result.schema.json`. Never label a synthetic fixture or a schema-valid case as an AI pass.

Separate development cases from holdout cases used to compare versions. Preserve the same task, host, model, tools, sources, and rubric for controlled comparisons. Repeat where practical and avoid statistical claims from small samples.

## References

See `docs/governance/CONTEXT_EVALUATION.md` for context-efficiency comparisons and `docs/governance/QUALITY_ASSURANCE.md` for general release and acceptance rules.
