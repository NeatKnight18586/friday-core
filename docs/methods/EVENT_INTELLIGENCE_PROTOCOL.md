# Event Intelligence Protocol

**Status:** B5 method specification  
**Version:** 0.1.0-draft  
**Applies to:** Hackathons, competitions, grants, accelerators, open calls, challenge programs

## 1. Purpose

Establish the event's actual requirements and constraints before recommending a project. This protocol prevents disqualification, deadline mistakes, invented judging criteria, and solution ideas that do not fit the challenge.

## 2. Source hierarchy

Use, in order where applicable:

1. Current official rulebook, terms, or submission portal.
2. Current official event page and FAQ.
3. Dated announcements from the organizer's verified channels.
4. Sponsor/partner material for sponsor-specific requirements.
5. Reputable reporting for context.
6. Community posts and social comments only as leads to verify.

The source must match the event edition. A prior-year rulebook is historical context, not proof of current rules. If only a third-party page is accessible, state that official verification is pending.

## 3. Intelligence checklist

- Identity: organizer, event name, edition, theme, track, geography, format.
- Eligibility: age/status, geography, institution, team size, team composition, disqualifications.
- Timeline: registration, kickoff, mentoring, submission, judging, demo and awards; timezone included.
- Challenge: tracks, themes, problem statements, target domains, sponsor briefs.
- Deliverables: prototype, code, deck, demo, report, video, repo, deployment, file formats and limits.
- Judging: criteria, official weights, scoring gates, presentation rules.
- Technology: required/allowed/prohibited platforms, AI tools, APIs, datasets, hardware, internet/connectivity.
- IP and disclosure: ownership, licenses, attribution, third-party assets, AI-use declaration, data and consent terms.
- Operations: venue, equipment, connectivity, support, submission portal, fallback demonstration.

## 4. Requirement status

Each material requirement receives one status:

- `confirmed` — explicitly supported by an inspected applicable official source.
- `interpreted` — reasonable reading, but wording is not fully explicit; flag for confirmation if consequential.
- `conflicting` — credible sources disagree.
- `not_found` — not found in the inspected sources; do not assume permitted or prohibited.
- `not_checked` — not yet investigated.

Record requirement ID, exact wording/summary, category, source ID, page/section, access date, implication, deadline/timezone if relevant, and follow-up action.

## 5. Judging criteria and scoring

Copy published criteria and weights faithfully. If the organizer does not publish weights, use qualitative alignment notes and clearly label them as analysis. Do not invent judge preferences, infer hidden criteria from prior winners without qualification, or combine event compliance with product merit. A disqualifying rule breach is a gate; it must not be averaged into a score.

## 6. Conflict resolution

For a material conflict:

1. Quote or summarize the conflicting statements and identify their sources.
2. Compare source authority, edition, publication date, and whether one supersedes the other.
3. Mark the requirement `conflicting` until resolved.
4. Prepare one precise organizer question.
5. Do not recommend a build path that depends on the favorable interpretation without disclosure.

## 7. Deadline discipline

Record exact date/time/timezone and the source. If a page states only a date, do not invent a cutoff time. Retain the original timezone. Recheck all high-impact deadlines before submission and record the recheck time.

## 8. Exit criteria

Event research is ready for concept work when eligibility, deadline, challenge/track, deliverables, judging, technology, AI-use and IP requirements have been checked or explicitly recorded as unresolved with an owner/action. Missing information is not the same as a confirmed absence of a rule.

## 9. Output

Use `skills/peanuts/assets/templates/event-dossier.md`. The dossier is a research artifact, not legal advice and not a guarantee of eligibility. Ask the organizer or qualified adviser where required.
