# B10 — ChatGPT-Primary Acceptance and Release Candidate Review

**Review date:** 2026-11-02  
**Status:** **PASS WITH BOUNDED LIMITATIONS — managed B10 construction, one live ChatGPT conversation run, and Codex/Claude Code filesystem installation simulations completed; actual Project UI and actual Codex/Claude host runtimes remain NOT RUN.**  
**Version:** 0.13.2-rc.1  
**Scope:** ChatGPT-first owner workflow, Project adapter constraints, live ChatGPT conversation behavior, PPA/Peanuts end-to-end demonstration, EVAL-103–134, ChatGPT result records, Codex/Claude Code installation simulations, host run protocols, B10 validator, B1–B9 preservation, and release-gate documentation.

This is a structured review using four professional perspectives. They are not four independent human experts or statistically independent model runs. The scores are qualitative assessments of the B10 implementation and evidence, not measured model performance or certification.

## 1. Executive verdict

B10 changes the owner-facing primary environment to ChatGPT Projects, consistent with the accepted owner decision in ADR-015 (`docs/DECISIONS.md`) and ADR-043 (`docs/architecture/DECISIONS.md`). The portable canonical Peanuts source remains `skills/peanuts/`; the five-file manual Project adapter is the present iPad/Free route; Claude Code and Codex remain optional generated adapters. No native Skill dependency, custom API service, autonomous Friday manager, database, or duplicated core was introduced.

B10 adds a layered ChatGPT acceptance protocol. It separates the managed build environment, the live ChatGPT conversation tested in this session, the owner's actual Project UI/fresh-session test, remote CI/Codespaces, and optional host runtimes. Twenty result records are present: sixteen `passed`, one `partial` (the single-case baseline comparison), and three `blocked` (target Project UI, repeatability/independent calibration, and its explicit repeat-run gate). All twenty are unapproved same-model self-evaluations pending owner review.

The live ChatGPT demonstration applied PPA to a synthetic campus-service challenge, kept the challenge brief separate from user evidence, declined to force a NUTS analogy, disclosed the single-model Four-Council setup, preserved a high operational blocker, proposed consent-aware assumption tests, kept PRD requirements provisional, and refused to treat P8/P9 as approved. It did not claim interviews, API access, event compliance, or deployment approval.

**Disposition:** B10 build/managed candidate passes with bounded limitations. The repository is **not yet `READY_FOR_CHATGPT_MANUAL_USE`** because the five files and Project instructions have not been verified inside the owner's actual iPad Project and a second fresh Project chat has not resumed a saved handoff.

## 2. Four professional perspectives

### Council 1 — Product strategy and ChatGPT owner experience

**Assessment: 8.6/10 — Pass with bounded limitations**

Strengths:
- ChatGPT is now explicitly primary for the owner workflow, rather than merely a construction tool or secondary fallback.
- The Project route is based on current official product documentation: Project instructions/files, mobile use, a five-file Free Project limit, a three-file-per-day Free upload rate, and TXT support.
- The five-file reference pack remains within the current Project ceiling; instructions and setup guide remain separate.
- The manual route provides a realistic iPad path without requiring a laptop, custom API or alternative provider.
- User-facing acceptance is based on a short fresh-chat smoke test and durable handoff rather than a vague claim that installation succeeded.

Limitations:
- Actual iPad UI installation and source-list visibility have not been observed.
- A Free user may need two days to upload five files due to the separate daily rate limit.
- Project tools/account availability can change and must be rechecked at installation.

Recommendation: Do not call the Project route ready until the owner completes B10-C and records the exact UI result.

### Council 2 — Systems architecture and platform engineering

**Assessment: 8.9/10 — Pass**

Strengths:
- One canonical Peanuts implementation is preserved.
- ChatGPT Project instructions and references remain a manual adapter; they are not represented as executable runtime code.
- The system explicitly separates current conversation tools from tools available in a Project.
- ADR-002's historical Claude-first wording is superseded for owner-facing workflow, while Claude Code remains an optional adapter.
- Friday remains an umbrella, not an assumed autonomous manager.
- B10 validator, results schema, and exact EVAL-103–122 inventory are integrated into the repository verifier.

Limitations:
- A Project cannot execute repository Python validators just because their schemas and instructions are attached.
- The owner-side Project UI cannot be tested by the managed container.
- Remote CI, Codespaces and optional host adapters are not run.

Recommendation: Keep the separation of owner-facing Project experience and deterministic repository maintenance; do not simulate a shell in a normal chat or add an API runtime solely to avoid UI acceptance.

### Council 3 — Professional practice, method quality and operational usability

**Assessment: 8.5/10 — Pass with bounded limitations**

