# B5 Four-Council Review — Research and Product Discovery

**Status:** Structural/method-specification review completed with bounded limitations  
**Date:** 2026-11-01  
**Scope:** Research Protocol, Event Intelligence Protocol, User Research Protocol, Evidence Synthesis Protocol, skill references/templates, B5 schemas/records, project validation, and evaluation cases EVAL-020–EVAL-030.

## 1. Executive verdict

**Verdict: PASS WITH BOUNDED LIMITATIONS.**

B5 establishes a coherent research and product-discovery foundation. It adds decision-led research planning, event requirement verification, participant selection and consent safeguards, evidence synthesis, triangulation, persistent research records, cross-record validation, and synthetic evaluation cases.

This review does not establish that Peanuts has performed actual event research, recruited/interviewed users, verified real-world facts, achieved research saturation, or improved model performance. The skill's research execution still depends on tools available in its host runtime. Evaluation cases are structurally validated and marked `ready`; no live-model evaluation results are claimed.

## 2. Four-Council assessment

Scores are qualitative judgments about the B5 specification and structural implementation, not benchmark scores. The councils are review perspectives, not four independent human reviewers or statistically independent AI runs.

| Council | Score | Verdict | Principal finding |
|---|---:|---|---|
| Event Intelligence and Research Strategy | 8.7/10 | Pass with improvements | Strong official-source hierarchy, edition/deadline discipline, decision-led coverage and conflict handling. Add more event-specific negative cases as B5 is exercised. |
| UX Research and Ethics | 8.6/10 | Pass with safeguards | Participant selection, neutral interviewing, consent, privacy, local review and segment limitations are covered. Local law/institutional review must be checked for each real study; GOV.UK is a practice reference, not Philippine legal advice. |
| Evidence/Data Architecture | 8.5/10 | Pass | Source/claim/question/round/finding/opportunity records and cross-record links provide traceability. Schema validation is not evidence validation; sensitive raw material remains outside Git. |
| AI Quality and Method Fidelity | 8.3/10 | Pass with limitations | Stale/conflicting sources, false triangulation, synthetic-user claims, small samples and consent failures are represented in evaluation cases. Cases have not yet been run against Claude/ChatGPT. |

## 3. What passed review

### Research discipline
- Research begins with a decision and answerable questions, not indiscriminate searching.
- Source authority is claim-specific; official event rules are distinguished from user-demand evidence.
- Time-sensitive event requirements record edition, source and timezone.
- Inaccessible, stale, conflicting and unverified information cannot be silently promoted to fact.
- Crossref is treated as a scholarly metadata discovery service, not full-text access or a study-quality judgment.

### User research integrity
- Desk research, generated personas and hypothetical user journeys are not called direct validation.
- Participant selection, inclusion/exclusion, recruitment rationale, selection bias, accessibility and language are specified.
- Neutral prompts focus on concrete past behavior and workarounds.
- Consent, recording, data minimization, withdrawal, retention, pseudonymous IDs and sensitive-participant escalation are included.
- UK GOV.UK guidance is clearly qualified as an operational practice reference, not local legal advice.

### Evidence synthesis
- Observation, participant statement, source-reported fact, interpretation and recommendation are separated.
- Contradictory findings, divergent segments and common-origin/source-dependence risks are preserved.
- Triangulation is not reduced to counting links.
- Research sufficiency is decision-based and time-boxed; repeated search results are not called saturation.

### Data and structural checks
- Project research plans, questions, rounds, findings and opportunities have schemas and starter templates.
- The project initializer creates the B5 research files.
- The validator checks schema validity, duplicate IDs, source/claim/question/round/finding/opportunity references, and that findings linked to a research round refer only to questions assigned to that round.
- Participant-derived finding records require a round, pseudonymous participant reference and confirmed consent.
- A finding's research-question links must belong to its referenced round; participant references must be listed in that round's pseudonymous participant list.
- Completed research rounds require resolved consent and an acceptable local-review disposition; where review is declared not required, rationale is required.

## 4. Issues found and corrections made

1. **B5 evaluation tests asserted against error-message wording.** Updated assertions to check the schema error's actual property path (`absolute_path`) rather than assuming the validator's prose contains a field name.
2. **Research finding consent rationale was not enforced.** Added `consent_rationale` and a conditional requirement when a finding declares consent not applicable with rationale.
3. **Completed research-round local review was underconstrained.** Completed rounds now require an approved or confirmed-not-required local-review disposition; a rationale is required where review is declared not applicable/not required.
4. **Finding/round question linkage was underconstrained.** The project validator now checks that question IDs attached to a finding belong to its linked research round.
5. **Peanuts skill workflow numbering duplicated step 3.** Corrected the Problem Brief stage to step 4.
6. **Tool registry/version and project/evaluation documentation were stale.** Updated the B5 registry review date, project record model description, evaluation library count, build roadmap and changelog.

## 5. Test coverage and results

B5 deterministic checks cover:

- Five B5 JSON schemas and record templates.
- Evaluation cases EVAL-020–EVAL-030.
- Initialized research workspace and empty-record validity.
- Valid linked source/claim/question/round/finding/opportunity records.
- Dangling question/claim, finding, plan and round-question references.
- User-statement consent requirements.
- Completed research-round consent and local-review requirements.
- Recovery after negative test cases.

Final local validation on Python 3.13.5/Linux (2026-11-01):

- `python tools/validate_repo.py`: PASS.
- `python tools/validate_b2.py`: PASS.
- `python tools/validate_vertical_slice.py`: PASS.
- `python tools/validate_b5.py`: PASS.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q`: 35 passed.
- `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python tools/verify.py --skip-lint`: PASS WITH SKIPS; all validators and 35 tests passed; Ruff explicitly not run.
- Package manifest coverage, sizes and SHA-256 values: checked after regeneration.

A test case marked `ready` means it is prepared for a model evaluation, not that a model passed it. Ruff was not executable in the managed environment; GitHub Actions, Codespaces, Windows/macOS runners, and live Claude/Codex/ChatGPT model runtimes have not been run.

## 6. Residual limitations / follow-up

- No real event research or direct user/field research was conducted as part of B5.
- No participant consent files, recordings or identifiable data were collected; private storage is only specified, not implemented as a secure participant-management service.
- No Philippine legal opinion or institutional ethics approval is provided. Real research must check applicable local law, school/event policy, and qualified review.
- Research tools such as Crossref are documented as candidates; no dedicated API connector or automated academic-search agent is implemented.
- Source reliability, finding quality, and research completeness require human/model evaluation; JSON Schema can only check structure.
- Evaluation cases have not been run against a live Claude, Codex or ChatGPT Peanuts runtime.

## 7. References

- GOV.UK, Plan user research: https://www.gov.uk/service-manual/user-research/plan-user-research-for-your-service
- GOV.UK, Informed consent: https://www.gov.uk/service-manual/user-research/getting-users-consent-for-research
- Crossref REST API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Claude Agent Skills: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- OpenAI Skills in ChatGPT: https://help.openai.com/en/articles/20001066-skills-in-chatgpt

---

**Final B5 disposition:** Accept the research/discovery foundation for progression to B6. Preserve the limitations above and do not treat any user-research, factual, or live-model evaluation claim as complete without actual evidence.
