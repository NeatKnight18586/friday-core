# Friday / Peanuts — Release Status

**Version:** 0.15.0-rc.2  
**Release class:** `STAGE_2_CHECKPOINT` — minimal capability selection/intake and CI/host preflight.  
**Intended audience:** people building projects and reusable AI capabilities across supported hosts, including iPad users.

## Implemented

- Peanuts prototype: evidence-led discovery, selective NUTS inspiration, Four-Council critique, Quick/Standard/Deep guidance, project records and planning handoffs.
- Read-only capability selector, dry-run intake validation, per-package contract and manual `Friday-Manager.txt` adapter; metadata catalog, schemas, project initialization, validators/tests and source manifest.
- Repository-local Codex/Claude Code discovery snapshots, Claude consumer export and ChatGPT Project manual export.

## Planned, not implemented

- Stage 3: simpler Peanuts context/output and portable dossier handoff.
- Stage 4: actual cross-host behavior and comparative method evaluation.
- Stage 5: optional user-reviewed private profile import, correction/export/deletion.
- Stage 6: public release acceptance, third-party rights review, focused onboarding and community/security files.

See [revision stages](docs/plans/REVISION_STAGES.md) and ADR-046/047/048 in [current decisions](docs/architecture/DECISIONS.md).

## Readiness boundaries

[RELEASE_VERIFICATION.md](RELEASE_VERIFICATION.md) is the authority for commands and observed results. Package/install simulation does not establish real host discovery, tool availability, memory persistence, recovery, output quality or credit savings. Configured consumer Projects, actual CLI model behavior and independent calibration remain unverified. Hosted CI status is recorded for each commit in [GitHub Actions](https://github.com/NeatKnight18586/friday-core/actions/workflows/ci.yml). The actual Codex CLI smoke attempt is BLOCKED by authentication; workflow lint passes and clean-container outcomes are recorded in delivery evidence. See [preflight](docs/acceptance/CI_AND_HOST_PREFLIGHT.md).

The owner selected the new public `NeatKnight18586/friday-core` repository for a clean source history. The older Friday repository remains separate. GitHub's branch head and Actions results are authoritative for the published commit and its checks. The MIT license already present in the owner's GitHub repository is preserved in this source. Third-party rights and release review remain pending. A private staging repository is an optional testing route, not the product's intended final visibility. Nothing in this checkpoint authorizes uploading personal documents to the public source or claiming universal support.
