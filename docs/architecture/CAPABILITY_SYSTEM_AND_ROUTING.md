# Friday Capability System and Routing Architecture

**Status:** B6.5 design baseline; capability catalog implemented; autonomous manager intentionally deferred  
**Version:** 0.2.0-draft  
**Last reviewed:** 2026-11-02

## 1. Friday's role

Friday is intended to manage reusable capabilities for public users across supported hosts. Today it provides the **repository umbrella and shared governance foundation**, a metadata catalog and generated host packages. Stage 2 implements a read-only explicit selector/intake helper and FRIDAY.md host-mediated instructions under ADR-049. See `MINIMAL_MANAGER.md`; this is not an autonomous executor.

The selector should identify intent, check scope and prerequisites, select the smallest capability set, preserve permission boundaries and pass compact handoffs. It should explain no-match/ambiguity and avoid recursive delegation. Host-native discovery remains a valid route. Autonomous coordination and a hosted memory service remain deferred.

The following catalog and interface contracts are implemented groundwork; selection is tested deterministically and host/model behavior requires separate tests.

## 2. Friday versus a capability

| Element | Responsibility | Example |
|---|---|---|
| Friday capability manager | Today: repository, standards and catalog. Stage 2: read-only selector and intake checks. | Helper implemented; actual host/model behavior unverified |
| Capability | A bounded reusable job with its own methods, inputs, outputs and evaluations | Peanuts |
| Skill package | Portable instructions/resources used by a compatible agent host | `skills/peanuts/SKILL.md` and supporting files |
| Harness | A workflow plus records, tools, validation, state and evaluation that makes a capability repeatable | Peanuts as a project-planning harness |
| Tool | A specific operation or integration | Search, file parser, schema validator, issue tracker connector |
| Project workspace | Project-specific state and evidence | A hackathon project folder under ignored `local-workspace/` |

A capability may be packaged as a skill, harness, workflow, toolset, or future agent. Do not assume every capability needs a separate agent or model.

## 3. Catalog and source of truth

`capabilities/registry.json` is a compact catalog of actual repository capabilities. It stores metadata and canonical paths; it is not an always-loaded prompt or an autonomous router. When the catalog grows, filter/query metadata before loading any capability body.

For an Agent Skill, its `SKILL.md` is the source of truth for skill name, description, and portable operating instructions. A non-skill harness, workflow, agent, or toolset may use a different documented entrypoint; do not force it to add a meaningless `SKILL.md`. Every registry entry must point to a real canonical package and an existing documented entrypoint within that package. A skill entrypoint may be `SKILL.md`; a non-skill harness or toolset may use a README, workflow definition, CLI entrypoint, or another appropriate file. Do not register speculative placeholder capabilities. A future capability should have a bounded charter and minimum usable package before it is marked active.

## 4. Capability interface contract

Before activation or composition, a capability should declare:

- Stable ID, summary, kind, lifecycle, maturity, canonical package path and documented entrypoint.
- Purpose, supported intents/domains, and explicit exclusions.
- Required/optional inputs and prerequisites.
- Expected output artifacts/record types and stable identifiers.
- References/methods it may load and dependencies on other capabilities.
- Supported resource modes and resource profile.
- Tools required, optional, or unavailable; permissions and data sensitivity.
- Failure conditions, fallback behavior, and escalation requirements.
- Quality checks, evaluation cases, owner, version and review date.

The contract should be concise and proportionate. A small skill does not need an elaborate API specification, but its boundaries must be clear enough that another capability can consume its output without guessing.

## 5. Routing policy (Stage 2 host-mediated selector)

1. Honor explicit user invocation unless unsafe, impossible, or out of scope.
2. Classify the requested outcome, not merely keywords or topic nouns.
3. Select the smallest set of capabilities that can complete the task. Start with one primary capability; add a supporting capability only for a declared need.
4. If no capability fits, answer directly or explain the gap. Never force an unrelated skill.
5. If two capabilities appear equally appropriate and the distinction changes the outcome, ask one focused clarification. Otherwise select the lower-risk default and state it.
6. Check prerequisites, access, permissions, cost/usage, and data sensitivity before tool use.
7. Load only the selected capability's instructions and task-relevant references.
8. Pass a declared output artifact or compact handoff between capabilities; do not dump entire histories by default.
9. Avoid recursive routing, uncontrolled delegation, or parallel agents unless a measured benefit justifies the overhead and the user has authorized the scope.
10. Preserve the user's authority over consequential choices and external actions.

