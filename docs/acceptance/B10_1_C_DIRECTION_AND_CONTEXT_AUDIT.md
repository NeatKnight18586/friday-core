# B10.1-C Preflight — Direction, Quality-per-Context, Hackathon Sprint

**Status:** Preflight engineering changes complete only after recorded tests; actual Claude-chat runtime acceptance remains **NOT RUN** until the owner runs it in the installed Skill/Project. This file is a review by one model adopting four professional perspectives, **not** four independent experts and not a measured field result.

## Four-lens scrutiny

**1. Product and hackathon strategy — Conditional PASS.** Missing feature: compact bridge from verified event rules and tracks to problem/solution shortlist and actual demo. Corrective action: add an event-triggered pathway P1–P6. Refuse a universal default, sponsor-weight mythology, and track lock-in before user pain is understood. Evidence is sufficient to design the pathway, **not** to prove competition outcomes. Formal organizer rules always outrank a reusable rank formula.

**2. Applied AI/context engineer — PASS WITH MEASUREMENT GAP.** Existing B6.5 hierarchy, Quick/Standard/Deep, selective loading and compact handoff are sound architectural defaults. Avoid per-host custom token gateway and always-on background model/council. The objective is quality per context, not simply minimum tokens. Introduce an ordinary-language short first deliverable and escalation triggers. Measure same-host quality, tool calls, elapsed work and exact usage only if the host exposes it; no claimed savings before repeatable field results.

**3. Systems and portability architect — PASS WITH LIVE-HOST GAP.** Existing canonical skill, generated adapters, schemas, ledgers and manifest are sufficient groundwork. Files/folders organize instructions and state; they do not themselves supply agent reasoning, authorization, fresh information, execution or persistent user-specific memory. Add the method to canonical docs and generate to all host packages rather than creating a new agent/router or Claude-only source. Keep Friday an umbrella and Peanuts independent.

**4. Red-team/QA and student usability — CONDITIONAL PASS.** Risks: copied event rules may be stale, unrelated inspiration may waste research, sponsor-fit scoring may hide disqualifying rules, premium AI usage could silently escalate, and multi-chat handoffs can lose approvals. Mitigations: hard eligibility gates, explicit unknowns, optional NUTS, 3 falsifiable assumption tests, plain-language one-page default, no hidden actions, session status/handoff, real owner test. No broad 'works everywhere' claim.

## Research note: file/folder agents

Anthropic's Agent Skills use dynamically loaded directories of instructions, resources and scripts. Zhou et al. (2026), *Filesystem-Based Memory for LLM Agents* (arXiv:2607.26637), found roughly lower retrieval cost in some organized memory settings but **did not find consistent better answers from organization alone**. Supermemory SMFS (May 2026) reports lower token use in its own benchmark; evaluate as vendor-reported evidence, not universally proven savings. The sober conclusion is to keep a small filesystem-backed skill plus handoff, not to introduce vector databases, specialized memory services or agent swarms for one student's first release.

## Live B10.1-C owner gates

1. Skill can actually upload, enable and trigger in ordinary Claude Chat on iPad; record version/model, exact UI evidence and any error.
2. Project instruction and Knowledge documents are attached and the relevant current source is retrievable; verify a fact unique to the uploaded file rather than assumed from conversation.
3. T1–T8 existing smoke suite; run new hackathon/efficiency tests from `adapters/claude-chat/SMOKE_TESTS.md`. Run new critical tests three times in fresh chats if feasible.
4. Fresh-chat resume from a saved, explicitly updated handoff; critical open assumptions and approval states remain intact.
5. Compare a short and detailed mode on the same scenario. Record actual tool calls, files referenced, response length, quality findings, and any host-exposed usage, but do not invent provider tokens.
6. No cross-provider 'guaranteed works' claim until actual Codex/Claude Code/ChatGPT checks run in those hosts.

**Release rule:** Package/static tests may pass while the owner-side `CLAUDE_CHAT_LIVE` gate remains BLOCKED. Never auto-mark it complete from this file.

## Sources

- Anthropic, Effective context engineering (2025): https://www.anthropic.com/research/effective-context-engineering-for-ai-agents
- Anthropic, Building effective AI agents: https://www.anthropic.com/research/building-effective-agents
- Anthropic, Agent Skills (2025): https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills
- Zhou et al., Filesystem-Based Memory for LLM Agents (2026): https://arxiv.org/abs/2607.26637
- Anthropic, Usage limit best practices: https://support.claude.com/en/articles/9797557-usage-limit-best-practices
- Devpost, judging criteria: https://info.devpost.com/blog/understanding-hackathon-submission-and-judging-criteria

## Managed test evidence (this build)

- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest` in six bounded module groups: **190/190 PASS** (11 initializer, 7 B5, 6 B6, 18 B7, 54 B8, 94 B9/B10/B10.1/shared and hackathon). All runs were local; group results are not model quality scores.
- `python tools/validate_repo.py`, `python tools/validate_b9.py`, `python tools/validate_claude_chat.py`, `python tools/inspect_context.py`: PASS in the authoring tree.
- Context proxies: Peanuts main entrypoint **1,929 words** under the existing 2,500-word soft budget; host root maps under 600 words. This does **not** measure actual tokens, subscription credits or context cost.
- The historical long-running consolidated `tools/verify.py` is not claimed as passed. Ruff, remote CI, live Claude/ChatGPT/Codex/Claude Code and owner-side iPad tests remain **NOT RUN** in this release.
- Existing T1–T8 gate is unchanged; T9/T10 are new pilots. The local tests verify documents/build source consistency and guardrails, **not** live model compliance, usefulness, cheaper credits, user demand or hackathon win rates.
