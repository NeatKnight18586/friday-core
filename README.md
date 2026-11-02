# Friday

A portable capability manager in development, with **Peanuts** as its first project-discovery and planning capability.

**Checkpoint:** `0.15.0-rc.2` · Stage 2 · Public-release preparation. Friday now provides a read-only capability selector and dry-run intake helper, portable host-mediated manager instructions, a capability catalog, records, packaging and validation. Peanuts is an installable prototype whose live behavior still needs testing on each target host.

## Use Friday to select or add capabilities

Start with [FRIDAY.md](FRIDAY.md), or attach the generated `Friday-Manager.txt` alongside a separately installed Peanuts route. The manager chooses a bounded capability and prepares a handoff; it does not run an autonomous agent loop or install capabilities by itself.

```bash
python tools/capability_manager.py list
python tools/capability_manager.py select --capability peanuts --host codex --input request --grant read-project-data
python tools/build_manager_adapter.py --out build/manager
```

The grant flag reports authorization already given; it grants no system access. Intake is a dry run. See [manager interfaces](docs/architecture/MINIMAL_MANAGER.md) for no-match/ambiguity, permission/dependency gates and future package intake.

## What Peanuts helps you do

Start with an idea, a problem, an existing project, or a hackathon. Peanuts guides evidence-led research, user/problem discovery, selective inspiration from nature/history/other domains, concept comparison, Four-Council critique, assumption testing, and a documented handoff for building.

NUTS (“Nothing New Under the Sun”) studies and transforms existing mechanisms with attribution. NUTS and Four-Council are experimental methods; they do not guarantee novelty, validated demand, or competition wins. Quick/Standard/Deep guide work depth, with Standard as the default. A Fast display name/alias is planned for Stage 3; the current identifier is `quick`.

## Try the prototype

Choose a host route below. For an iPad, follow [Start here](START_HERE_IPAD.md). Packages must be generated from this source tree; an entire repository ZIP is not a consumer Skill upload.

| Route | Entry point / package | Evidence at this checkpoint |
|---|---|---|
| Codex | Generated `.agents/skills/peanuts/SKILL.md`; invoke `$peanuts` after confirming host discovery | File parity and installation simulation pass; actual discovery/model behavior NOT RUN |
| Claude Code | Generated `.claude/skills/peanuts/SKILL.md`; invoke `/peanuts` after confirming host discovery | File parity and installation simulation pass; actual discovery/model behavior NOT RUN |
| Claude ordinary chat | Separate consumer Skill ZIP and optional Project companion | Package validation passes; account upload, activation and recovery NOT RUN |
| ChatGPT Project | Separate Project instructions and five generated text reference files | Manual adapter validates; configured Project UI and recovery NOT RUN |
| Native ChatGPT Skills | Conditional route, subject to actual account/surface support | Not accepted as a tested route at this checkpoint |

Check account eligibility, tool access and product instructions during installation. Shared source does not mean identical discovery, permissions, browsing, persistence or output quality. See [host acceptance](docs/acceptance/CROSS_HOST_RUNTIME_ACCEPTANCE.md) and [smoke prompts](docs/acceptance/CROSS_HOST_SMOKE_TEST_PROMPTS.md).

After setup, an example request is:

> Use Peanuts in standard mode. Help me identify a project worth building for this event: [official event URL]. Check the rules and affected users, compare a few options, and recommend a feasible demo. Mark assumptions and give me a resumable handoff.

This is a usage prompt, not a recorded success. If research tools are unavailable, Peanuts must disclose that and provide a research plan or work from supplied sources. A [synthetic end-to-end fixture](examples/vertical-slice-synthetic/campus-service-status/README.md) demonstrates the record format; it is not user validation.

## Verify and build packages

In an environment with Python 3.11+ and a terminal:

```bash
python -m pip install -r requirements-dev.txt
python tools/verify.py
python tools/build_skill_packages.py --out build/skill-packages
python tools/build_claude_chat_companion.py --out build/claude-chat
python tools/build_manager_adapter.py --out build/manager
```

[Release verification](RELEASE_VERIFICATION.md) records actual results and limits. Passing tests checks package/record behavior, not idea quality, host instruction following, or token savings. Workflow lint and clean-environment checks reduce risk; [GitHub Actions](https://github.com/NeatKnight18586/friday-core/actions/workflows/ci.yml) records hosted results for each source commit. Real user pilots and baseline comparisons remain separate gates. See [host/CI preflight](docs/acceptance/CI_AND_HOST_PREFLIGHT.md) for the actual Codex authentication blocker and test method.

## Source and development

- [Architecture](docs/architecture/ARCHITECTURE.md) and [current decisions](docs/architecture/DECISIONS.md).
- [Revision stages](docs/plans/REVISION_STAGES.md); [historical build roadmap](docs/plans/BUILD_ROADMAP.md).
- [Peanuts purpose](docs/product/PEANUTS_CONSTITUTION.md) and [capability catalog](capabilities/registry.json).
- [Contributing](CONTRIBUTING.md), [release status](RELEASE_STATUS.md), and [changelog](CHANGELOG.md).

`skills/peanuts/` is the authored skill source. Host folders and upload packages are generated distributions. Update canonical files, regenerate, and check parity; do not independently edit host copies.

## Privacy and release boundaries

Keep personal profiles, resumes, participant data, credentials and confidential projects outside the shareable source. Profile import is planned as an optional, user-reviewed feature; no persistent memory service is implemented. Private project paths are ignored, but `.gitignore` is not an access control.

This is MIT-licensed prototype source, preserving the existing owner-authored license. The repository tracks source files directly; downloadable archives belong outside the source tree. Third-party rights review and public-release acceptance remain pending. See [publication policy](docs/governance/PUBLICATION_AND_PRIVACY.md). No supported-host, popularity or universal compatibility guarantee is claimed.
