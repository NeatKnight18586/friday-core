from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator, FormatChecker

from tools.b8_rules import validate_b8_records

ROOT = Path(__file__).resolve().parents[1]
NOW = "2026-11-01T00:00:00Z"
B8_CASE_NUMBERS = tuple(range(62, 88))


def source_record(**overrides: Any) -> dict[str, Any]:
    row = {
        "source_id": "SRC-0001",
        "access_status": "accessed",
        "validity_status": "current",
        "assessment": {"authority": "high"},
    }
    row.update(overrides)
    return row


def requirement_record(**overrides: Any) -> dict[str, Any]:
    row = {
        "schema_version": "1.0.0",
        "requirement_id": "REQ-001",
        "title": "Export a project report",
        "statement": "The system shall export a project report as a readable PDF file.",
        "requirement_type": "functional",
        "priority": "must",
        "status": "approved",
        "release_scope": "mvp",
        "mandatory": False,
        "evidence_status": "verified",
        "origin_refs": [{"record_type": "source", "record_id": "SRC-0001"}],
        "rationale": "The requirement follows from the verified project constraint.",
        "acceptance_criteria": [{
            "criterion_id": "AC-001",
            "statement": "A valid project report can be exported as a readable PDF.",
            "verification_method": "test",
            "pass_condition": "The produced PDF opens and contains the expected report sections.",
        }],
        "depends_on": [],
        "conflicts_with": [],
        "owner": "project owner",
        "created_at": NOW,
        "updated_at": NOW,
        "approved_by": "project owner",
        "approved_at": NOW,
    }
    row.update(overrides)
    return row


def acceptance_test(**overrides: Any) -> dict[str, Any]:
    row = {
        "schema_version": "1.0.0",
        "test_id": "AT-001",
        "title": "Verify PDF report export",
        "test_type": "functional",
        "objective": "Verify that the project report export produces a readable PDF.",
        "criterion_refs": [{"requirement_id": "REQ-001", "criterion_id": "AC-001"}],
        "preconditions": ["A valid project report is available."],
        "steps": ["Export the report and open the resulting PDF."],
        "expected_result": "The exported PDF opens and contains the expected report sections.",
        "pass_condition": "The PDF opens and every required report section is present.",
        "test_data_strategy": "synthetic",
        "involves_human_participants": False,
        "contains_identifiable_personal_data": False,
        "status": "planned",
        "created_at": NOW,
        "updated_at": NOW,
        "owner": "test owner",
    }
    row.update(overrides)
    return row


def build_task(**overrides: Any) -> dict[str, Any]:
    row = {
        "schema_version": "1.0.0",
        "task_id": "TASK-001",
        "title": "Implement project report export",
        "phase": "implementation",
        "task_type": "feature",
        "objective": "Deliver the project report export behavior required for the MVP.",
        "deliverable": "A working report export function.",
        "requirement_ids": ["REQ-001"],
        "depends_on": [],
        "priority": "must",
        "status": "planned",
        "owner": "implementation owner",
        "sequence_index": 1,
        "exit_criteria": ["The export behavior passes the linked acceptance test."],
        "created_at": NOW,
        "updated_at": NOW,
    }
    row.update(overrides)
    return row


def validate(
    tmp_path: Path,
    *,
    requirements: list[dict[str, Any]] | None = None,
    tests: list[dict[str, Any]] | None = None,
    tasks: list[dict[str, Any]] | None = None,
    artifacts: list[dict[str, Any]] | None = None,
    demo_plan: dict[str, Any] | None = None,
    sources: list[dict[str, Any]] | None = None,
    claims: list[dict[str, Any]] | None = None,
    assumptions: list[dict[str, Any]] | None = None,
    decisions: list[dict[str, Any]] | None = None,
    findings: list[dict[str, Any]] | None = None,
    opportunities: list[dict[str, Any]] | None = None,
    analogies: list[dict[str, Any]] | None = None,
    nuts_runs: list[dict[str, Any]] | None = None,
    reviews: list[dict[str, Any]] | None = None,
    assumption_tests: list[dict[str, Any]] | None = None,
    evaluation_results: list[dict[str, Any]] | None = None,
    artifact_ledger_present: bool = True,
    state: dict[str, Any] | None = None,
) -> list[str]:
    resolved_artifacts = artifacts if artifacts is not None else []
    if demo_plan is not None and artifacts is None:
        (tmp_path / "demo-plan.json").write_text(json.dumps(demo_plan), encoding="utf-8")
        resolved_artifacts.append(artifact_record("demo-plan.json", artifact_type="demo_plan_data"))
    return validate_b8_records(
        project_dir=tmp_path,
        requirements=requirements if requirements is not None else [requirement_record()],
        acceptance_tests=tests if tests is not None else [acceptance_test()],
        build_tasks=tasks if tasks is not None else [build_task()],
        artifacts=resolved_artifacts,
        demo_plan=demo_plan,
        sources=sources if sources is not None else [source_record()],
        claims=claims if claims is not None else [],
        assumptions=assumptions if assumptions is not None else [],
        decisions=decisions if decisions is not None else [],
        findings=findings if findings is not None else [],
        opportunities=opportunities if opportunities is not None else [],
        analogies=analogies if analogies is not None else [],
        nuts_runs=nuts_runs if nuts_runs is not None else [],
        council_reviews=reviews if reviews is not None else [],
        assumption_tests=assumption_tests if assumption_tests is not None else [],
        evaluation_results=evaluation_results if evaluation_results is not None else [],
        artifact_ledger_present=artifact_ledger_present,
        state=state,
    )


