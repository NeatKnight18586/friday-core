# ChatGPT Project Adapter — iPad-First Operating Plan

> Historical owner-specific setup plan. Current public/provider-neutral direction and stages are in [REVISION_STAGES.md](REVISION_STAGES.md). Account quotas and UI instructions must be checked at installation time.


**Status:** B9 generated and structurally validated; UI runtime acceptance pending.
**Last checked:** 2026-11-02

## Why this route

Use a ChatGPT Project with project instructions and five generated plain-text reference files. This preserves the Peanuts methods on a Free ChatGPT account without relying on native Skills eligibility. Project instructions act as a small Level-0 map; reference files provide method knowledge only when relevant.

## Five-file allocation

| Slot | Generated file | Contains |
|---|---|---|
| 1 | `00_PEANUTS_CORE_SKILL.txt` | Core instructions, trigger boundaries, P1–P10 map, progressive-disclosure index |
| 2 | `01_RESEARCH_AND_EVIDENCE.txt` | Research engine, event intelligence, user discovery, evidence synthesis and boundaries |
| 3 | `02_NUTS_AND_REVIEW.txt` | NUTS, source-domain playbook, Four-Council, quick screen and assumption validation |
| 4 | `03_PRODUCT_AND_ENGINEERING.txt` | Vertical slice, requirements/PRD, technical design, delivery handoff and Project Brief/PRD/design/build/demo/status templates |
| 5 | `04_GOVERNANCE_AND_RECORDS.txt` | PPA, method governance, QA, tool/knowledge registry, context/resource controls, project records and capability architecture |

`PROJECT_INSTRUCTIONS.md` is copied into Project settings and is separate from the file slots. `SETUP.md` is a user guide, not a Project source. The generated ChatGPT ZIP contains only the five `.txt` source files containing Markdown-formatted text, not the setup guide or Project instructions.

## Fresh-session continuity

At each meaningful milestone, preserve a concise status/handoff with:

- Project identifier/title and revision/date.
- Desired outcome, mode and current Peanuts stage.
- Completed stages and artifacts, with stable IDs/paths.
- Approved decisions and who approved them.
- Evidence status, sources, critical findings and counterevidence.
- Unvalidated assumptions and planned/completed tests.
- Open questions, blockers and risks.
- Exact next action and required inputs/tools.

When continuing, read the latest handoff and relevant artifacts first. Do not reconstruct or rewrite a stage merely because the conversation changed. When a chat response is saved as a Project source, verify it appears in the Project sources list. The chat itself is not the only source of truth.

## Capability honesty

The five Project files do not execute repository scripts or guarantee local filesystem access. For JSON Schema, package hashes, lint, tests, archive extraction and CI, use the full repository in a coding host that actually has shell/filesystem tools. In ChatGPT, explicitly mark these deterministic checks `NOT RUN` unless the host executes them and supplies results.

## Maintenance

Edit only `skills/peanuts/`, `docs/`, `templates/`, `schemas/` and other canonical sources. Regenerate the ChatGPT files and host bundles with `python tools/build_skill_packages.py`. Run `python tools/validate_b9.py` and the full repository verifier. Do not hand-edit generated files; this is how method drift is prevented.


## B10 — ChatGPT-first acceptance smoke test (2026-11-02)

After the five sources and Project instructions are installed, run the smoke prompt below in a **new chat inside the Project**. It checks actual context retrieval and capability honesty; it does not certify all methods.

> Use Peanuts. Explain the difference between P1–P10 and B0–B10. Then classify this task: I have a rough campus app idea, no user interviews, no confirmed API, and a one-month student-team deadline. State the mode, default depth, three most important unknowns, and exact next action. Do not claim scripts or JSON validators ran.

Expected behavior: distinguish operational stages from build milestones; default to Standard; preserve missing user/API facts as unknown; select only relevant methods; do not claim the Project has shell/filesystem access; do not treat the idea as validated. Follow with a concise status/handoff and test a second fresh Project chat. Full protocol: `docs/acceptance/CHATGPT_PRIMARY_RUNTIME_ACCEPTANCE.md`.
