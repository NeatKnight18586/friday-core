# Stage 2 — Minimal manager and early integration checks

**Checkpoint:** 0.15.0-rc.1, 2026-11-02. **Scope:** explicit host-mediated selection/intake plus CI/host preflight requested by the owner. Stages 3–6 remain planned.

## Implemented

- `FRIDAY.md` gives a portable manager procedure; the generated `Friday-Manager.txt` supports manual chat attachment alongside separately installed/attached capability resources.
- `tools/capability_manager.py` lists validated metadata, selects by explicit ID or exact declared intent, handles no-match/ambiguity, and gates active lifecycle, dependencies, host/mode, inputs, tools and caller-reported permissions. It never imports/executes capability code or writes the catalog.
- `capability.json` contracts define bounded inputs/outputs, prerequisites, fallback and handoff. A new schema and optional registry `contract_file` preserve older registry compatibility while manager selection requires valid contracts. Peanuts is the only real registered package; temporary tests supply a second non-skill workflow.
- Dry-run intake checks a proposed metadata entry against the catalog and existing staged package; validated structure is explicitly not approval, registration, trust or host acceptance. Source/rights/permission review remains separate.
- Added 30 manager regression cases. The complete suite now contains 226 tests, and the verifier includes 14 validator steps. Existing test rules, assertions and dependency pins are retained. Clean wheel resolution exposed the missing transitive typing_extensions pin; the resolved version is now pinned as well.
- Updated host guidance, current product/release docs and decisions (ADR-049/050); regenerated canonical host/consumer distributions.

## Early CI/host evidence

At the owner's request, integration-risk checks were pulled forward from Stage 4. See [preflight method](../acceptance/CI_AND_HOST_PREFLIGHT.md). An actual read-only Codex CLI invocation was attempted; the token could not refresh and no model turn completed. The result is BLOCKED, not a Peanuts method pass or failure. Claude Code/account UI is unavailable.

Workflow actionlint passes and both action commit pins exist upstream. Docker can launch clean Python environments. The delivery's machine-readable results and logs record the actual final clean-container Python matrix outcomes, source ZIP hash and resolved image digests. These are Linux test environments, not GitHub-hosted, macOS/Windows, Claude or iPad passes.

Read-only account inspection found an existing public Friday repository with no Actions runs and only root files plus the source ZIP, lacking extracted nested source/workflow directories. It also found an owner-authored MIT license, preserved verbatim in this checkpoint. This checkpoint is prepared locally; no source push, remote repository creation, paid service or publication occurred. Actual GitHub Actions success requires a reviewed commit to run there.

## Acceptance and limits

The first complete local Stage 2 verification run passed all 226 tests, 14 validators and Ruff. Final source/archive evidence accompanies the checkpoint kit. The new tests cover extension without manager code changes, dependency order, prerequisite gates, no execution/no writes, metadata-only export, malformed/oversized/duplicate JSON, invalid identity/paths, symlink escape, inactive packages and ambiguous/no-match behavior. These are deterministic helper tests; real model obedience, research quality, consumer retrieval and comparative usefulness remain separate.

No autonomous loop, native manager plugin, automatic package installation, account synchronization, profile memory importer or new production capability was introduced. Manager permissions are declarative/caller-reported; OS/API enforcement and external-action authorization remain the host's responsibility. Source review and safe runtime permissions are still necessary.

## Stage 3 handoff

Next scope: simplify Peanuts' compulsory context, introduce Fast naming without breaking `quick`, and finalize a readable Project Dossier plus compact portable handoff. Preserve source provenance, unknowns, conditional event constraints and honest demo claims. Validate Fast/Standard/Deep examples, missing-research fallback and downstream fresh-session continuity. Do not refactor manager/packaging without a concrete need. Continue to label actual host/remote CI blockers explicitly.


## Clean-container harness recovery

The first container attempts could not read a restrictive host-mounted archive; the harness was changed to transfer source through stdin with no host filesystem mounts. Direct container dependency downloads then hit this environment's untrusted-intermediary TLS certificate. TLS verification was not disabled. The recovery downloads version-specific wheels through the host's functioning verified package connection, records their SHA-256 hashes, transfers them with the source, and installs inside network-disabled containers using `--no-index`. This checks clean dependency installation and execution, not container network/TLS configuration or GitHub's package index connectivity. Initial failures are preserved separately from final results.
