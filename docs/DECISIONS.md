# Historical Architecture Decision Records — Stage 0

**Document status:** Historical archive; superseded as current decision authority  
**Version:** 0.1.0-draft  
**Date:** 2026-10-31

Current decisions are maintained in [docs/architecture/DECISIONS.md](architecture/DECISIONS.md), especially ADR-046–048. IDs in this Stage 0 archive are local historical IDs and must not be treated as current approvals.

This file records the original decisions that shaped Peanuts and Friday. A decision is not final merely because it appears here: its status must be explicit. Future decisions should be added as separate ADR files when the repository grows.

## ADR-001 — Friday is the repository; Peanuts is the first capability

**Status:** Proposed  
**Decision:** Use `Friday` as the repository/home for the growing system and `Peanuts` as its first specialized capability.  
**Context:** The long-term goal is a personal AI environment with multiple reusable skills and tools. Peanuts should be useful independently before it is integrated into a broader Friday assistant.  
**Consequences:** Repository-wide principles belong outside Peanuts; Peanuts-specific procedures belong inside its skill package. Peanuts must remain portable and extractable.

## ADR-002 — Claude-first, portable-core architecture

**Status:** Superseded for the owner-facing workflow by ADR-015; retained as a portable-host design option  
**Decision:** Develop and test Peanuts first in Claude Code while authoring its core around the open Agent Skills format and avoiding vendor-specific assumptions in core instructions.  
**Context:** Claude is the preferred primary environment, but the owner also wants to use ChatGPT.  
**Consequences:** Use host-specific adapters and packaging rather than maintaining duplicate core skills. Compatibility means shared procedure and artifacts, not identical runtime behavior. Reassess exact packaging and install paths during integration.

## ADR-003 — ChatGPT compatibility must have a fallback path

**Status:** Proposed  
**Decision:** Support native Skills/Codex/plugin routes where available, but also maintain a manual route using the canonical Markdown files in a ChatGPT Project or conversation where file/project features are supported.  
**Context:** OpenAI documents different availability across standalone Skills, plugins, Chat, Work, desktop, web, and mobile. Account and workspace entitlements vary.  
**Consequences:** Never promise universal native installation. Confirm current account and surface support before selecting an installation route.

## ADR-004 — Start with one Peanuts skill

**Status:** Proposed  
**Decision:** Start with one main skill and modular reference files, templates, schemas, scripts, and evaluations. Split into additional skills only when a distinct capability has stable boundaries and a demonstrated need for independent invocation or distribution.  
**Context:** Over-fragmentation creates maintenance and context-routing overhead; one huge skill creates context bloat.  
**Consequences:** Apply progressive disclosure and keep the entry point navigational.

## ADR-005 — Use an adaptive staged workflow

**Status:** Proposed  
**Decision:** Use the ten-stage lifecycle in the Constitution as a flexible process, scaling depth to complexity, risk, deadline, uncertainty, and cost of error.  
**Context:** Event and project planning ranges from small ideas to complex products. A rigid process creates bureaucracy; an unstructured process skips important checks.  
**Consequences:** Allow justified skips and loops, but record why important stages were skipped. Keep gates for event constraints, concept approval, critical risks, validation disposition, and PRD approval.

## ADR-006 — NUTS is an experimental Peanuts method

**Status:** Proposed  
**Decision:** Use “Nothing New Under the Sun” as the guiding philosophy for cross-domain inspiration and recombination. Treat the formal NUTS procedure as experimental until evaluated.  
**Context:** The owner wants a systematic method inspired by creative recombination, biomimicry, history, and engineering analogies.  
**Consequences:** Create source-backed Analogy Cards; abstract mechanisms rather than copy surface features; record transfer limitations and attribution; test whether the method produces useful concepts. Do not claim legal originality.

## ADR-007 — Four-Council review is a structured critique, not a proven universal standard

**Status:** Proposed  
**Decision:** Use four review lenses: Human Value, Strategic Innovation, Technical Feasibility, and Red-Team/Delivery. Use 1–5 scores only with an explicit rubric and separate confidence; allow Unknown/Not assessed. Do not blindly average unlike dimensions.  
**Context:** The user wants a repeatable, critical decision process. No universal validated four-council framework has been established for all product and hackathon ideas.  
**Consequences:** Treat the method as a Peanuts hypothesis. Test it on strong, weak, infeasible, low-value, and non-compliant concepts. A single model simulating four perspectives must not be described as four independent reviewers.

## ADR-008 — Validate critical assumptions before finalizing the PRD

