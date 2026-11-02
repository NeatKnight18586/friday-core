# Product Requirements Document — Draft 0.1

> **SYNTHETIC TEST DATA — illustrative draft; not an approved product baseline.**

**Project:** Campus Service Status Board  
**Baseline approved:** NO  
**Decision gate:** VALIDATE (P5); P6 user/operational validation pending.

## 1. Executive summary

A hypothetical one-service status page may help students check current availability before visiting. The problem is unvalidated; this PRD exists to define a testable prototype, not authorize full development.

## 2. Problem and evidence

The fictional brief requests service-visit planning support. Actual student uncertainty, frequency, and severity remain unknown (`CLM-0002`).

## 3. Target users

- Primary hypothesis: students planning to visit one administrative service counter.
- Operational stakeholder: staff member responsible for status updates.

## 4. Goals and non-goals

**Goals:** Test whether a simple current-status signal is understandable and operationally maintainable.

**Non-goals:** Accounts, student records, exact wait-time prediction, queue ranking, payments, and real campus integrations.

## 5. Key flow

Staff updates a status state and timestamp; student opens a public page and sees the selected service status, update time, and a stale/unknown message when freshness expires.

## 6. Functional requirements

| ID | Requirement | Origin | Priority | Acceptance criteria | Status |
|---|---|---|---|---|---|
| REQ-001 | Display one service's current status from a staff-entered value. | CLM-0001; ASM-0001 | Must | Given a saved valid status, the public page displays the same status. | Draft |
| REQ-002 | Display when the status was last updated. | CF-002 | Must | Page displays a human-readable timestamp for the last successful update. | Draft |
| REQ-003 | Warn when the status exceeds a configured freshness period. | CF-002 | Must | A stale record is labelled stale/unknown and is not presented as current. | Draft |
| REQ-004 | Avoid collecting student personal identifiers in the prototype. | Fictional brief constraint | Must | No student account, ID, or case-detail field exists in the tested flow. | Draft |

## 7. Non-functional considerations

- Clear status language and readable contrast.
- Basic accessibility testing with keyboard and screen-reader considerations.
- Minimal data retention.
- Manual update failure must fail visibly, not silently.

## 8. Constraints and dependencies

The fictional brief permits a low-cost software prototype. Real hosting, authentication, campus integration, and event rules are unknown.

## 9. Risks and assumptions

- ASM-0001 is untested.
- Staff update burden is untested.
- The status freshness threshold needs user/staff input.
- Existing alternatives and differentiation are unresearched.

## 10. Validation plan

Conduct appropriately consented, exploratory interviews about recent service visits and current alternatives. Then test a low-fidelity prototype with relevant students and staff. Record limitations; do not claim statistical representativeness.

## 11. Success measures

Provisional measures for a later test: comprehension of status, ability to identify stale status, staff update completion, and whether the information changes a real visit decision. Numeric thresholds must be set after understanding the context, not invented here.

## 12. Open decisions

- Whether to proceed after user discovery.
- Who owns status updates.
- How to determine freshness/expiry.
- Whether the status page duplicates an existing channel.
