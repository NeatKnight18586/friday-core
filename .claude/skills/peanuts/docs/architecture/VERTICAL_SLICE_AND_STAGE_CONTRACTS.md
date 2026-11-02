# B4 — Vertical Slice and Stage Contracts

**Status:** B4 prototype specification and synthetic fixture delivered; host runtime verification pending.

## Purpose

B4 proves that Peanuts' minimum workflow can carry an opportunity through a connected set of artifacts and persistent records. It is a vertical slice, not the full product-discovery, NUTS, Four-Council, or PRD engine.

## Prototype scope

- Canonical skill prototype: `skills/peanuts/SKILL.md`.
- Skill-specific references: `skills/peanuts/references/`.
- Self-contained sample templates: `skills/peanuts/assets/templates/`.
- Synthetic demonstration: `examples/vertical-slice-synthetic/campus-service-status/`.
- Run contract: `schemas/vertical-slice-run.schema.json`.
- Deterministic validator: `tools/validate_vertical_slice.py`.
- Test coverage: `tests/test_vertical_slice.py` and `evals/cases/EVAL-019.json`.

## Stage interface

| Stage | Contract | Exit evidence |
|---|---|---|
| P1 | Intake and event/idea dossier | Input, mode, constraints, source records, unknowns |
| P2 | Problem brief | User/need hypothesis, current behavior/alternatives, evidence status |
| P3 | NUTS check | Analogy card or documented decision not to retain an analogy |
| P4 | Concept brief | Candidate, value, MVP boundary, alternatives, assumptions |
| P5 | Quick Four-Council | Four perspectives, scores/confidence, critical findings, disposition |
| P6 | Assumption validation | Research/test plan and real evidence or explicit awaiting-user state |
| P7 | Draft PRD | Traceable draft requirements and acceptance criteria |

A stage artifact is not, by itself, proof that the stage is complete. The quality gate and required evidence must be satisfied. P7 may exist as a draft while P6 is unresolved; the PRD must remain unapproved.

## Synthetic fixture boundary

The `campus-service-status` example is fictional. It tests record schemas, references, artifact paths, stage accounting, synthetic-data labels, and a fresh-session handoff. It does not verify event research, user need, concept novelty, actual staff workflow, model behavior, or platform integration.

## Host-runtime boundary

The skill follows the portable Agent Skills `SKILL.md` pattern. Native discovery paths and host-specific execution are not tested in B4. Claude Code, Codex, ChatGPT Skills, and manual ChatGPT Project use must be separately verified in B9/B10. A structurally valid skill is not proof of reliable model execution.

## Commands

```bash
python tools/validate_vertical_slice.py
python -m pytest -q tests/test_vertical_slice.py
python tools/verify.py --skip-lint
```

The full `tools/verify.py` command also runs Ruff; CI installs the pinned dependencies and must execute the full suite.