## 6. Composition and dependency rules

- Capabilities should be independently useful where practical.
- Reuse shared records, schemas, standards, and tools rather than copying them.
- Prefer one-way handoffs over circular dependencies.
- A dependency must identify why it is required and what happens if it is unavailable.
- A capability must not silently change another capability's approved outputs or decisions.
- Avoid hidden coupling through shared prompt text or undocumented file paths.
- If two capabilities duplicate the same job, consolidate or define distinct boundaries before both become active.

## 7. Growth and installation profiles

Friday should not automatically install or activate every capability merely because it exists in the repository. For now, treat the catalog as a source of truth for people and compatible hosts; it is not an always-loaded prompt. When the catalog grows, a future manager or helper should query/filter metadata and return only a small set of candidates rather than injecting the complete catalog and all capability instructions into every request. For a small library, direct skill discovery can be convenient; as the library grows, host-injected metadata and active skill lists can consume context and create routing collisions.

At B9, test host-specific profiles such as:

- **Single capability:** install only the capability needed for a focused environment.
- **Curated set:** install Friday's manager plus a small set of frequently used capabilities.
- **Catalog/on-demand:** keep additional capability packages in the repository and let a manager load a selected package where the host supports filesystem access and the security model permits it.

These are design options, not yet implemented installation modes. The best route may differ by Claude Code, Codex, ChatGPT, or other hosts. Verify actual discovery behavior and metadata budgets for each host.

## 8. Capability lifecycle

Use these lifecycle states:

- `planned`: approved for investigation but not available for invocation.
- `active`: source package exists and may be selected subject to host support.
- `deprecated`: supported only for migration/legacy work; replacement is documented.
- `retired`: no longer offered; historical records remain.

Keep lifecycle separate from maturity (`experimental`, `prototype`, `validated`, `production`). An active prototype is not a production capability.

## 9. Decision gate before autonomous coordination

ADR-049 implements the minimal read-only selector for Stage 2; see `MINIMAL_MANAGER.md`. Do not expand to an autonomous Friday manager until real use demonstrates a recurring need. Evidence may include repeated capability ambiguity, costly manual handoffs, duplicated context, permission conflicts, or repeated user effort when coordinating two or more stable capabilities. Before building, compare: (a) simple host-native skill discovery, (b) a curated install set plus a small catalog, and (c) a custom manager. Select the lowest-complexity option that meets observed needs. Require a small prototype, realistic routing evaluation cases, permission model, failure/recovery behavior, and measured benefit before promoting it beyond experimental status.

## 10. Manager maturity ladder and evidence gate

Do not jump from a repository catalog directly to an autonomous manager. Use the lowest-complexity level that solves observed needs:

0. **Repository umbrella:** a human navigates packages and invokes host-native skills. This is Friday's current state.
1. **Curated activation:** a small owner-selected set of capabilities is installed/enabled for a particular host or project.
2. **Deterministic catalog helper:** a script filters registry metadata by declared domains, intents, or dependencies and returns a short candidate list. It does not make autonomous decisions.
3. **Assisted selector:** an AI may recommend a capability from a bounded catalog summary; the user or host confirms consequential selection and handoffs.
4. **Bounded manager:** a runtime coordinates a small, tested number of capabilities with explicit state, permission checks, handoff schemas, recovery, and action logs.
5. **Agentic orchestration:** delegation or parallel agents are considered only if controlled evaluations show material quality or throughput improvement after accounting for context, token/API cost, latency, coordination errors, and maintenance.

Before moving upward, record actual usage incidents: task type, capabilities involved, manual steps repeated, ambiguity or routing error, context duplication, handoff failure, permission friction, impact, and whether a simpler change would solve it. Do not use arbitrary task-count thresholds as universal proof. A manager decision must cite representative use cases and a comparative prototype/evaluation.

A future manager may be a deterministic helper, an assisted workflow, or a model-backed agent. Do not assume it must be autonomous.

## 11. What is intentionally not built yet

B6.5 does not implement autonomous routing, subagent orchestration, a dynamic plugin marketplace, a vector database, or a multi-agent manager. The current capability validator checks catalog consistency. Actual routing and host execution are future runtime work and must be evaluated before being claimed.
