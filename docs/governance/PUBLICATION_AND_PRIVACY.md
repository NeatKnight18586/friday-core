# Publication, Licensing, and Privacy Baseline

**Status:** B1 repository policy draft  
**Version:** 0.3.0-draft

## 1. Visibility

The owner intends Friday for public distribution under ADR-046. Prepare reusable source for that destination while keeping publication gated by license/rights, privacy and release review. Private staging is optional for remote tests; it is not the final product requirement. A private repository is not a complete privacy boundary: collaborators, integrations, automation, archives and account permissions still matter.

## 2. Preserve the existing MIT license

Stage 2 read-only inspection of the owner's public Friday repository found an MIT license, copyright 2026 Mark Jemiel Guevarra. The source checkpoint preserves that existing license verbatim in `LICENSE`; this is an existing owner choice, not a new grant selected by the assistant. Before public release, confirm ownership/third-party notices and check that references/assets can be distributed. Do not assume that “Steal Like an Artist” or NUTS permits copying protected expression.

## 3. Data separation

Do not store the following in the shared capability repository:

- API keys, passwords, access tokens, private keys, session cookies, or credentials.
- Personal-memory exports or sensitive personal profiles.
- Private conversations or confidential project documents.
- Identifiable participant recordings, transcripts, contact details, or research datasets.
- Third-party content that cannot legally or contractually be redistributed.

Keep private project workspaces and research participant data in appropriately protected locations. Commit only reusable methods/templates that contain no sensitive or confidential information.

## 4. Research participant data

Before collecting research data, define purpose, minimization, access, retention/deletion, sharing, consent, and applicable legal/institutional requirements. Use anonymized or pseudonymized notes where appropriate. Never upload identifiable data to an AI tool unless the participant information, applicable rules, service terms, and user's authorization allow it.

## 5. Repository hygiene

Use `.gitignore`, review staged changes before committing, and use secret scanning/push protection when available. A `.gitignore` file does not remove a secret already committed. If a secret is exposed, revoke/rotate it immediately and remove it from history using an appropriate procedure; deletion from the latest commit alone is insufficient.

## 6. External publication gate

Before making the repository public, review: license, contributor/third-party rights, source citations, personal data, secrets, generated files, dependency licenses, private examples, contact/security reporting details, and whether all claims are suitable for public release. Publishing requires explicit owner authorization.
