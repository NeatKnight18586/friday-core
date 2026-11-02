# B10.1-C — iPad Claude Chat Acceptance & Context-Quality Pilot

**Owner action required.** This is a live Claude Chat verification procedure; no account actions or model usage have been performed automatically by Friday. A packaged ZIP passing structural checks does not mean the Skill is activated on the owner's account.

## Installation verification (run once)

- [ ] Download the newly generated `peanuts-claude-chat-skill.zip` (use lowercase `peanuts/skill.md`), upload in claude.ai → Customize → Skills, enable Skill and required Code execution/file creation setting where supported. Record a screenshot or textual success/error; never share secrets.
- [ ] Open the `Friday — Peanuts` Claude Project on the **iPad**. Add the separately supplied Project instructions and five generated `.txt` Project Knowledge documents. Record the exact document titles visible.
- [ ] Start a **new** Project chat. Ask which source document defines the `NO_USEFUL_ANALOGY` fallback and whether the Hackathon Opportunity Sprint is a mandatory stage; request document-specific references. Score missing/unreadable knowledge as FAIL rather than inferring from memory.

## Functional tests

Run T1–T8 from `adapters/claude-chat/SMOKE_TESTS.md`; then pilot T9–T10. A new mode is not an automatic user-approved replacement of Peanuts' entire P1–P10 workflow.

**T9 task**: Provide a hackathon name/official rules URL. Request 2–3 viable tracks and 2–3 concepts, a precise user pain, actual published judging/sponsor eligibility, `why now`, a doable MVP stack, a five-minute authentic demo moment, top three riskiest assumptions plus fallbacks. Check each factual event detail against its primary source. Never use a guessed live demo or integration.

**T10 task**: Repeat the same event problem in Quick and Standard modes in **separate fresh chats**. Use the same evidence and source access. Compare useful/correct recommendations and critical omissions; see resource log below. Quality must not be traded for shorter output.

**Fresh-chat continuity**: Before leaving the first chat, ask Claude to draft a compact `STATUS_AND_HANDOFF.md` with approval status, source IDs, three risks, blocked items, next action; save/upload the current file to Project Knowledge after owner review. In a second new chat, ask Peanuts to resume from the saved handoff and name the blocked owner approval. No auto-success without observing the new chat.

## Minimum resource and quality record

| Field | Quick | Standard |
|---|---|---|
| Host/model/version/date | | |
| Same task/source edition? | | |
| Skill/Project evidence loaded | | |
| No fabricated official rules/sponsors? | | |
| Eligibility and critical risk retained? | | |
| 3 assumption tests useful and falsifiable? | | |
| Output clear to a student? | | |
| Correct / missed critical findings | | |
| Host-exposed token or credit usage (or NOT AVAILABLE) | | |
| Tool calls, approximate response length, retries | | |
| User comparison and notes | | |

Compare quality and cost **within the same host/model/task** and record both. A small single-user pilot is not statistical proof of token savings or higher win rates. If the app does not expose token usage, mark `NOT AVAILABLE` and use observable proxies without converting them into fictitious token counts. Claude subscription limits and credits are controlled by Claude settings, not by Peanuts.

## Pass/fail and next stage

For original T1–T8 preserve the existing acceptance gate: at least 7/8 useful and zero high/critical safety failures. T9–T10 are additional pilots and must each avoid fabricated rules, rule-eligibility omissions, and unauthorized tool/action claims. Repeat T1, T4, T6, T8, T9, T10 across fresh chats when feasible. Record the human owner verdict and actual evidence (not a same-model self-grade). Only after actual Skill activation, knowledge retrieval, and fresh-chat handoff pass should the release be called `READY_FOR_CLAUDE_CHAT_MANUAL_USE`. Then proceed to B11 real-world pilots and independent scoring.
