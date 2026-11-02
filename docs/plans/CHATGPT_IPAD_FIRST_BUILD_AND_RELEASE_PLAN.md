# ChatGPT/iPad-First Build and Release Plan

**Status:** Historical owner-specific delivery plan; current product direction is provider-neutral under ADR-046  
**Version:** 0.7.0-draft  
**Last checked:** 2026-11-02

> Current staged work is governed by [REVISION_STAGES.md](REVISION_STAGES.md). This plan records the earlier owner build route; its platform priorities, account assumptions and private staging instructions do not override current product/release decisions.

## 1. Purpose

This plan adapts the Friday/Peanuts build so the owner can continue using ChatGPT from an iPad without needing a laptop or running local commands during construction.

ChatGPT is the build partner and the owner-facing collaboration surface. The assistant creates and edits repository files, runs available deterministic checks in its managed development environment, audits the results, and provides a complete milestone ZIP. The owner supplies direction, makes consequential product choices, reviews major outputs, and downloads or preserves milestone packages.

The owner is not expected to act as the developer during the current iPad-only phase. ChatGPT is also the primary intended working environment for Peanuts, not merely the build partner.

## 2. What ChatGPT can and cannot prove

### Can be done during the build

- Design and create the repository files.
- Write Python utilities, JSON schemas, tests, configuration, Markdown instructions, skill packages, and examples.
- Execute deterministic tests in the assistant's managed Linux/container environment when tools are available.
- Inspect test output, validate schemas, check links, compare manifests/hashes, and review diffs.
- Run synthetic scenario evaluations and rubric-based reviews, while labelling them as model-assisted evaluations rather than independent human evidence.
- Create reproducible environment configuration, GitHub Actions workflows, and setup documentation.
- Package every milestone into a cumulative ZIP for download.

### Cannot be truthfully claimed before the relevant environment is available

- That Claude Code discovers and executes the skill correctly on the owner's actual computer.
- That ChatGPT's native Skills feature is available on the owner's current account/surface.
- That GitHub Actions have passed before the repository has been pushed to GitHub.
- That Windows, macOS, and Linux behavior has been tested merely because a Linux container test passed.
- That a simulated Four-Council review is equivalent to four independent human specialists.
- That passing structural tests proves research truth, user demand, product viability, or real-world success.

Every report must distinguish **implemented**, **tested in this environment**, **configured for later CI**, **tested on target host**, and **not tested**.

## 3. Build environment strategy

### During current iPad-only construction

1. ChatGPT authors and maintains the canonical working tree in its managed environment. B3 adds a one-command verification route, a test suite, pinned action references, and a Codespaces Dev Container configuration.
2. ChatGPT runs available tests and validation after each milestone.
3. ChatGPT creates a cumulative, versioned ZIP and a manifest/check report.
4. The owner downloads the ZIP to the iPad Files app as a backup/review artifact; no local coding is required.
5. The next milestone continues from the latest canonical working tree and package, not from a manually edited older ZIP.

The assistant must never state that the user's iPad ran a test. Test reports must identify the actual environment used by the assistant. Local managed-environment tests, remote GitHub Actions, Codespaces builds, and actual model runtime tests are separate evidence levels.

### After a private GitHub repository is created

The preferred iPad-capable development environment is GitHub Codespaces, not `github.dev` alone. B3 now provides `.devcontainer/devcontainer.json`, `.github/workflows/ci.yml`, `.github/dependabot.yml`, `pyproject.toml`, and the one-command verification tool.

- `github.dev` is a browser-based editor for browsing, editing, and committing. It does not provide a build terminal or compute environment.
- GitHub Codespaces provides a cloud-hosted Linux development container that can be used in a browser, including a terminal and Git operations.
- A repository `.devcontainer/devcontainer.json` should describe a repeatable environment.
- A GitHub Actions workflow should run deterministic validation on pushes and pull requests.

Codespaces has included monthly quotas and may incur charges after the applicable quota if billing is enabled. Check account budgets and spending limits before using it. Do not assume unlimited free compute.

