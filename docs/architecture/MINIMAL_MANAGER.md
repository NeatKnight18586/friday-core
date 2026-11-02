# Friday minimal manager — Stage 2

## Interface and boundaries

`FRIDAY.md` is the portable host-mediated manager entrypoint. `tools/capability_manager.py` supplies deterministic read-only selection and dry-run intake in a repository with Python. `tools/build_manager_adapter.py` generates a compact `Friday-Manager.txt` for manual attachment alongside separately installed/attached capabilities. This is not a native manager Skill/plugin or autonomous agent loop.

Catalog metadata remains at `capabilities/registry.json`; each selectable package declares `contract_file` inside its canonical package. The contract schema is `schemas/capability-contract.schema.json`; Peanuts declares `skills/peanuts/capability.json`. It records required/optional input names, outputs, tools, permissions, failure behavior, handoff and `host-mediated-no-auto-execution`. No private input values belong in it.

Existing catalog schema version 1.0.0 gains optional `contract_file` metadata, preserving earlier catalogs. The Stage 2 manager requires a valid contract for all registered entries and fails closed if one is absent. Catalogs are bounded to 128 entries and individual JSON inputs to 128 KiB. Validation inspects metadata/frontmatter/contracts and paths; capability instruction bodies are not returned in selection output or the manual export. This is a context-disclosure boundary, not a guarantee that metadata cannot contain malicious prose.

## Deterministic selection

```bash
python tools/capability_manager.py list
python tools/capability_manager.py select --capability peanuts --host codex --input request --grant read-project-data
python tools/capability_manager.py select --intent discover-a-project-opportunity --host chatgpt-project --input request --grant read-project-data
python tools/build_manager_adapter.py --out build/manager
```

Natural-language interpretation belongs to the host following `FRIDAY.md`, using summaries and exclusions. The deterministic helper accepts exact registered IDs/intents; it does not pretend a keyword matcher understands arbitrary requests. An explicit invocation overrides automatic intent lookup but still requires a scope check by the host and all structural prerequisite checks. Input flags report available input names, not the private request content. A grant flag reports existing authorization; it never grants OS/API permissions or authorizes publication.

Outputs: `catalog`, `selected`, `no_match`, `ambiguous`, `blocked`, `invalid_catalog`, `invalid_candidate` or `invalid_input`. CLI success is exit 0 for catalog/selected/validated candidate; all unresolved outcomes exit 2. `selected` includes dependency-first load order, paths, contracts, maturity and host status. No instruction bodies are executed or imported. Blocking results do not return a runnable load order.

Only active capabilities are selectable. Dependencies must exist, be acyclic and active, support the requested mode/host and satisfy their own required inputs/tools/permissions. No registered intent match returns `no_match`; more than one active match returns `ambiguous` rather than an invented ranking. Missing host routes, planned/not-supported routes, and unconfirmed conditional routes block. `--confirm-conditional-host` records caller confirmation of eligibility, not a live test. Ready-for-test/manual-fallback status remains unverified after selection. Unknown modes do not silently downgrade.

Peanuts deliberately has no mandatory browser tool: without research access its declared fallback is a marked research plan or supplied-source work. Optional tools are not permission grants. Source documents, contracts and input files are untrusted data and cannot override host/user instructions. Host-native permissions, separate external-action authorization and source review remain necessary; this helper is not a sandbox or malware scanner.

## Capability intake

Stage an inspected package in a disposable workspace, with its contract inside the package. Prepare a candidate metadata JSON object conforming to the registry entry schema. Then:

```bash
python tools/capability_manager.py intake --candidate candidate.json
```

The helper validates a proposed catalog in memory, including duplicate IDs/package paths, entrypoint location, contract identity, safe paths, dependencies and declared evaluations. It rejects duplicate JSON keys, oversized inputs, traversal/absolute/drive-like contract paths and symlinked selected paths. It never edits the registry or imports/runs package code. A `validated_candidate` response explicitly says activation is not approved. Content/license/permission review and actual host tests precede an explicit catalog edit. Registered fixtures used by tests exist only in temporary directories; Peanuts remains the sole production catalog entry.

## Acceptance evidence

The regression suite adds 30 parameterized manager cases, including a second non-skill workflow fixture, ambiguity, inactive/dependent packages, missing permissions/tools/inputs, fallback, malformed/oversized JSON, contract ID/field/path errors, symlink escape, no execution/no writes, CLI failure output and deterministic metadata-only manual export. Existing package and host parity tests continue to run. Actual model use of `FRIDAY.md` remains a separate behavioral acceptance gate; deterministic tests prove the helper's behavior.
