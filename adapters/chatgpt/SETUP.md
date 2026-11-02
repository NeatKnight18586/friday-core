# Install Peanuts in a ChatGPT Project (iPad-first manual route)

**Recommended for the current ChatGPT Free workflow.** This is a project-instructions-and-files setup, not a native installed ChatGPT Skill. OpenAI currently documents standalone ChatGPT Skills for eligible Business, Enterprise, Healthcare and Edu accounts; availability differs by product surface. ChatGPT Projects are available on Free and mobile, but current Free limits are up to five files per project and three file uploads per day. Recheck the official help pages at installation time because plan limits and availability can change.

## Setup

1. Create a dedicated ChatGPT Project named **Friday — Peanuts** (or use an existing project only if it has room for five reference files and is not already overloaded).
2. Open Project settings and paste the complete contents of `PROJECT_INSTRUCTIONS.md` into Project instructions. These instructions are separate from the five reference files.
3. Upload the five plain-text `.txt` files (their contents use Markdown headings and tables) from `chatgpt-project-files/`:
   - `00_PEANUTS_CORE_SKILL.txt`
   - `01_RESEARCH_AND_EVIDENCE.txt`
   - `02_NUTS_AND_REVIEW.txt`
   - `03_PRODUCT_AND_ENGINEERING.txt`
   - `04_GOVERNANCE_AND_RECORDS.txt`
4. Free accounts may have a separate daily upload-rate limit in addition to the five-file Project limit. If you cannot upload all five in one day, upload the first three and add the remaining two after the upload allowance resets. Keep the five Project slots for these core references; avoid uploading the full repository ZIP as a Project source.
5. Start a chat with: **“Use Peanuts. My project/event/idea is … My desired outcome is …”** You can invoke it explicitly at any time by saying “Use Peanuts” or “Continue the Peanuts project.”

## Important boundaries

- Project files provide reference text, including the actual JSON Schema definitions and record starters grouped by method. They do not create local directories, execute the repository's Python scripts, or automatically enforce JSON Schema. Do not claim deterministic validation unless an available tool actually ran it.
- For strict schema checks, packaging, hashes, CI, and repeatable validators, use the full Friday repository in a compatible coding environment such as Codex or Claude Code. The ChatGPT Project route can still perform the methods, research, analysis, and document drafting, while disclosing which deterministic checks were unavailable.
- Keep project state resumable. At meaningful milestones ask Peanuts to produce an updated `STATUS_AND_HANDOFF.md` (or concise equivalent) and save it to the Project when that UI action is available. For important decisions, retain the artifact and approval state, not only chat prose.
- The full repository is the canonical source. These five files are generated snapshots; regenerate them after any change to the canonical skill, references, or governance.

## Official documentation checked 2026-11-02

- ChatGPT Skills access: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- ChatGPT Projects: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- ChatGPT file upload and plan limits: https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt
- Agent Skills specification: https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx


## B10 acceptance after setup

After installing the Project instructions and all five sources, run a new Project chat with:

> Use Peanuts. Explain the difference between P1–P10 and B0–B10. Then classify this task: I have a rough campus app idea, no user interviews, no confirmed API, and a one-month student-team deadline. State the mode, default depth, three most important unknowns, and exact next action. Do not claim scripts or JSON validators ran.

A good answer distinguishes operational stages from repository milestones, defaults to Standard, preserves unknowns, and does not pretend that Project files provide shell access. Save a status/handoff as a Project source if available, then open a second fresh Project chat and test continuity. Record the actual surface, date, files visible and observed result. The full acceptance protocol is in the full Friday repository at `docs/acceptance/CHATGPT_PRIMARY_RUNTIME_ACCEPTANCE.md`.
