# Concept Brief — Campus Service Status Board

> **SYNTHETIC TEST DATA — proposed concept only; no user validation.**

**Concept ID:** CON-0001  
**Status:** PROPOSED FOR VALIDATION

## 1. One-sentence concept

A simple, staff-updated page showing whether a selected campus service counter is open, paused, or operating with limited service, so students can check before visiting.

## 2. Intended user and problem

Students planning a visit; the underlying uncertainty problem remains an untested hypothesis.

## 3. Value proposition

Offer a low-complexity way to see a current service status before travelling to a counter.

## 4. How it works

A staff member updates a small set of status states. Students view the latest status and its update timestamp. The prototype avoids exact wait-time predictions, student accounts, and personal queue records.

## 5. Why this approach

It tests the smallest plausible value proposition—status visibility—without requiring queue algorithms or access to sensitive student information.

## 6. Alternatives

- Existing campus announcements or social channels.
- A static service-hours page.
- A shared spreadsheet or low-cost form.
- A full queue-management system (more complex and not justified yet).

## 7. NUTS influence

The general status-before-arrival pattern is a hypothesis, not a novel invention or validated mechanism transfer. See the analogy card.

## 8. MVP boundary

One service, a few manually updated status states, visible last-updated time, and a simple student-facing page.

## 9. Critical assumptions

- Students experience the problem often enough to care (`ASM-0001`).
- Staff can keep status current without unacceptable burden.
- Existing channels do not already solve the problem adequately.

## 10. Recommendation

Prototype only after brief student/staff discovery. If the problem or update workflow is weak, pivot or stop rather than adding features.
