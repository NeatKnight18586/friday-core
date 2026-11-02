"""Semantic rules for B7 council-review and assumption-test records."""
from __future__ import annotations

from collections.abc import Iterable


def _ids(records: Iterable[dict], key: str) -> set[str]:
    return {row.get(key) for row in records if isinstance(row, dict) and row.get(key)}


def _check_refs(refs: list[dict], lookup: dict[str, set[str]], label: str, errors: list[str]) -> None:
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        kind, record_id = ref.get("record_type"), ref.get("record_id")
        if kind in lookup and record_id not in lookup[kind]:
            errors.append(f"{label}: missing {kind} reference {record_id}")
        elif kind == "artifact" or kind == "external_requirement":
            # These references are documented project artifacts or external
            # requirements and are not necessarily JSONL ledger records.
            if not record_id:
                errors.append(f"{label}: {kind} reference requires a record_id")


def validate_b7_records(
    *, council_reviews: list[dict], assumption_tests: list[dict], assumptions: list[dict],
    sources: list[dict], claims: list[dict], decisions: list[dict],
    research_findings: list[dict], opportunities: list[dict], analogies: list[dict], nuts_runs: list[dict], project_id: str | None = None,
) -> list[str]:
    """Return semantic cross-record and progression-gate errors."""
    errors: list[str] = []
    lookup = {
        "source": _ids(sources, "source_id"),
        "claim": _ids(claims, "claim_id"),
        "assumption": _ids(assumptions, "assumption_id"),
        "decision": _ids(decisions, "decision_id"),
        "research_finding": _ids(research_findings, "finding_id"),
        "opportunity": _ids(opportunities, "opportunity_id"),
        "analogy": _ids(analogies, "analogy_id"),
        "nuts_run": _ids(nuts_runs, "run_id"),
        "test": _ids(assumption_tests, "test_id"),
    }
    assumption_by_id = {row.get("assumption_id"): row for row in assumptions if isinstance(row, dict)}

    completed_by_assumption: dict[str, list[dict]] = {}
    for row_no, test in enumerate(assumption_tests, start=1):
        if not isinstance(test, dict):
            continue
        label = f"records/assumption-tests.jsonl:{row_no}"
        assumption_id = test.get("assumption_id")
        if assumption_id not in assumption_by_id:
            errors.append(f"{label}: missing assumption reference {assumption_id}")
        if test.get("status") == "completed":
            completed_by_assumption.setdefault(assumption_id, []).append(test)
            result = test.get("result") or {}
            _check_refs(result.get("evidence_refs", []), lookup, f"{label}.result", errors)
        controls = test.get("participant_controls") or {}
        if controls.get("involves_human_participants") and test.get("status") in {"approved", "in_progress", "completed"}:
            if controls.get("consent_status") != "obtained":
                errors.append(f"{label}: human-participant tests require obtained consent before approval/execution")
            if controls.get("deidentification_confirmed") is not True:
                errors.append(f"{label}: human-participant tests require de-identification")
            if controls.get("ethics_review_status") not in {"approved", "not_required"}:
                errors.append(f"{label}: human-participant tests require resolved ethics-review status")

    for row_no, assumption in enumerate(assumptions, start=1):
        if not isinstance(assumption, dict):
            continue
        status = assumption.get("status")
        completed = completed_by_assumption.get(assumption.get("assumption_id"), [])
        outcomes = {((row.get("result") or {}).get("outcome")) for row in completed}
        if status == "supported" and "supports" not in outcomes:
            errors.append(f"records/assumptions.jsonl:{row_no}: supported status requires a completed supporting test")
        if status == "invalidated" and "invalidates" not in outcomes:
            errors.append(f"records/assumptions.jsonl:{row_no}: invalidated status requires a completed invalidating test")

    review_ids: set[str] = set()
    for row_no, review in enumerate(council_reviews, start=1):
        if not isinstance(review, dict):
            continue
        label = f"records/council-reviews.jsonl:{row_no}"
        review_id = review.get("review_id")
        if project_id and review.get("project_id") != project_id:
            errors.append(f"{label}: project_id does not match project.json")
        if review_id in review_ids:
            errors.append(f"{label}: duplicate review_id {review_id}")
        review_ids.add(review_id)

        evidence_pack = review.get("evidence_pack") or {}
        for key, kind in [("source_ids", "source"), ("claim_ids", "claim"), ("assumption_ids", "assumption"), ("decision_ids", "decision")]:
            for record_id in evidence_pack.get(key, []):
                if record_id not in lookup[kind]:
                    errors.append(f"{label}.evidence_pack: missing {kind} reference {record_id}")

        for council_key, council in (review.get("councils") or {}).items():
            if not isinstance(council, dict):
                continue
            for dimension, assessment in (council.get("dimensions") or {}).items():
                if not isinstance(assessment, dict):
                    continue
                dlabel = f"{label}.{council_key}.{dimension}"
                score = assessment.get("score")
                evidence_status = assessment.get("evidence_status")
                if score == "UNKNOWN" and evidence_status not in {"UNKNOWN", "NOT_ASSESSED"}:
                    errors.append(f"{dlabel}: UNKNOWN score requires UNKNOWN or NOT_ASSESSED evidence status")
                if score == "N_A" and not assessment.get("na_reason"):
                    errors.append(f"{dlabel}: N_A score requires an applicability reason")
                _check_refs(assessment.get("evidence_refs", []), lookup, dlabel, errors)

        finding_by_id = {}
        for finding in review.get("findings", []):
            if not isinstance(finding, dict):
                continue
            fid = finding.get("finding_id")
            if fid in finding_by_id:
                errors.append(f"{label}: duplicate finding_id {fid}")
            finding_by_id[fid] = finding
            _check_refs(finding.get("evidence_refs", []), lookup, f"{label}.{fid}", errors)

        overlay = review.get("event_alignment") or {}
        mandatory_event_blockers: set[str] = set()
        for criterion in overlay.get("criteria", []):
            if not isinstance(criterion, dict):
                continue
            criterion_label = f"{label}.event_alignment.{criterion.get('criterion_id')}"
            _check_refs(criterion.get("evidence_refs", []), lookup, criterion_label, errors)
            if criterion.get("status") in {"compliant", "partial", "noncompliant"} and not criterion.get("evidence_refs"):
                errors.append(f"{criterion_label}: assessed criterion requires evidence")
            if criterion.get("mandatory") and criterion.get("status") in {"partial", "noncompliant", "unknown"}:
                linked_id = criterion.get("linked_finding_id")
                linked = finding_by_id.get(linked_id)
                expected_severity = "critical" if criterion.get("status") == "noncompliant" else "high"
                if not linked:
                    errors.append(f"{criterion_label}: mandatory unresolved criterion requires a linked blocking finding")
                else:
                    mandatory_event_blockers.add(linked_id)
                    if linked.get("severity") != expected_severity or linked.get("status") != "open" or linked.get("risk_domain") != "mandatory_compliance":
                        errors.append(f"{criterion_label}: linked finding must be open {expected_severity} mandatory_compliance")

        gate = review.get("gate") or {}
        blockers = set(gate.get("blocking_finding_ids", []))
        for blocker in blockers:
            if blocker not in finding_by_id:
                errors.append(f"{label}.gate: unknown blocking finding {blocker}")
        unresolved = {
            fid for fid, finding in finding_by_id.items()
            if finding.get("severity") in {"critical", "high"} and finding.get("status") == "open"
        }
        unresolved.update(mandatory_event_blockers)
        if unresolved and gate.get("status") != "blocked":
            errors.append(f"{label}.gate: unresolved critical/high findings require a blocked gate")
        if not unresolved.issubset(blockers):
            missing = sorted(unresolved - blockers)
            errors.append(f"{label}.gate: unresolved critical/high findings missing from blockers: {', '.join(missing)}")
        accepted_high = [f for f in finding_by_id.values() if f.get("severity") == "high" and f.get("status") == "accepted_with_rationale"]
        if accepted_high and gate.get("status") == "pass":
            errors.append(f"{label}.gate: accepted high findings require pass_with_conditions, not pass")
        if accepted_high and not gate.get("conditions"):
            errors.append(f"{label}.gate: accepted high findings require explicit gate conditions")
        if gate.get("status") in {"pass", "pass_with_conditions"} and blockers:
            errors.append(f"{label}.gate: a passing gate cannot retain blocking_finding_ids")
        if review.get("verdict") == "ADVANCE" and (unresolved or gate.get("status") not in {"pass", "pass_with_conditions"}):
            errors.append(f"{label}: ADVANCE requires a passing gate and no unresolved critical/high finding")
        if review.get("verdict") == "STOP" and gate.get("status") != "blocked":
            errors.append(f"{label}: STOP verdict requires a blocked gate")
        setup = review.get("reviewer_setup") or {}
        if setup.get("statistical_independence_claim") is True:
            errors.append(f"{label}.reviewer_setup: Four-Council lenses cannot claim statistical independence")
        if gate.get("status") == "blocked" and not blockers:
            errors.append(f"{label}.gate: blocked gate requires at least one blocking finding ID")
        nonblocking = blockers - unresolved
        if nonblocking:
            errors.append(f"{label}.gate: blocker list contains resolved/nonblocking findings: {', '.join(sorted(nonblocking))}")
        criterion_ids = [c.get("criterion_id") for c in overlay.get("criteria", []) if isinstance(c, dict)]
        if len(criterion_ids) != len(set(criterion_ids)):
            errors.append(f"{label}.event_alignment: duplicate criterion_id")

    return errors
