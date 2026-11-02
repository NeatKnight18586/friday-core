# Peanuts Context and Resource Procedure

**Canonical policy:** `docs/architecture/CONTEXT_ENGINEERING.md` and `docs/governance/RESOURCE_BUDGETS.md`.

## Load only what the current task needs

1. Use the current request and selected project state first.
2. Load Peanuts `SKILL.md` when this capability is selected.
3. Load only the relevant stage reference(s): event intelligence, user discovery, evidence synthesis, NUTS, or Four-Council.
4. Read source passages/records only when they affect a material claim or decision.
5. Run deterministic validators/scripts where useful; return concise results with paths and record IDs.
6. Use the compact project handoff for continuation. Do not replay the entire conversation by default.

## Modes

- **Fast** (`fast`, stored as `quick`): exploration; selected skill plus normally no more than one supporting reference. Label preliminary or unverified findings.
- `standard`: default; decision-led research and selective references. Use the normal evidence/quality gates.
- `deep`: for consequential decisions or explicit requests; load all relevant evidence and methods, use deeper review and testing. Do not load unrelated project or capability files.

The counts are starting targets, not hard limits. Escalate when risk, uncertainty, or missing evidence requires it. Never drop a safety or evidence requirement to save context.

## Cost-aware quality gate (all hosts)

Reuse inspected findings and approved decisions. Begin with the smallest decision-changing output; do not commission deep research, a full Four-Council or multiple model passes for ordinary first-pass brainstorming. Escalate if hard event requirements are unknown, decisive facts conflict, critical user/safety risks arise, or the owner needs a commitment-ready result. A shorter response is not automatically a cheaper or better one: count retries and omitted critical findings. Prefer one verified answer over many plausible guesses. Never silently skip consent, source integrity, eligibility or approval gates. Claude app subscription usage is not controllable by an ordinary Skill; turn off unused tools and monitor the host's Usage display. Exact tokens/cost only when actually exposed. Compare quality and usage on the *same* model/host/task before claiming savings.

## Friday capability boundary

Peanuts is one independent capability in Friday's catalog. Friday provides the Stage 2 read-only selector/intake helper and host-mediated instructions; it does not execute capabilities autonomously. Do not assume Peanuts owns general writing, coding, or unrelated tasks. If another capability is registered, host-available, and genuinely needed, use its declared interface and pass a compact handoff rather than loading every capability. If no suitable capability exists, state the gap or help directly without pretending a tool exists.

## Growth and metadata discipline

Do not install or auto-discover every future Friday capability by default. Keep host skill metadata curated. The registry is a small catalog and source of truth; it is not the full knowledge base and must not be pasted wholesale into every task. If capability count grows, filter metadata before reading any skill body. Autonomous coordination remains deferred; the explicit selector loads only the chosen capability.

## Measurement honesty

Record exact token usage only when the host exposes it. Word/character counts, number of files read, and tool calls are proxies, not token counts. Do not promise a fixed percentage of provider-credit savings.

## Compact continuation

Use planning-handoff.md only when delivering/resuming the dossier. It defines two files instead of duplicating a full ledger set for early exploration. Formal P7–P9 records and approvals remain unchanged. A shorter entrypoint reduces static words/characters, not proven host tokens or cost.
