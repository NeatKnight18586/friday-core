# B4 — End-to-End Vertical Slice Review

**Status:** Structural vertical slice accepted with bounded limitations. Local deterministic checks executed; Ruff and model-host runtime not executed.

## Scope delivered

B4 adds an initial canonical Peanuts Agent Skill prototype, stage/workflow references, self-contained artifact templates, a synthetic event-first example, a vertical-slice run schema, deterministic artifact/record validator, five regression tests, and evaluation case EVAL-019. The evaluation-case disposition is `ask` (the runtime should request real user evidence); the example Four-Council artifact separately retains its conditional `VALIDATE` recommendation. These are different fields with different meanings.

## What is proven

- The skill file has the required minimal Agent Skills metadata and a concise description. **B9 correction:** current Anthropic Agent Skills documentation specifies a 1,024-character maximum; the earlier reference to a stricter 200-character Claude limit was unsupported as a universal rule and is superseded by the B9 metadata validation.
- The synthetic fixture contains all seven stage handoffs P1–P7.
- Project and state JSON conform to B2 schemas.
- Source, claim, assumption, and decision records conform to their schemas and references resolve.
- The manifest's required artifact paths exist, remain within the fixture directory, and carry synthetic-data labels.
- The PRD is explicitly draft/unapproved; the handoff leaves P6 awaiting user evidence.
- Validator negative tests reject missing artifacts, dangling source references, missing synthetic labels, and path traversal.

## What is not proven

- No Claude Code or Codex runtime invoked the skill.
- No native ChatGPT Skill installation or Project context loading was executed.
- No real external event research, interviews, observations, usability tests, or market validation were performed.
- The synthetic fixture is not an independent LLM benchmark; it is a structural demonstration and test oracle.
- No production web/API connectors are implemented in the skill.

## Four-perspective review

### 1. Product and UX

**Pass with limitation.** The workflow starts from minimal input, separates a problem hypothesis from user validation, and ends with a concrete next action. Real participant research and ethics checks remain future live-work requirements.

### 2. Innovation and research

**Pass with limitation.** NUTS explicitly permits rejecting an analogy and avoids unsupported novelty claims. The fixture's status-display analogy is illustrative and unresearched; it does not prove NUTS' creative effectiveness.

### 3. Systems and software engineering

**Pass.** Stage IDs, artifact contracts, state, schemas, safe relative paths, and a deterministic validator provide a connected handoff chain. Host-specific skill discovery remains deferred.

### 4. AI quality and assurance

**Pass with limitation.** Tests establish structural integrity and negative-path handling. They do not measure model adherence, reasoning quality, source accuracy, or decision improvement. Those require actual runtime evaluations in B9/B10.

## Disposition

**B4 accepted as a structural vertical-slice milestone.** Do not label Peanuts ready for first use. Proceed to B5 only after the owner accepts the B4 scope and its explicit runtime limitations. The full remote/runtime release gate remains B10.

## Final local verification record (2026-11-01)

The final combined command `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python tools/verify.py --skip-lint` completed successfully in the managed Linux/Python 3.13.5 environment:

- Repository integrity and manifest coverage: PASS.
- B2 validation: 8 schemas and 19 evaluation cases PASS; temporary workspace lifecycle and negative checks PASS.
- B4 structural validator: PASS.
- Python unit/integration tests: 28 passed.
- Ruff: NOT RUN because Ruff is unavailable in this managed environment; CI installs the pinned development requirements and requires lint.
- GitHub Actions, Codespaces, Claude Code, Codex, and ChatGPT runtime: NOT RUN; no remote repository or eligible host execution was available.

A real evaluation-case schema mismatch was found and corrected: `EVAL-019.correct_disposition` had used `validate`, which is not part of the established evaluation disposition enum. It is now `ask`, meaning the next runtime step should request the user's help obtaining real user evidence. The sample Four-Council artifact's own `VALIDATE` recommendation is unchanged. The package manifest was regenerated after the correction.

The earlier combined verification timeout was an orchestration/overall execution-limit issue, not a reproducible failing test suite. In the final isolated combined run, all requested checks passed with the explicit Ruff skip.