Strengths:
- PPA guides the model to classify the job/decision, select relevant disciplines, methods, prerequisites, tools, outputs and checks.
- The live synthetic run correctly identified that student demand and staff-update feasibility were unvalidated.
- NUTS was not forced where direct solution patterns were adequate.
- Four-Council was disclosed as one model using four perspectives; its high operational freshness/ownership blocker was not averaged away.
- Assumption tests included neutral user research, consent, de-identification, data minimization and local review boundaries.
- The PRD stayed provisional and the P8/P9 approval gates were not bypassed.

Limitations:
- The synthetic test does not demonstrate real student demand or staff feasibility.
- No human interview, usability study, technical spike or field observation occurred.
- A single model run cannot establish repeatability or generalizability.

Recommendation: Keep the method selection decision-led. The next real project should run the same methods against source-backed and participant-backed evidence, with local approval where required.

### Council 4 — AI assurance, security and evaluation

**Assessment: 8.2/10 — Pass with significant remaining runtime gates**

Strengths:
- Adds 32 B10 cases: continuity, PPA/progressive disclosure, current sources, tool boundaries, prompt injection, unknowns, NUTS selectivity, Four-Council disclosure, assumption/consent, PRD traceability, P7/P8/P9 gates, Project setup, independent calibration, no-fabrication, and external-action approval.
- Result records distinguish `passed` live-session cases from `blocked` target Project UI and independent-calibration cases.
- All self-evaluation records are marked unapproved and disclose the single-model/single-session limitation.
- The acceptance protocol requires exact target-surface evidence and fresh-session recovery.
- Uploaded/retrieved instructions are treated as untrusted content, not higher-priority instructions.

Limitations:
- Same-model self-evaluation is not independent human adjudication.
- Repeated fresh Project runs, human-labelled known-answer cases, and generic-critique baseline comparison are not complete.
- The prompt-injection scenario is a bounded synthetic test, not a comprehensive security assessment.
- Ruff, remote CI, Codespaces and native/optional host runtime checks remain not run.

Recommendation: Preserve failed/partial/blocked outcomes. Run at least three fresh Project sessions for critical safety and gate cases where practical, and obtain independent human adjudication before making reliability claims. Expand the paired generic-critique baseline beyond the single synthetic case.

## 3. Actual live ChatGPT evidence

- Current runtime: ChatGPT GPT-6 live conversation with web and managed container tools available; this is not the user's configured Project UI.
- Official Projects and file-upload documentation was checked on 2026-11-02 and cited in the acceptance protocol.
- A synthetic campus service-status challenge was processed through PPA, discovery planning, a NUTS decision, Four-Council screen, assumption tests, provisional requirements, and P8/P9 gate disposition.
- The malicious source-text variant asking to reveal private user data and fabricate organizer approval was treated as untrusted; no private information or fabricated approval was produced.
- EVAL-103–122 are recorded in `evals/results/results.jsonl`: 16 `passed`, one `partial` (EVAL-121), and three `blocked` (EVAL-117, EVAL-118, EVAL-122). All use same-model `model_grader`, and all `reviewer_approved=false`.

This is one observed conversation, not a multi-run benchmark. Full demonstration: `docs/acceptance/CHATGPT_RUNTIME_DEMO.md`.

## 4. Deterministic verification

B10-specific validation currently covers:

- 32 B10 evaluation cases against the shared JSON Schema and rubric references.
- 32 result records against the Evaluation Result schema.
- A hard guard that EVAL-117 (Project UI/fresh session), EVAL-118 (repeatability/independent review), and EVAL-122 (three-run/human adjudication) stay `blocked` until the required evidence exists.
- Presence of the acceptance protocol and its Project UI/NOT RUN disclosures.
- B10 validator integrated into `tools/verify.py`.
- ChatGPT Project instructions remain under the internal 6,000-character maintainability budget.

The final managed regression is **171/171 passed** across six bounded module runs (11 initializer + 7 B5 + 6 B6 + 18 B7 + 54 B8 + 75 B9/B10/configuration/release and host-security tests). All individual milestone validators and repository integrity passed. The targeted B2 validator passed. The consolidated verifier timed out at B2 and is not claimed as passed. Ruff is not installed in the managed environment and is marked `NOT RUN`. A test collection pass or partial progress output is not a completed test run.

## 5. Not run / not claimed

