from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def validator(schema_name: str):
    schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def council_template() -> dict:
    return json.loads((ROOT / "templates/records/council-review.json").read_text(encoding="utf-8"))


def test_b7_templates_validate() -> None:
    assert not list(validator("council-review.schema.json").iter_errors(council_template()))
    test = json.loads((ROOT / "templates/records/assumption-test.json").read_text(encoding="utf-8"))
    assert not list(validator("assumption-test.schema.json").iter_errors(test))


def test_all_core_dimensions_are_required_for_every_depth() -> None:
    review = council_template()
    del review["councils"]["council_3"]["dimensions"]["technical_plausibility"]
    errors = list(validator("council-review.schema.json").iter_errors(review))
    assert any("technical_plausibility" in error.message for error in errors)


def test_same_model_sequential_review_cannot_claim_independence() -> None:
    review = council_template()
    review["reviewer_setup"]["statistical_independence_claim"] = True
    errors = list(validator("council-review.schema.json").iter_errors(review))
    assert errors


def test_verified_dimension_requires_evidence_reference() -> None:
    review = council_template()
    dimension = review["councils"]["council_1"]["dimensions"]["problem_evidence"]
    dimension.update({"score": 5, "evidence_status": "VERIFIED"})
    errors = list(validator("council-review.schema.json").iter_errors(review))
    assert any(list(error.absolute_path)[-1:] == ["evidence_refs"] for error in errors)


def test_not_applicable_dimension_requires_reason() -> None:
    review = council_template()
    dimension = review["councils"]["council_2"]["dimensions"]["adoption_operating_model"]
    dimension["score"] = "N_A"
    errors = list(validator("council-review.schema.json").iter_errors(review))
    assert any("na_reason" in error.message for error in errors)


def test_critical_finding_cannot_be_accepted_with_rationale() -> None:
    review = council_template()
    review["findings"] = [{
        "finding_id": "CRF-0001", "title": "Critical safety issue", "description": "A critical safety issue remains unresolved and could cause harm.",
        "primary_owner": "C4", "risk_domain": "safety", "severity": "critical",
        "status": "accepted_with_rationale", "evidence_status": "SUPPORTED", "evidence_refs": [],
        "acceptance_rationale": "The team accepts this despite the unresolved safety concern.",
        "accepted_by": "project owner", "revisit_trigger": "Revisit before any public test.",
    }]
    assert list(validator("council-review.schema.json").iter_errors(review))


def test_advance_with_blocked_gate_is_rejected() -> None:
    review = council_template()
    review["verdict"] = "ADVANCE"
    review["gate"]["status"] = "blocked"
    errors = list(validator("council-review.schema.json").iter_errors(review))
    assert errors


def test_event_alignment_assessed_criterion_requires_evidence_semantically() -> None:
    from tools.b7_rules import validate_b7_records

    review = council_template()
    review["event_alignment"] = {
        "applicable": True, "assessment_status": "assessed",
        "criteria": [{"criterion_id": "ELIG-1", "requirement": "Team members must meet eligibility rules.", "status": "compliant", "mandatory": False, "evidence_refs": []}],
        "overall_notes": "Fixture", "limitations": [],
    }
    errors = validate_b7_records(
        council_reviews=[review], assumption_tests=[], assumptions=[], sources=[], claims=[], decisions=[],
        research_findings=[], opportunities=[], analogies=[], nuts_runs=[],
    )
    assert any("assessed criterion requires evidence" in error for error in errors)


def test_unresolved_critical_or_high_finding_blocks_advance() -> None:
    from tools.b7_rules import validate_b7_records

    review = council_template()
    review["findings"] = [{
        "finding_id": "CRF-0001", "title": "Unresolved delivery blocker", "description": "A high-severity delivery dependency has not been verified.",
        "primary_owner": "C4", "risk_domain": "delivery", "severity": "high", "status": "open",
        "evidence_status": "ASSUMPTION", "evidence_refs": [],
    }]
    review["verdict"] = "REVISE"
    review["gate"].update({"status": "pass", "blocking_finding_ids": []})
    errors = validate_b7_records(
        council_reviews=[review], assumption_tests=[], assumptions=[], sources=[], claims=[], decisions=[],
        research_findings=[], opportunities=[], analogies=[], nuts_runs=[],
    )
    assert any("require a blocked gate" in error for error in errors)
    assert any("missing from blockers" in error for error in errors)


