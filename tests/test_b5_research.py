from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def validator(name: str) -> Draft202012Validator:
    schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def test_b5_research_templates_validate() -> None:
    examples = {
        "research-plan.schema.json": "templates/project/research-plan.json",
        "research-question.schema.json": "templates/records/research-question.json",
        "research-finding.schema.json": "templates/records/research-finding.json",
        "research-round.schema.json": "templates/records/research-round.json",
        "opportunity-record.schema.json": "templates/records/opportunity.json",
    }
    for schema_name, example_path in examples.items():
        sample = json.loads((ROOT / example_path).read_text(encoding="utf-8"))
        assert list(validator(schema_name).iter_errors(sample)) == []


def test_user_statement_requires_round_participant_and_consent() -> None:
    finding = json.loads((ROOT / "templates/records/research-finding.json").read_text(encoding="utf-8"))
    finding.update({
        "finding_type": "user_statement",
        "evidence_label": "user_reported",
        "round_id": "RR-0001",
        "participant_ref": "P-0001",
        "consent_status": "unknown",
    })
    errors = list(validator("research-finding.schema.json").iter_errors(finding))
    assert any(list(error.absolute_path) == ["consent_status"] for error in errors)


def test_completed_research_round_requires_resolved_consent() -> None:
    research_round = json.loads((ROOT / "templates/records/research-round.json").read_text(encoding="utf-8"))
    research_round.update({
        "status": "completed",
        "consent_status": "incomplete",
        "started_at": "2026-11-01T09:00:00Z",
        "completed_at": "2026-11-01T10:00:00Z",
    })
    errors = list(validator("research-round.schema.json").iter_errors(research_round))
    assert any(list(error.absolute_path) == ["consent_status"] for error in errors)


def test_b5_evaluation_cases_are_valid_and_ready() -> None:
    case_validator = validator("evaluation-case.schema.json")
    for number in range(20, 31):
        path = ROOT / "evals/cases" / f"EVAL-{number:03d}.json"
        case = json.loads(path.read_text(encoding="utf-8"))
        assert list(case_validator.iter_errors(case)) == []
        assert case["case_status"] == "ready"


def test_non_participant_finding_requires_consent_rationale_when_not_applicable() -> None:
    finding = json.loads((ROOT / "templates/records/research-finding.json").read_text(encoding="utf-8"))
    finding["consent_rationale"] = None
    errors = list(validator("research-finding.schema.json").iter_errors(finding))
    assert any(list(error.absolute_path) == ["consent_rationale"] for error in errors)


def test_completed_research_round_cannot_have_unresolved_local_review() -> None:
    research_round = json.loads((ROOT / "templates/records/research-round.json").read_text(encoding="utf-8"))
    research_round.update({
        "status": "completed",
        "consent_status": "obtained_for_all",
        "started_at": "2026-11-01T09:00:00Z",
        "completed_at": "2026-11-01T10:00:00Z",
        "local_review_status": "unknown",
    })
    errors = list(validator("research-round.schema.json").iter_errors(research_round))
    assert any(list(error.absolute_path) == ["local_review_status"] for error in errors)


def test_research_round_participant_references_are_pseudonymous_and_unique() -> None:
    research_round = json.loads((ROOT / "templates/records/research-round.json").read_text(encoding="utf-8"))
    research_round["participant_refs"] = ["P-0001", "P-0001"]
    errors = list(validator("research-round.schema.json").iter_errors(research_round))
    assert any(error.validator == "uniqueItems" for error in errors)
    research_round["participant_refs"] = ["Jane Smith"]
    errors = list(validator("research-round.schema.json").iter_errors(research_round))
    assert any(list(error.absolute_path) == ["participant_refs", 0] for error in errors)
