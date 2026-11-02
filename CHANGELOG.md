## [0.15.0-rc.2] - 2026-11-02 — Clean source publication

### Changed
- Prepared the complete Stage 2 source tree for the owner-selected friday-core repository.
- Excluded source ZIPs from the new main tree; preserved the existing MIT license. The older repository and its history remain separate.
- Updated current release guidance to point to commit-specific GitHub Actions results.

### Limits
- Source verification and hosted CI are separate from actual model/consumer host behavior.

## [0.15.0-rc.1] - 2026-11-02 — Stage 2 minimal manager

### Added
- Portable FRIDAY.md entrypoint, deterministic read-only capability selector and dry-run intake validator, plus generated manual chat adapter.
- Per-package capability contracts with input/output, prerequisite, permission, fallback and handoff declarations.
- Thirty manager regression cases covering extension, no-match/ambiguity, dependency/prerequisite gates, malformed paths/data, no execution/no writes and metadata-only export.
- Early CI/host preflight method and preserved evidence of an authentication-blocked real Codex attempt; clean Linux Python matrix checks supplement existing verification.

### Changed
- Updated current architecture and host guidance to distinguish the implemented helper from autonomous/model behavior.
- Added manager validation/test group to complete verification; retained previous checks, dependency pins and test assertions. Pinned the previously undeclared transitive typing_extensions dependency discovered during clean Python wheel resolution.
- Refreshed source/consumer packages and current release evidence. Preserved the existing owner-authored MIT license discovered in the public GitHub repository. No remote source was pushed or published.

### Limits
- CLI authentication must be repaired before a real Peanuts model smoke result is possible. Workflow lint/Linux containers do not establish GitHub-hosted, macOS/Windows or consumer iPad behavior. Profile memory, third-party rights review and public-release acceptance remain later work.

## [0.14.1-rc.1] - 2026-11-02 — Stage 1 baseline repair

### Fixed
- Resolved all 21 baseline Ruff findings without weakening lint rules: unused imports, unnecessary f-strings and direct-script import ordering. Repository-local imports after path bootstrap have targeted E402 annotations; third-party imports moved before it.
- Reconciled conflicting public/private and provider-priority guidance. Current architecture decisions are authoritative; Stage 0 decisions remain explicitly historical.
- Updated cross-host acceptance scope and source archive name without claiming a new runtime test.

### Changed
- Set the public, provider-neutral Friday manager destination while stating the selector is planned for Stage 2, not implemented.
- Replaced the construction-history README with purpose, prototype setup, capability boundaries, verification and source links.
- Added the six-stage revision sequence; separated optional user-reviewed profile import from reusable public source.
- Regenerated affected host snapshots, consumer packages and source manifest from canonical files.

### Evidence and limits
- See `RELEASE_VERIFICATION.md` for actual commands/results and `docs/reviews/REVISION_STAGE_1_REVIEW.md` for handoff.
- Real host behavior, configured Project recovery, remote CI, measured savings and independent usefulness calibration remain unverified. License/publication and later-stage features are pending.

## [0.11.0-draft] - 2026-11-01 — B8 PRD, Technical Design, and Delivery Handoff

### Added
- Requirement, acceptance-test, build-task, artifact, and structured demo-plan schemas, templates, and project ledgers.
- Project Brief, PRD, Technical Design, Build Plan, human-readable Demo Plan, and machine-readable `demo-plan.json` templates.
- Peanuts P7/P8/P9 references for requirements, technical design, build planning, demo honesty, and execution handoff.
- Three B8 quality rubrics and EVAL-062–087 synthetic evaluation cases.
- B8 semantic validation for evidence provenance, approval constraints, acceptance-test coverage/lifecycle, requirement/task dependency graphs, artifact integrity and cross-stage references, Markdown traceability, demo-claim evidence strength, and P7–P9 gates.
- Positive and negative full-workspace integration tests, including legacy-workspace compatibility checks.