def test_accepted_high_risk_requires_conditional_gate() -> None:
    from tools.b7_rules import validate_b7_records

    review = council_template()
    review["findings"] = [{
        "finding_id": "CRF-0002", "title": "Residual schedule risk", "description": "A high schedule risk remains but the owner accepts it with a revisit condition.",
        "primary_owner": "C4", "risk_domain": "delivery", "severity": "high", "status": "accepted_with_rationale",
        "evidence_status": "SUPPORTED", "evidence_refs": [],
        "acceptance_rationale": "The remaining schedule risk is understood and bounded for this small prototype.",
        "accepted_by": "project owner", "revisit_trigger": "Revisit if the delivery date moves by one week.",
    }]
    review["gate"]["status"] = "pass"
    errors = validate_b7_records(
        council_reviews=[review], assumption_tests=[], assumptions=[], sources=[], claims=[], decisions=[],
        research_findings=[], opportunities=[], analogies=[], nuts_runs=[],
    )
    assert any("pass_with_conditions" in error for error in errors)


def test_human_interview_test_requires_consent_and_ethics_controls() -> None:
    test = json.loads((ROOT / "templates/records/assumption-test.json").read_text(encoding="utf-8"))
    test["method"] = "user_interview"
    test["participant_controls"].update({
        "involves_human_participants": True, "consent_status": "pending",
        "deidentification_confirmed": False, "ethics_review_status": "pending",
    })
    # A planned interview may be recorded before consent is obtained.
    assert not list(validator("assumption-test.schema.json").iter_errors(test))
    test["status"] = "approved"
    test["approved_at"] = "2026-11-01T09:00:00Z"
    assert list(validator("assumption-test.schema.json").iter_errors(test))
    test["participant_controls"].update({
        "consent_status": "obtained", "deidentification_confirmed": True,
        "ethics_review_status": "not_required",
        "ethics_review_rationale": "No formal institutional review is required for this low-risk exercise; local policy was checked.",
    })
    assert not list(validator("assumption-test.schema.json").iter_errors(test))


def test_completed_test_requires_result_and_traceable_evidence() -> None:
    test = json.loads((ROOT / "templates/records/assumption-test.json").read_text(encoding="utf-8"))
    test.update({"status": "completed", "approved_at": "2026-11-01T09:00:00Z", "completed_at": "2026-11-01T10:00:00Z"})
    assert list(validator("assumption-test.schema.json").iter_errors(test))
    test["result"] = {"outcome": "supports", "summary": "The technical spike demonstrated that the documented interface works under the tested conditions.", "sample_size": None, "evidence_refs": [{"record_type": "source", "record_id": "SRC-0001"}], "limitations": ["One local test only."], "deviations_from_protocol": []}
    assert not list(validator("assumption-test.schema.json").iter_errors(test))


def test_b7_eval_cases_are_valid_and_ready() -> None:
    case_v = validator("evaluation-case.schema.json")
    for number in range(51, 62):
        case = json.loads((ROOT / "evals/cases" / f"EVAL-{number:03d}.json").read_text(encoding="utf-8"))
        assert not list(case_v.iter_errors(case))
        assert case["case_status"] == "ready"


def test_new_project_gets_b7_ledgers_and_legacy_workspace_remains_valid(tmp_path: Path) -> None:
    from tools.init_project import main as init_main
    from tools.validate_project import main as validate_main
    import sys
    from contextlib import redirect_stdout, redirect_stderr
    from io import StringIO

    workspace = tmp_path / "projects"
    old_argv = sys.argv[:]
    try:
        sys.argv = ["init_project.py", "--id", "b7-test", "--title", "B7 Test", "--workspace-root", str(workspace)]
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            assert init_main() == 0
    finally:
        sys.argv = old_argv
    project = workspace / "b7-test"
    assert (project / "records/council-reviews.jsonl").exists()
    assert (project / "records/assumption-tests.jsonl").exists()
    old_argv = sys.argv[:]
    try:
        sys.argv = ["validate_project.py", str(project)]
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            assert validate_main() == 0
    finally:
        sys.argv = old_argv
    (project / "records/council-reviews.jsonl").unlink()
    (project / "records/assumption-tests.jsonl").unlink()
    old_argv = sys.argv[:]
    try:
        sys.argv = ["validate_project.py", str(project)]
        out = StringIO()
        with redirect_stdout(out), redirect_stderr(StringIO()):
            assert validate_main() == 0
        assert "legacy project has no" in out.getvalue()
    finally:
        sys.argv = old_argv