**Status:** Proposed  
**Decision:** Include a validation disposition before the PRD becomes the approved product baseline.  
**Context:** A polished PRD can formalize incorrect assumptions. Research, interviews, prototypes, technical spikes, and experiments provide different kinds of evidence.  
**Consequences:** Unvalidated assumptions must remain visible. Time-constrained projects may proceed provisionally, but the accepted uncertainty and reason must be recorded.

## ADR-009 — Separate product requirements from technical design

**Status:** Proposed  
**Decision:** Maintain a PRD for what/why and a separate Technical Design for how. A Build Plan translates the design into execution steps.  
**Context:** Mixing product needs with implementation choices makes it harder to change technology without losing the user's underlying requirements.  
**Consequences:** Maintain traceability from user/event evidence to product requirements, acceptance criteria, technical decisions, and tests.

## ADR-010 — Project artifacts are the durable source of truth

**Status:** Proposed  
**Decision:** Store approved project state, decisions, sources, assumptions, requirements, and next actions in versioned project artifacts rather than relying on conversation history.  
**Context:** Multi-prompt work must survive session endings and context loss.  
**Consequences:** Stage 2 defines the schemas and templates. Every handoff must identify completed work, pending work, blockers, decisions, and the next action.

## ADR-011 — Human approval for consequential actions

**Status:** Proposed  
**Decision:** The user approves important project decisions and all consequential external actions. Deterministic checks should enforce important technical constraints where feasible; prompt instructions alone are not a security boundary.  
**Context:** The user wants collaboration and control. AI instructions can be misunderstood or ignored, and external actions may have irreversible consequences.  
**Consequences:** Later implementation must define permission boundaries and approval records. No autonomous submission, publication, spending, messaging, deletion, or permission change by default.

## ADR-012 — No infrastructure without demonstrated need

**Status:** Proposed  
**Decision:** Begin with Markdown, Git, the skill format, and small deterministic scripts only when useful. Defer databases, vector memory, custom backends, multi-agent orchestration, and dashboards.  
**Context:** Premature infrastructure makes a beginner project harder to understand and maintain.  
**Consequences:** Revisit only when actual usage exposes limitations that simpler tools cannot reasonably solve.

## ADR-013 — Method evidence and method maturity must be recorded separately

**Status:** Proposed  
**Decision:** Record what kind of evidence supports a method and separately record whether Peanuts has tested and adopted it.  
**Context:** An official standard, empirical study, practitioner framework, and internal experiment support different kinds of claims.  
**Consequences:** Do not use a single “proven” label. Use the evidence taxonomy and lifecycle in `METHOD_GOVERNANCE.md`.

## ADR-014 — Keep private context out of the shared repository

**Status:** Proposed  
**Decision:** Keep personal memory, secrets, tokens, private source material, and sensitive project data outside the shareable core. Default the GitHub repository to private until the owner deliberately approves publication and licensing.  
**Context:** Friday may eventually contain personal context and tools. A repository may later be shared or made public.  
**Consequences:** Separate public/reusable system instructions from private user profile and project workspaces; use `.gitignore` and secret-management practices when code is added.


## ADR-015 — ChatGPT-first owner workflow with a portable core

**Status:** Accepted for the current build and owner workflow (2026-11-02)  
**Decision:** Use ChatGPT Projects as the primary owner-facing environment for completing, operating, and maintaining Peanuts/Friday where the current account and product surface support the needed work. Keep `skills/peanuts/` as the single canonical portable implementation. Use the five-file manual Project adapter and separate Project instructions on the current Free/iPad route. Keep Claude Code and Codex as generated, optional coding-host adapters rather than mandatory dependencies.  
**Context:** The owner explicitly wants to complete and use Peanuts/Friday in ChatGPT. Requiring migration to another provider would reduce accessibility and continuity. At the same time, Project instructions and uploaded text references do not execute repository scripts or guarantee shell access; quality must not be preserved by pretending that unavailable deterministic checks ran.  
**Consequences:** Design the ChatGPT route around progressive disclosure, clear tool-availability checks, durable handoffs, actual evidence, and explicit `NOT RUN` reporting. Perform deterministic repository tests in an environment that demonstrably exposes the needed filesystem/shell tools (including the managed build environment used during construction). Keep portable packages generated from canonical sources. Do not add a custom API service, autonomous Friday manager, or duplicate implementation merely to simulate capabilities the ChatGPT surface does not provide. Reassess native Skills only when the owner's account, workspace, and product surface are verified eligible.
