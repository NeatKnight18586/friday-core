# Build, Demo, and Execution Handoff (B8 / P9)

## Purpose

Turn the approved product and technical definition into an executable, sequenced, inspectable handoff. P9 prepares execution; it does not execute external actions or grant authority to spend, publish, contact participants, change permissions, deploy, or submit.

## Build plan

Use `records/build-tasks.jsonl` as the structured work breakdown. Each task has one owner, a concrete deliverable, linked requirement IDs, explicit exit criteria, sequence index, status, and optional effort estimate with a confidence/basis note. Record unknown capacity as unknown; never manufacture precise schedules.

Dependencies must exist, be cycle-free, and precede dependent tasks. A task is not ready while its prerequisites are incomplete. Completed tasks need completion evidence; a planned test is not completion evidence. Ensure every approved in-scope requirement is covered by at least one active task.

Sequence work to reduce risk early. Prefer a thin end-to-end path, high-risk technical spikes, and critical compliance/security checks before expensive polish. Include integration, verification, accessibility, privacy/security, deployment/setup, rollback, operations, documentation, and contingency work where they apply.

## Demo plan

Use `demo-plan.json` as the structured source and `DEMO_PLAN.md` as the presenter-facing script. Define the audience, decision or understanding the demo supports, one coherent scenario, timed steps, expected observations, requirement links, prerequisites, and fallback. Use synthetic/de-identified/public or authorized test data. Keep secrets and identifiable participant data out of project artifacts.

Distinguish:

- `demonstrated`: an implemented behavior backed by a passing acceptance test or inspectable artifact.
- `measured`: a result with a recorded method, environment, data, and evidence.
- `illustrative`: an example/mockup/simulation that does not establish live capability.
- `hypothetical`: a proposed future behavior, not implemented.

A staged recording, mockup, synthetic data, or scripted output must not be presented as a live system or real user result. Include a failure plan and stop condition. Disclose material limitations before the audience forms a false impression.

## Artifact and handoff integrity

Register referenced deliverables in `records/artifacts.jsonl`. Every artifact path must be a safe relative path inside the project workspace and must exist. If a SHA-256 digest is recorded, it must match the current file. Do not reuse an artifact ID for a different file or silently mutate an approved artifact; update its version/status and preserve superseded history as needed.

Update `state.json`, `STATUS_AND_HANDOFF.md`, and `PROJECT_BRIEF.md` with the exact stage status, completed work, approved decisions, blockers, open assumptions, next action, owners, and limitations. A fresh session should be able to resume without replaying the entire chat.

## P9 exit gate

P9 can be marked complete only when the PRD and applicable technical design are approved, the build plan has a coherent dependency graph and requirement coverage, acceptance tests are linked and honestly status-labelled, the demo plan has evidence boundaries and fallback, artifacts resolve to real files, material risks/owners are visible, and the owner approves the handoff. The owner still separately authorizes actual execution and publication.