def artifact_record(path: str, **overrides: Any) -> dict[str, Any]:
    row = {
        "schema_version": "1.0.0",
        "artifact_id": "ART-0001",
        "title": "Supporting research note",
        "artifact_type": "other",
        "path": path,
        "status": "draft",
        "version": "0.1.0",
        "owner": "project owner",
        "created_at": NOW,
        "updated_at": NOW,
    }
    row.update(overrides)
    return row


def test_baseline_valid_requirement_test_and_task_have_no_semantic_errors(tmp_path: Path) -> None:
    assert validate(tmp_path) == []


@pytest.mark.parametrize(
    ("evidence_status", "origin_refs", "source", "expected"),
    [
        ("assumption", [{"record_type": "source", "record_id": "SRC-0001"}], source_record(), "requires a linked assumption"),
        ("verified", [{"record_type": "source", "record_id": "SRC-0001"}], source_record(assessment={"authority": "low"}), "verified evidence needs"),
        ("supported", [{"record_type": "source", "record_id": "SRC-0001"}], source_record(assessment={"authority": "low"}), "supported evidence needs"),
        ("verified", [{"record_type": "source", "record_id": "SRC-MISSING"}], source_record(), "missing source reference"),
    ],
)
def test_requirement_evidence_claims_are_checked(
    tmp_path: Path, evidence_status: str, origin_refs: list[dict[str, str]], source: dict[str, Any], expected: str
) -> None:
    req = requirement_record(evidence_status=evidence_status, origin_refs=origin_refs)
    assert any(expected in error for error in validate(tmp_path, requirements=[req], sources=[source]))


def test_supported_requirement_accepts_supported_claim(tmp_path: Path) -> None:
    req = requirement_record(
        evidence_status="supported",
        origin_refs=[{"record_type": "claim", "record_id": "CLM-0001"}],
    )
    claim = {"claim_id": "CLM-0001", "evidence_status": "supported"}
    assert validate(tmp_path, requirements=[req], claims=[claim]) == []


def test_assumption_based_requirement_must_link_existing_assumption(tmp_path: Path) -> None:
    req = requirement_record(
        status="proposed", evidence_status="assumption",
        origin_refs=[{"record_type": "assumption", "record_id": "ASM-0001"}],
        approved_by=None, approved_at=None,
    )
    assert any("missing assumption reference ASM-0001" in e for e in validate(tmp_path, requirements=[req]))


def test_approved_mandatory_compliance_requires_strong_evidence(tmp_path: Path) -> None:
    req = requirement_record(
        requirement_type="legal_regulatory", mandatory=True, evidence_status="unknown",
        origin_refs=[{"record_type": "external_requirement", "record_id": "EXT-1", "note": "A claimed policy source."}],
    )
    errors = validate(tmp_path, requirements=[req])
    assert errors


def test_requirement_dependency_cycles_and_missing_refs_are_blocked(tmp_path: Path) -> None:
    first = requirement_record(requirement_id="REQ-001", depends_on=["REQ-002"])
    second = requirement_record(requirement_id="REQ-002", depends_on=["REQ-001"])
    errors = validate(tmp_path, requirements=[first, second])
    assert any("dependency cycle" in e for e in errors)


def test_requirement_conflicts_must_be_reciprocal_and_not_both_approved(tmp_path: Path) -> None:
    first = requirement_record(requirement_id="REQ-001", conflicts_with=["REQ-002"])
    second = requirement_record(requirement_id="REQ-002", conflicts_with=[])
    errors = validate(tmp_path, requirements=[first, second])
    assert any("reciprocally" in e for e in errors)
    second["conflicts_with"] = ["REQ-001"]
    errors = validate(tmp_path, requirements=[first, second])
    assert any("cannot both be approved" in e for e in errors)


def test_superseded_requirement_reference_must_resolve(tmp_path: Path) -> None:
    req = requirement_record(supersedes_requirement_id="REQ-099")
    assert any("superseded requirement REQ-099 not found" in e for e in validate(tmp_path, requirements=[req]))


def test_approved_criterion_requires_active_linked_test_and_build_task(tmp_path: Path) -> None:
    errors = validate(tmp_path, tests=[], tasks=[])
    assert any("has no active linked acceptance-test specification" in e for e in errors)
    assert any("has no build task" in e for e in errors)


def test_acceptance_test_must_reference_a_real_criterion(tmp_path: Path) -> None:
    test = acceptance_test(criterion_refs=[{"requirement_id": "REQ-001", "criterion_id": "AC-999"}])
    assert any("criterion AC-999 is not defined" in e for e in validate(tmp_path, tests=[test]))


def test_test_status_and_execution_result_cannot_disagree(tmp_path: Path) -> None:
    test = acceptance_test(execution={"outcome": "pass"})
    assert any("only permitted when status=executed" in e for e in validate(tmp_path, tests=[test]))
    test = acceptance_test(status="executed", execution=None)
    assert any("executed status requires a result" in e for e in validate(tmp_path, tests=[test]))


