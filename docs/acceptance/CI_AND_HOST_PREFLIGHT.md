# Reducing CI and host risk before public release

**Reviewed:** 2026-11-02. This extends the staged plan in response to the owner's request to catch host/CI problems early. Local tests cannot guarantee all future accounts, products or operating systems.

## Method

Use layers of evidence rather than treating one simulated pass as universal support:

1. Verify source/package integrity, contracts and meaningful negative tests.
2. Validate workflow syntax/expressions with actionlint and verify pinned upstream action commits exist.
3. In clean containers, install the pinned dependencies and run the full verifier on the declared Python versions. Do not pass account tokens or personal files into containers. Record resolved image digests, Python versions, source ZIP hash, commands and failures.
4. Use actual CLI non-interactive runs where installed and authenticated. Run bounded synthetic tasks with minimal permissions, collect events/output/exit status, and inspect the actual trace for skill loading, evidence boundaries and recovery. No trace or failed login means BLOCKED, not a behavioral pass.
5. Run the real GitHub matrix on the reviewed source commit in an authorized branch/repository. Confirm all jobs actually complete for that exact SHA. Workflow lint and Linux containers do not exercise hosted permissions, action setup/cache, macOS or Windows.
6. Test consumer Skill/Project installation and fresh-chat continuity in each actual account/surface. API/CLI success cannot substitute for an iPad app test. Where account access is unavailable, keep the route experimental and supply the shortest possible owner-side test.

## Stage 2 pre-publication observations

The observations below describe the pre-publication audit for 0.15.0-rc.1. The owner subsequently authorized replacing main with the full source and removing the tracked ZIP. See [GitHub Actions](https://github.com/NeatKnight18586/friday-core/actions/workflows/ci.yml) for hosted checks on the current commit.

- Codex CLI 0.163.0 is installed. `codex login status` reported ChatGPT login, but the actual read-only synthetic Peanuts invocation failed with an unrefreshable-token/401 error. No model response or Peanuts method execution occurred. This is an authentication blocker, not evidence that Peanuts failed its workflow. Do not copy another application's credentials or disable permissions to make it pass.
- Claude Code is not installed and no authenticated Claude consumer UI is available in this build. No Claude behavior pass is claimed.
- Docker runs here; a clean Python image was successfully pulled and launched. Final clean-container verification outcomes and immutable resolved image digests are recorded in the delivery evidence.
- actionlint 1.7.12 was downloaded from its upstream release and its release checksum verified. It passed the current workflow. Both pinned GitHub Action commits resolve upstream.
- Read-only inspection found a public `NeatKnight18586/Friday` repository and no Actions runs. Its root contains source files and the unopened ZIP, but no nested tools/skills/workflow directories, explaining why the workflow is absent remotely. The existing MIT LICENSE is preserved verbatim in this checkpoint. That is not evidence that this checkpoint is installed there. This stage does not push to or modify that remote. GitHub-hosted CI for this source remains NOT RUN until a reviewed commit is uploaded and the workflow completes.

The Stage 1 statement that no remote repository exists is historical build scope; it must not be repeated as a current account fact. The owner intends public distribution, but a source-upload authorization for this specific checkpoint is separate from preparing it locally. The existing main branch and license must be preserved; test a reviewed complete source tree on a separate branch first.

## Reproducible CLI smoke command

Use a disposable checkout and actual authenticated Codex session. Supply the synthetic prompt from the delivery evidence or [the cross-host smoke guide](CROSS_HOST_SMOKE_TEST_PROMPTS.md); never inject secrets into it.

```bash
codex exec --ephemeral --skip-git-repo-check --sandbox read-only --json -C /path/to/disposable/friday -o /path/to/evidence/answer.txt - < /path/to/evidence/prompt.txt
```

A successful login-status check alone is insufficient. Require a successful turn, evidence of relevant instruction loading, useful task output and a separate fresh-session handoff test. The actual attempt here is retained as BLOCKED. No credentials are bundled with the evidence. Do not run unattended against unreviewed uploaded code or weaken sandbox/approval controls.

## Sources and limits

- [OpenAI non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode): scripted `codex exec`, event output and automation. Applicable to CLI, not consumer Project UI.
- [Claude Code programmatic use](https://code.claude.com/docs/en/headless): `claude -p`, structured output and exit/failure behavior. A possible future authenticated route; not exercised here.
- [actionlint upstream](https://github.com/rhysd/actionlint): static workflow checker, not execution of hosted Actions.
- [act's documented unsupported behavior](https://nektosact.com/not_supported.html): local workflow emulation is incomplete; permissions, concurrency and timeouts differ. For this checkpoint, clean Python containers plus actionlint were chosen over implying `act` proves hosted CI.

Remaining release risks: actual host/account activation, untrusted-content response quality, consumer retrieval/recovery, remote matrix behavior and comparative usefulness. Each requires its own evidence. No workaround honestly removes the need for those tests.


## Clean-container harness recovery

The first container attempts could not read a restrictive host-mounted archive; the harness was changed to transfer source through stdin with no host filesystem mounts. Direct container dependency downloads then hit this environment's untrusted-intermediary TLS certificate. TLS verification was not disabled. The recovery downloads version-specific wheels through the host's functioning verified package connection, records their SHA-256 hashes, transfers them with the source, and installs inside network-disabled containers using `--no-index`. This checks clean dependency installation and execution, not container network/TLS configuration or GitHub's package index connectivity. Initial failures are preserved separately from final results.
