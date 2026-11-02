# Evaluation Results

Actual run records belong in `results.jsonl` and must validate against `schemas/evaluation-result.schema.json`.

B10 contains 20 live ChatGPT conversation run records (RUN-001–020) for EVAL-103–122: 16 `passed`, 1 `partial` (EVAL-121 paired baseline exploration), and 3 `blocked` (EVAL-117 Project UI, EVAL-118 independent calibration, EVAL-122 repeatability/human adjudication). These are same-model, single-session self-evaluations; they are not independent human adjudication. All records remain `reviewer_approved=false`.

Preserve failed, partial, blocked and future repeated runs. Never add hypothetical or manually assumed passing results. Record exact runtime, date, model label where visible, tool availability, evidence and limitations.


B10 cross-host supplement adds RUN-021–032 for EVAL-123–134: four deterministic install/package checks (RUN-021–024) and three deterministic malicious-archive checks (RUN-030–032) `passed`; five actual host/UI tests (RUN-025–029) remain `blocked`. The Codex/Claude Code executables and claude.ai upload UI are unavailable in the managed environment. All new records remain `reviewer_approved=false`; simulated installation and archive rejection tests are not live model passes. Across B10 there are 32 total run records: 23 passed, 1 partial, and 8 blocked.
