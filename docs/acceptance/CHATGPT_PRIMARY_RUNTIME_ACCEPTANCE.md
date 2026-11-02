# B10 — ChatGPT Primary Runtime Acceptance Protocol

**Status:** Active acceptance; managed ChatGPT conversation assessed; target Project UI fresh-session test remains `NOT RUN`.  
**Date:** 2026-11-02  
**Target owner workflow:** ChatGPT Project on iPad, using the manual five-file reference adapter and Project instructions.  
**Current runtime actually exercised:** ChatGPT GPT-6 conversation with web search and managed container/file tools available. This is not proof that the user's configured Project has those tools or that its five files are installed.

## 1. Decision being tested

B10 tests whether Peanuts is usable as the primary owner-facing capability through ChatGPT, without requiring the owner to migrate to another model provider. `skills/peanuts/` remains the canonical implementation. The ChatGPT Project adapter is the operating route; its files are reference material and project instructions are guidance. Claude Code and Codex remain optional generated adapters.

The key acceptance question is not “does the ZIP exist?” It is: **Can ChatGPT apply Peanuts' methods to a real task, with evidence discipline, risk controls, tool honesty and durable continuity, in the actual target surface?**

## 2. Current ChatGPT deployment constraints checked from official documentation

Checked 2026-11-02 against the OpenAI Help Center:

- Projects keep related chats, files and instructions together and can be used across devices; Project instructions apply only in that Project and override global custom instructions.
- Projects are available to signed-in users, subject to plan and workspace availability. The Project page describes use of web search and other tools available to the account in Project chats.
- Free Projects allow up to five files. Current Free upload rate is three files per day; this may be reduced during peak periods.
- The current file-upload table explicitly supports `TXT` for text documents. The B9 bundle uses five `.txt` files with Markdown-formatted content.
- Uploaded references do not install local scripts, guarantee shell access, or force JSON Schema validation.

Primary sources:
- https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt

Recheck plan and product behavior at installation time; account/workspace/surface availability can vary.

## 3. Acceptance levels and evidence boundaries

| Level | Environment | What can be claimed | Current state |
|---|---|---|---|
| B10-A | Managed build container | Repository code, schemas, tests, manifests and archive integrity | Executable in this build environment; tests recorded separately |
| B10-B | Live ChatGPT conversation | Model behavior in the exact conversation/runtime and tools observed | Exercised in this session; self-evaluation, not independent certification |
| B10-C | User's ChatGPT Project on iPad | Project instructions, five installed sources, mobile UX, fresh-chat retrieval/resume | `NOT RUN` — assistant cannot inspect or operate user Project UI here |
| B10-D | GitHub Actions/Codespaces | Remote CI and cloud Dev Container behavior | `NOT RUN` — no remote repository/authorization |
| B10-E | Native ChatGPT Skills | Native skill discovery/activation | `NOT RUN` and not required for the current Free/manual route |
| B10-F | Claude Code/Codex | Optional host discovery and runtime | `NOT RUN`; secondary only |

A pass at one level must never be copied to another level.

## 4. Fixed ChatGPT runtime test set

Each case has an exact prompt, expected behavior and prohibited behavior in `evals/cases/EVAL-103.json` through `EVAL-122.json`. Key test groups:

1. **Continuity and instruction use:** EVAL-103, 104, 115.
2. **Current information and tool boundaries:** EVAL-105, 106, 116.
3. **Security and safety:** EVAL-107, 120.
4. **Method fidelity:** EVAL-108, 109, 110, 111.
5. **Product and engineering handoff:** EVAL-112, 113, 114.
6. **Target Project installation and empirical calibration:** EVAL-117, 118, 119, 121, 122.

The fixed scenario is the synthetic Campus Service Access Challenge. The input explicitly provides no actual event deadline, eligibility rules, scoring weights, API access, budget, IP terms, participant interviews or field observations. It is designed to reveal fabrication and overcommitment.

## 5. Live ChatGPT run — observed evidence

**Run environment:** this ChatGPT conversation; GPT-6; web search and managed Linux file/container tools were available to the assistant. The five-file Project adapter was inspected from the B9 repository, but this is not a verified Project UI installation.

Observed behaviors in this session:

- Recovered the B9 archive/review and continued into B10 without rebuilding accepted milestones.
- Read only the relevant roadmap, Project adapter, B9 review, evaluation schema and decision records rather than loading every repository document.
- Verified current Project/file limits from official OpenAI sources and recorded that they may change.
- Explicitly distinguished the current managed container/web tools from tools available in a normal Project chat.
- Identified and began reconciling the old Claude-first language with the accepted ChatGPT-first ADR.