### Laptop/PC phase

When a laptop becomes available, use it for native host acceptance testing. The target operating systems should initially be Windows 10+ and macOS 13+, with a supported Linux route documented where practical. Current Claude Desktop requirements and plan eligibility must be rechecked at that time.

The system should not require a powerful GPU: Peanuts is a file-based skill/harness that uses a hosted model. Local hardware requirements are primarily those of the supported desktop/runtime tools, development environment, and ordinary repository checks.

## 4. ChatGPT-primary owner workflow and optional host adapters

### ChatGPT Projects — primary owner-facing environment

Use the five-file manual Project adapter plus separate Project instructions as the current baseline. Projects keep files, instructions and related chats together; Project instructions apply only in that Project. Use the Project's available web search and other tools where present, but verify the exact current tools in the active chat. The five reference files are context, not executable scripts or guaranteed JSON Schema enforcement.

The current OpenAI Help Center states that Free Projects allow up to five files and Free uploads are limited to three files per day, subject to adjustments. The same documentation lists TXT as a supported text-file format. Recheck these product details at installation time. The five-file pack is designed for this limit; it may take two days to upload all five on Free.

### ChatGPT live-conversation acceptance

B10 evaluates ChatGPT in the exact live conversation/runtime, while keeping that separate from the configured Project UI. A live ChatGPT conversation may have tools that a normal Project chat does not; do not transfer tool claims between surfaces. Record the visible model label, available tools, date, and evidence.

### Actual Project UI acceptance

The owner must create/open `Friday — Peanuts`, paste `adapters/chatgpt/PROJECT_INSTRUCTIONS.md` into Project settings, upload the five `.txt` files, and run a fresh Project-chat smoke test. A second fresh Project chat must resume from a saved handoff. The assistant cannot claim this was done without the owner-visible Project UI evidence.

### Claude Code and Codex — optional generated coding-host adapters

The repository prepares portable Agent Skill, Claude Code and Codex packages. These remain secondary optional adapters. Actual discovery, permissions and runtime behavior must be tested before claiming compatibility. They are not prerequisites to completing Peanuts in ChatGPT.

### Native ChatGPT Skills

Native Skills are conditional on account, workspace, and product-surface eligibility. Do not require native activation for the current manual Project route; test it only if the owner's surface explicitly exposes it.

## 5. Revised construction milestones

B0–B2 remain the completed foundation milestones. The remaining sequence is revised to front-load reproducibility and host testing.

| Milestone | Purpose | Main outputs | Exit criteria |
|---|---|---|---|
| **B3 — Reproducible development and CI foundation** | Make the repository testable in ChatGPT's environment, GitHub Actions, and Codespaces. | Development dependency configuration, test runner, cross-platform CI workflow, Dev Container config, one-command validation, test instructions. | All deterministic checks pass in the available Linux environment; CI and container configurations are structurally validated; limitations are documented. |
| **B4 — Minimal end-to-end vertical slice** | Prove the stages connect before expanding every method. | Minimal Peanuts skill prototype, synthetic event example, research record, problem brief, concept, quick council screen, draft brief/PRD, fresh-session handoff. | A new session can resume using saved artifacts; no fabricated user validation; all handoff/traceability tests pass. |
| **B5 — Research and Product Discovery** | Implement event intelligence, prior-art research, JTBD, opportunity mapping, balanced validation, and event alignment. | Skill references, research templates, evidence records, discovery tests. | Cases for complete, vague, conflicting, stale, and missing official event information pass their defined rubrics. |
| **B6 — NUTS Innovation** | Implement broad but selective cross-domain inspiration and analogy transfer. | Creative Influence workflow, source-specific research paths, Analogy Card, rejection checks, evaluation cases. | Strong and superficial analogies are distinguished on representative cases; source fidelity and limitations are preserved. |
| **B7 — Four-Council and assumption validation** | Implement adaptive critique, stable dimensions, severity, event overlay, and validation planning. | Rubrics, review record, calibration cases, comparison against simpler critique baseline. | Critical seeded risks are not hidden by averages; results are compared with baseline; limitations and false positives are reported. |
| **B8 — PRD, Technical Design, and delivery handoff** | Convert approved, traceable findings into buildable specifications. | Project Brief, PRD, Technical Design, Build Plan, Demo Plan, requirement traceability checks. | Material requirements link to origin/evidence, acceptance criteria and verification methods; unresolved assumptions stay visible. |
| **B9 — Skill packaging and host adapters** | Package the canonical Peanuts skill and host-specific integration guidance. | `SKILL.md`, references, templates, scripts, generated install bundles, Claude/Codex paths, ChatGPT manual Project instructions and five-file reference pack. | Packaging is reproducible; no duplicated hand-maintained core; metadata and file paths validated. Actual host runtime tests remain separate. |
| **B10 — Full verification and release candidate** | Run regression, privacy/security, usability, reproducibility, and model-runtime acceptance. | Release candidate ZIP, CI report, evaluation report, known limitations, setup guide, release checklist. | Deterministic tests pass; supported CI matrix passes; target runtime smoke tests are completed where access exists; no unresolved critical failure is hidden. |

