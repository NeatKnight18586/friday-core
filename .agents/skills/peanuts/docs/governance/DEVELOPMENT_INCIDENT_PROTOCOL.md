# Development Incident, Limit and Recovery Protocol

**Status:** Active development-governance rule  
**Applies to:** All Friday build milestones, verification runs, packaging, and later host/runtime acceptance

## 1. Purpose

A test timeout, unavailable dependency, tool failure, or environment limitation must not be hidden or converted into a pass. Friday's development process must preserve acceptance criteria and make the evidence behind each status inspectable.

## 2. Required status vocabulary

| Status | Meaning |
|---|---|
| `PASS` | The named check completed and all assertions passed. |
| `FAIL` | The check completed and detected a defect or unmet acceptance criterion. |
| `TIMEOUT` | Execution ended before a result was obtained. Treat as unresolved, not as a code failure or a pass. |
| `NOT RUN` | The check was not executed (for example, missing dependency or unavailable host). |
| `BLOCKED` | A prerequisite, permission, external service, or environment prevents the check or work. |
| `PASS WITH SKIPS` | All executed checks passed, but one or more declared checks were not run. |
| `INCONCLUSIVE` | The result is ambiguous, nondeterministic, or insufficient to support a decision. |

Every aggregate result must list skipped, blocked, timed-out, or inconclusive checks.

## 3. Incident classification

- **Critical:** security/privacy exposure, corrupted or lost project data, release-integrity failure, or a defect that invalidates a major acceptance gate. Stop dependent work.
- **High:** a core workflow, schema, handoff, or repeatable test is broken. Fix before building on the affected component.
- **Medium:** a non-core check, environment, documentation contract, or packaging issue is unresolved. Continue only if dependencies are unaffected and the limitation is visible.
- **Low:** cosmetic or non-blocking improvement with no material effect on correctness, safety, reproducibility, or maintainability. Record for planned cleanup.

Severity describes impact, not the amount of time needed to fix the issue.

## 4. Required response to a significant incident

1. **Disclose:** Tell the owner what happened as soon as it materially affects the build, test confidence, cost, security, or schedule.
2. **Preserve evidence:** Keep the command, environment, exit status, logs/output, affected files, and test IDs. Do not overwrite the only failure evidence.
3. **Classify:** Separate implementation defects from timeouts, missing dependencies, permissions, network restrictions, and test-harness problems.
4. **Contain:** Stop dependent work when a critical/high issue could invalidate later stages.
5. **Diagnose:** Reproduce the smallest failure, inspect the root cause, and avoid speculative fixes.
6. **Recover without weakening criteria:** Split long suites, remove unnecessary nested process boundaries, add timeouts, use a suitable environment, or repair the test/implementation. Never delete or dilute an acceptance test merely to obtain a green result.
7. **Retest:** Re-run the failed check, affected component tests, and the relevant regression suite.
8. **Record:** Add an incident record for critical/high issues and recurring medium issues, including cause, resolution, remaining uncertainty, and regression test.
9. **Report accurately:** State what passed, failed, timed out, was skipped, or remains untested.

## 5. Timeouts and execution limits

A timeout is an unresolved result. The preferred recovery order is:

1. Check whether the process is still running or left partial outputs.
2. Re-run the same command once when safe and deterministic.
3. If the command is too broad, split by independently meaningful validator/test groups while preserving the full acceptance coverage.
4. Prefer in-process calls or one controlled runner over unnecessary nested subprocesses.
5. Compare the aggregate list of required checks against the individual results; do not infer missing coverage.
6. Run a fresh-extraction/package test when packaging or path assumptions may be involved.

Do not change timeouts repeatedly without evidence. If the managed environment cannot execute the full workload, mark it `BLOCKED` or `NOT RUN` and move the check to the explicitly designated CI/Codespaces/runtime gate.

## 6. Test integrity rules

- Do not remove a failing test without documenting why the test was invalid and adding an appropriate replacement when the behavior remains required.
- Do not lower a rubric, score threshold, evidence requirement, or quality gate solely to obtain a pass.
- A schema-valid evaluation case is not a model pass.
- A local Linux pass is not a Windows/macOS pass.
- A configured GitHub Actions workflow is not a successful remote CI run until it has executed.
- A valid `SKILL.md` is not proof that a target host discovers or follows it.
- A package hash proves package integrity, not runtime correctness.

## 7. Required incident record fields

For critical/high incidents and repeated medium incidents, record:

- Incident ID and date.
- Milestone and affected component.
- Severity and status.
- Exact command/operation and environment.
- Observed result and expected result.
- Root cause or explicitly `unknown`.
- Files/tests affected.
- Recovery/fix performed.
- Regression evidence.
- Remaining limitations and owner-facing decision, if any.

## 8. Owner communication

The owner must be told about material setbacks, untested dependencies, unavailable tools, external billing/permission requirements, security concerns, or changes to an approved architecture. Small, routine test fixes may be summarized in the milestone report. Never imply background work or future verification that has not occurred.