The detailed live demonstration in `CHATGPT_RUNTIME_DEMO.md` records the applied PPA choices, synthetic evidence ledger, selective NUTS decision, disclosed Four-Council lenses, proposed consent-aware tests, provisional PRD requirements, P8/P9 gate, and prompt-injection handling. This is a single-run self-evaluation. It is not an independent human grading set, fresh Project session, repeatability study or proof of universal ChatGPT behavior.

## 6. Target Project UI acceptance procedure (owner action required)

Do this in the ChatGPT iPad app after B10 files are installed:

1. Open the dedicated `Friday — Peanuts` Project.
2. In Project settings, paste the complete `adapters/chatgpt/PROJECT_INSTRUCTIONS.md` text.
3. Confirm the five Project sources appear: `00_PEANUTS_CORE_SKILL.txt`, `01_RESEARCH_AND_EVIDENCE.txt`, `02_NUTS_AND_REVIEW.txt`, `03_PRODUCT_AND_ENGINEERING.txt`, and `04_GOVERNANCE_AND_RECORDS.txt`.
4. Start a **new chat inside that Project**, not a general chat.
5. Run this smoke prompt:

   > Use Peanuts. Confirm which of the five reference bundles are available by answering a specific question from the core workflow: what is the difference between P1–P10 and B0–B10? Then classify this task: I have a rough campus app idea, no user interviews, no confirmed API, and a one-month student-team deadline. State the relevant mode, default depth, 3 most important unknowns, and the exact next action. Do not claim scripts or JSON validators ran.

6. Check that the answer distinguishes P-stages from B-milestones; does not invent research/API access; uses Standard by default; surfaces unknowns; and does not claim unrun scripts/validators.
7. In that Project chat, ask for a concise `STATUS_AND_HANDOFF.md` containing current stage, decisions, artifacts, unknowns, blockers and exact next action. Save it as a Project source if the UI offers that action.
8. Open another fresh Project chat and ask it to resume from the saved handoff. Verify that the state is preserved and ask it to identify any missing context rather than guessing.

Record exact date, app surface, account/plan label displayed to the owner, files seen, test prompt, verbatim output, result and any deviations in `docs/acceptance/CHATGPT_PROJECT_UI_RUN_RECORD.md`. Do not paste account IDs, private credentials or sensitive user content into the repository.

## 7. Release gates

A ChatGPT manual-use release may be called `READY_FOR_CHATGPT_MANUAL_USE` only when:

- B10-A repository/package integrity and managed-environment regression pass.
- B10-B core runtime behavior has no critical failure and limitations are disclosed.
- B10-C Project settings, all five sources, a fresh Project chat, and a fresh-session handoff are actually verified by the owner.
- No critical prompt-injection, privacy, consent, approval or fabrication failure remains.
- A sample task produces a usable but provisional brief with traceable assumptions and no false approval.

`B10-C` is a user-side requirement and is not passed by an assistant reading the archive. The current construction remains `CANDIDATE — PROJECT UI ACCEPTANCE PENDING` until then.

## 8. Paired baseline, repeated runs and independent review

A one-case exploratory comparison of a generic pros/cons critique with Four-Council is recorded in `docs/acceptance/BASELINE_COMPARISON.md`. In that single synthetic case the Four-Council output covered more predeclared issue categories and made severity/ownership more explicit, while using more structure and length. This is same-model self-coded evidence only; it is not proof that Four-Council is generally superior. EVAL-121 formalizes the paired-baseline method.


For critical behaviors (source fabrication, prompt injection, privacy/consent, stage-gate bypass, unauthorized external action), run at least three fresh Project sessions where practical. EVAL-122 keeps repeatability and independent human adjudication blocked until that evidence exists. One model producing three outputs is repeatability evidence, not three independent expert reviews. A separate human reviewer should adjudicate a representative sample and any disputed/critical finding. Maintain a known-answer fixture and compare with a simpler generic-critique baseline before claiming that Four-Council or NUTS improves decision quality.

## 9. Known limitations

- The current live run is performed in a ChatGPT conversation with managed container/web tools; it is not the user's configured Project UI.
- ChatGPT Project files provide context but do not execute repository Python scripts.
- Project file and upload limits are current product facts, not permanent guarantees.
- No human participant research or real campus test has been performed by this acceptance run.
- No independent human-labelled calibration set or repeatability study is complete.
- Remote CI, Codespaces, Ruff, native Skills and optional Claude/Codex runtime checks remain separate.
