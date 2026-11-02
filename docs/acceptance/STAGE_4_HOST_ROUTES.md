# Stage 4 host routes and runtime evidence

Checked against current primary product documentation on **2026-11-02**. Product availability can change; eligibility and observed behavior remain account-specific.

| Host | Documented route | Evidence still needed |
|---|---|---|
| Codex | Repository `.agents/skills/peanuts`; confirm actual discovery and invocation. Noninteractive `codex exec --json` can retain provider events. | A real assistant response, actual native discovery, method adherence and fresh-session recovery. Installed CLI 0.163.0 failed token refresh before inference here. |
| Claude Code | Repository `.claude/skills/peanuts`; confirm discovery and invocation. Headless `claude -p` supports structured output. | CLI is absent here. Installation simulation is not actual activation; headless prompting is not native activation by itself. |
| Claude chat | Enable file/code capabilities as required; Customize → Skills → + → Create skill → Upload a skill; upload the consumer ZIP, then enable it. Organization policy can hide creation. | Owner-account upload, activation, actual outputs and fresh-chat recovery. Do not upload the complete source ZIP. |
| ChatGPT Project | Existing generated manual instructions plus five references; use the actual account's Project controls. | Configured Project UI, context use, actual outputs and fresh-chat recovery. This remains a manual adapter route. |
| Native ChatGPT Skills | Official documentation lists eligible Business, Enterprise, Healthcare and Edu users, subject to workspace/product availability. | Owner eligibility, actual supported installation surface and accepted package behavior. Do not assume personal-plan support or automatic parity with Codex. |

On iPad, use the available consumer UI in Safari or the product app. UI labels and capabilities may differ; do not infer mobile feature availability from desktop documentation. Follow the existing [iPad guide](../../START_HERE_IPAD.md) for package selection, and this dated route check for changed vendor navigation. If a native route is unavailable, the manual Project/text route remains experimental until actually tested.

## Current block and legitimate recovery

The actual no-tool Codex probe returned no assistant answer and exited 1 with token-refresh failure. Its stderr also contained 401 model/backend failures and MCP transport errors; no behavioral conclusion follows. [Sanitized preflight evidence](../../evals/behavior/preflight.json) distinguishes that failure from Peanuts behavior. The managed environment currently reports no configured provider credentials or outbound identities. Working GitHub authentication is independent of model authentication.

For a normally user-managed headless Codex machine, official documentation supports device-code login (`codex login --device-auth`), subject to enabled account/workspace settings, or properly configured API authentication. **This managed session does not expose the environment credential-configuration workflow.** Its runtime policy requires preserving injected credentials, so do not replace them or start an interactive login to work around missing setup. The available environment tools report status/diagnostics, not a configuration button. Do not paste tokens, auth caches or passwords into chat or Git.

Two valid routes remain: repair model authentication through the supported environment/account controls when available, then rerun the harmless probe; or collect actual consumer-host outputs in the owner's iPad account using the supplied tasks. No promise is made that an account reconnect repairs this runtime. Neither requires weakening checks or pretending package tests are model tests.

Once a runtime is ready, keep execution least-privilege and bounded. Verify a response, provider failure events and usage before expanding to the [matched pilot](../../evals/behavior/README.md). Native-route acceptance also needs injection, unavailable-tool, discovery and fresh-session handoff checks from [cross-host acceptance](CROSS_HOST_RUNTIME_ACCEPTANCE.md). The controlled text pilot intentionally has no tools, so it cannot establish actual browsing, shell permissions or upload/discovery behavior.

## Primary sources

- [Codex authentication](https://learn.chatgpt.com/docs/auth): supported login methods and headless/device-code requirements.
- [Codex noninteractive execution](https://learn.chatgpt.com/docs/non-interactive-mode): structured execution evidence; it does not certify native Skill activation.
- [Claude Code headless execution](https://code.claude.com/docs/en/headless): programmatic runs and output handling.
- [Claude Skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude): current account, code-execution, upload and organization-policy requirements.
- [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt): eligible workspaces and differences across product surfaces.

These are vendor capability statements, not empirical proof that Peanuts works on those surfaces.