## 6. Validation ladder and evidence labels

| Level | Validation | Where it runs | What it proves |
|---|---|---|---|
| **V0** | File/package integrity, Markdown links, JSON schemas, secret-pattern scan, manifest hashes | ChatGPT-managed build environment | Files are internally consistent under the checks performed. |
| **V1** | Python unit and integration tests | ChatGPT-managed Linux/container environment | Deterministic tools work in that Linux environment. |
| **V2** | Cross-platform GitHub Actions matrix | GitHub-hosted runners after private upload | Supported scripts/tests pass on configured OS/Python combinations. |
| **V3** | Dev Container/Codespaces initialization and commands | GitHub Codespaces in browser | Reproducible cloud Linux environment can initialize and run checks. |
| **V4** | Claude Code skill discovery, invocation, permissions, project resumption | Actual Claude Code host or eligible Codespaces terminal | The real Claude runtime recognizes and uses the package as intended. |
| **V5** | ChatGPT manual/native skill route | Actual supported ChatGPT account/surface | The documented primary Project route works on the exact account/surface tested. |

A level must not be marked passed unless its checks were actually run. If an environment is unavailable, mark it `NOT RUN` with a reason.

## 7. Private GitHub upload from an iPad

The recommended final handoff is one cumulative ZIP. Keep it below GitHub's current browser-upload per-file limit (currently 25 MiB) and verify the limit again when uploading.

A practical route:

1. Create a **private**, initially empty GitHub repository named `Friday` (do not add a README, license, or `.gitignore` because those files are already in the package).
2. From Safari on iPad, use GitHub's browser upload to upload the single final ZIP as a temporary repository file and commit it.
3. Create a Codespace for the repository and open it in the browser.
4. The cumulative release ZIP is built with repository contents at the archive root (there is no enclosing `Friday/` folder). In the Codespaces terminal, run `unzip -q Friday-<milestone>.zip -d .`, then remove the temporary ZIP with `rm Friday-<milestone>.zip`. The archive will place `README.md`, `.github/`, `.devcontainer/`, `docs/`, `tools/`, and the other repository paths directly in the repository root. Run the documented validation commands before committing.
5. Commit and push the extracted repository contents. The GitHub Actions workflow then runs the configured checks.

The exact archive name and copy-paste commands will be supplied in the final handoff guide. `tools/package_release.py` builds and verifies the repository-root archive layout so users do not accidentally create a nested `Friday/Friday` directory. The archive must never remain committed in the final repository unless deliberately required.

If the upload route or Codespaces UI behaves differently on the owner's iPad/browser, stop and use the alternative at the next available computer; do not improvise by exposing the repository publicly.

## 8. `github.dev` versus Codespaces

