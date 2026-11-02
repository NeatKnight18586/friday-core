# Repository tools

## Repository/documentation validation

```bash
python tools/validate_repo.py
```

Checks required files, relative Markdown links, code-fence balance, common secret-token patterns and manifest hashes. It does not prove factual correctness, complete secret absence, or AI runtime behavior.

## B2 schema and evaluation-case validation

Install the development dependency:

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_b2.py
```

Uses JSON Schema Draft 2020-12 to validate schemas, project/record templates, and synthetic evaluation cases. It does not execute an AI evaluation.

## Create a project workspace

```bash
python tools/init_project.py --id my-project --title "My Project" --mode MODE-IDEA
```

Default output is `local-workspace/projects/my-project/`, which is Git-ignored. The tool refuses to overwrite an existing project directory.

## Validate a project workspace

```bash
python tools/validate_project.py local-workspace/projects/my-project
```

Checks project/state schemas, JSONL records, duplicate record IDs, and B2–B8 cross-record/semantic invariants. It does not verify the truth of claims, quality of sources, real user demand, design feasibility, or model behavior.


## B7 council and assumption validation

```bash
python tools/validate_b7.py
```

Checks the Four-Council review, assumption-test and assumption schemas, templates, and synthetic B7 evaluation cases. Project-level semantic validation is also run by `python tools/validate_project.py PATH`, which enforces evidence links, human-participant safeguards, assumption/test consistency, mandatory event-rule blockers, and non-compensatory progression gates.

## Full verification (B3–B8)

Install the exact-version development snapshot with `python -m pip install --disable-pip-version-check -r requirements-dev.txt`. After intentional file changes, refresh the distributable source manifest with `python tools/update_manifest.py`. Run `python tools/verify.py` for repository checks, B2/B4/B5/B6/B6.5/B7/B8 milestone validators, Ruff static analysis, and pytest unit/integration tests. The CI workflow runs the same command. Do not use `--skip-lint` in CI.

`python tools/update_manifest.py --check` verifies manifest freshness without modifying it. The manifest excludes local workspaces, private-data directories, virtual environments, caches, archives, symlinks, and secrets/environment files (except the safe `.env.example` template).


## B8 product and delivery validation

```bash
python tools/validate_b8.py
```

Checks B8 requirement, acceptance-test, build-task, artifact, and demo-plan schemas/templates plus EVAL-062–087. The project-level B8 semantic rules run through `python tools/validate_project.py PATH`; they check evidence/approval gates, linked test coverage, dependency sequencing, task completion evidence, participant controls, artifact file/hash/path integrity, earlier-stage artifact references, cross-document identifier traceability, demo-claim evidence strength, and P7–P9 stage gates. `ready` evaluation cases are preparation artifacts, not model passes.

## Full verification (B3–B8)

`python tools/verify.py` runs repository integrity, the consolidated B2/B4/B5/B6/B6.5/B7/B8 validators, Ruff, and pytest. `--skip-lint` is local-only and must be reported as PASS WITH SKIPS.

## Stage 2 manager

`python tools/capability_manager.py list` shows validated metadata. Use `select --capability peanuts --host codex --input request --grant read-project-data` to identify instructions subject to prerequisite gates; grants report existing permission, not system authority. `intake --candidate candidate.json` is a dry run and never edits the catalog or executes package code. See `docs/architecture/MINIMAL_MANAGER.md`. Build the manual consumer adapter with `python tools/build_manager_adapter.py --out build/manager`.

## Compact planning

Use `python tools/init_project.py --id my-idea --title "My idea" --layout compact --resource-mode fast` for a private two-file planning workspace. The default full layout and its gates remain unchanged. `python tools/handoff.py <project-dir> --resume` validates and returns context without executing the recorded action; pass `--available-tool` only for tools actually present. `python tools/validate_planning.py` checks authored synthetic examples. Fast is stored as quick through `tools/resource_modes.py`.
