# Release verification — Friday 0.15.0-rc.3

**Classification:** `STAGE_2_CHECKPOINT` — read-only manager selection/intake, portable manual adapter and early CI/host preflight.  
**Date:** 2026-11-02. **Managed environment:** Linux / Python 3.12.14.

## Observed local verification

An actual complete `python tools/verify.py` run passed after Stage 2 implementation: **226 tests at the initial Stage 2 baseline**, **14 validator steps**, Python compilation, test-module coverage and Ruff. The manager adds 30 cases; all previous 196 tests remain. The Windows checkout regression brings the current suite to **227 tests**. Final archive runs, clean-container outcomes, exact source SHA-256, resolved image digests and blocked CLI evidence are recorded in the external checkpoint kit's machine-readable results and logs. These artifacts are evidence only for the exact commands/environments they name.

| Check | Evidence scope |
|---|---|
| Initial managed Linux verifier | PASS: 226 baseline tests, 14 validators, Ruff; current suite adds the Windows checkout regression |
| Manager contracts, metadata-only manual export and read-only selection/intake | PASS: deterministic helper tests; actual host/model behavior remains separate |
| Generated host snapshots and consumer upload packages | Canonical parity, package/resource closure, safe layout and deterministic-build checks |
| Workflow syntax/expressions | PASS: actionlint 1.7.12, upstream release checksum verified |
| Pinned GitHub Action commits | PASS: both commit SHAs resolve upstream |
| Clean offline Linux Python 3.11–3.14 installations/full verification | Version-specific verified-download wheel sets, offline installs, exact outcomes and image digests in delivery evidence; not GitHub-hosted CI |
| Actual Codex CLI Peanuts smoke attempt | BLOCKED: unrefreshable authentication token/401 before model completion |
| Actual Claude Code/consumer activation and configured ChatGPT Project recovery | NOT RUN |
| GitHub-hosted Ubuntu/macOS/Windows, Python 3.11–3.14 | PASS: all 12 jobs at `10bbd13`; [hosted run](https://github.com/NeatKnight18586/friday-core/actions/runs/41419736151). Current-commit results remain visible in Actions |
| Independent user usefulness, NUTS/Four-Council advantage, credit/token savings | NOT ESTABLISHED |

The Stage 1 count correction remains: the original full lint diagnostics contained 21 findings, not the initial truncated-output count of nine. Stage 1 fixed them without weakening lint. Historical evaluation records retain their original scope; no new consumer/model pass is inferred here.

## Reproduce

```bash
python -m pip install -r requirements-dev.txt
python tools/sync_host_entrypoints.py --check
python tools/update_manifest.py --check
python tools/verify.py
python tools/build_manager_adapter.py --out build/manager
python tools/build_skill_packages.py --out build/skill-packages
python tools/build_claude_chat_companion.py --out build/claude-chat
python tools/package_release.py --output build/Friday-Stage-2-Source.zip
```

For canonical changes, regenerate with `python tools/sync_host_entrypoints.py --sync`, then update the manifest before checking it. Build the source ZIP twice and compare bytes; extract into a fresh directory and run full verification. The source manifest excludes itself and private/build/cache data; external checksums cover the archive without self-reference. Heuristic secret scans do not prove absence of every sensitive item.

## Boundaries

The owner selected `NeatKnight18586/friday-core` for a clean initial source commit, with no tracked source ZIP. The older repository remains separate. Hosted checks must be assessed for their exact commit in GitHub Actions; the earlier Stage 2 preflight findings remain historical evidence. The existing owner-authored MIT license was recovered from that repository and is preserved in this source; third-party rights review remains a release gate. Source installation and CI success do not establish native host model behavior, autonomous execution or persistent private memory. Follow [the preflight method](docs/acceptance/CI_AND_HOST_PREFLIGHT.md) and [revision stages](docs/plans/REVISION_STAGES.md).


## INC-002 — Windows source verification

**Date/stage:** 2026-11-02, Stage 2 source publication. **Severity:** High. **Status:** Resolved at `10bbd13`; all 12 jobs in the [fix run](https://github.com/NeatKnight18586/friday-core/actions/runs/41419736151) passed.

**Trigger/evidence:** [Initial hosted run](https://github.com/NeatKnight18586/friday-core/actions/runs/41418737423) at `37816d2` passed Ubuntu/macOS but failed Windows. `python tools/verify.py` reported 18 manifest size/hash errors across nine files and two hackathon-test failures on Windows/Python 3.13. Other Windows jobs showed the same failure class.

**Cause:** The default Git attribute specified text detection without an LF checkout rule for extensionless files/JSONL. Windows core.autocrlf converted those bytes. Tests also omitted encoding on reads of UTF-8 method files, invoking cp1252 decoding on Python versions before UTF-8 became the default.

**Recovery:** Set default text checkout to LF, preserve existing binary/batch overrides, specify UTF-8 on remaining test text I/O, and pin the observed Windows-only colorama dependency. No manifest comparisons, test assertions or matrix entries were removed. New regression creates a real Git fixture and clones it with core.autocrlf=true, comparing original bytes including binary data. It detects the original attributes and passes after correction.

**Acceptance/residual risk:** Full local verification passed 227 tests, 14 validators and lint. All 12 hosted OS/Python jobs passed on the fix commit `10bbd13`. Actual model/consumer runtime behavior remains separate. The failed first run remains visible; source upload alone is not a CI pass.
