# PC / Laptop Readiness Acceptance Checklist

**Status:** B3 local configuration and B9 host packages delivered; ChatGPT is primary owner-facing route; remote/host acceptance remains separate  
**Version:** 0.7.0-draft  
**Last updated:** 2026-11-02

This checklist defines what must be verified before Friday/Peanuts is described as ready for a normal laptop/PC setup. It separates repository portability from model-runtime compatibility.

## 1. Supported host targets

Initial target matrix:

- Windows 10 or later, subject to current Claude Code/Claude Desktop requirements at test time.
- macOS 13 or later, subject to current requirements at test time.
- Linux as a documented secondary route, using a currently supported distribution.
- GitHub Codespaces as a browser-based Linux development environment.

Exact requirements must be rechecked at installation time. Claude Code access is plan-dependent; the owner must have an eligible subscription or configured/billed API/enterprise access.

## 2. Repository acceptance

- [ ] Clean clone/extraction opens at repository root.
- [ ] No accidental nested `Friday/Friday/` directory.
- [ ] No secrets, API keys, personal memory, participant records, or confidential project material.
- [ ] `README.md`, `CLAUDE.md`, and `AGENTS.md` point to the same canonical documentation.
- [ ] The canonical skill source is not duplicated as independently maintained copies.
- [ ] All required files are present and manifest hashes match.

## 3. Deterministic code acceptance

- [x] Supported Python version range is explicitly declared (Python 3.11+; default 3.13).
- [ ] Dependencies are declared and install reproducibly.
- [x] One documented command runs all repository checks (`python tools/verify.py`).
- [ ] Unit tests pass.
- [ ] Integration tests pass.
- [ ] JSON Schemas and project records validate.
- [ ] Cross-record references and state transitions validate.
- [ ] Windows path handling and file operations pass in CI.
- [ ] macOS path handling and file operations pass in CI.
- [ ] Linux path handling and file operations pass in CI.
- [ ] No tests depend on secrets or paid external services unless separately marked optional.

## 4. Reproducible cloud environment

- [x] `.devcontainer/devcontainer.json` exists and passes structural JSON/configuration checks.
- [ ] Dev Container creates the declared Python/runtime environment.
- [ ] Setup commands are deterministic and least-privilege.
- [ ] Codespaces terminal can run the same verification command.
- [ ] Codespaces quota/billing behavior is explained to the owner.

## 5. GitHub CI acceptance

- [x] GitHub Actions workflow is configured for pushes, pull requests, and manual dispatch; remote execution is pending.
- [x] Workflow uses least-privilege `contents: read` permissions.
- [x] Workflow configures Ubuntu, Windows, and macOS across Python 3.11–3.14; remote matrix results are pending.
- [x] Dependencies are installed from the exact-version development snapshot; artifact hashes are not yet pinned.
- [x] Repository checks, unit tests, and integration tests are defined and run locally; remote CI execution is pending.
- [x] CI does not require secrets for ordinary validation.
- [x] Workflow steps fail the job on non-zero exit; actual hosted-runner behavior is pending remote validation.

## 6. Claude Code runtime acceptance

- [ ] Claude Code is installed on an eligible host and plan.
- [ ] `claude --version` succeeds.
- [ ] Claude Code opens the Friday repository root.
- [ ] Project guidance is loaded from `CLAUDE.md`.
- [ ] Peanuts skill is discovered from the intended `.claude/skills/` install path.
- [ ] Explicit invocation works.
- [ ] Skill instructions load the correct references/templates.
- [ ] Scripts, if any, execute only with intended permissions.
- [ ] A fresh Claude Code session can resume a synthetic project using saved files.
- [ ] A real evaluation set is run and results are recorded without fabricating passes.

## 7. Primary ChatGPT route acceptance

- [ ] Project is created/opened on the exact iPad/web surface the owner will use.
- [ ] Current account/surface/plan and Project file/upload limits are rechecked against official documentation.
- [ ] Project instructions from `adapters/chatgpt/PROJECT_INSTRUCTIONS.md` are installed in Project settings.
- [ ] The five `.txt` reference sources are all visible in the Project sources list.
- [ ] A fresh Project chat passes the B10 smoke prompt without inventing interviews/API access or claiming scripts ran.
- [ ] A status/handoff is saved as a Project source where available.
- [ ] A second fresh Project chat correctly resumes from the saved handoff.
- [ ] ChatGPT is not assumed to have local repository/shell access merely because files are attached.
- [ ] The exact tested surface, displayed account/plan label, date, test prompt and result are recorded.
- [ ] Native Skills are tested only if the exact account/surface exposes them; not required for the manual Project route.

## 8. User-facing acceptance

- [ ] Beginner setup guide is understandable without assuming command-line experience.
- [ ] Laptop setup includes copy-paste commands with expected success output.
- [ ] Common errors have recovery instructions.
- [ ] No API key is hardcoded in documentation or examples.
- [ ] User can create a project, pause it, and resume it in a fresh session.
- [ ] The skill distinguishes verified research from assumptions and unknowns.

## 9. Release disposition

Use one of:

- `READY_FOR_PRIVATE_UPLOAD` — pre-upload checks in the managed environment pass; remote CI/runtime checks are configured but not yet run.
- `READY_FOR_CODESPACES_USE` — GitHub Actions and Codespaces checks pass.
- `READY_FOR_CLAUDE_RUNTIME` — actual Claude Code smoke tests pass on a supported, eligible host.
- `READY_FOR_CHATGPT_NATIVE_SKILL` — native Skills route passes on the exact supported account/surface.
- `READY_FOR_CHATGPT_MANUAL_USE` — documented file/Project fallback passes.
- `BLOCKED` — a critical required check fails or cannot be safely completed.

Never collapse these distinct statuses into a single unqualified “works everywhere” statement.
