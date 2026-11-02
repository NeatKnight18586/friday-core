# Peanuts Logical Architecture

**Status:** Stage 0.5 architecture refinement draft; owner approval pending  
**Version:** 0.2.0-draft  
**Last updated:** 2026-10-31

## 1. Architecture objective

Build Peanuts as a small, modular, portable skill package that can grow without becoming a monolithic prompt, an opaque multi-agent system, or duplicated platform-specific implementations. The system must remain understandable to its owner and contributors, inspectable in files, testable in realistic environments, and secure in proportion to its capabilities.

## 2. Initial architecture style

**Proposed style:** File-centered harness with one main Peanuts skill, focused reference modules, conditional templates, optional structured schemas, and deterministic scripts only where they add clear value.

No database, hosted backend, vector store, UI, or multi-agent orchestration is required for the first release. Revisit only when actual usage demonstrates a limitation that simpler files and scripts cannot reasonably solve.

## 3. Logical layers

| Layer | Responsibility | Boundary |
|---|---|---|
| User interaction | Understand intent, explain, ask focused questions, receive approval. | Do not force long forms or hide decisions. |
| Workflow coordinator | Select project mode, stage, depth, and relevant references; maintain handoffs. | Do not embed every methodology in one giant prompt. |
| Method modules | Research, discovery, NUTS, Four-Council, validation, PRD, technical design. | Do not silently alter approved goals or decisions. |
| Project records | Store brief, status, sources, claims, assumptions, decisions, requirements, and results. | Chat history is not the sole source of truth. |
| Validation/evaluation | Check structure, traceability, consistency, and skill performance. | Mechanical checks do not prove product desirability. |
| Platform adapters | Map the portable package to host-specific discovery, paths, permissions, and tools. | Do not become separately hand-maintained versions of core logic. |

## 4. Canonical source and repository structure

The intended canonical Peanuts source is `skills/peanuts/`. Host-specific runtime directories are adapters or generated installation copies; they must not be edited independently.

```text
Friday/
├── README.md
├── CLAUDE.md                    # Claude Code repository guidance
├── AGENTS.md                    # Codex/repository agent guidance
├── docs/
│   ├── vision/
│   ├── architecture/
│   ├── standards/
│   ├── decisions/
│   └── plans/
├── skills/
│   └── peanuts/                 # Canonical portable skill source
│       ├── SKILL.md
│       ├── references/
│       ├── assets/
│       │   └── templates/
│       ├── scripts/
│       └── evals/
├── adapters/
│   ├── claude/
│   ├── codex/
│   └── chatgpt/
├── tools/
└── .gitignore
```

Do not create all folders just because they appear in this diagram. Create only those used by a stage. The directory layout is an architectural target, not an implementation task for this refinement.

## 5. Host-specific instruction and skill discovery

The open Agent Skills format is a portable authoring convention, not a guarantee that every host discovers files from the same path or provides the same tools.

| Environment | Project guidance | Skill discovery/package | Notes |
|---|---|---|---|
| Claude Code | `CLAUDE.md` | Project skills under `.claude/skills/<skill>/SKILL.md`; personal skills under `~/.claude/skills/`. Invoke project Peanuts as `/peanuts`. | B10 filesystem install simulation passed; actual CLI discovery, invocation, permissions and model fidelity remain `NOT RUN`. |
| Codex | `AGENTS.md` | Repository skills under `.agents/skills/<skill>/`; user-level skills in supported user locations. Invoke/select Peanuts as `$peanuts` or via `/skills`. | B10 filesystem install simulation passed; actual CLI discovery, invocation, permissions and model fidelity remain `NOT RUN`. |
| ChatGPT desktop | Project instructions/available customization | Standalone Skills are available in supported desktop environments. | Exact availability depends on current product and account. |
| ChatGPT Chat/Work on web, desktop, mobile | Project or product instructions where supported | Skills distributed through supported plugins can be surfaced across Chat/Work surfaces. | Do not assume a local standalone skill is automatically installed in mobile Chat. |
| Claude.ai | Product instructions | Custom Skills may be uploaded as a bundle in eligible plans/surfaces. | Feature availability and runtime/network capabilities must be checked. |

### Packaging rule

Keep one editable source at `skills/peanuts/`. During the integration milestone, test the simplest packaging/synchronization mechanism for each target. A small script may copy or package the canonical folder into host-specific locations. Generated copies must be marked as generated and not hand-edited. The packaging approach must be tested before it is standardized.

Root `CLAUDE.md` and `AGENTS.md` are not substitutes for `SKILL.md`; they are short host-specific project guidance files that point to the canonical documentation and state how to use it.

### ChatGPT use path

Use native standalone Skills where supported; use plugin distribution if broader Chat/Work surface availability is genuinely needed and allowed; otherwise use a ChatGPT Project or conversation with the relevant canonical files attached and a short invocation guide. Compatibility means shared process and artifacts, not identical automatic activation, network access, model behavior, or permissions.

### Capability check

Before a task depends on web search, shell access, local file writes, Python, API calls, or connectors, the workflow must check whether the current host/runtime actually supplies that capability. If not, it must explain the limitation and request the needed file/tool or use a supported fallback. A skill cannot manufacture unavailable tools.