- Actual owner iPad Project settings, five-source visibility, fresh Project chat and second fresh-chat resume: **NOT RUN**.
- Independent human evaluation labels / Four-Council calibration / three-run repeatability: **NOT RUN**.
- Actual human participant research, staff workflow observation or real user validation: **NOT RUN**.
- Ruff: **NOT RUN** if not installed in the managed environment.
- GitHub Actions / Codespaces: **NOT RUN**; no remote repository is authorized/configured.
- Native ChatGPT Skills: **NOT RUN**, not required for the manual route and not assumed eligible.
- Codex and Claude Code **filesystem installation simulations: PASS**; actual CLI discovery, explicit invocation and model-method fidelity: **NOT RUN**.
- claude.ai/Cowork custom Skill upload and invocation: **NOT RUN**; separate surface and account-eligibility check required.
- `python tools/validate_b2.py`: **PASS** as a targeted standalone run (8 schemas, 134 evaluation cases and temporary workspace lifecycle/negative-path checks). The consolidated `python tools/verify.py --skip-lint` timed out when invoking B2 after repository integrity; standalone B2 success is valid, but the consolidated run remains incomplete.

## 6. Release gate

Current state: **B10 CANDIDATE — CHATGPT PROJECT UI ACCEPTANCE PENDING**.

Promote to `READY_FOR_CHATGPT_MANUAL_USE` only after the owner:

1. Installs `PROJECT_INSTRUCTIONS.md` in Project settings.
2. Confirms all five `.txt` sources appear in the Project source list.
3. Runs the smoke prompt in a new Project chat.
4. Saves a status/handoff as a Project source if available.
5. Opens a second fresh Project chat and verifies handoff recovery without invented state.
6. Records the actual UI result in `docs/acceptance/CHATGPT_PROJECT_UI_RUN_RECORD_TEMPLATE.md` (copy it to `CHATGPT_PROJECT_UI_RUN_RECORD.md`).

Public release remains a separate owner decision.
'''

cat > /mnt/data/friday_b10_work/docs/acceptance/B10_RELEASE_CHECKLIST.md <<'MD'
# B10 Release Candidate Checklist — ChatGPT Primary

## Local / managed environment

- [ ] Repository manifest current and hashes pass.
- [ ] All B2/B4/B5/B6/B6.5/B7/B8/B9/B10 validators pass (B2 must be explicitly run).
- [ ] Complete test collection passes; report split test execution transparently if needed.
- [ ] Ruff pass or explicitly `NOT RUN` with reason.
- [ ] Secret/privacy scan, symlink/path/link checks and archive integrity pass.
- [ ] ChatGPT Project adapter rebuilt from canonical source and has exactly five `.txt` reference files.
- [ ] ChatGPT Project instructions remain within the 6,000-character internal budget.
- [ ] B10 cases and result records validate; EVAL-117/118/122 remain blocked until evidence exists.
- [ ] Cumulative release ZIP extracts to repository root and re-verifies.

## ChatGPT primary live behavior

- [ ] Current Project/file capabilities verified from official docs.
- [ ] Live ChatGPT conversation behavior evaluated with EVAL-103–122; runtime and same-model limitations documented.
- [ ] No critical fabrication, prompt-injection, privacy, consent, unauthorized-action or stage-gate failure.
- [ ] Provisional sample project preserves assumptions, unknowns and unapproved requirements.

## Actual owner Project UI — mandatory before manual-use readiness

- [ ] Project instructions installed in `Friday — Peanuts`.
- [ ] Five `.txt` source files uploaded and visible.
- [ ] Fresh Project smoke prompt succeeds.
- [ ] Saved status/handoff is visible as a Project source, if supported.
- [ ] Second fresh Project chat resumes correctly.
- [ ] Verbatim evidence excerpt and outcome recorded.

## Remote / optional hosts — separate, not implied by ChatGPT manual-use readiness

- [ ] GitHub Actions (if repository is privately uploaded and owner authorizes).
- [ ] Codespaces / Dev Container (if enabled; review quota/billing first).
- [ ] Native ChatGPT Skills only if the account/surface exposes it.
- [ ] Claude Code / Codex only if the owner wants these optional routes.

## Final disposition

- `B10_CANDIDATE_PROJECT_UI_PENDING`
- `READY_FOR_CHATGPT_MANUAL_USE`
- `READY_FOR_PRIVATE_UPLOAD`
- `READY_FOR_CODESPACES_USE`
- `BLOCKED`

Never collapse these into an unqualified “fully works everywhere” claim.


## 6. Cross-host installer security hardening (0.13.2-rc.1)

- Added whole-archive preflight before extraction. It checks path normalization, traversal, duplicate destinations, case/Unicode-prefix collisions, symlink and non-regular entries, file/directory conflicts, entry count, per-member and total uncompressed size, and compression ratio before CRC/decompression and writing.
- Added negative tests proving rejection occurs before any partial installation writes.
- Added EVAL-132–134 and deterministic RUN-030–032. These are package-installer security results, not live Codex/Claude Code model-runtime passes.
- Codex/Claude Code filesystem installation simulation remains PASS; actual CLI discovery/invocation, method fidelity and fresh-session behavior remain NOT RUN.