def test_supported_assumption_requires_completed_supporting_test() -> None:
    from tools.b7_rules import validate_b7_records

    assumption = json.loads((ROOT / "templates/records/assumption.json").read_text(encoding="utf-8"))
    assumption["status"] = "supported"
    errors = validate_b7_records(
        council_reviews=[], assumption_tests=[], assumptions=[assumption], sources=[], claims=[], decisions=[],
        research_findings=[], opportunities=[], analogies=[], nuts_runs=[],
    )
    assert any("completed supporting test" in error for error in errors)


def test_project_validator_accepts_linked_b7_records_and_rejects_dangling_links(tmp_path: Path) -> None:
    import sys
    from contextlib import redirect_stderr, redirect_stdout
    from io import StringIO
    from tools.init_project import main as init_main
    from tools.validate_project import main as validate_main

    workspace = tmp_path / "projects"
    old_argv = sys.argv[:]
    try:
        sys.argv = ["init_project.py", "--id", "b7-linked", "--title", "B7 Linked Records", "--workspace-root", str(workspace)]
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            assert init_main() == 0
    finally:
        sys.argv = old_argv
    project = workspace / "b7-linked"
    records = project / "records"

    source = json.loads((ROOT / "templates/records/source.json").read_text(encoding="utf-8"))
    source["source_id"] = "SRC-0001"
    claim = json.loads((ROOT / "templates/records/claim.json").read_text(encoding="utf-8"))
    claim["claim_id"] = "CLM-0001"
    claim["source_ids"] = ["SRC-0001"]
    assumption = json.loads((ROOT / "templates/records/assumption.json").read_text(encoding="utf-8"))
    assumption["assumption_id"] = "ASM-0001"
    assumption["status"] = "supported"

    test = json.loads((ROOT / "templates/records/assumption-test.json").read_text(encoding="utf-8"))
    test.update({
        "test_id": "TST-0001", "assumption_id": "ASM-0001", "status": "completed",
        "approved_at": "2026-11-01T09:00:00Z", "completed_at": "2026-11-01T10:00:00Z",
        "result": {
            "outcome": "supports",
            "summary": "The technical spike demonstrated the interface works under the documented test conditions.",
            "sample_size": None,
            "evidence_refs": [{"record_type": "source", "record_id": "SRC-0001"}],
            "limitations": ["One synthetic technical test only."],
            "deviations_from_protocol": [],
        },
    })
    review = council_template()
    review.update({
        "review_id": "REV-0001", "project_id": "b7-linked", "concept_title": "Linked test concept",
        "evidence_pack": {
            "source_ids": ["SRC-0001"], "claim_ids": ["CLM-0001"], "assumption_ids": ["ASM-0001"],
            "decision_ids": [], "scope_and_limitations": ["Synthetic integration fixture only."], "as_of_date": "2026-11-01",
        },
    })

    def write_jsonl(filename: str, rows: list[dict]) -> None:
        (records / filename).write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")

    write_jsonl("sources.jsonl", [source])
    write_jsonl("claims.jsonl", [claim])
    write_jsonl("assumptions.jsonl", [assumption])
    write_jsonl("assumption-tests.jsonl", [test])
    write_jsonl("council-reviews.jsonl", [review])

    def run_project_validator() -> tuple[int, str]:
        prior = sys.argv[:]
        out = StringIO()
        try:
            sys.argv = ["validate_project.py", str(project)]
            with redirect_stdout(out), redirect_stderr(StringIO()):
                code = validate_main()
        finally:
            sys.argv = prior
        return code, out.getvalue()

    code, output = run_project_validator()
    assert code == 0, output

    # A dangling reference in a council evidence pack must be rejected.
    review["evidence_pack"]["source_ids"] = ["SRC-9999"]
    write_jsonl("council-reviews.jsonl", [review])
    code, output = run_project_validator()
    assert code != 0 and "missing source reference SRC-9999" in output

    # Restore the review and make its assumption test point to an unknown assumption.
    review["evidence_pack"]["source_ids"] = ["SRC-0001"]
    write_jsonl("council-reviews.jsonl", [review])
    test["assumption_id"] = "ASM-9999"
    write_jsonl("assumption-tests.jsonl", [test])
    code, output = run_project_validator()
    assert code != 0 and "missing assumption reference ASM-9999" in output


