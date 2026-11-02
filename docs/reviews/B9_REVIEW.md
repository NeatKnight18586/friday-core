# B9 — Skill Packaging and Host Adapters: Four-Lens Review

**Review date:** 2026-11-02  
**Status:** PASS WITH BOUNDED LIMITATIONS — portable packaging, canonical-source parity, ChatGPT Project fallback design, deterministic local checks, repository integrity, and the complete local regression suite passed. Actual host discovery/invocation and model behavior remain untested.  
**Scope:** Canonical Peanuts skill metadata and entrypoint; portable Agent Skills package; generated Claude Code and Codex adapters; ChatGPT Project manual fallback; deterministic packager and validator; capability registry; B9 evaluation cases EVAL-088–102 (15 cases); B1–B8 regression boundaries.

This is a structured review using four professional perspectives, not four independent human experts, a certification, or evidence that an AI system possesses professional credentials. Scores are qualitative judgments of the implementation and its local verification, not measured model-performance scores.

## 1. Executive assessment

B9 establishes one canonical Peanuts skill source and reproducible distribution routes. It corrects the Agent Skills metadata/folder-name alignment (`name: peanuts` for `skills/peanuts/`), keeps the discovery description concise while validating the documented 1,024-character maximum, validates local reference integrity, and generates host-specific packages rather than maintaining duplicated skill logic. An earlier B9 draft incorrectly treated 200 characters as a universal Claude limit; current official Anthropic docs state 1,024. The unsupported limit and its test were corrected before release.

The ChatGPT route is deliberately a manual Project adapter: five curated plain-text reference files containing Markdown-formatted content plus separate Project instructions and setup guidance. The five source files are generated from canonical repository sources and checked for required schemas/templates and exact file-set membership. It is designed around the documented five-file Free Project limit. It does not claim automatic skill activation, local file access, shell execution, JSON Schema validation, or deterministic execution from Project instructions alone.

The design keeps Friday as the repository/umbrella and Peanuts as an independent capability. It does not add an autonomous manager, hosted service, database, or provider-specific runtime dependency.

## 2. Four professional perspectives

### Council 1 — Product/platform architecture and interoperability

**Assessment: 8.8/10 — Pass with bounded limitations**

Strengths:
- One canonical source under `skills/peanuts/`; host copies are generated.
- Canonical metadata follows the Agent Skills name/folder contract and validates the documented 1,024-character description maximum. The actual description is 191 characters by editorial choice, not because of an undocumented host cap.
- Portable, Claude Code, and Codex archives use their respective expected directory layouts.
- Each skill archive contains 102 files: 30 canonical skill files plus 72 generated support resources from repository schemas, record templates, project templates and governing docs. The support layer is copied from canonical sources at build time; it is not separately authored or maintained.
- Package tests compare generated files against canonical source bytes and check local link closure after support-resource injection.
- The capability registry distinguishes ready-for-test, manual fallback, and conditional native routes instead of implying equivalent support.
- Friday remains an umbrella. The capability package can be used independently.

Limitations:
- Package layout validation does not prove that the target host discovers or loads the skill. Local Markdown-link closure is checked after resource injection so a self-contained ZIP does not retain links to files omitted from the package.
- Host discovery conventions and product availability can change; verify official host documentation at installation time.
- The Claude Code and Codex packages are generated adapters, not live-tested installations.

Recommendation: Keep the canonical-source/generated-adapter boundary. Do not hand-edit generated host copies.

### Council 2 — ChatGPT user experience and practical deployment

**Assessment: 9.0/10 — Pass with bounded limitations**

Strengths:
- ChatGPT Project is the primary route for the current Free/iPad-first workflow, avoiding dependence on an account-gated native Skills feature.
- Exactly five curated plain-text `.txt` files containing Markdown-formatted content are included in the Project source bundle; Project instructions and setup are separate.
- The five bundles organize core method navigation, research/evidence, NUTS/review, product/engineering, and governance/records.
- Subject bundles embed the relevant complete JSON Schema definitions, record starters and selected method/governance source text while retaining exactly five upload files.
- The instructions preserve progressive disclosure: retrieve only the relevant reference bundle instead of loading every method for every request.
- The adapter says plainly that it is manual and that reference files do not install scripts or provide guaranteed tool access.
- The setup guide includes a recovery/continuity practice so future sessions can resume from a saved handoff.

