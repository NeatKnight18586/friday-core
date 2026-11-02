# Peanuts for ordinary Claude chat

B10.1 provides two separate Claude app components:

1. **Custom Skill:** upload `peanuts-claude-chat-skill.zip` through Claude's Customize → Skills interface. It uses the generated `peanuts/skill.md` consumer entrypoint.
2. **Friday Project:** create a `Friday — Peanuts` Project, paste `CLAUDE_PROJECT_INSTRUCTIONS.md`, and extract the five `.txt` documents from `friday-peanuts-claude-project-knowledge.zip` and upload them as Project knowledge. These contain Markdown-formatted text but use a documented upload extension.

Read [`SETUP_IPAD.md`](SETUP_IPAD.md) before installation. Run the prompts in [`SMOKE_TESTS.md`](SMOKE_TESTS.md) and record the result in [`RUN_RECORD_TEMPLATE.md`](RUN_RECORD_TEMPLATE.md).

The Claude Chat package is generated from the single canonical `skills/peanuts/SKILL.md` source. Do not edit generated ZIP contents. This route is for ordinary claude.ai/Claude app chat, not the `.claude/skills/` Claude Code filesystem adapter.
