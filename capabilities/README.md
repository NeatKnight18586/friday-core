# Friday Capability Registry

This directory contains Friday's lightweight, machine-readable catalog of capabilities that actually exist in the repository. It is **metadata, not an autonomous router**. Friday is initially the repository umbrella and shared governance layer; an active manager/control-plane runtime is an optional future decision that must be justified by observed coordination needs.

- `registry.json` records stable IDs, short summaries, capability kind, canonical package path, lifecycle/maturity, domains/intents, dependencies, operating modes, permissions, evaluation references, and host-adapter status.
- A skill capability may point to an Agent Skills `SKILL.md`. A non-skill harness, workflow, toolset, or agent package is not forced to invent a `SKILL.md`; it must have a documented entrypoint appropriate to its implementation before it is activated.
- The registry does not duplicate full descriptions, methodologies, or instructions. Canonical capability content stays in its own package and references.

## Adding a capability

1. Create a bounded, independently maintainable package under an appropriate source root (for example `skills/`, `harnesses/`, `workflows/`, `agents/`, or `toolsets/`). Do not create empty placeholders.
2. Define purpose, summary, scope/exclusions, stable ID, lifecycle/maturity, inputs/outputs, dependencies, permissions, failure behavior, resource modes, quality checks, and evaluation cases.
3. Provide a documented package `entrypoint` for every capability. If it is a native Agent Skill, also provide a valid `SKILL.md`; a non-skill package may use a README, workflow file, CLI entrypoint, or another appropriate documented entrypoint.
4. Add one compact registry entry. Dependencies must point to registered capabilities; avoid circular or unnecessary coupling.
5. Run `python tools/validate_capabilities.py`, `python tools/inspect_context.py`, and the complete verification suite.
6. Add evaluation cases for discovery, boundary, handoff, and task behavior. Keep the capability out of host auto-discovery unless the owner chooses a curated install profile.

## Growth policy

- Do not load or install every capability by default.
- Keep a small host-specific list of enabled capabilities; full content is loaded only after selection.
- If registry size becomes material, build a deterministic metadata filter/index before introducing an AI router.
- Consider a Friday manager only after real usage demonstrates repeated routing ambiguity, handoff friction, or policy coordination needs that simpler host-native discovery cannot solve.
- Preserve each capability's independence so it can be tested, packaged, or extracted without requiring the entire Friday repository.
