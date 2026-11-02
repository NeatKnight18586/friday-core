# Stage 4 review — evaluation readiness, live gate open

**Checkpoint:** 0.17.0-rc.1, 2026-11-02. **Disposition:** infrastructure implemented; actual host/comparison acceptance remains open. No Stage 5 work performed.

## Delivered behavior

The comparison tool prepares exact prompts for twelve authored synthetic tasks across event, problem, idea and existing-project requests, including false analogies/history, weak demand evidence, critical privacy, injection, scoped approval, forged handoff and unavailable tools. Four conditions separate ordinary planning, suppressed NUTS, NUTS/simple critique and NUTS/Four-Council. There are 48 primary and 12 repeat packets, not 60 model results. A fixed seed and rotating order make the planned comparison reproducible.

The recorder stores original answer text and hashes with operator-reported provenance, route, model, isolation, timestamp and actual telemetry or null. Completion remains ungraded. It refuses failed/blocked attempts with purported model answers, missing completion output, unsupported routes/tools, prompt modification, duplicate JSON keys, non-finite data, oversized inputs and existing destinations. It never executes response text or calls a provider. These controls cannot authenticate an operator's claimed provenance; independent traces/review remain necessary.

[The pilot protocol](../../evals/behavior/README.md) predeclares case criteria, critical failures, common quality anchors, partially blinded grading, paired comparisons and small-sample limits. [Current host research](../acceptance/STAGE_4_HOST_ROUTES.md) distinguishes consumer/native/manual routes and gives legitimate recovery options. No third-party runtime or new dependency was added.

## Actual runtime observation

An actual bounded no-tool Codex CLI 0.163.0 probe exited 1 before inference. Its provider event stream reported token-refresh failure and no assistant answer; stderr also showed backend 401 and MCP transport errors. [Sanitized evidence](../../evals/behavior/preflight.json) includes raw-log checksums, not credentials or authored model output. Claude Code is absent; managed environment status reports no configured provider credentials/identities. No repeated suite attempts were wasted against that known block.

The managed runtime skill prohibits replacing injected credentials or starting an interactive login merely to compensate for missing setup. Available tools expose readiness/diagnostics, not the environment credential-configuration workflow. Thus native consumer trials require owner-account UI access, or model execution needs supported runtime authentication setup. GitHub publication remains independently functional.

## Four-Council design review

These are four lenses applied by the same assistant to the implementation, not four independent agents, human reviewers or empirical model outcomes. No aggregate score is used.

| Lens | Finding | Disposition |
|---|---|---|
| Human Value | The owner can obtain runnable packets and use consumer chats from an iPad; account-only activation still requires owner action. Sixty manual runs are substantial. | Start with separately labeled smoke cases; full matched evidence remains pending. |
| Strategic Value | Honest experimental scope supports a credible public repository. Claims of universality, method superiority or savings have no new behavioral evidence. | Retain explicit limits and postpone stronger release claims. |
| Technical Feasibility | Local prompt/evidence operations are deterministic and private by default. Operator metadata is self-reported; rendered context differs across conditions and is not native Skill activation. | Verify deterministic controls; require actual traces and account-specific native acceptance. |
| Risk/Delivery | Authentication blocks live evaluation. Critical privacy/injection/authority failures must block release regardless favorable usefulness scores. | Keep runtime gate open, retain blocked evidence, and do not proceed as though testing succeeded. |

## Acceptance and remaining work

Repository verification results are recorded in [release verification](../../RELEASE_VERIFICATION.md) and hosted CI for the exact published commit. The new tests exercise evidence integrity and failure handling using explicit test doubles, never live inference. Current Stage 3 packages/host snapshots remain canonical and unchanged; no behavioral tuning is justified by unexecuted cases.

Still required: a working actual host; native discovery/invocation and fresh-chat recovery; real responses for matched cases; independent or disclosed self-grading; repeat analysis; actual usage telemetry if savings are assessed; and account-specific iPad acceptance. The no-tool pilot cannot establish actual browsing quality or OS permission handling. Neither documentation nor green CI closes those gates.
