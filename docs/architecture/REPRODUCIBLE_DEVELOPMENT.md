# Reproducible Development and CI

**Status:** B3 local configuration and Linux checks delivered; remote execution pending  
**Version:** 0.6.0-draft

## 1. Purpose

B3 establishes a repeatable development environment, a single verification entry point, a cross-platform CI definition, and a Codespaces-ready Dev Container. It does not prove model-runtime compatibility or claim that GitHub-hosted checks have run before a remote repository exists.

## 2. Supported development baseline

- Python minimum: 3.11.
- Default local/Codespaces interpreter: Python 3.13, recorded in `.python-version`.
- CI matrix: Python 3.11, 3.12, 3.13, and 3.14 on Ubuntu, Windows, and macOS hosted runners.
- Development dependencies: direct and transitive exact-version snapshot in `requirements-dev.txt`.
- Tool configuration: `pyproject.toml`.

The requirements file pins exact package versions but does not pin wheel/source-distribution hashes. It improves version repeatability but is not a fully hash-locked artifact set. A future network-enabled maintenance task may migrate to a reviewed `uv.lock` or a hash-checked pip requirements file. Do not describe the current snapshot as a complete supply-chain lock.

## 3. Fresh environment setup

```bash
python --version
python -m pip install --disable-pip-version-check -r requirements-dev.txt
python tools/update_manifest.py
python tools/verify.py
```

The repository expects Python 3.11 or newer. Python 3.13 is the default developer environment, not the only supported version.

## 4. Verification command

`python tools/verify.py` runs:

1. Python bytecode compilation for repository tooling and tests.
2. Repository integrity, configuration, and package-manifest checks.
3. B2 JSON Schema and project-workspace checks.
4. Ruff static analysis.
5. Pytest unit and integration tests.

`--skip-lint` exists only for constrained local environments and must not be used by CI. CI must run the full verification command. If Ruff is unavailable, record lint as `NOT RUN`; do not report the skipped suite as a full pass.

Before committing intentional source changes, run `python tools/update_manifest.py`. CI runs `python tools/update_manifest.py --check` through repository validation and fails if paths, sizes, or SHA-256 values drift.

## 5. GitHub Actions

`.github/workflows/ci.yml` runs on pushes, pull requests, and manual dispatch. Its matrix covers Ubuntu, Windows, and macOS with Python 3.11–3.14. It grants only `contents: read`, pins direct action references to reviewed full commit SHAs, and sets `persist-credentials: false` for checkout.

The workflow has no repository secrets and requires no write permission. It is configured locally and is not considered executed until an actual run appears in the repository's Actions tab. GitHub documents `setup-python` and OS/Python matrix strategies in its official Python CI guide: https://docs.github.com/en/actions/tutorials/build-and-test-code/python.

GitHub workflow dependency lockfiles can pin direct and transitive action dependencies. This repository pins the direct actions by full SHA but does not yet contain a generated transitive action lockfile. Generate and review that lockfile after the repository is uploaded, using GitHub's supported tooling. Do not fabricate generated lock data. See https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles.

## 6. Dev Container / Codespaces

`.devcontainer/devcontainer.json` uses the `dev-3.13-bookworm` Python Dev Container image pinned to an immutable OCI SHA-256 digest and runs as the non-root `vscode` user. The digest intentionally prevents an upstream tag change from silently changing the development image. Updating the base image requires reviewing the upstream image, changing the digest, rebuilding the container, and rerunning verification.

The selected upstream image supports Linux amd64 and arm64. The Microsoft Artifact Registry currently lists the `dev-3.13-bookworm` variant and the configured digest: https://mcr.microsoft.com/en-us/artifact/mar/devcontainers/python/tag/dev-3.13-bookworm.

Codespaces can provide a browser-based full development environment with a terminal, debugging, Git and application execution. `github.dev` is a lighter browser editor and does not provide the same compute/terminal environment. See:

- https://docs.github.com/en/codespaces/developing-in-a-codespace
- https://docs.github.com/en/codespaces/the-githubdev-web-based-editor

Codespaces billing and quota depend on the owner's GitHub plan and usage. Check current quota and spending limits before creating or resuming a Codespace.

## 7. Dependency maintenance

Dependabot checks Python and GitHub Actions dependencies monthly. It proposes updates; it does not auto-merge them. Dependency changes must be reviewed, tested, and accompanied by a regenerated source manifest.

The exact-version requirements snapshot is a practical initial baseline. It does not guarantee identical artifacts across operating systems or indexes. Stronger artifact reproducibility requires reviewed hashes or a lockfile generated by a supported dependency manager in a network-enabled environment.

## 8. Boundaries of the proof

Passing local checks demonstrates that deterministic repository tooling works in the environment and interpreter where those checks ran. It does not prove:

- GitHub Actions passed before a remote run.
- Windows or macOS compatibility before those runners execute.
- Codespaces successfully built the Dev Container before launch.
- Claude Code discovered or invoked the future Peanuts skill.
- ChatGPT native Skills is enabled on a particular account or surface.
- Research findings are true or that a proposed product will succeed.

Record each environment, exact command, tool version, result, and limitation in its validation report.


## 9. Release ZIP layout

`python tools/package_release.py --output <path>` creates a deterministic cumulative source ZIP from `PACKAGE_MANIFEST.json`. Archive members are rooted at the repository root (`README.md`, `.github/`, `docs/`, `tools/`), not nested inside an enclosing `Friday/` folder. The builder first verifies manifest paths, sizes, and SHA-256 values; it then verifies ZIP CRC, exact member coverage, byte counts, and hashes.

For the iPad-to-GitHub handoff, upload the ZIP as a temporary file to an initially empty private repository, open Codespaces, and extract with `unzip -q <archive-name>.zip -d .`. Remove the ZIP afterward and run the full verification command. The archive does not contain `.git/`; GitHub's repository metadata is created separately.