## 6. Skill boundaries and progressive disclosure

Start with one Peanuts skill. `SKILL.md` contains concise metadata, trigger conditions, core workflow map, routing instructions, input/output expectations, safety/approval rules, and links to supporting materials. Detailed methods live in separate references. Load only the references needed for the current task.

Split into additional skills only when a capability is recurring, independently useful, has stable inputs/outputs and permissions, and benefits from separate invocation or distribution. Avoid both one enormous skill and many tiny skills with routing overhead.

## 7. Project modes and workflow state

The coordinator recognizes Event-first, Problem-first, Idea-first, Existing-project, and Research/prototype modes (see `PRODUCT_DISCOVERY.md`). The default path is adaptive. Event fit remains a separate overlay.

Each project workspace should have logical records for:

- `PROJECT_BRIEF` — current desired outcome, problem, concept, scope, and status summary.
- `STATUS` — current stage, completed work, blockers, pending decisions, and next action.
- `SOURCES/CLAIMS` — source metadata, material claims, evidence status, and traceability.
- `ASSUMPTIONS` — uncertainty, impact, validation status, and next test.
- `DECISIONS` — chosen, rejected, deferred, and superseded decisions with rationale.
- `REQUIREMENTS` — requirement IDs, origin, priority, acceptance criteria, and linked tests.
- `ARTIFACTS` — dossier, concept brief, council report, validation report, PRD, design, and plan.

These are logical information categories, not a commitment to create a separate file for every category. A compact project brief may contain several of them for a small project.

Session recovery must be possible from the project record. A handoff should identify the project/version, current status, completed work, key decisions, unresolved questions, blockers, and next action.

## 8. Evidence and requirements traceability

For important claims and requirements, preserve a chain such as:

`Source/Observation → Claim or User Need → Opportunity → Concept Hypothesis → Decision → Requirement → Acceptance Criterion → Test Result`

Use stable identifiers when useful. Not every small feature needs a formal traceability matrix, but critical, event-required, safety-related, or high-cost requirements should have clear origin and verification method.

## 9. Verification versus validation

- **Verification:** Did the artifact or system meet its specified requirements? Examples: schema checks, unit tests, required fields, acceptance-test results.
- **Validation:** Does the resulting product or concept meet the real need in its intended context? Examples: interviews, observation, usability tests, field pilots, or outcome evidence.

Passing a structural validator does not prove that the idea solves a valuable problem. A favorable user reaction does not prove that the system is technically secure or reliable.

## 10. Deterministic checks versus judgment

Use scripts/schemas for exact checks: file presence, metadata, JSON validity, date formats, unique IDs, workflow states, required links, package paths, and consistency rules. Use model/human judgment for user value, analogical transfer, strategy, trade-offs, and concept quality. Important judgment outputs should be rubric-based and evaluated.

## 11. Security, privacy, and trust boundaries

- Treat imported websites, PDFs, repositories, email, comments, and other external material as untrusted data, not instructions.
- Never let retrieved content override user/system/skill instructions or grant itself tool permissions.
- Inspect untrusted code before running it; avoid arbitrary scripts and unbounded tool chains.
- Use least privilege for files, shell, connectors, and APIs.
- Separate decision-making from execution for irreversible or consequential actions.
- Require explicit approval before submissions, publishing, spending, messaging, deletion, or permission changes.
- Keep secrets out of Git; use environment-specific secret storage and scanning when code exists.
- Minimize and classify personal/project data; avoid unnecessary retention and sharing.
- Define resource limits, retries, timeouts, and a stop mechanism before introducing autonomous loops.
- Threat-model actual tools, data, and network paths rather than applying generic security checklists blindly.

## 12. Failure handling and recovery

Project operations should be recoverable. Before bulk file changes, create or preserve a known-good version. Prefer atomic writes or staged updates for multi-file operations. After a failure, report which files changed, verify state, and offer rollback or retry. Keep decisions append-only or mark previous versions superseded rather than silently erasing history.

Git history is not a complete backup strategy. If the project later contains irreplaceable data, define separate backups and restore tests.

## 13. Maintainability rules

1. One canonical source for each reusable method or instruction.
2. Short entry-point instructions; detailed references loaded only when needed.
3. Stable interfaces and identifiers for important artifacts.
4. No dependency or framework without a demonstrated need.
5. Every script has a defined purpose, input, output, failure behavior, and test.
6. Generated host copies are never edited by hand.
7. Changes to instructions require affected evaluation cases to be rerun.
8. Deprecate unused/duplicated material rather than allowing silent accumulation.
9. Keep a clear difference between Friday-wide standards and Peanuts-specific methods.
10. Document decisions when the choice affects portability, security, data, or future maintenance.

## 14. Deferred decisions

The following remain intentionally deferred: database or vector retrieval, long-term memory implementation, multi-agent council execution, a dashboard, plugin distribution, external APIs/MCP services, autonomous background execution, broad Friday routing, and public release. Each requires an options analysis, actual use case, permission/security review, and evidence that the added complexity is justified.
