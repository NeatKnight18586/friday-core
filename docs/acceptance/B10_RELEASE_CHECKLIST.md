# B10 Release Candidate Checklist — ChatGPT Primary

**Version:** 0.13.2-rc.1  
**Disposition:** `B10_CANDIDATE_PROJECT_UI_PENDING`  
**Acceptance target:** ChatGPT Projects as the primary owner-facing environment.

## 1. Managed repository and deterministic checks

- [x] Repository integrity and manifest validation pass.
- [x] B2 targeted standalone schemas and temporary-workspace lifecycle validator passes.
- [x] B4 vertical-slice validator passes.
- [x] B5 research validator passes.
- [x] B6 NUTS validator passes.
- [x] B6.5 capability registry and context inspection pass.
- [x] B7 Four-Council and assumption-validation validator passes.
- [x] B8 requirements, technical design and handoff validator passes.
- [x] B9 skill packaging and host-adapter validator passes.
- [x] B10 ChatGPT-primary and cross-host evaluation/result validator passes.
- [x] Codex and Claude Code adapter archives safely install into disposable fixtures at official project paths with root guidance present.
- [x] Archive installer preflight rejects traversal, symlinks, duplicate destinations, case/Unicode path-prefix collisions, file/directory conflicts and oversized members before writing.
- [x] Canonical source parity, relative references, absence of executable helpers and absence of implicit `allowed-tools` grants checked.
- [x] 171/171 pytest cases pass across bounded module runs (11 initializer + 7 B5 + 6 B6 + 18 B7 + 54 B8 + 75 B9/B10/configuration/release and host-security tests).
- [x] Project instructions remain within the 6,000-character internal budget.
- [x] Main Peanuts skill remains within the 2,500-word soft budget; Claude/Codex root maps remain within 600-word soft budgets.
- [x] Manifest is regenerated and verified after final source changes.
- [x] Archive CRC, source path safety, SHA-256 and fresh extraction are checked.
- [ ] Consolidated `python tools/verify.py --skip-lint` completes end-to-end. Current run timed out at B2 although the targeted B2 standalone validator passed.
- [ ] Ruff static analysis. **NOT RUN:** Ruff is not installed in the managed environment.

## 2. ChatGPT runtime acceptance

- [x] Current official Projects and file-upload constraints verified.
- [x] Live ChatGPT GPT-6 conversation applied the Peanuts/PPA workflow to a synthetic challenge.
- [x] The live demonstration disclosed missing evidence, avoided fabricated research/API access, declined to force NUTS, disclosed Four-Council dependence, retained provisional requirements, and did not bypass P7–P9 gates.
- [x] Prompt-injection content in the synthetic source was treated as untrusted input.
- [x] 32 B10 case files and result records validate (23 passed, 1 partial, 8 blocked; all records unapproved). Of these, the 20 live ChatGPT conversation records are 16 passed, 1 partial and 3 blocked; cross-host records are 7 deterministic passes and 5 actual-host/UI blocks.
- [x] One exploratory generic-critique vs Four-Council paired comparison is recorded, with its single-case and same-model limitations.
- [ ] Repeated fresh Project sessions and independent human adjudication. **NOT RUN / BLOCKED.**

## 3. Owner's actual ChatGPT Project UI — required before manual-use readiness

- [ ] Install `PROJECT_INSTRUCTIONS.md` in a Project named `Friday — Peanuts`.
- [ ] Upload and confirm all five `.txt` reference files are visible in the Project source list.
- [ ] Run the exact smoke prompt in a new chat inside that Project.
- [ ] Verify that the Project distinguishes P1–P10 from B0–B10, uses Standard depth by default, states unknowns and does not claim script/validator execution.
- [ ] Save a compact status/handoff as a Project source if that action is available.
- [ ] Open a second fresh Project chat and test handoff recovery without invented state.
- [ ] Record date, visible plan/surface, source list, prompt, verbatim excerpt, deviations and outcome in `CHATGPT_PROJECT_UI_RUN_RECORD.md`.

**Current state: NOT RUN.** The assistant cannot inspect or operate the owner's iPad Project settings or source list from this conversation. Until this section is completed, do not call the route `READY_FOR_CHATGPT_MANUAL_USE`.

## 4. Remote and optional environments

- [ ] GitHub Actions / remote CI. **NOT RUN:** no owner-authorized remote repository was used.
- [ ] Codespaces / Dev Container. **NOT RUN.**
- [ ] Native ChatGPT Skills. **NOT RUN;** not required for the manual Project route and not assumed available on this account.
- [ ] Claude Code and Codex runtime checks. **NOT RUN;** filesystem simulation and malicious-archive checks pass, but actual CLI discovery/invocation/model fidelity remain untested.

## 5. Release decisions

Use one of these explicit dispositions; never collapse them into an unqualified “works everywhere” claim:

- `B10_CANDIDATE_PROJECT_UI_PENDING` — current disposition.
- `READY_FOR_CHATGPT_MANUAL_USE` — only after section 3 is completed with evidence.
- `READY_FOR_PRIVATE_UPLOAD` — only after owner review and repository/remote policy checks.
- `READY_FOR_CODESPACES_USE` — only after actual Codespaces checks.
- `BLOCKED` — if a critical failure is found.

Owner approval for publication remains separate from technical acceptance.
