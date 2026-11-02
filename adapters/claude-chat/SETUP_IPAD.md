# Install Friday / Peanuts in the Claude Chat app (iPad-first)

**Purpose:** Use Peanuts as a reusable custom Skill in ordinary Claude chat, and use a Claude Project for persistent Friday background. Claude Code is not required for this route.

## 1. Prepare the two separate packages

1. `peanuts-claude-chat-skill.zip` — reusable task procedures and references. Upload this through Claude's Skills settings.
2. `friday-peanuts-claude-project-knowledge.zip` — five background documents for a Claude Project. Extract it in the iPad Files app and upload the five `.txt` documents (each contains Markdown-formatted text) to Project knowledge. `.txt` is on Anthropic’s published supported document list.
3. `CLAUDE_PROJECT_INSTRUCTIONS.md` — paste its complete contents into the Project's instructions.

Do not upload the whole Friday repository ZIP as Project knowledge. The canonical repository remains the source of truth; the Project pack is a curated companion.

## 2. Enable Skills

Anthropic currently documents custom Skills for Free, Pro, Max, Ultra, Team and Enterprise accounts, provided code execution and file creation are enabled. On an individual account, open Claude settings, go to **Capabilities**, and enable **Code execution and file creation** (the updated UI may label this **Create and edit files**). Then open **Customize → Skills**.

If the iPad app does not expose the upload controls, use Safari to open `https://claude.ai`, sign in to the same account, and use the web settings. The upload UI may change; follow the current labels shown by Claude.

## 3. Upload and enable the Peanuts Skill

1. In **Customize → Skills**, choose **+** or **Create skill**, then **Upload a skill**.
2. Select `peanuts-claude-chat-skill.zip` from Files.
3. Confirm the skill appears as **peanuts** and enable its toggle.
4. If upload fails, check that the ZIP contains a top-level `peanuts/` folder and a lowercase `peanuts/skill.md` entry file. The package also stays under Anthropic's documented 200-character description limit.
5. Do not upload the `.claude/skills/` Claude Code adapter here; that is for filesystem-based Claude Code, not regular Claude chat.

Claude can load enabled Skills automatically when relevant. For predictable testing, explicitly say: **“Use the Peanuts Skill for this task.”** Ordinary Claude chat does not use the `/peanuts` Claude Code slash-command convention.

## 4. Create the Friday Project

1. Open Projects and create **Friday — Peanuts**.
2. Open Project settings and paste `CLAUDE_PROJECT_INSTRUCTIONS.md` into **Project instructions**.
3. Extract the Project knowledge ZIP in Files.
4. Upload the five `.txt` documents from `claude-project-knowledge/` to the Project knowledge area.
5. Confirm all five appear in Project knowledge. These files hold durable background across Project chats; do not assume a new chat automatically receives every detail from an older conversation unless it was saved in Project knowledge or memory.
6. Start a new chat inside this Project and run the smoke prompts in `CLAUDE_CHAT_SMOKE_TESTS.md`.

Claude Projects are available to Free accounts; current documentation says Free users can create up to five Projects. The five `.txt` documents are a curation choice, not a Claude file-count limit. Anthropic documents unlimited Project files subject to the total content fitting within the Project context window; Free accounts are limited to five Projects, not five files per Project. Recheck current plan/account UI before setup.

## 5. Continuity practice

At the end of a major work session, ask Peanuts to produce an updated `STATUS_AND_HANDOFF.md`. Review it, then add the updated file to Project knowledge (remove or supersede the older copy if needed). In the next fresh Project chat, ask Claude to resume from the latest handoff and state any missing context. Project memory may help, but the handoff is the auditable source of truth.

## 6. Boundaries

- A Claude Project is not a Git checkout, terminal, or local repository. Uploading methods and schemas does not run Friday's Python validators.
- Claude Skills use the capabilities provided by the Claude product and plan. Confirm code execution/file creation is enabled; do not assume local shell, unrestricted web access, or connected GitHub access.
- Claude Chat Skill and Claude Code filesystem adapter are separate installation routes. They share the same canonical methodology but are not automatically interchangeable or synchronized.
- Do not share private repository files or project knowledge publicly. Do not include credentials, passwords, or API keys in handoffs.

## Official references (checked 2026-11-02)

- Use Skills in Claude: https://support.claude.com/en/articles/12512180-use-skills-in-claude
- Create custom Skills: https://support.claude.com/en/articles/12512198-how-to-create-custom-skills
- Manage Claude Projects: https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects
- Upload files to Claude: https://support.claude.com/en/articles/8241126-upload-files-to-claude