### Changed
- Added `validate_b8.py` to the consolidated verifier without replacing or weakening B1–B7 validation.
- Added explicit status explanations for blocked/cancelled tests and tasks; made acceptance-criterion IDs local to their owning requirement; hardened document traceability against partial-ID matches.
- Kept JSONL ledgers and file-centered project architecture; no database, runtime orchestrator, or automatic product approval was introduced.

### Limitations
- Structural tests do not prove market demand, user desirability, architecture feasibility, estimate accuracy, legal/security sign-off, or live Peanuts model behavior.
- EVAL-062–087 are valid and ready for later runtime evaluation; they have not been passed by a live model. Ruff, remote CI, Codespaces, and Claude/Codex/ChatGPT host runtime tests remain separately gated.

## [0.9.4-draft] - 2026-11-01

### Added
- B6.5 capability growth maturity ladder and development incident disclosure/recovery protocol.
- Registry safeguards for unique canonical package paths, skill entrypoint identity, and verified host discovery claims.

### Changed
- Clarified Friday as repository umbrella/shared governance foundation first; an active manager remains optional and must be justified by observed coordination needs.
- Kept the capability registry extensible across skills, harnesses, workflows, agents, and toolsets without forcing non-skills to expose `SKILL.md`.
- Consolidated evaluation catalog documentation and corrected its synthetic case count/status.

### Limitations
- No live model token-savings comparison, autonomous manager, remote CI/Codespaces run, or Claude/ChatGPT runtime pass is claimed.

## [0.9.0-draft] - 2026-11-01

### Added
- B6 NUTS operational skill reference and source-domain playbook for biology, history, engineering, culture/social systems, economics/operations, and existing products/processes.
- Analogy Card and NUTS Run JSON Schemas, project record templates, and append-oriented project ledgers.
- Project-level traceability from analogy records to source/claim records and from NUTS runs to analogy/source/claim records.
- NUTS analogy-quality rubric, EVAL-031–EVAL-038, B6 validator, and regression tests.
- Explicit “no useful analogy” outcome and retained-for-test evidence gate.

### Changed
- Updated NUTS method to B6 operational specification and expanded the Creative Influence System, domain-specific research procedures, relational mapping, mismatch analysis, baseline comparison, and rejection conditions.
- Updated Peanuts skill routing, PPA, Tool & Knowledge Registry, project record architecture, evaluation index, roadmap, and README.
- Project validation remains backward-compatible with older workspaces missing B6 ledgers; it reports a warning and treats those ledgers as empty rather than modifying user data.

### Limitations
- B6 synthetic cases and structural tests are not live-model evaluation results.
- No actual domain-specific analogy research, novelty determination, or user-facing innovation outcome is claimed.

# Friday Changelog

## [0.13.2-rc.1] - 2026-11-02 — Cross-host installer security hardening

### Added
- Whole-archive preflight before extraction, including safe path normalization, duplicate and case/Unicode-prefix collision rejection, symlink/non-regular entry rejection, file/directory conflict checks, and bounded entry/member/total-size/compression-ratio checks.
- Negative tests proving path traversal, symlinks, duplicate destinations, case-insensitive prefix collisions, parent-file conflicts, and oversized members are rejected before any installation write.
- EVAL-132–134 and RUN-030–032 for deterministic malicious-archive rejection cases.

### Changed
- Strengthened Codex and Claude Code adapter installation simulation without changing canonical skill instructions, host discovery paths, or permission grants.
- Updated B10 validation and release records to 32 cases/results through EVAL-134.

### Limitations
- These checks establish safe package structure and simulated extraction only. Actual Codex CLI and Claude Code discovery/invocation, method fidelity, and fresh-session runtime checks remain NOT RUN until executed in those real hosts.

---



## [0.13.1-rc.1] - 2026-11-02 — B10 cross-host acceptance supplement

### Added
- Codex and Claude Code project-installation simulation using the current official discovery paths and matching root guidance files.
- Cross-host relative-reference, canonical byte-parity, path-safety, executable-content and no-auto-permission checks.
- Actual Codex/Claude Code and claude.ai runtime installation/smoke-test protocols, exact prompts, and a run-record template.
- EVAL-123–131 and RUN-021–029: four deterministic host-package/install passes; five actual host runtime/UI tests remain blocked until executed in eligible real hosts.

