# Release verification — Friday 0.17.0-rc.1

**Classification:** `STAGE_4_EVALUATION_CHECKPOINT` — behavioral comparison infrastructure; real-model gate open.
**Date:** 2026-11-02. **Managed environment:** Linux / Python 3.12.14.

## Observed verification

The actual full Stage 4 `python tools/verify.py` run passed **278 tests**, **16 validator steps**, Python compilation, configured test-module coverage and Ruff. Twenty new tests check evaluation-packet integrity, condition setup, repeat/order reproducibility, blocked execution handling, missing/modified outputs, incompatible routes/tools, telemetry metadata and bounded/no-overwrite operations. They use explicit fixtures, not model inference.

| Check | Observed evidence and scope |
|---|---|
| Full local Stage 4 verifier | PASS: 278 tests, 16 validators, Ruff |
| Prior Stage 3 hosted matrix | PASS: all 12 jobs at `59568ca`; [actual run](https://github.com/NeatKnight18586/friday-core/actions/runs/41424796031) |
| Stage 4 hosted matrix | Check exact published commit in [Actions](https://github.com/NeatKnight18586/friday-core/actions/workflows/ci.yml); results are retained in the delivery evidence. Local success is not a remote pass. |
| Actual current Codex preflight | BLOCKED before inference: token refresh failed, exit 1, no assistant response; [sanitized actual evidence](evals/behavior/preflight.json) |
| Comparison packets | 60 prepared (48 primary plus 12 critical repeats), zero behavioral executions; preparation is not a model result |
| Native host discovery, consumer UI and fresh-chat acceptance | NOT ESTABLISHED |
| Independent usefulness, method advantage, token/credit savings | NOT ESTABLISHED |

The prior Stage 3 skill reduction (1,949 to 831 words) remains only a text-size measurement. No additional skill-method changes or efficacy claims are inferred from the new evaluation infrastructure. The earlier lint-count correction remains historical: Stage 1 fixed all 21 findings, not the initial truncated count of nine.

## Reproduce

```bash
python -m pip install -r requirements-dev.txt
python tools/sync_host_entrypoints.py --check
python tools/update_manifest.py --check
python tools/verify.py
python tools/behavior_eval.py check
python tools/behavior_eval.py prepare
python tools/build_manager_adapter.py --out build/manager
python tools/build_skill_packages.py --out build/skill-packages
python tools/build_claude_chat_companion.py --out build/claude-chat
python tools/package_release.py --output build/Friday-Stage-4-Source.zip
```

Generated evaluation packets and collected responses default to ignored local storage. The tool does not call a provider or assign grades. To reproduce delivery checks, build the source ZIP twice and compare bytes, then extract into a new directory and run full verification. Archive hashes and exact-commit hosted CI results belong in the external delivery evidence to avoid circular source checksums. The source manifest excludes itself, archives and private/build/cache data.

## Boundaries

Publication to the owner-authorized `NeatKnight18586/friday-core` main branch is distinct from actual model runtime acceptance. The older repository is untouched. Existing MIT license remains preserved; third-party rights review, personal profile import and final public-release acceptance remain later gates. No credentials, private profile or actual participant data are introduced. Managed-runtime authentication must be repaired through supported controls; do not replace injected credentials or paste secret caches into chat. See [host routes](docs/acceptance/STAGE_4_HOST_ROUTES.md), [pilot protocol](evals/behavior/README.md) and [Stage 4 review](docs/reviews/REVISION_STAGE_4_REVIEW.md).

## INC-002 — Windows source verification

**Date/stage:** 2026-11-02, Stage 2 source publication. **Severity:** High. **Status:** Resolved at `10bbd13`; all 12 jobs in the [fix run](https://github.com/NeatKnight18586/friday-core/actions/runs/41419736151) passed.

**Trigger/evidence:** [Initial hosted run](https://github.com/NeatKnight18586/friday-core/actions/runs/41418737423) at `37816d2` passed Ubuntu/macOS but failed Windows. `python tools/verify.py` reported 18 manifest size/hash errors across nine files and two hackathon-test failures on Windows/Python 3.13. Other Windows jobs showed the same failure class.

**Cause:** The default Git attribute specified text detection without an LF checkout rule for extensionless files/JSONL. Windows core.autocrlf converted those bytes. Tests also omitted encoding on reads of UTF-8 method files, invoking cp1252 decoding on Python versions before UTF-8 became the default.

**Recovery:** Set default text checkout to LF, preserve existing binary/batch overrides, specify UTF-8 on remaining test text I/O, and pin the observed Windows-only colorama dependency. No manifest comparisons, test assertions or matrix entries were removed. New regression creates a real Git fixture and clones it with core.autocrlf=true, comparing original bytes including binary data. It detects the original attributes and passes after correction.

**Acceptance/residual risk:** Full local verification passed 227 tests, 14 validators and lint. All 12 hosted OS/Python jobs passed on the fix commit `10bbd13`. Actual model/consumer runtime behavior remains separate. The failed first run remains visible; source upload alone is not a CI pass.