Use `github.dev` when only reading or making small file edits. It runs in the browser sandbox and does not provide a build terminal/compute environment.

Use Codespaces when installing development dependencies, running Python, invoking Claude Code, or testing the Dev Container. It is a cloud compute environment and may consume the account's included quota.

## 9. Definition of ready for upload

Before the first private GitHub upload, the assistant must deliver:

- A complete cumulative repository ZIP.
- Updated package manifest and SHA-256 verification.
- A deterministic test report identifying environment and exact commands.
- JSON Schema and cross-record validation results.
- Python unit/integration test results.
- Markdown-link and repository-integrity checks.
- Static privacy/secret scan with its limitations.
- Dev Container and GitHub Actions configurations ready for remote execution.
- Skill package and platform-specific install instructions.
- A list of tests that cannot be run until GitHub/Claude/ChatGPT runtime access is available.

This is **pre-upload readiness**, not proof that GitHub Actions or Claude Code already passed.

## 10. Definition of ready for first real use

After private upload, require:

- GitHub Actions configured matrix passes.
- Codespaces initializes from the checked-in Dev Container and executes all required checks.
- Claude Code recognizes and invokes Peanuts in a fresh session on an eligible host.
- A saved project can be resumed in a fresh session without relying on old chat history.
- Critical evaluation cases meet their predeclared acceptance criteria.
- No critical security/privacy issue remains unresolved.
- Known limitations and product-plan dependencies are documented.

ChatGPT manual Project acceptance is marked only after the exact target account/surface and a fresh Project chat are tested. Native activation is not required for the current manual route and is not assumed.

## 11. Owner effort during the build

During B3–B10, the owner should only need to:

- Give direction and approve consequential design decisions.
- Say `GO` to advance a milestone.
- Review the milestone summary and optionally download its ZIP.
- Avoid editing files manually unless specifically desired.

The owner will need to perform account-level actions later: create the private GitHub repository, authorize GitHub/Codespaces, and sign in to Claude Code if that runtime is to be tested. These actions cannot be performed or authorized by ChatGPT on the owner's behalf.

## 12. Decision summary

- Use ChatGPT as the primary owner-facing build and operating environment; no laptop is required for authoring and the deterministic checks available in the managed environment.
- Build reproducible CI and Dev Container support before expanding complex methods.
- Use Codespaces from iPad as an optional cloud terminal after private upload; do not confuse it with `github.dev`.
- Do not promise Claude/ChatGPT native runtime compatibility until tested on the actual eligible host/surface.
- Upload a private ZIP only after pre-upload readiness checks; treat GitHub Actions and actual runtime acceptance as post-upload validation gates.
- Public release is a separate decision and is not implied by private upload.

## 13. Official references

- GitHub Codespaces development: https://docs.github.com/en/codespaces/developing-in-a-codespace
- What are GitHub Codespaces / billing and Dev Container configuration: https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces
- VS Code for the Web / `github.dev`: https://docs.github.com/en/codespaces/the-githubdev-web-based-editor
- GitHub browser file upload limits: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- GitHub Actions Python CI: https://docs.github.com/en/actions/tutorials/build-and-test-code/python
- Claude Code first-day setup: https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code
- Claude Desktop availability and system requirements: https://support.claude.com/en/articles/10065433-install-claude-desktop
- ChatGPT Skills availability: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- ChatGPT/Codex Skills authoring: https://learn.chatgpt.com/docs/build-skills


## 14. B10 ChatGPT-primary acceptance amendment (2026-11-02)

Use `docs/acceptance/CHATGPT_PRIMARY_RUNTIME_ACCEPTANCE.md` as the B10 acceptance protocol. It separates managed repository tests, live ChatGPT conversation behavior, target Project UI/fresh-session behavior, remote CI/Codespaces, and optional host runtimes. The owner-side Project UI test is required before `READY_FOR_CHATGPT_MANUAL_USE`; do not infer it from current conversation behavior or from a valid ZIP.