Limitations:
- Five files is a product-plan limit checked against current OpenAI documentation, not a permanent contract. Free upload limits may also restrict how quickly the files can be added.
- Project instructions and reference files guide behavior but cannot make a model follow every procedure or invoke unavailable tools.
- The actual iPad UI setup has not been executed in the user's account.

Recommendation: Use this manual Project adapter as the working ChatGPT route. Save the generated five files and Project instructions together; update them only by regenerating from the canonical repository source.

### Council 3 — Professional methods, context engineering and developer experience

**Assessment: 8.7/10 — Pass**

Strengths:
- The Project instructions use the existing Professional Practice Architecture: classify the job/decision, identify disciplines and stakeholders, select methods, check prerequisites, choose trustworthy available tools, produce traceable outputs, and apply verification/escalation.
- Existing P1–P10 operational workflow is kept distinct from B0–B10 repository construction milestones.
- Existing research integrity, NUTS limitations, Four-Council independence disclosure, assumption-validation gates, product/technical handoff and privacy boundaries remain referenced rather than rewritten into a competing framework.
- Root guidance is concise and points to deeper references; context inspection remains within the existing maintainability budget.
- The manual ChatGPT route includes a resumable handoff protocol and advises the assistant not to restart accepted stages.

Limitations:
- The quality of professional judgment remains dependent on the model, evidence and human oversight; the architecture cannot confer professional licensure or expertise.
- Grouping many reference documents into five files is a compromise for the current Project limit. Fine-grained progressive disclosure is less precise than a host with filesystem reference loading.

Recommendation: Preserve PPA and progressive disclosure. Use the method governance and QA checks to select methods rather than adding frameworks for appearance.

### Council 4 — AI assurance, security and evaluation

**Assessment: 8.8/10 — Pass with bounded limitations**

Strengths:
- Packager validates metadata, local links, resource folders, symlink exclusion, unsafe/generated-file exclusion and path boundaries.
- Host ZIP contents are checked against canonical source bytes.
- Repeated archive builds are byte-reproducible.
- ChatGPT Project pack is exactly five plain-text `.txt` files containing Markdown-formatted content and excludes Project instructions from the uploaded-file ZIP.
- EVAL-088–102 cover metadata/name alignment, description limits, reference integrity, source drift, host paths, five-file constraints, manual-fallback honesty, resource budget, deterministic builds, archive traversal/symlinks, tool availability, project continuity and prompt injection.
- Negative tests check unsafe paths, content drift, missing references and mismatched folder names.

Limitations:
- Evaluation cases are marked `ready`; no live Claude, Codex or ChatGPT model has passed them.
- The security checks are structural/heuristic and do not replace host permission review, sandbox testing, dependency scanning or a security audit. Package validation also checks local Markdown-link closure after support-resource injection, preventing links to omitted files.
- Ruff was not run in this environment; remote CI and Codespaces remain not run.

Recommendation: Keep the B9 evaluation suite as a release gate for packaging changes. Run actual host discovery and fresh-session tests during B10, with explicit permissions and no untrusted tool instructions.

## 3. Key architecture decisions preserved

B9 records ADR-015 to make the owner-facing workflow explicitly ChatGPT-first while retaining a provider-neutral canonical core. The earlier Claude-first proposal is superseded for the owner-facing route; Claude Code remains a generated optional adapter.

1. **Canonical source:** `skills/peanuts/` remains the only authored Peanuts skill source. Generated packages are disposable outputs.
2. **ChatGPT first:** The Project adapter is the default working route for this current Free-plan workflow. Native Skills are conditional on account/surface eligibility.
3. **No false capability claims:** Project files are reference text, not installed code or a guarantee of shell access.
4. **No premature Friday manager:** Friday remains the umbrella; an active orchestration/control plane is still evidence-dependent.
5. **No weakening of prior stages:** B1–B8 sources, schemas, ledgers, evaluation cases and validators are preserved; B9 adds packaging and host routing.
6. **Professional methods over framework accumulation:** PPA selects methods according to the task and decision. Research, NUTS, Four-Council, assumption tests, PRD and engineering methods remain complementary and risk-adaptive.

## 4. Local verification evidence

Environment: managed Linux container, Python 3.13.5; local package/test execution only.

