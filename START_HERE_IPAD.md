# Start here — iPad and source checkpoint

**Release:** 0.15.0-rc.2 · Stage 2. **Purpose:** prepare a public, provider-neutral capability manager; Peanuts is the current prototype. The read-only selector/intake helper and manual manager adapter are implemented; actual host behavior remains separately gated. The main branch is the source development branch; [Actions](https://github.com/NeatKnight18586/friday-core/actions/workflows/ci.yml) shows checks for each uploaded commit.

To use Friday in a consumer chat, attach the generated `Friday-Manager.txt` alongside the selected capability route. It contains instructions/catalog/contracts, not the Peanuts method files or an executable native manager. If Peanuts is missing, Friday must report the missing package.

## Choose what you need

| Destination | Use | Boundary |
|---|---|---|
| Source repository / engineering workspace | Extract `Friday-Stage-2-Source.zip` at the repository root | Includes source, tests, schemas and generated Codex/Claude Code snapshots |
| Ordinary Claude chat | Upload `peanuts-claude-chat-skill.zip` as a Skill ZIP using the supported account UI | Separate consumer adapter, not the whole repository |
| Claude Project | Extract `friday-peanuts-claude-project-knowledge.zip`; upload the five text documents and paste `CLAUDE_PROJECT_INSTRUCTIONS.md` | Background and handoffs; no automatic source synchronization |
| ChatGPT Project | Extract `peanuts-chatgpt-project-files.zip`; upload its five text documents and paste the separate Project instructions | Manual reference adapter, not an executable native Skill |
| Codex / Claude Code | Open the source workspace in the actual host | Generated discovery paths exist; real invocation still needs testing |

This checkpoint does not require a particular provider. Check actual account/device eligibility, upload limits and tool access during setup. A successful upload is not proof of useful behavior. Use the [cross-host acceptance guide](docs/acceptance/CROSS_HOST_RUNTIME_ACCEPTANCE.md) and [smoke prompts](docs/acceptance/CROSS_HOST_SMOKE_TEST_PROMPTS.md).

## Work from an iPad

1. Save the source ZIP and read [release status](RELEASE_STATUS.md). Source updates, testing and package builds can be performed by an available file-enabled engineering assistant or cloud terminal; you do not need a laptop for that work.
2. Choose a host route above. Build or obtain its separate upload bundle. The source ZIP does not itself install Peanuts into a consumer app.
3. For Claude, use [setup](adapters/claude-chat/SETUP_IPAD.md) and record actual results. For ChatGPT, use the generated Project setup/instructions. If a required control is unavailable, mark the route blocked rather than guessing it installed.
4. Keep a compact status handoff. Uploaded Project files and Skill bundles must be refreshed explicitly after source changes.
5. Keep resumes, private writing, credentials and confidential projects outside the shareable repository. Profile import is planned, not implemented.

## Source work in a cloud terminal

GitHub does not extract a ZIP merely because it was uploaded as a repository file. A browser editor is not necessarily a terminal. An available Codespace or other authorized cloud workspace can extract and verify source. Check access and usage terms before using paid services. Private staging is optional; final public release still needs license, privacy and evidence review.

These commands assume a clean disposable directory containing the source ZIP. Extract there first to avoid overwriting an existing checkout:

```bash
mkdir friday-stage2
unzip -q Friday-Stage-2-Source.zip -d friday-stage2
cd friday-stage2
python -m pip install -r requirements-dev.txt
python tools/verify.py
python tools/build_skill_packages.py --out build/skill-packages
python tools/build_claude_chat_companion.py --out build/claude-chat
python tools/build_manager_adapter.py --out build/manager
```

Publishing/committing/pushing are separate deliberate actions after review of the concrete files. The owner selected the new public friday-core repository for current source work. For current source, use its main-branch checkout; source ZIPs and consumer upload bundles remain separate delivery artifacts.

## Maintain the canonical source

`skills/peanuts/` is authored; `.agents/skills/peanuts/` and `.claude/skills/peanuts/` are generated. After approved source edits:

```bash
python tools/sync_host_entrypoints.py --sync
python tools/update_manifest.py
python tools/verify.py
```

Rebuild consumer upload bundles as well. Local checks verify structure and contracts; actual host behavior, Project retrieval, account persistence and token/credit savings require separate evidence. See [verification](RELEASE_VERIFICATION.md) and [next stages](docs/plans/REVISION_STAGES.md).