def test_mandatory_event_noncompliance_requires_critical_blocker_and_blocked_gate() -> None:
    """Mandatory rule failures must block even when product dimensions look strong."""
    from copy import deepcopy
    from tools.b7_rules import validate_b7_records

    review = council_template()
    review["event_alignment"] = {
        "applicable": True,
        "assessment_status": "assessed",
        "criteria": [{
            "criterion_id": "RULE-01",
            "requirement": "A working offline prototype is mandatory.",
            "status": "noncompliant",
            "mandatory": True,
            "evidence_refs": [{"record_type": "external_requirement", "record_id": "EVENT-RULE-01"}],
            "linked_finding_id": "CRF-0001",
        }],
        "overall_notes": "Synthetic event requirement used for a validator fixture.",
        "limitations": ["No real event has been assessed."],
    }
    review["findings"] = [{
        "finding_id": "CRF-0001",
        "title": "Mandatory prototype requirement not met",
        "description": "The concept does not currently provide the mandatory working offline prototype required by the event.",
        "primary_owner": "C4",
        "risk_domain": "mandatory_compliance",
        "severity": "critical",
        "status": "open",
        "evidence_status": "VERIFIED",
        "evidence_refs": [{"record_type": "external_requirement", "record_id": "EVENT-RULE-01"}],
    }]
    review["verdict"] = "REVISE"
    review["gate"].update({"status": "blocked", "blocking_finding_ids": ["CRF-0001"]})

    def errors_for(candidate: dict) -> list[str]:
        return validate_b7_records(
            council_reviews=[candidate], assumption_tests=[], assumptions=[], sources=[], claims=[], decisions=[],
            research_findings=[], opportunities=[], analogies=[], nuts_runs=[],
        )

    # The correctly linked critical blocker and blocked gate is valid.
    assert errors_for(review) == []

    # Removing the link must not allow mandatory non-compliance to disappear.
    candidate = deepcopy(review)
    del candidate["event_alignment"]["criteria"][0]["linked_finding_id"]
    assert any("requires a linked blocking finding" in error for error in errors_for(candidate))

    # A high-severity finding is insufficient for confirmed non-compliance.
    candidate = deepcopy(review)
    candidate["findings"][0]["severity"] = "high"
    assert any("must be open critical mandatory_compliance" in error for error in errors_for(candidate))

    # A favorable/pass gate cannot override a mandatory event failure.
    candidate = deepcopy(review)
    candidate["gate"].update({"status": "pass", "blocking_finding_ids": []})
    assert any("require a blocked gate" in error for error in errors_for(candidate))

    # The blocking finding must remain explicitly listed at the gate.
    candidate = deepcopy(review)
    candidate["gate"]["blocking_finding_ids"] = []
    assert any("missing from blockers" in error for error in errors_for(candidate))


def test_mandatory_event_partial_or_unknown_requires_high_blocker() -> None:
    """Unresolved mandatory requirements cannot pass on partial or unknown evidence."""
    from copy import deepcopy
    from tools.b7_rules import validate_b7_records

    base = council_template()
    base["event_alignment"] = {
        "applicable": True, "assessment_status": "assessed",
        "criteria": [], "overall_notes": "Synthetic fixture.", "limitations": [],
    }
    base["gate"].update({"status": "blocked", "blocking_finding_ids": ["CRF-0002"]})
    base["verdict"] = "VALIDATE"

    for index, status in enumerate(("partial", "unknown"), start=1):
        review = deepcopy(base)
        finding_id = f"CRF-{index:04d}"
        review["gate"]["blocking_finding_ids"] = [finding_id]
        criterion = {
            "criterion_id": f"RULE-{index:02d}",
            "requirement": "A required event deliverable must be available.",
            "status": status, "mandatory": True, "evidence_refs": [],
            "linked_finding_id": finding_id,
        }
        if status == "partial":
            criterion["evidence_refs"] = [{"record_type": "external_requirement", "record_id": "EVENT-RULE-02"}]
        review["event_alignment"]["criteria"].append(criterion)
        review["findings"] = [{
            "finding_id": finding_id,
            "title": "Mandatory requirement remains unresolved",
            "description": "The mandatory requirement has not yet been demonstrated as compliant.",
            "primary_owner": "C4", "risk_domain": "mandatory_compliance",
            "severity": "high", "status": "open",
            "evidence_status": "PRELIMINARY", "evidence_refs": [],
        }]

        errors = validate_b7_records(
            council_reviews=[review], assumption_tests=[], assumptions=[], sources=[], claims=[], decisions=[],
            research_findings=[], opportunities=[], analogies=[], nuts_runs=[],
        )
        assert errors == [], f"{status} mandatory criterion should be valid when properly blocked: {errors}"

        review["gate"].update({"status": "pass", "blocking_finding_ids": []})
        errors = validate_b7_records(
            council_reviews=[review], assumption_tests=[], assumptions=[], sources=[], claims=[], decisions=[],
            research_findings=[], opportunities=[], analogies=[], nuts_runs=[],
        )
        assert any("require a blocked gate" in error for error in errors)