def test_human_participant_tests_require_consent_and_review_before_ready(tmp_path: Path) -> None:
    test = acceptance_test(
        involves_human_participants=True,
        participant_controls={
            "consent_status": "pending", "ethics_review_disposition": "pending",
            "data_minimization": "Collect only responses required for the test.",
            "retention_and_access": "Restrict access and delete recordings on the stated date.",
            "withdrawal_plan": "Participants may stop and request data withdrawal.",
        },
        status="ready",
    )
    errors = validate(tmp_path, tests=[test])
    assert any("before consent is obtained" in e for e in errors)
    assert any("review disposition is resolved" in e for e in errors)


def test_consent_withdrawal_cancels_test_and_personal_data_is_forbidden(tmp_path: Path) -> None:
    test = acceptance_test(
        involves_human_participants=True,
        participant_controls={
            "consent_status": "withdrawn", "ethics_review_disposition": "approved",
            "data_minimization": "Collect only responses required for the test.",
            "retention_and_access": "Restrict access and delete recordings on the stated date.",
            "withdrawal_plan": "Participants may stop and request data withdrawal.",
        },
        status="ready", contains_identifiable_personal_data=True,
    )
    errors = validate(tmp_path, tests=[test])
    assert any("withdrawn consent requires status=cancelled" in e for e in errors)
    assert any("identifiable personal data" in e for e in errors)


def test_not_required_ethics_review_needs_rationale_for_execution(tmp_path: Path) -> None:
    test = acceptance_test(
        involves_human_participants=True,
        participant_controls={
            "consent_status": "obtained", "ethics_review_disposition": "not_required",
            "ethics_review_rationale": "", "data_minimization": "Only necessary feedback is collected.",
            "retention_and_access": "Store deidentified notes in access-controlled storage.",
            "withdrawal_plan": "Participants may withdraw before synthesis.",
        },
        status="executed",
        execution={"outcome": "pass", "executed_at": NOW, "executed_by": "researcher",
                   "evidence_refs": [{"record_type": "source", "record_id": "SRC-0001"}],
                   "limitations": ["Small convenience sample."],
        },
    )
    assert any("not_required ethics disposition requires a rationale" in e for e in validate(tmp_path, tests=[test]))


def test_task_dependencies_require_order_and_completed_prerequisites(tmp_path: Path) -> None:
    first = build_task(task_id="TASK-001", sequence_index=1, status="planned")
    second = build_task(task_id="TASK-002", sequence_index=2, depends_on=["TASK-001"], status="ready")
    errors = validate(tmp_path, tasks=[first, second])
    assert any("cannot be ready while dependency TASK-001 is not completed" in e for e in errors)
    second["sequence_index"] = 1
    assert any("sequence_index must be later" in e for e in validate(tmp_path, tasks=[first, second]))


def test_task_cycle_and_missing_dependency_are_blocked(tmp_path: Path) -> None:
    first = build_task(task_id="TASK-001", sequence_index=1, depends_on=["TASK-002"])
    second = build_task(task_id="TASK-002", sequence_index=2, depends_on=["TASK-001"])
    assert any("dependency cycle" in e for e in validate(tmp_path, tasks=[first, second]))
    assert any("missing task dependency TASK-404" in e for e in validate(tmp_path, tasks=[build_task(depends_on=["TASK-404"])]))


def test_completed_task_needs_real_completion_evidence(tmp_path: Path) -> None:
    task = build_task(status="completed", completion_evidence_refs=[])
    assert any("completed task needs" in e for e in validate(tmp_path, tasks=[task]))
    task["completion_evidence_refs"] = [{"record_type": "acceptance_test", "record_id": "AT-001"}]
    assert any("not an executed passing test" in e for e in validate(tmp_path, tasks=[task]))


def test_artifact_path_must_exist_and_stay_inside_workspace(tmp_path: Path) -> None:
    assert any("path must be a normalized relative path" in e for e in validate(tmp_path, artifacts=[artifact_record("../outside.md")]))
    assert any("file does not exist" in e for e in validate(tmp_path, artifacts=[artifact_record("missing.md")]))
    (tmp_path / "safe.md").write_text("safe", encoding="utf-8")
    good = artifact_record("safe.md", sha256=hashlib.sha256(b"safe").hexdigest())
    assert validate(tmp_path, artifacts=[good]) == []
    bad_hash = artifact_record("safe.md", sha256="0" * 64)
    assert any("SHA-256 mismatch" in e for e in validate(tmp_path, artifacts=[bad_hash]))