### Changed
- Expanded B10 to distinguish install-layout compatibility from actual model-runtime compatibility for Codex, Claude Code and claude.ai.
- Added the host-adapter simulation validator to the consolidated verifier and regression suite.
- Updated root `AGENTS.md` and `CLAUDE.md` with exact installation and explicit invocation instructions.

### Limitations
- No Codex CLI, Claude Code CLI or claude.ai upload/runtime was available in the managed environment. Simulated installation does not establish discovery, invocation, method fidelity, tool permissions or fresh-session behavior.
- Actual host acceptance requires separate real sessions for each host and independent review of critical results.

---


## [0.8.0-draft] - 2026-11-01

### Added
- B5 event intelligence, user/problem research and evidence-synthesis protocols.
- Research plan, question, round, finding and opportunity schemas/records with project-level traceability.
- User research consent, privacy, local-review and sensitive-participant safeguards.
- Event dossier, research plan, interview guide, coverage matrix, synthesis and opportunity-map templates.
- EVAL-020–EVAL-030 synthetic cases and three B5 research-quality rubrics.
- B5 deterministic validator and research record tests.

### Changed
- Peanuts skill routes event, user-discovery and evidence-synthesis tasks to dedicated references.
- Project validator checks question-to-round linkage and consent-related conditions.
- Product discovery protocol versioned to 0.4.0-draft; tool/knowledge registry reviewed for B5 research capability.

### Limitations
- Evaluation cases are structurally validated and marked ready; no live-model evaluation results are claimed.
- No real event research, participant interviews, or direct field validation were performed as part of this milestone.
- Ruff was not executed in the managed environment; full CI lint remains configured for a network-enabled environment.


## 0.7.0-draft — 2026-11-01

### Added
- Canonical Peanuts Agent Skill prototype under `skills/peanuts/`.
- Self-contained workflow, evidence-boundary, and quick-council references.
- Reusable artifact templates for event dossier, problem brief, analogy card, concept brief, quick review, draft PRD, and handoff.
- Synthetic end-to-end event-first fixture and vertical-slice run schema.
- Deterministic vertical-slice validator and five negative/positive tests.
- Evaluation case `EVAL-019`.

### Changed
- Root Claude/Codex instructions now point to the B4 canonical skill prototype while preserving the B9 native-discovery boundary.
- Repository validation checks the skill metadata and required skill resources.
- `tools/verify.py` includes B4 vertical-slice validation.
- Roadmap and README status updated for B4.

### Limitations
- No Claude Code, Codex, or ChatGPT host runtime was executed.
- The example is synthetic, not external research or user validation.
- The skill prototype uses whatever research/tools the host actually provides; no browser/API integration is bundled yet.

# Changelog

## 0.9.4-draft — 2026-11-01

- Refined B6.5 context efficiency and extensible capability architecture without changing earlier milestone acceptance criteria.
- Clarified Friday as repository umbrella/shared governance foundation first; active manager/control plane remains optional and evidence-gated.
- Kept the capability catalog generic across skill, harness, workflow, agent, and toolset package kinds; only skill packages require `SKILL.md`, while all packages require a documented entrypoint.
- Added explicit development incident disclosure, timeout recovery, status vocabulary, and regression-integrity protocol.
- Consolidated evaluation-library documentation and corrected evaluation case counts/status language.
- No live provider token-savings claim, autonomous routing claim, or host-runtime pass is made.

All notable Friday repository changes are recorded here. The project is pre-release; entries describe documentation/scaffold work, not a deployed assistant.

## 0.3.0-draft — 2026-10-31

- Completed the Stage 0.5 four-perspective document review and applied required amendments.
- Added Professional Practice Architecture, Tool & Knowledge Registry, and Quality Assurance specifications.
- Strengthened participant research ethics, synthesis, triangulation, and validation distinctions.
- Expanded NUTS with Creative Influence System, source-specific methods, and analogy rejection criteria.
- Calibrated Four-Council dimensions, severity, ownership, and evaluation plan.
- Created B1 local repository scaffold, Claude/Codex project guidance, contributor rules, and Git hygiene files.
- No remote GitHub repository or public license created.

