# B3 — Reproducible Development and CI Review

**Status:** Local deterministic checks executed; Ruff and remote checks pending  
**Version:** 0.6.0-draft  
**Date:** 2026-11-01

## 1. Scope

B3 adds the dependency baseline, Python tool configuration, unit/integration tests, manifest tooling, one-command verification, GitHub Actions CI, Dependabot, and a digest-pinned Dev Container for Codespaces.

## 2. Four-perspective review

### Council 1 — Systems and Release Architecture

**Assessment:** Pass with bounded limitations.

- One verification command creates a predictable local/CI entry point.
- The Dev Container and CI matrix describe the same declared Python baseline.
- The source manifest detects missing, unexpected, changed, and duplicate file entries.
- The dependency snapshot pins exact package versions but does not verify package artifact hashes.
- The Dev Container image is pinned by OCI digest. Updates require an intentional digest change and rebuild.

### Council 2 — Software Quality and Test Engineering

**Assessment:** Pass for deterministic B3 scope after the final run recorded below.

- Unit tests cover project-ID normalization, invalid identifiers, manifest behavior, configuration, and malformed data handling.
- Integration tests cover project initialization and refusal to overwrite existing workspaces.
- The B2 validator exercises schemas, record references, and project-workspace invariants.
- Configuration tests parse TOML, JSON, and GitHub YAML and check action SHA references, matrix coverage, and dependency pins.
- The Python suite does not evaluate model judgment or complete Peanuts behavior; those evaluations are introduced with the method and runtime stages.

### Council 3 — Developer Experience and Portability

**Assessment:** Configured; remote confirmation pending.

- The repository has one documented setup command and one verification command.
- Windows, macOS, and Linux checks are configured in CI.
- Codespaces has a digest-pinned Python 3.13 Bookworm Dev Container and a non-root user.
- This managed environment can execute only its own Linux runtime. Windows, macOS, remote CI, and Codespaces remain `NOT RUN` until those environments execute the configuration.

### Council 4 — CI Security and Supply Chain

**Assessment:** Pass with documented limitations.

- Workflow permissions are `contents: read` only.
- Direct Actions references use full upstream commit SHAs.
- Checkout credentials are not persisted.
- Dependabot proposes updates; no automatic merge is configured.
- CI uses no repository secrets.
- Requirements pin exact versions but not artifact hashes.
- The source secret scan is heuristic and cannot prove absence of all secrets.
- A generated transitive Actions lockfile remains a post-upload maintenance task; it must be generated and reviewed with supported GitHub tooling rather than fabricated.

## 3. Local validation record

Recorded from the B3 implementation environment (Python 3.13.5, Linux). Commands were rerun after the Dev Container tag/digest pairing and verifier corrections.

| Check | Command | Result |
|---|---|---|
| Repository integrity | `python tools/validate_repo.py` | PASS |
| B2 regression | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python tools/validate_b2.py` | PASS — 8 schemas, 18 evaluation cases, temporary workspace invariants |
| Unit/integration tests | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q` | PASS — 23 passed |
| Combined verification | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python tools/verify.py --skip-lint` | PASS WITH SKIP — repository integrity, B2 validation, compilation and 23 tests; Ruff explicitly skipped |
| Manifest consistency | `python tools/update_manifest.py --check` | PASS — 106 tracked source files match the manifest |
| Ruff | `python -m ruff check tools tests` | BLOCKED / NOT EXECUTED — Ruff is pinned but its module is unavailable in this managed environment; package-network access is unavailable |
| Full verification without skips | `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python tools/verify.py` | BLOCKED — the Ruff step returned exit 1 because the module is unavailable; repository integrity, B2, and 23 tests still completed and passed |
| GitHub Actions matrix | Remote workflow | NOT RUN — no remote repository is configured |
| Codespaces | Dev Container build and verification | NOT RUN — no remote Codespace has been created |
| Claude/ChatGPT runtime | Actual host/account smoke tests | NOT RUN — no packaged Peanuts skill/runtime adapter yet |

A prior test exposed a stale package-manifest entry for the removed `requirements-dev.lock`; regenerating the manifest resolved that failure. The verifier was also changed to call repository/B2 validators and pytest in-process where appropriate, with the repository root explicitly added to `sys.path`. This avoids an unnecessary nested process layer and preserves normal test imports. These were corrected before the recorded passing run.

## 4. Release disposition

B3 is a reproducibility and CI configuration milestone, not proof of full cross-platform execution or model-runtime behavior. The local non-lint verification passed with Ruff explicitly skipped. The full verifier was also attempted and exited unsuccessfully only because Ruff is unavailable; it continued to run and pass the other checks. Remote CI, Codespaces, Windows/macOS compatibility, and model-runtime behavior remain unverified. Do not label the repository `READY_FOR_FIRST_USE` based only on local Linux tests.