- `python tools/build_skill_packages.py --out /mnt/data/friday_b9_packages` — passed; generated all four routes. Portable, Claude Code and Codex archives each contain 102 files (30 canonical skill files plus 72 generated support resources); the ChatGPT Project archive contains exactly five `.txt` files.
- Final resource-closure build outputs at the current package snapshot: portable 180,193 bytes (SHA-256 `c94d4f33d4f501f66fbcac1bb7df8081163c8f4f771a43a46c898043bb9ec297`); Claude Code 183,253 bytes (`2ab392030ff2e2f8da2ab3eeff778304a6a6f1cf29d4be547db7ddfe7e9a6553`); Codex 183,253 bytes (`82c953e1630118a794d651b1518d182827644b9898453f369a9dd19ca951c936`); ChatGPT Project 135,799 bytes (`cdb2d97bc3885a2098510353e26e7973f46ddf8fd768766e12a541bc07c842a7`). Rebuilt package hashes are reported in the final package README/manifest where documentation changes affect bytes.
- `python tools/validate_b9.py` — passed; 15 B9 cases EVAL-088–102 validated and rubric-linked.
- `python tools/validate_b9.py --out /mnt/data/friday_b9_packages` — passed; generated output set, exact five `.txt` Project files, host ZIP contents, support-resource closure and source-byte parity checked.
- `python tools/validate_capabilities.py` — passed.
- `python tools/validate_repo.py` and `python tools/update_manifest.py --check` — passed after the B9 resource-closure and review-document updates; 347 source files are covered by the manifest.
- `python tools/validate_vertical_slice.py` (B4), `validate_b5.py`, `validate_b6.py`, `validate_b7.py`, `validate_b8.py`, and `validate_b9.py` — passed individually.
- `python tools/inspect_context.py` — passed after the B9 resource-closure documentation updates; host instructions and canonical Peanuts skill remain within their word budgets. Word counts are maintainability proxies, not actual token-use measurements.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/test_b9_packaging.py` — 18 passed in 3.37 seconds on the package snapshot.
- Full regression: **156/156 passed across three bounded runs**: `test_init_project.py` (11 passed); B5–B8 modules (85 passed, including the previously problematic legacy-workspace subprocess test); remaining B9/configuration/context/manifest/package/validation/vertical-slice modules (60 passed). The 156-test collection was confirmed separately. A single all-modules invocation timed out after partial progress without an assertion failure; split runs covered every collected test and completed successfully.
- The B2 lifecycle validator was not reliably completed in this B9 session; a separate invocation timed out. B9 did not alter B2 implementation. Do not report that standalone validator as passed; retain it as a targeted B10 rerun.

## 5. Not run / not claimed

- Ruff/lint: NOT RUN (tool unavailable in the managed environment; no network package installation assumed).
- GitHub Actions: NOT RUN (requires private repository upload and remote CI execution).
- Codespaces/devcontainer: NOT RUN (requires remote host execution).
- Claude Code: NOT RUN (no actual target host discovery/invocation/fresh-session test).
- Codex: NOT RUN (no actual target host discovery/invocation/fresh-session test).
- ChatGPT Project UI: NOT RUN in the user's account; setup instructions are prepared but not account-verified.
- Native ChatGPT Skills: NOT RUN and not assumed available to this Free-plan workflow.
- Live-model behavior, instruction adherence and human-labelled calibration: NOT RUN.

## 6. Exit recommendation

**B9 is accepted as a local packaging, interoperability-design and deterministic-validation milestone.** The canonical-source/generated-adapter boundary, Agent Skills metadata, four packaging routes, exact five-file ChatGPT Project fallback, capability registry and 15 B9 evaluation cases are implemented. Repository integrity, the regenerated file manifest, individually run B4–B9 validators, the focused 18-test B9 suite, and all 156 collected tests passed in module-level runs, including from a fresh extraction of the final archive. A single combined invocation remains intermittently unreliable in this container. B2's standalone lifecycle validator remains a specifically disclosed rerun item. Actual host discovery, UI setup, permissions, fresh-session model behavior and empirical calibration remain B10 work. Do not claim portable runtime success based only on a valid ZIP or schema test.

## 7. Official host references checked 2026-11-02

- Agent Skills specification: https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx
- Anthropic Agent Skills metadata/description requirements: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- OpenAI — Skills in ChatGPT: https://help.openai.com/en/articles/20001066-skills-in-chatgpt
- OpenAI — Projects in ChatGPT: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- OpenAI — File uploads and limits: https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt
- Claude Code skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Codex skills: https://developers.openai.com/codex/skills/