## 0.4.0-draft — 2026-10-31

- Completed B2 project-record and evaluation foundation locally.
- Added project/state, source, claim, assumption, decision, evaluation-case and evaluation-result JSON Schemas (Draft 2020-12).
- Added project/record templates, safe local workspace initializer and project validator.
- Added 18 synthetic evaluation cases and six evaluation rubrics; no AI run results are claimed.
- Added project-record/state architecture documentation and B2 review.
- Added JSON Schema validation as a development-only dependency.
- No remote repository, publication, or Peanuts skill installation performed.


## 0.5.0-draft — 2026-11-01

- Revised the remaining build sequence for ChatGPT-assisted, iPad-first construction.
- Added explicit validation levels separating assistant-managed tests, GitHub Actions, Codespaces, Claude Code runtime, and ChatGPT routes.
- Added PC/laptop readiness acceptance checklist.
- Clarified the distinction between `github.dev` (browser editor) and Codespaces (cloud terminal/compute).
- Documented private ZIP upload and later remote validation; no GitHub remote or publication created.
- Reordered B3 to establish reproducible development and CI before the B4 end-to-end vertical slice.
- Documented account/plan dependencies for Claude Code and current ChatGPT Skills availability.


## 0.6.0-draft — 2026-11-01

- Added Python 3.11+ tool configuration and an exact-version development dependency snapshot.
- Added pytest unit/integration coverage for project initialization, validation, configuration, and package-manifest behavior.
- Added a shared package-manifest builder/checker and full source-file coverage verification.
- Added `tools/verify.py` as the single deterministic verification entry point.
- Added SHA-pinned GitHub Actions CI across Ubuntu, Windows, and macOS with Python 3.11–3.14; workflow is configured but not remotely executed.
- Added Dependabot configuration for Python and GitHub Actions dependencies.
- Added a non-root Python 3.13 Dev Container configuration for Codespaces; container build not yet executed remotely.
- Hardened project ID parsing to reject path-like/traversal input before slug normalization.
- Added B3 reproducibility documentation and four-perspective review.
- Pinned the Codespaces Dev Container to the verified `dev-3.13-bookworm` image digest and corrected the tag/digest pairing.
- Refined the verification runner to execute repository validators and pytest without an unnecessary nested process layer.

### B3 — Reproducible development and CI foundation

- Added a Python 3.11+ development baseline, exact-version development requirements, pytest/Ruff configuration, and a pinned Codespaces Dev Container image digest.
- Added cross-platform GitHub Actions CI for Windows, macOS, and Linux across Python 3.11–3.14, Dependabot updates, repository verification, manifest checks, and B2 regression coverage.
- Added unit/integration tests for configuration, safe project initialization, record parsing, and manifest behavior.
- Local Linux/Python 3.13 checks: repository validator PASS; B2 validator PASS; pytest PASS (23 tests); verifier PASS with Ruff skipped. Ruff itself and remote CI/Codespaces were not run in this managed environment.

## B4 completion note — 2026-11-01

- Delivered a structural end-to-end Peanuts vertical slice: canonical skill prototype, stage contracts, artifact templates, synthetic fixture, source/claim/assumption/decision traceability, run schema, validator, evaluation case, and five regression tests.
- Corrected EVAL-019's `correct_disposition` to the established `ask` enum; the sample Council artifact independently retains its conditional `VALIDATE` recommendation.
- Final local verifier: repository integrity PASS; B2 schema/workspace checks PASS (8 schemas, 19 evaluation cases); B4 validator PASS; pytest PASS (28 tests).
- Ruff NOT RUN in the managed environment; `--skip-lint` was explicit. CI is configured to install and run Ruff.
- GitHub Actions, Codespaces, and Claude/Codex/ChatGPT runtime tests remain NOT RUN. B4 is accepted as a structural milestone only, not as proof of live AI performance.


## B6 packaging handoff refinement

