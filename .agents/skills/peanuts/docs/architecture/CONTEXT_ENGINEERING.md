# Friday Context Engineering and Progressive Disclosure

**Status:** B6.5 design baseline; host behavior still requires runtime verification  
**Version:** 0.2.0-draft  
**Last reviewed:** 2026-11-01

## 1. Purpose

Context engineering is the deliberate selection, organization, and timing of information supplied to an AI system for a task. Friday should provide the smallest sufficient context that preserves the required quality, evidence, safety, and decision standards.

This is not a promise of a fixed token reduction. Tokenization, hidden system context, tool output, caching, context windows, and billing differ by model and host. Friday can control the content it owns; it cannot universally control provider-managed context or subscription credits in consumer interfaces.

## 2. Progressive-disclosure model

Use four content levels. Hosts may implement these levels differently; adapters must be tested rather than assumed equivalent.

| Level | Content | Loading rule |
|---|---|---|
| 0 — Map | Short host instructions, capability catalog/metadata, safety rules | Keep small and stable; point to sources of truth. |
| 1 — Capability | One selected capability's `SKILL.md` | Load only after the task matches or the user explicitly invokes it. |
| 2 — Method/reference | Relevant method guide, schema, rubric, policy, or template | Retrieve only the references needed for the current stage or decision. |
| 3 — Evidence/data/execution | Specific source passages, project records, datasets, or script results | Retrieve narrowly; run deterministic scripts instead of reading source code when possible; return concise, traceable outputs. |

Never load the entire `docs/`, every capability, all project records, or every evaluation case by default.

## 3. Retrieval sequence

1. Understand the user's requested outcome and explicit mode.
2. Read the short host entry point already supplied by the runtime.
3. Consult the capability catalog only when routing or capability boundaries matter.
4. Select one primary capability. Add a supporting capability only when there is a clear dependency.
5. Load that capability's `SKILL.md`.
6. Read its current project handoff/state before broad project history.
7. Follow only the references required by the selected task and stage.
8. Retrieve source passages or records only for material claims/decisions.
9. Run deterministic tools when they replace repetitive inspection or exact checking; return concise output plus file/record references.
10. Before finishing, update the compact project state/handoff if the work is file-enabled.

If a required reference or source is missing, state the gap. Do not infer its contents from a filename or old summary.

## 4. Source-of-truth and duplication rules

- Full professional methods and governance standards live under `docs/`.
- A capability's `SKILL.md` is its concise operational entry point.
- Files under `skills/<capability>/references/` are runtime-oriented guides. They must identify their canonical source when they summarize or adapt a repository method.
- Do not independently maintain multiple full copies of the same method. If a runtime bundle needs a self-contained copy, generate/review it from the canonical source during packaging and test for drift.
- Host-specific `CLAUDE.md`, `AGENTS.md`, or adapter files are maps and host behavior; they are not parallel copies of the capability's methodology.
- Project state and decision records are the source of truth for that project; chat history is context, not the only record.

## 5. Context prioritization

When context is constrained, prioritize in this order:

1. Applicable safety, permissions, and user instructions.
2. The current task and required output.
3. Current project state, approved decisions, and blockers.
4. Selected capability instructions and mandatory method prerequisites.
5. Evidence directly bearing on the decision.
6. Supporting examples and optional background.

Do not drop mandatory evidence or safety checks merely to fit a smaller context. Reduce unrelated background, summarize with source/record references, or split work into a resumable stage.

## 6. Summarization and compaction

A project summary must preserve, at minimum:

- Project ID and version/date.
- Desired outcome and current framing.
- Current workflow stage and lifecycle status.
- Approved decisions (with IDs and rationale/source references).
- Important findings and evidence status.
- Open assumptions, unknowns, counterevidence, and blockers.
- Completed work and artifacts (with paths/IDs).
- Exact next useful action.

A summary is not a replacement for the underlying source or record. Link to it. Do not compress away uncertainty, contradictory evidence, consent restrictions, critical risks, or decision provenance.

