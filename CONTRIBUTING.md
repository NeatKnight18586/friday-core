# Contributing to Friday

This repository is initially owner-maintained with AI assistance. Contributions should preserve clarity, evidence, privacy, and maintainability.

## Change workflow

1. Identify the problem or decision the change addresses.
2. Read the relevant Constitution, architecture decision records, method specifications, and roadmap.
3. Prefer the smallest change that resolves the issue.
4. State files affected, rationale, trade-offs, and any new dependency or permission.
5. Update related links, source register, decision record, manifest, and tests.
6. Run the repository checks available at the current milestone.
7. Record limitations and unresolved questions; do not imply an unrun test passed.

## Documentation standards

- Explain jargon on first use when the target reader is a beginner.
- Distinguish normative standards, empirical research, practitioner frameworks, vendor guidance, and Peanuts experiments.
- Attribute ideas and cite primary/authoritative sources where possible.
- Record date/version for time-sensitive sources.
- Avoid unsupported “best,” “proven,” “unique,” or “guaranteed” claims.
- Keep one canonical version of each method; link rather than duplicate.
- Keep documents focused; move detailed methods to a reference when the main guide becomes hard to navigate.

## File and code standards

- UTF-8 text, LF line endings, final newline.
- Use stable IDs for decisions, claims, requirements, and tests when traceability needs them.
- Avoid secrets, personal memory exports, participant identifiers, and private project records.
- Scripts added later must have clear usage, safe defaults, bounded behavior, and useful error messages.
- Dependencies require a reason, version/maintenance review, license check, and fallback assessment.

## Commit convention

Use concise conventional-style messages when commits are introduced, such as `docs: refine user research protocol` or `chore: add repository scaffold`. Do not combine unrelated changes into one commit.

## Review checklist

- Is the change aligned with the Constitution and an identified need?
- Are method prerequisites and limitations respected?
- Are factual claims traceable?
- Are security/privacy implications considered?
- Do links and references still work?
- Are relevant tests/quality checks run and accurately reported?
- Is the resulting architecture simpler or materially more capable without unnecessary complexity?

## B2 project records and evaluation

- Project data defaults to ignored `local-workspace/projects/`; keep it out of Git unless the owner explicitly approves a sanitized artifact.
- Validate generic schemas/templates/evaluation cases with `python tools/validate_b2.py`.
- Validate a workspace with `python tools/validate_project.py <project-dir>`.
- Install the development dependency with `python -m pip install -r requirements-dev.txt`.
- Never fabricate evaluation results. Cases and results are separate records.
- If a JSON Schema changes incompatibly, update `schema_version`, migration guidance, templates, and regression cases.

## Test and incident reporting

Follow `docs/governance/DEVELOPMENT_INCIDENT_PROTOCOL.md`. Report timeouts, missing dependencies, and unrun checks honestly. Preserve acceptance criteria and add regression tests for corrected defects.