- Added a deterministic repository-root ZIP builder and archive verifier.
- Release ZIP members now extract directly into an empty GitHub repository root; no enclosing `Friday/` directory is created.
- Added tests for flat layout, manifest drift rejection, unsafe paths, and archive hash verification.
- Updated the iPad/Codespaces upload guide with exact extraction behavior.


## 0.9.1-draft — 2026-11-01

- Added deterministic repository-root release packaging through `tools/package_release.py`.
- Added archive verification for CRC integrity, exact file coverage, byte counts, and SHA-256 hashes.
- Refuse to package stale manifests, missing source files, unmanifested source files, duplicate paths, and path traversal entries.
- Write release archives atomically and use stable ZIP metadata for reproducible output.
- Changed iPad/Codespaces handoff so the archive extracts directly into the GitHub repository root without a nested `Friday/` directory.
- Added five package-builder tests; total Python suite now contains 46 passing tests.
- Fresh-extraction verification completed successfully on Linux/Python 3.13.5 with Ruff explicitly skipped.


## [0.9.2-draft] - 2026-11-01 — B6.5 Context and Capability Architecture

- Added a capability registry so Friday can grow beyond Peanuts without turning into a monolithic skill.
- Defined Friday as the future manager/control plane; autonomous routing remains unimplemented.
- Added progressive-disclosure/context engineering and provider-neutral resource modes.
- Added context evaluation cases/rubric and a compact session handoff template.
- Added capability validation and context inspection utilities.
- Explicitly documented that portable skills cannot enforce universal consumer-plan token/credit caps and that word/character counts are not token measurements.


## B7 — Four-Council and assumption validation (0.10.0-draft)

- Added structured Four-Council review and assumption-test schemas, templates, and project ledgers.
- Added dimension-specific score records, reviewer setup disclosure, event-alignment evidence, severity-ranked findings, and non-compensatory progression-gate invariants.
- Added assumption-test protocols with predeclared signals/thresholds, participant consent and data controls, completion outcomes, evidence and limitations.
- Extended project validation with B7 cross-record checks while preserving compatibility for older workspaces without B7 ledgers.
- Added operational Peanuts references, rubrics, EVAL-051–061, a B7 validator, and regression tests.
- Live-model behavior, rubric calibration, Ruff, remote CI, and host runtime acceptance remain separate verification gates.


## 0.12.0-draft — B9 Skill packaging and host adapters (2026-11-02)

- Corrected canonical Agent Skills metadata so `name: peanuts` matches `skills/peanuts/`; kept the description within a stricter Claude compatibility budget.
- Added deterministic generation for portable Agent Skills, Claude Code `.claude/skills/peanuts/`, and Codex `.agents/skills/peanuts/` packages.
- Added a ChatGPT Project manual fallback with exactly five generated plain-text `.txt` source files containing Markdown-formatted content, separate concise Project instructions, and iPad-first setup guide for the current Free-plan constraints.
- Added host adapter architecture and ChatGPT Project operating plan; updated capability registry and root host maps.
- Added B9 packaging validator, parity/reproducibility checks, packaging rubric, and EVAL-088–102.
- B9 resource-closure correction: portable, Claude Code and Codex bundles now include generated canonical support schemas, record starters, project templates and governing docs at referenced paths; ChatGPT's five files carry the actual subject-specific schemas and starters, not only a schema index.
- Updated standalone skill guidance to distinguish project-workspace record paths from skill-package resources and to avoid claiming unavailable repository scripts ran.
- Runtime discovery/invocation, current-user UI setup, remote CI/Codespaces, Ruff, and live-model evaluations remain separate B10 acceptance items.


## 0.12.1-draft — B9 resource-closure correction (2026-11-02)

- Closed a standalone portability gap by generating the canonical schemas, record templates, project templates and governing references into portable and host-specific skill packages.
- Embedded the complete relevant schema and record-template JSON in the corresponding five ChatGPT Project reference files without increasing the five-file upload count.
- Clarified that project record ledgers live in the project workspace; standalone skill packages do not include or claim to execute Friday's repository validators.
- Added EVAL-102 and regression tests for support-resource closure, schema/template coverage and ChatGPT bundle readability.


