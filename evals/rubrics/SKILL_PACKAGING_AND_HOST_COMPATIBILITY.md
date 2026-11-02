# Skill Packaging and Host Compatibility Rubric

**Rubric ID:** SKILL_PACKAGING_AND_HOST_COMPATIBILITY  
**Version:** 1.0.0-draft  
**Owner:** Friday / Peanuts  
**Status:** B9 starter rubric; runtime calibration pending

## Purpose

Evaluate whether a capability is packaged from one canonical source, discoverable at the documented host path, honest about host limits, secure to install, and usable without inflating context or duplicating method logic.

## Scoring dimensions (0–4 each)

| Dimension | 0 — Fail | 1 — Weak | 2 — Partial | 3 — Good | 4 — Strong |
|---|---|---|---|---|---|
| Portable specification fidelity | Invalid/missing metadata or structure | Significant spec violations | Basic format but metadata/path issues remain | Valid structure and metadata | Valid, minimal, portable, version-aware package |
| Canonical-source integrity | Hand-maintained divergent copies | Duplication likely | Mostly copied but drift checks absent | Generated copies and parity checks | Deterministic generation, manifest, drift and regression checks |
| Host discovery correctness | Wrong/misleading install path | Path is vague or surface-confused | Some paths correct | Paths and guidance match official docs | Per-surface path/availability/permissions explicitly verified |
| Context/progressive disclosure | Monolithic context dump | Weak navigation and excessive duplication | Basic references | Clear map, selective loading | Evidence-preserving, measured/maintainable context selection |
| ChatGPT fallback honesty | Claims native activation/execution without support | Omits major plan/surface limits | Mentions manual fallback but under-specifies | Correct Project instructions and file plan | Adapted to actual plan/device limits, continuity and tool constraints |
| Security and trust boundaries | Unsafe scripts, secret leakage, broad permissions | Incomplete source/ZIP/path audit | Basic safe packaging | Path, symlink, content and permission checks | Threat-aware install, provenance, rollback and least privilege |
| Evaluation quality | No cases | Happy-path only | Some negative cases | Positive, negative and adversarial cases | Cases cover compatibility, drift, resource, recovery and real runtime boundaries |

## Interpretation

- Critical failures in portability, path safety, secret handling, or false capability claims are non-compensatory blockers; a high average cannot offset them.
- Packaging success proves artifact structure and copy integrity only. It does not establish host discovery, tool availability, instruction adherence, factual correctness, or user value.
- A runtime pass requires an actual fresh-session execution in the named host/surface with version, permissions, tool access, date, expected behavior, observed behavior, and limitations recorded.
- Four perspectives reviewing this rubric are not statistically independent reviewers. Use human and host-level evidence where stakes justify it.
