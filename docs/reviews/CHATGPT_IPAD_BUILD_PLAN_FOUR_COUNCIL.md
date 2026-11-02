# Four-Council Review — ChatGPT/iPad-First Build and PC Readiness Plan

**Status:** Completed planning review; roadmap updated  
**Date:** 2026-11-01  
**Scope:** Delivery workflow and proof strategy only; no B3 implementation performed in this review.

## Executive verdict

**PASS WITH BOUNDED LIMITATIONS.** The project can continue to be authored and pre-tested with ChatGPT while the owner uses an iPad. A laptop is not required for the assistant to create repository files, write scripts, run available deterministic tests in its managed environment, inspect results, and produce cumulative ZIP packages.

However, ChatGPT's managed Linux test environment is not the owner's future laptop and does not prove Claude Code or ChatGPT native Skills runtime behavior. The revised roadmap therefore distinguishes pre-upload checks from post-upload CI, Codespaces checks, and real-host runtime acceptance.

## Council 1 — Systems Architect

**Verdict: PASS**

- Maintain one canonical portable skill source and separate host adapters.
- Add a reproducible Dev Container for browser-based cloud development.
- Keep `CLAUDE.md`, `AGENTS.md`, and `SKILL.md` distinct because their host roles differ.
- Use staged validation: managed environment, cross-platform CI, Codespaces, then actual model runtime.
- Avoid database, vector store, and multi-agent complexity until a measured need exists.

**Concern:** Do not conflate cross-platform Python tests with Claude Code skill discovery. They prove different properties.

## Council 2 — Build and Release Engineer

**Verdict: PASS WITH CONDITIONS**

- Add a one-command verification entry point.
- Run unit/integration tests plus schema and repository validation.
- Configure GitHub Actions for a documented OS/Python matrix.
- Pin or otherwise govern CI actions and dependencies; use least-privilege workflow permissions.
- Preserve the test report, package manifest and SHA-256 hashes for every release candidate.

**Concern:** GitHub-hosted CI cannot be claimed as passed before the repository is pushed and the workflow has run. The same applies to Codespaces.

## Council 3 — iPad UX and Developer Experience

**Verdict: PASS**

- ChatGPT remains the main authoring/build partner during the iPad-only period.
- Owner interaction during construction is limited to decisions, `GO`, and milestone review.
- Deliver cumulative ZIP packages, not instructions requiring manual local code editing.
- Use GitHub Codespaces for a terminal and cloud compute from a browser after private upload.
- Do not mistake `github.dev` for Codespaces: `github.dev` is an editor without build compute/terminal.
- Offer a one-ZIP private upload route if the archive remains within the current browser upload limit.

**Concern:** Codespaces quotas and billing must be checked before use. Touch UI may be less comfortable than a laptop, but the cloud terminal is technically available in the browser.

## Council 4 — AI Evaluation and Security

**Verdict: PASS WITH CONDITIONS**

- Every build milestone has deterministic acceptance criteria.
- Synthetic model evaluations must remain labelled as synthetic until actually run against the finished skill.
- Model outputs must preserve uncertainty and evidence provenance.
- ChatGPT native Skills availability is account/surface dependent; use a manual file/Project fallback when native installation is unavailable.
- Claude Code runtime acceptance requires an eligible plan or configured paid route, and an actual invocation test.
- No credentials, private context or participant data enter the repository package.

**Concern:** No system can guarantee every LLM answer is correct. The release standard is transparent, risk-based evidence and tests, not an absolute correctness promise.

## Decision

Reorder remaining construction milestones:

1. B3 — Reproducible development and CI foundation.
2. B4 — Minimal end-to-end vertical slice.
3. B5 — Research and Product Discovery.
4. B6 — NUTS Innovation.
5. B7 — Four-Council and assumption validation.
6. B8 — PRD, Technical Design, and delivery handoff.
7. B9 — Skill packaging and host adapters.
8. B10 — Full verification and release candidate.

The owner can remain iPad-only during B3–B10. Before first private upload, the assistant must pass available managed-environment checks and provide a complete release candidate. After private upload, GitHub Actions and Codespaces provide additional remote evidence. Actual Claude Code and ChatGPT runtime status is reported separately.

## Sources consulted

- GitHub Codespaces development: https://docs.github.com/en/codespaces/developing-in-a-codespace
- GitHub Codespaces architecture/billing: https://docs.github.com/en/codespaces/about-codespaces/what-are-codespaces
- VS Code for the Web: https://docs.github.com/en/codespaces/the-githubdev-web-based-editor
- GitHub browser upload: https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository
- GitHub Actions Python CI: https://docs.github.com/en/actions/tutorials/build-and-test-code/python
- Claude Code first-day setup: https://support.claude.com/en/articles/14552382-your-first-day-in-claude-code
- Claude Desktop requirements: https://support.claude.com/en/articles/10065433-install-claude-desktop
- ChatGPT Skills availability: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- ChatGPT Skills authoring: https://learn.chatgpt.com/docs/build-skills