## 0.13.0-rc.1 — B10 ChatGPT-primary acceptance (2026-11-02)

- Makes ChatGPT Projects the primary owner-facing environment; Claude Code/Codex remain optional generated adapters.
- Adds the B10 ChatGPT primary runtime acceptance protocol and rubric separating live conversation, configured Project UI, managed repository tests, remote CI, and optional host runtimes.
- Adds EVAL-103–122 for continuity, PPA/tool choice, current facts, prompt injection, evidence boundaries, NUTS selectivity, Four-Council independence disclosure, consent, PRD/design gates, handoff, Project setup and calibration.
- Updates owner-facing build/release plans and supersedes the historical Claude-first proposal for the current owner workflow.
- Target Project UI fresh-session validation remains NOT RUN until the owner installs the Project instructions/five files and provides the observed result.
- Managed regression passed 160/160 across three bounded test groups; repository integrity and individual B2/B4/B5/B6/B6.5/B7/B8/B9/B10 validators passed. The targeted B2 workspace lifecycle validator completed; the consolidated verifier remained incomplete in this runner.
- Actual owner Project UI/fresh-session acceptance, Ruff, remote CI/Codespaces, optional host runtimes and independent human calibration remain NOT RUN.


## 0.13.3-rc.1 — B10.1 Claude Chat and Project integration (2026-11-02)

- Added a dedicated ordinary Claude chat Skill upload package. It keeps the single canonical Peanuts content but generates the consumer-compatible `peanuts/skill.md` lowercase entrypoint; the portable/Codex/Claude Code canonical `SKILL.md` remains unchanged.
- Corrected the Claude consumer description validation to Anthropic's current 200-character limit; the canonical 191-character description fits without editing the shared methodology.
- Added a separate `Friday — Peanuts` Claude Project companion: compact Project instructions, five curated governance/architecture/method/status knowledge files, iPad setup guide, smoke prompts, and owner run-record template.
- Distinguished reusable Skill procedures from persistent Project instructions/knowledge and cross-chat handoff state. No claim that Project chat history, repository filesystem, shell or validators are automatically available.
- Added B10.1 acceptance protocol, rubric, EVAL-135–140 and RUN-033–038. Local deterministic cases pass; owner-side Skill upload, Project setup, fresh-chat continuity, and actual Claude chat tool-boundary behavior remain blocked/NOT RUN.
- Added a standalone B10.1 builder and validator; generated outputs remain disposable and are rebuilt from canonical sources.


## 0.13.5-rc.1 — B10.1-C context and hackathon preflight (2026-11-02)

- Added optional, gate-first Hackathon Opportunity Sprint under P1–P6; official competition eligibility takes precedence over proposed prize/fit scores, and unknowns are preserved.
- Added canonical method, lightweight Peanuts reference, compact shortlist template and tests. Included them via deterministic generation in all host packages and Claude Project Knowledge.
- Tightened quality-per-context guidelines: selective reference loading, existing findings, short first output, risk-based escalation and honest provider token/credit measurement.
- Added four-perspective direction audit and iPad owner-run Claude activation/quality-efficiency pilot; live upload and fresh-session tests remain NOT RUN until performed.
- Preserved the original B10.1 acceptance threshold and P1–P10 stage gates; no unnecessary manager or API token-control service introduced.

## 0.14.0-rc.1 — Ready-to-upload source and bounded verifier (2026-11-02)

- Preserves canonical Peanuts and B0–B10.1-C with no core methodology rewrite.
- Includes generated checked-in skill discovery paths for Codex (`.agents/skills/peanuts/`) and Claude Code (`.claude/skills/peanuts/`). Generated files are checked against the canonical skill and must never be independently authored.
- Introduces `tools/sync_host_entrypoints.py --sync|--check` and focused regression tests.
- Replaces the test-order-sensitive one-command verifier with individually bounded validator processes and exhaustive pytest module groups; runs Ruff separately when installed.
- Adds iPad-first deployment instructions, visible release gates and an exact-package verification report.
- Preserves the separate Claude Chat consumer ZIP and ChatGPT Project companion; actual provider account UI acceptance remains pending and is not claimed.