def test_artifact_symlink_escape_is_rejected(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-outside.md"
    outside.write_text("outside", encoding="utf-8")
    link = tmp_path / "linked.md"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("Symlinks are not available on this platform")
    assert any("symlink paths are not accepted" in e for e in validate(tmp_path, artifacts=[artifact_record("linked.md")]))


def test_artifact_paths_are_unique_case_insensitively(tmp_path: Path) -> None:
    (tmp_path / "one.md").write_text("same", encoding="utf-8")
    (tmp_path / "ONE.md").write_text("same", encoding="utf-8")
    rows = [artifact_record("one.md", artifact_id="ART-0001"), artifact_record("ONE.md", artifact_id="ART-0002")]
    assert any("case-insensitive check" in e for e in validate(tmp_path, artifacts=rows))


def test_only_one_active_primary_artifact_per_type(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("draft", encoding="utf-8")
    (tmp_path / "b.md").write_text("draft", encoding="utf-8")
    rows = [
        artifact_record("a.md", artifact_type="prd", artifact_id="ART-0001"),
        artifact_record("b.md", artifact_type="prd", artifact_id="ART-0002"),
    ]
    assert any("Multiple active prd artifacts" in e for e in validate(tmp_path, artifacts=rows))
    rows[0]["status"] = "superseded"
    assert not any("Multiple active prd artifacts" in e for e in validate(tmp_path, artifacts=rows))


def test_artifact_refs_in_b7_reviews_decisions_and_assumption_tests_resolve(tmp_path: Path) -> None:
    review = {"dimensions": {"product": {"evidence_refs": [{"record_type": "artifact", "record_id": "ART-9999"}]}}}
    decision = {"evidence_refs": [{"record_type": "artifact", "record_id": "ART-8888"}]}
    assumption_test_record = {"result": {"evidence_refs": [{"record_type": "artifact", "record_id": "ART-7777"}]}}
    errors = validate(tmp_path, reviews=[review], decisions=[decision], assumption_tests=[assumption_test_record])
    assert sum("missing artifact reference" in e for e in errors) >= 3
    errors_legacy = validate(
        tmp_path, reviews=[review], decisions=[decision], assumption_tests=[assumption_test_record],
        artifact_ledger_present=False,
    )
    assert not any("missing artifact reference" in e for e in errors_legacy)


def demo_plan(**overrides: Any) -> dict[str, Any]:
    row = {
        "schema_version": "1.0.0", "project_id": "demo", "status": "draft",
        "objective": "Show the report export workflow.", "audience": "Project reviewers",
        "duration_minutes": 5, "core_scenario": "Export a synthetic report and inspect the result.",
        "environment_prerequisites": ["A clean demo environment is available."],
        "steps": [{"step_id": "DEMO-01", "narration": "Explain the report flow.",
                   "action": "Run the synthetic report flow.",
                   "expected_observation": "The exported file appears in the output folder.",
                   "requirement_ids": ["REQ-001"]}],
        "demo_claims": [], "data_strategy": "synthetic",
        "privacy_and_safety_controls": ["Use synthetic data and remove credentials."],
        "failure_plan": {"trigger": "The export fails.", "response": "Explain the failure honestly.",
                         "fallback": "Show the failure state.", "stop_condition": "Do not claim success."},
        "limitations_to_disclose": ["This is not production evidence."],
        "owner": "project owner", "created_at": NOW, "updated_at": NOW,
    }
    row.update(overrides)
    return row


def test_demo_plan_cannot_reference_unknown_requirement(tmp_path: Path) -> None:
    plan = demo_plan(steps=[{"step_id": "DEMO-01", "narration": "Show flow", "action": "Run flow",
                            "expected_observation": "A report appears", "requirement_ids": ["REQ-404"]}])
    assert any("missing requirement reference REQ-404" in e for e in validate(tmp_path, demo_plan=plan))


def test_demo_measured_claim_needs_measured_evidence(tmp_path: Path) -> None:
    plan = demo_plan(demo_claims=[{"claim": "The report export is 40 percent faster.",
                                   "claim_strength": "measured", "evidence_refs": []}])
    assert any("measured claim requires" in e for e in validate(tmp_path, demo_plan=plan))


def test_generic_passing_functional_test_cannot_support_measured_demo_claim(tmp_path: Path) -> None:
    test = acceptance_test(
        test_type="functional", status="executed",
        execution={"outcome": "pass", "executed_at": NOW, "executed_by": "tester",
                   "evidence_refs": [{"record_type": "source", "record_id": "SRC-0001"}],
                   "limitations": ["The test checks output existence, not performance." ]},
    )
    plan = demo_plan(demo_claims=[{"claim": "The report export is 40 percent faster.",
                                   "claim_strength": "measured",
                                   "evidence_refs": [{"record_type": "acceptance_test", "record_id": "AT-001"}]}])
    errors = validate(tmp_path, tests=[test], demo_plan=plan)
    assert any("measured claim requires" in e for e in errors)


def test_measured_demo_claim_accepts_performance_test_with_reviewed_result_artifact(tmp_path: Path) -> None:
    (tmp_path / "demo-plan.json").write_text("{}", encoding="utf-8")
    (tmp_path / "measurements.json").write_text('{"latency_ms": 120}', encoding="utf-8")
    measurement_artifact = artifact_record("measurements.json", artifact_id="ART-0002", status="reviewed")
    structured_demo = artifact_record("demo-plan.json", artifact_id="ART-0001", artifact_type="demo_plan_data")
    test = acceptance_test(
        test_type="performance", status="executed",
        execution={"outcome": "pass", "executed_at": NOW, "executed_by": "tester",
                   "evidence_refs": [{"record_type": "artifact", "record_id": "ART-0002"}],
                   "limitations": ["One controlled synthetic environment." ]},
    )
    plan = demo_plan(demo_claims=[{"claim": "The report export met the declared latency threshold.",
                                   "claim_strength": "measured",
                                   "evidence_refs": [{"record_type": "acceptance_test", "record_id": "AT-001"}]}])
    (tmp_path / "demo-plan.json").write_text(json.dumps(plan), encoding="utf-8")
    errors = validate(tmp_path, tests=[test], demo_plan=plan,
                      artifacts=[structured_demo, measurement_artifact])
    assert not any("measured claim requires" in e for e in errors)


def test_measured_demo_claim_accepts_measured_research_finding(tmp_path: Path) -> None:
    plan = demo_plan(demo_claims=[{"claim": "The measured result is 120 milliseconds.",
                                   "claim_strength": "measured",
                                   "evidence_refs": [{"record_type": "research_finding", "record_id": "FND-0001"}]}])
    finding = {"finding_id": "FND-0001", "evidence_label": "measured"}
    assert not any("measured claim requires" in e for e in validate(tmp_path, demo_plan=plan, findings=[finding]))


def test_demo_demonstrated_claim_rejects_draft_artifact_only_evidence(tmp_path: Path) -> None:
    (tmp_path / "prototype.md").write_text("Prototype sketch", encoding="utf-8")
    art = artifact_record("prototype.md", artifact_type="prototype", status="draft")
    plan = demo_plan(demo_claims=[{"claim": "The report export works.", "claim_strength": "demonstrated",
                                   "evidence_refs": [{"record_type": "artifact", "record_id": "ART-0001"}]}])
    assert any("reviewed or approved status" in e for e in validate(tmp_path, artifacts=[art], demo_plan=plan))


def test_demo_demonstrated_claim_accepts_passing_test(tmp_path: Path) -> None:
    test = acceptance_test(
        status="executed",
        execution={"outcome": "pass", "executed_at": NOW, "executed_by": "tester",
                   "evidence_refs": [{"record_type": "source", "record_id": "SRC-0001"}],
                   "limitations": ["Synthetic environment." ]},
    )
    plan = demo_plan(demo_claims=[{"claim": "The export flow passed the defined test.",
                                   "claim_strength": "demonstrated",
                                   "evidence_refs": [{"record_type": "acceptance_test", "record_id": "AT-001"}]}])
    assert validate(tmp_path, tests=[test], demo_plan=plan) == []


def test_demo_plan_project_id_must_match_workspace_state(tmp_path: Path) -> None:
    plan = demo_plan(project_id="different")
    assert any("project_id does not match" in e for e in validate(tmp_path, demo_plan=plan, state={"project_id": "demo"}))


def test_completed_stages_require_approved_artifacts(tmp_path: Path) -> None:
    errors = validate(tmp_path, state={"project_id": "demo", "completed_stages": ["P7"]})
    assert any("P7 is marked complete" in e for e in errors)


def test_non_applicable_demo_plan_can_satisfy_p9_when_upstream_gates_are_met(tmp_path: Path) -> None:
    required_headings = {
        "prd": ["Executive summary", "Problem and opportunity", "Target users and use context",
                "Jobs, needs, and user journeys", "Goals and measurable outcomes", "Non-goals and boundaries",
                "Scope and release slices", "Requirements and acceptance criteria",
                "Success measures and release decision", "Approval and limitations"],
        "technical_design": ["Purpose, design status, and scope", "System context and boundaries",
                "Architecture overview", "Components and responsibilities", "Data model and lifecycle",
                "Interfaces and contracts", "Security, privacy, safety, and abuse cases",
                "Reliability and failure handling", "Accessibility and human factors",
                "Observability and operations", "Verification and test strategy", "Alternatives and trade-offs",
                "Technical risks, assumptions, and unresolved questions", "Decisions and traceability",
                "Approval and limitations"],
        "build_plan": ["Delivery objective and definition of done", "In-scope and excluded work",
                "Work breakdown and ownership", "Sequence, milestones, and dependency logic",
                "Resources, estimates, and assumptions", "Quality and verification plan",
                "Risk reduction and contingency", "Communication and handoff", "Change control",
                "Release readiness and approval"],
        "demo_plan": ["Demo objective and audience", "Core scenario and story", "Timed walkthrough",
                "Proof points and evidence boundaries", "Environment and prerequisites",
                "Data, consent, privacy, and safety", "Failure and fallback plan",
                "Limitations and audience questions", "Readiness and approval"],
    }
    artifacts = []
    for index, (kind, headings) in enumerate(required_headings.items(), start=2):
        path = {"prd": "PRD.md", "technical_design": "TECHNICAL_DESIGN.md",
                "build_plan": "BUILD_PLAN.md", "demo_plan": "DEMO_PLAN.md"}[kind]
        (tmp_path / path).write_text("# Document\n\n" + "\n\n".join(f"## {heading}\nContent recorded." for heading in headings), encoding="utf-8")
        status = "draft" if kind == "demo_plan" else "approved"
        record = artifact_record(path, artifact_id=f"ART-{index:04d}", artifact_type=kind, status=status)
        if status == "approved":
            record.update(approved_by="owner", approved_at=NOW)
        artifacts.append(record)
    (tmp_path / "demo-plan.json").write_text("{}", encoding="utf-8")
    artifacts.append(artifact_record("demo-plan.json", artifact_id="ART-0006", artifact_type="demo_plan_data"))
    plan = demo_plan(status="not_applicable", not_applicable_rationale="No live demo is appropriate for this project.",
                     steps=[], demo_claims=[])
    errors = validate(tmp_path, artifacts=artifacts, demo_plan=plan,
                      state={"project_id": "demo", "completed_stages": ["P7", "P8", "P9"]})
    assert not any("P9 is marked complete" in e for e in errors)


def test_p8_cannot_be_marked_complete_before_p7(tmp_path: Path) -> None:
    errors = validate(
        tmp_path,
        state={"project_id": "demo", "completed_stages": ["P8"]},
        artifacts=[
            artifact_record("PRD.md", artifact_id="ART-PRD", artifact_type="prd", status="approved"),
            artifact_record("TECHNICAL_DESIGN.md", artifact_id="ART-TD", artifact_type="technical_design", status="approved"),
        ],
    )
    assert any("P8 is marked complete but prerequisite stage P7 is not complete" in e for e in errors)


def test_p9_cannot_bypass_p7_and_p8_approval_prerequisites(tmp_path: Path) -> None:
    errors = validate(tmp_path, state={"project_id": "demo", "completed_stages": ["P9"]})
    assert any("prerequisite stage P7 is not complete" in e for e in errors)
    assert any("prerequisite stage P8 is not complete" in e for e in errors)
    assert any("P9 is marked complete but prd is not approved" in e for e in errors)
    assert any("P9 is marked complete but technical_design is not approved" in e for e in errors)


def test_document_sections_and_approved_placeholder_scanning(tmp_path: Path) -> None:
    doc = tmp_path / "PRD.md"
    doc.write_text("# PRD\n\n## Executive summary\nTBD\n", encoding="utf-8")
    row = artifact_record("PRD.md", artifact_type="prd", status="approved",
                          approved_by="owner", approved_at=NOW)
    errors = validate(tmp_path, artifacts=[row])
    assert any("missing required section heading" in e for e in errors)
    assert any("unresolved placeholder" in e for e in errors)



def test_document_traceability_uses_identifier_boundaries(tmp_path: Path) -> None:
    (tmp_path / "PRD.md").write_text("# Product Requirements Document\n\nREQ-0010 is a different requirement. AC-0010 is a different criterion.\n", encoding="utf-8")
    first = requirement_record()
    second = requirement_record(
        requirement_id="REQ-0010", status="proposed", evidence_status="supported",
        origin_refs=[{"record_type": "source", "record_id": "SRC-0001"}],
        acceptance_criteria=[{
            "criterion_id": "AC-0010", "statement": "A separate requirement is recorded.",
            "verification_method": "inspection", "pass_condition": "The separate identifier is present.",
        }], approved_by=None, approved_at=None,
    )
    prd = artifact_record("PRD.md", artifact_type="prd")
    errors = validate(tmp_path, requirements=[first, second], artifacts=[prd])
    assert any("missing machine-record reference REQ-001" in e for e in errors)
    assert any("missing machine-record reference AC-001" in e for e in errors)


def test_duplicate_demo_step_ids_are_rejected(tmp_path: Path) -> None:
    plan = demo_plan(steps=[
        {"step_id": "DEMO-01", "narration": "Explain the first step.",
         "action": "Run the first action.", "expected_observation": "The expected output appears.",
         "requirement_ids": ["REQ-001"]},
        {"step_id": "DEMO-01", "narration": "Explain the second step.",
         "action": "Run the second action.", "expected_observation": "A second expected output appears.",
         "requirement_ids": ["REQ-001"]},
    ])
    errors = validate(tmp_path, demo_plan=plan)
    assert any("duplicate demo step ID DEMO-01" in e for e in errors)


def test_not_applicable_demo_cannot_contain_live_walkthrough_or_claims(tmp_path: Path) -> None:
    plan = demo_plan(
        status="not_applicable", not_applicable_rationale="A live demonstration is not suitable for this project.",
        demo_claims=[{"claim": "This is a claim.", "claim_strength": "hypothetical", "evidence_refs": []}],
    )
    errors = validate(tmp_path, demo_plan=plan)
    assert any("not_applicable demo plan must not contain" in e for e in errors)


def test_new_project_initializes_and_validates_b8_workspace(tmp_path: Path) -> None:
    workspace = tmp_path / "projects"
    created = subprocess.run(
        [sys.executable, str(ROOT / "tools/init_project.py"), "--id", "b8-project",
         "--title", "B8 Project", "--workspace-root", str(workspace)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert created.returncode == 0, created.stderr
    project = workspace / "b8-project"
    assert (project / "PRD.md").is_file()
    assert (project / "TECHNICAL_DESIGN.md").is_file()
    assert (project / "BUILD_PLAN.md").is_file()
    assert (project / "DEMO_PLAN.md").is_file()
    assert len((project / "records/artifacts.jsonl").read_text().splitlines()) == 6
    checked = subprocess.run(
        [sys.executable, str(ROOT / "tools/validate_project.py"), str(project)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert checked.returncode == 0, checked.stdout + checked.stderr


def test_legacy_workspace_without_b8_ledgers_remains_readable(tmp_path: Path) -> None:
    workspace = tmp_path / "projects"
    created = subprocess.run(
        [sys.executable, str(ROOT / "tools/init_project.py"), "--id", "legacy-project",
         "--title", "Legacy Project", "--workspace-root", str(workspace)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert created.returncode == 0, created.stderr
    project = workspace / "legacy-project"
    for name in ("requirements.jsonl", "acceptance-tests.jsonl", "build-tasks.jsonl", "artifacts.jsonl"):
        (project / "records" / name).unlink()
    (project / "demo-plan.json").unlink()
    checked = subprocess.run(
        [sys.executable, str(ROOT / "tools/validate_project.py"), str(project)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert checked.returncode == 0, checked.stdout + checked.stderr
    assert "legacy project" in checked.stdout



def test_acceptance_criterion_ids_are_scoped_to_each_requirement(tmp_path: Path) -> None:
    first = requirement_record(requirement_id="REQ-001")
    second = requirement_record(
        requirement_id="REQ-002", status="proposed", evidence_status="supported",
        origin_refs=[{"record_type": "source", "record_id": "SRC-0001"}],
        approved_by=None, approved_at=None,
    )
    # AC-001 is a local identifier within a requirement, not a repository-global key.
    assert not any("duplicate acceptance criterion" in e for e in validate(
        tmp_path, requirements=[first, second]
    ))


def test_duplicate_acceptance_criterion_within_one_requirement_is_rejected(tmp_path: Path) -> None:
    req = requirement_record(acceptance_criteria=[
        {"criterion_id": "AC-001", "statement": "A valid report is exported.",
         "verification_method": "test", "pass_condition": "The PDF opens correctly."},
        {"criterion_id": "AC-001", "statement": "A second criterion reuses the ID.",
         "verification_method": "inspection", "pass_condition": "The repeated ID is detected."},
    ])
    errors = validate(tmp_path, requirements=[req])
    assert any("duplicate acceptance criterion ID AC-001 within requirement REQ-001" in e for e in errors)


def test_approved_requirement_cannot_depend_on_unapproved_requirement(tmp_path: Path) -> None:
    dependency = requirement_record(
        requirement_id="REQ-002", status="proposed", evidence_status="supported",
        origin_refs=[{"record_type": "source", "record_id": "SRC-0001"}],
        approved_by=None, approved_at=None,
    )
    approved = requirement_record(depends_on=["REQ-002"])
    errors = validate(tmp_path, requirements=[approved, dependency])
    assert any("approved requirement depends on unapproved requirement REQ-002" in e for e in errors)


def test_in_progress_task_cannot_bypass_incomplete_dependency(tmp_path: Path) -> None:
    prerequisite = build_task(task_id="TASK-001", requirement_ids=["REQ-001"], sequence_index=1, status="planned")
    dependent = build_task(
        task_id="TASK-002", requirement_ids=["REQ-001"], depends_on=["TASK-001"],
        sequence_index=2, status="in_progress",
    )
    errors = validate(tmp_path, tasks=[prerequisite, dependent])
    assert any("task cannot be in_progress while dependency TASK-001 is not completed" in e for e in errors)


def test_blocked_and_cancelled_records_require_explanations_in_schemas() -> None:
    schema_pairs = [
        ("acceptance-test.schema.json", acceptance_test(status="blocked")),
        ("build-task.schema.json", build_task(status="cancelled")),
    ]
    for schema_name, record in schema_pairs:
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        assert any("status_reason" in error.message or "status_reason" in error.path
                   for error in validator.iter_errors(record))
        record["status_reason"] = "A documented condition prevents progress."
        assert not list(validator.iter_errors(record))


def test_artifact_hash_is_checked_against_current_file_bytes(tmp_path: Path) -> None:
    (tmp_path / "design.md").write_text("current content", encoding="utf-8")
    row = artifact_record("design.md", sha256=hashlib.sha256(b"old content").hexdigest())
    errors = validate(tmp_path, artifacts=[row])
    assert any("SHA-256 mismatch for design.md" in e for e in errors)


def test_full_project_b8_handoff_validates_end_to_end(tmp_path: Path) -> None:
    workspace = tmp_path / "projects"
    created = subprocess.run(
        [sys.executable, str(ROOT / "tools/init_project.py"), "--id", "traceable-project",
         "--title", "Traceable Project", "--workspace-root", str(workspace)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert created.returncode == 0, created.stderr
    project = workspace / "traceable-project"

    source = {
        "source_id": "SRC-0001", "title": "Official product constraint",
        "source_kind": "official_event", "publisher": "Project owner", "author": None,
        "url": None, "doi": None, "publication_date": None, "version": "current",
        "accessed_at": NOW, "access_status": "accessed", "validity_status": "current",
        "assessment": {
            "authority": "high", "directness": "primary", "recency": "current_for_claim",
            "context_fit": "high", "limitations": [],
        },
    }
    req = requirement_record()
    test = acceptance_test()
    task = build_task()
    (project / "records/sources.jsonl").write_text(json.dumps(source) + "\n", encoding="utf-8")
    (project / "records/requirements.jsonl").write_text(json.dumps(req) + "\n", encoding="utf-8")
    (project / "records/acceptance-tests.jsonl").write_text(json.dumps(test) + "\n", encoding="utf-8")
    (project / "records/build-tasks.jsonl").write_text(json.dumps(task) + "\n", encoding="utf-8")

    demo = json.loads((project / "demo-plan.json").read_text(encoding="utf-8"))
    demo["steps"] = [{
        "step_id": "DEMO-01", "narration": "Show the report export journey.",
        "action": "Export a synthetic project report.",
        "expected_observation": "A readable report file is produced.",
        "requirement_ids": ["REQ-001"],
    }]
    demo["demo_claims"] = [{
        "claim": "The walkthrough illustrates the proposed export journey.",
        "claim_strength": "illustrative", "evidence_refs": [],
    }]
    (project / "demo-plan.json").write_text(json.dumps(demo, indent=2) + "\n", encoding="utf-8")

    prd = project / "PRD.md"
    prd.write_text(prd.read_text(encoding="utf-8") + "\nRequirement REQ-001; criterion AC-001.\n", encoding="utf-8")
    design = project / "TECHNICAL_DESIGN.md"
    design.write_text(design.read_text(encoding="utf-8") + "\nApproved requirement REQ-001 is addressed in this provisional design.\n", encoding="utf-8")
    build = project / "BUILD_PLAN.md"
    build.write_text(build.read_text(encoding="utf-8") + "\nTask TASK-001 delivers REQ-001.\n", encoding="utf-8")
    demo_doc = project / "DEMO_PLAN.md"
    demo_doc.write_text(demo_doc.read_text(encoding="utf-8") + "\nWalkthrough DEMO-01 demonstrates REQ-001 illustratively.\n", encoding="utf-8")

    checked = subprocess.run(
        [sys.executable, str(ROOT / "tools/validate_project.py"), str(project)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert checked.returncode == 0, checked.stdout + checked.stderr


def test_full_project_b8_handoff_rejects_dangling_document_traceability(tmp_path: Path) -> None:
    workspace = tmp_path / "projects"
    created = subprocess.run(
        [sys.executable, str(ROOT / "tools/init_project.py"), "--id", "broken-traceability",
         "--title", "Broken Traceability", "--workspace-root", str(workspace)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert created.returncode == 0, created.stderr
    project = workspace / "broken-traceability"
    source = {
        "source_id": "SRC-0001", "title": "Official product constraint",
        "source_kind": "official_event", "accessed_at": NOW, "access_status": "accessed",
        "validity_status": "current",
        "assessment": {"authority": "high", "directness": "primary",
                       "recency": "current_for_claim", "context_fit": "high", "limitations": []},
    }
    (project / "records/sources.jsonl").write_text(json.dumps(source) + "\n", encoding="utf-8")
    req = requirement_record()
    (project / "records/requirements.jsonl").write_text(json.dumps(req) + "\n", encoding="utf-8")
    (project / "records/acceptance-tests.jsonl").write_text(json.dumps(acceptance_test()) + "\n", encoding="utf-8")
    (project / "records/build-tasks.jsonl").write_text(json.dumps(build_task()) + "\n", encoding="utf-8")

    checked = subprocess.run(
        [sys.executable, str(ROOT / "tools/validate_project.py"), str(project)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    assert checked.returncode == 1, checked.stdout + checked.stderr
    assert "PRD.md: missing machine-record reference REQ-001" in checked.stdout
    assert "TECHNICAL_DESIGN.md: missing machine-record reference REQ-001" in checked.stdout
    assert "BUILD_PLAN.md: missing machine-record reference TASK-001" in checked.stdout



def test_b8_evaluation_rubric_references_resolve() -> None:
    for number in B8_CASE_NUMBERS:
        path = ROOT / "evals/cases" / f"EVAL-{number:03d}.json"
        case = json.loads(path.read_text(encoding="utf-8"))
        for rubric_ref in case.get("rubric_refs", []):
            assert (ROOT / "evals/rubrics" / rubric_ref).is_file(), f"{path.name}: {rubric_ref}"


def test_b8_templates_and_evaluation_cases_are_schema_valid() -> None:
    # EVAL-087 is intentionally included; an exclusive upper bound of 87 would silently omit it.
    assert B8_CASE_NUMBERS[0] == 62 and B8_CASE_NUMBERS[-1] == 87 and len(B8_CASE_NUMBERS) == 26
    schema_files = [
        "requirement-record.schema.json", "acceptance-test.schema.json",
        "build-task.schema.json", "artifact-record.schema.json", "demo-plan.schema.json",
    ]
    for schema_name in schema_files:
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    for schema_name, template_name in [
        ("requirement-record.schema.json", "requirement.json"),
        ("acceptance-test.schema.json", "acceptance-test.json"),
        ("build-task.schema.json", "build-task.json"),
        ("artifact-record.schema.json", "artifact.json"),
        ("demo-plan.schema.json", "../project/demo-plan.json"),
    ]:
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        template = json.loads((ROOT / "templates" / "records" / template_name).resolve().read_text(encoding="utf-8"))
        issues = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(template))
        assert not issues, f"{template_name}: {[e.message for e in issues]}"

    eval_schema = json.loads((ROOT / "schemas/evaluation-case.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(eval_schema)
    for number in B8_CASE_NUMBERS:
        path = ROOT / "evals/cases" / f"EVAL-{number:03d}.json"
        case = json.loads(path.read_text(encoding="utf-8"))
        assert not list(validator.iter_errors(case)), path.name
        assert case["case_status"] == "ready"


def test_b8_validator_reports_all_26_cases(capsys: pytest.CaptureFixture[str]) -> None:
    from tools.validate_b8 import main as validate_b8_main

    assert validate_b8_main() == 0
    output = capsys.readouterr().out
    assert "26 B8 evaluation cases (EVAL-062–087)" in output
