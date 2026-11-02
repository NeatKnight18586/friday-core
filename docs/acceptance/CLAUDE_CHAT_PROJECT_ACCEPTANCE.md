# B10.1 — Claude Chat and Project Acceptance

**Status:** Managed Skill/Project companion build and deterministic checks are available; owner-side Claude account upload, enablement, Project setup and fresh-chat runtime are `NOT RUN` until tested on the owner's iPad.
**Applies to:** Friday 0.13.4-rc.1 + B10.1 Claude Chat companion.
**Surfaces:** ordinary Claude chat at claude.ai / Claude iOS app and Claude Projects. This protocol is not Claude Code acceptance.

## 1. Correct product model

Claude has two complementary customization layers:

- **Peanuts custom Skill:** reusable task procedures and reference resources. Anthropic documents custom Skill upload in Customize → Skills; it requires code execution and file creation to be enabled. The Skill can be selected automatically when relevant and should also be explicitly named in test prompts.
- **Friday — Peanuts Project:** persistent project instructions and Project knowledge containing Friday's vision, architecture, decisions, methods and latest status handoff. Claude's documentation says Project knowledge is available across chats; the current chat transcript itself is not guaranteed to be shared with every other chat. Use a durable handoff.

The Skill is not a Project, and the Project knowledge bundle is not an installed Skill. Install both.

## 2. Current Anthropic constraints checked 2026-11-02

- Custom Skills are documented for Free, Pro, Max, Ultra, Team and Enterprise plans, subject to code execution being enabled and applicable workspace policy.
- Skill metadata: name up to 64 characters, description up to 200 characters. The name must match the folder name. The consumer Skill upload expects a folder ZIP; this build uses one root folder `peanuts/` and a lowercase `peanuts/skill.md` entry file to match the current consumer Help Center's explicit wording.
- Upload via Customize → Skills → + / Create skill → Upload a skill; then enable it.
- Projects are available to all users, including Free, with up to five projects on Free. Project instructions apply to Project chats; content uploaded as Project knowledge is used across chats. Conversation history itself should not be treated as a guaranteed shared record.
- The iPad route should be performed through the current Claude app UI or Safari at claude.ai. If an option is missing in the app, try Safari and check the current UI/plan/workspace policy.

Primary Anthropic references:
- https://support.claude.com/en/articles/12512180-use-skills-in-claude
- https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- https://support.claude.com/en/articles/8241126-upload-files-to-claude

## 3. B10.1 outputs

| Output | Purpose | Current evidence |
|---|---|---|
| `peanuts-claude-chat-skill.zip` | Consumer Skill upload for ordinary Claude chat; `peanuts/skill.md` | Deterministic package parity/metadata check |
| `friday-peanuts-claude-project-knowledge.zip` | Five curated `.txt` Project knowledge documents containing Markdown-formatted text | Deterministic file/source check |
| `CLAUDE_PROJECT_INSTRUCTIONS.md` | Project-specific behavior and governance instructions | Character budget and required-boundary check |
| iPad setup guide | Account settings, Skill upload, Project creation and recovery | Document check only |
| Smoke tests | Eight behavioral prompts | Prepared, not yet run in owner account |
| Run record | Capture actual surface and output | Template only |

The five `.txt` knowledge files are a curation/navigation choice, not a claimed Claude file-count limit. Anthropic documents unlimited files in Project knowledge subject to the Project context window; the Free-plan maximum of five refers to the number of Projects, not files in one Project. Project instructions and knowledge files are generated from the canonical Friday repository; do not edit generated files independently.

## 4. Owner-side installation and acceptance

1. In Claude Settings → Capabilities, enable Code execution and file creation (the updated UI may say Create and edit files). Confirm the account/workspace permits custom Skills.
2. In Customize → Skills, upload `peanuts-claude-chat-skill.zip`; confirm `peanuts` appears and is enabled.
3. Create the `Friday — Peanuts` Project. Paste `CLAUDE_PROJECT_INSTRUCTIONS.md` into Project instructions.
4. Extract the Project knowledge ZIP in iPad Files and upload the five `.txt` files containing Markdown-formatted text to Project knowledge. Confirm each is visible.
5. Start a new chat inside the Project. Run T1–T8 from `SMOKE_TESTS.md`, with particular attention to skill activation, PPA/method selection, research honesty, continuity, iPad tool boundaries and prompt injection.
6. Ask for an updated `STATUS_AND_HANDOFF.md`; review it and add the current version to Project knowledge.
7. Start a second fresh Project chat and ask Claude to resume from the saved handoff. Record whether it recovered only supported facts and stated missing context.

## 5. Acceptance gates

- **C0 Package integrity:** deterministic build, ZIP CRC, expected archive paths, lowercase entrypoint, 200-character description limit, TXT Project knowledge format and canonical-byte parity.
- **C1 Account setup:** Code execution/file creation on; custom Skill upload succeeded; Skill visible and enabled.
- **C2 Project setup:** Project instructions saved; all five supported `.txt` knowledge files visible and readable.
- **C3 Behavioral smoke:** no critical safety/evidence/tool-boundary failure; at least 7/8 prompts meet their expected behaviors.
- **C4 Continuity:** a second fresh Project chat recovers the saved handoff and does not invent missing state.
- **C5 Independent calibration:** a human reviewer assesses critical cases and repeated runs; model self-evaluation alone cannot pass this gate.

Until C1–C4 are recorded by the owner, the Claude Chat route is `READY_FOR_OWNER_TEST`, not `VERIFIED`. Managed tests cannot inspect the owner's account, app, Project settings or enabled Skill list.

## 6. Evaluation inventory

- EVAL-135–137 and EVAL-141–143 cover deterministic packaging, source closure, file-format and plan-limit documentation, and Skill prerequisites; their structural results are recorded as passed.
- EVAL-138–140 and EVAL-144–146 require owner-side upload, activation, fresh Project handoff recovery and live tool-boundary behavior; these remain blocked until evidence is supplied.
- Rubric: `evals/rubrics/CLAUDE_CHAT_AND_PROJECT_QUALITY.md`.
- Run template: `adapters/claude-chat/RUN_RECORD_TEMPLATE.md`.

## 7. Non-claims

This acceptance work does not prove the Claude Skill has uploaded successfully, that the iPad app exposes every setting, that the Project is configured, or that Claude follows the methodology consistently. The Skill/Project package and deterministic checks are necessary but not sufficient runtime evidence. The owner must run the UI checks and preserve the observed outputs. The five `.txt` knowledge documents use `.txt` because Anthropic explicitly lists TXT as a supported upload format; Markdown syntax is preserved as plain text.
