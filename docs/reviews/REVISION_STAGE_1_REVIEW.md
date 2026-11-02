# Stage 1 — Verified baseline and product alignment

**Checkpoint:** 0.14.1-rc.1, 2026-11-02. **Scope:** baseline repairs and documentation alignment, not manager implementation. **Decision authority:** ADR-046–048 in [current decisions](../architecture/DECISIONS.md).

## Changes

- Fixed the 21 baseline Ruff findings in thirteen files. Unused imports/f-strings were removed; third-party imports moved before path bootstrap; local imports that require the direct-script path setup carry narrow E402 annotations, consistent with existing repository scripts. Lint configuration and test assertions were not weakened.
- Aligned README, release/iPad guides, vision, architecture, routing design, host maps, roadmap and relevant adapter instructions with the intended public, provider-neutral manager. Documented the currently implemented catalog/prototype separately from the planned selector.
- Made `docs/architecture/DECISIONS.md` authoritative and retained `docs/DECISIONS.md` as a marked historical Stage 0 archive. Corrected the audit: the latter file exists; overlapping IDs and conflicting authority were the problem.
- Recorded bounded optional profile import as planned, with explicit user review/provenance/private storage boundaries. No memory ingestion or new permission grant was added.
- Preserved old evaluation records and historical milestone rationale without reinterpreting their results as new runtime evidence. Added the sequential [revision plan](../plans/REVISION_STAGES.md).
- Regenerated affected repository-local host snapshots and companion upload packages from canonical sources; refreshed version, changelog and source manifest.

## Acceptance evidence

The complete verifier passed all 13 validator steps, Ruff and 196 tests on managed Linux/Python 3.12.14. See [release verification](../../RELEASE_VERIFICATION.md) for commands and exclusions. External delivery evidence records the final source/archive runs and checksums. Existing tests cover package/direct-script behavior; no new tests were added solely to check documentation wording or removed imports.

The first audit undercounted Ruff findings as nine from truncated output; the full baseline diagnostics and fresh lint run establish 21. The Stage 1 package fixes the full set. No prior failure was reclassified as a pass.

## Residual limits

No real target-host invocation, authenticated consumer setup, configured Project recovery, remote CI, non-Linux run, method-effectiveness pilot or measured token saving was established. License/rights selection and public publication remain pending. Heuristic privacy scanning is not a complete privacy guarantee.

## Stage 2 handoff

Next scope: minimal explicit capability selector and capability intake checks. Start from `capabilities/registry.json`, its schema/validator and canonical entrypoints. Preserve current Peanuts behavior and direct host invocation. Define required inputs/outputs and permission/dependency/failure behavior before broad edits. Use a disposable second fixture to prove extension without registering an invented production capability.

Acceptance: explicit invocation respected; relevant capability selected; no-match/ambiguity handled; inactive or invalid packages refused; dependency/permission issues surfaced; selected content loaded selectively; no arbitrary imported code execution or autonomous loop. Keep host execution claims limited to actual evidence. Stage 2 is planned, not delivered here.