Use `templates/session/SESSION_HANDOFF.md` as the canonical handoff structure. Project-level `STATUS_AND_HANDOFF.md` remains the user's concise project snapshot.

## 7. Scripts and deterministic processing

Prefer a small deterministic script for exact, repeatable tasks such as schema validation, duplicate detection, indexing, filtering, counting, file generation, and traceability checks. The model should receive concise results and relevant IDs, not thousands of raw rows or the full script source unless debugging requires it.

Scripts must:

- Have a narrow documented purpose and explicit inputs/outputs.
- Avoid network access unless specifically required and reviewed.
- Avoid destructive writes by default; use dry-run/confirmation for consequential actions.
- Handle malformed input and report errors clearly.
- Be tested and included in the repository's quality checks.
- Avoid sending private project data to external services without explicit authorization.

## 8. Token and resource measurement

Do not estimate exact provider tokens from character counts or word counts. `tools/inspect_context.py` reports characters/words as maintainability proxies only; it is not a tokenizer or usage meter.

Record exact input/output/cached token usage only when the host or API actually exposes it. Otherwise report `not_available`; do not manufacture estimates. Compare usage within the same provider/model/task setup where possible. Cross-provider token counts are not directly comparable without tokenizer and measurement normalization.

See `docs/governance/RESOURCE_BUDGETS.md` and `docs/governance/CONTEXT_EVALUATION.md`.

## 9. Context efficiency acceptance principles

- Relevant context is retrieved; irrelevant context is not loaded by default.
- Required evidence, prerequisites, and safety rules remain available.
- A compact handoff allows a fresh session to resume without replaying the entire conversation.
- Lower-context operation does not silently lower output quality or confidence standards.
- Resource use is measured where available and otherwise explicitly unmeasured.
- Context architecture is reviewed as capabilities are added; metadata and automatic skill lists must not grow without bound.

## 10. Capability growth without context/catalog bloat

- The current `capabilities/registry.json` is a compact source-of-truth catalog, not an instruction file and not an autonomous router. Do not paste the full registry into every conversation as Friday grows.
- A host should discover only the capabilities installed or enabled for that environment. Use curated profiles when host skill metadata is injected into context; do not install every experimental package by default.
- A future manager may query/filter registry metadata and return a small candidate set. It must not load every capability's `SKILL.md` to decide which one is relevant. This manager is optional and should be built only if actual coordination friction justifies it.
- Keep each capability independent. A capability's full method library remains in its package/docs; Friday's shared map contains only concise metadata and canonical paths.
- Avoid duplicate copies of canonical methods. Runtime-specific copies should be generated or packaged from the source and checked for drift.
- If the catalog becomes large enough that manual metadata review is error-prone, add a deterministic index/query utility before adding an AI router.

## 11. References

- Anthropic, Agent Skills overview, especially progressive disclosure and skill structure: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- OpenAI, Harness engineering: leveraging Codex in an agent-first world (2026-02-11): https://openai.com/index/harness-engineering/
- OpenAI, Skills guide: https://developers.openai.com/api/docs/guides/tools-skills
- VS Code, Agent Skills: https://code.visualstudio.com/docs/agent-customization/agent-skills

These platform documents describe their own products. Friday's portable rules are design principles; exact host discovery, skill budgets, and runtime behavior must be verified in the chosen environment at B9/B10.


## 12. Host metadata and capability growth

The portable catalog is not automatically injected wholesale into every host conversation. Host skill discovery may expose names and descriptions before a skill body is loaded; this metadata has a host-specific context cost. At B9/B10, compare direct installation of all skills with curated installation and catalog/on-demand approaches on each supported host. Prefer a small enabled set for routine work. Do not assume host metadata is free or that discovery behavior matches another host.

Friday's possible manager should start at the lowest maturity level in `CAPABILITY_SYSTEM_AND_ROUTING.md`: repository umbrella, curated activation, deterministic catalog helper, assisted selector, bounded manager, then agentic orchestration only if measured. This preserves future growth without making today's architecture depend on a manager that may never be necessary.
