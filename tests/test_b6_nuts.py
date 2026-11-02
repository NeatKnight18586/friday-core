from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


def get_validator(name: str) -> Draft202012Validator:
    schema = json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def test_b6_templates_validate() -> None:
    for schema_name, template in [
        ("analogy-card.schema.json", "templates/records/analogy-card.json"),
        ("nuts-run.schema.json", "templates/records/nuts-run.json"),
    ]:
        sample = json.loads((ROOT / template).read_text(encoding="utf-8"))
        assert list(get_validator(schema_name).iter_errors(sample)) == []


def test_retained_for_test_requires_verified_source_and_adequate_mapping() -> None:
    card = json.loads((ROOT / "templates/records/analogy-card.json").read_text(encoding="utf-8"))
    card["status"] = "retained_for_test"
    card["assessment"].update({
        "source_accuracy": "verified", "functional_relevance": "adequate",
        "relational_mapping": "adequate", "testability": "adequate",
        "disposition": "plausible_needs_test"
    })
    validator = get_validator("analogy-card.schema.json")
    assert list(validator.iter_errors(card)) == []
    card["assessment"]["source_accuracy"] = "unverified"
    assert list(validator.iter_errors(card))


def test_no_useful_analogy_is_valid_without_forced_card() -> None:
    run = json.loads((ROOT / "templates/records/nuts-run.json").read_text(encoding="utf-8"))
    run.update({
        "status": "completed", "conclusion": "no_useful_analogy", "analogy_ids": [],
        "conclusion_rationale": "A bounded search found no credible analogy with sufficient transfer value."
    })
    validator = get_validator("nuts-run.schema.json")
    assert list(validator.iter_errors(run)) == []
    run["analogy_ids"] = ["ANL-0001"]
    assert list(validator.iter_errors(run))


def test_b6_evaluation_cases_valid_and_ready() -> None:
    validator = get_validator("evaluation-case.schema.json")
    for number in range(31, 39):
        case = json.loads((ROOT / "evals/cases" / f"EVAL-{number:03d}.json").read_text(encoding="utf-8"))
        assert list(validator.iter_errors(case)) == []
        assert case["case_status"] == "ready"


def test_analogy_card_requires_multiple_relational_assessment_dimensions() -> None:
    card = json.loads((ROOT / "templates/records/analogy-card.json").read_text(encoding="utf-8"))
    del card["assessment"]["relational_mapping"]
    errors = list(get_validator("analogy-card.schema.json").iter_errors(card))
    assert any("relational_mapping" in error.message for error in errors)


def test_analogy_card_rejects_unsupported_legal_clearance_status() -> None:
    card = json.loads((ROOT / "templates/records/analogy-card.json").read_text(encoding="utf-8"))
    card["rights_and_attribution"]["patent_or_prior_art_status"] = "cleared_by_qualified_reviewer"
    # The schema has no status that lets an AI certify legal novelty or freedom to operate.
    errors = list(get_validator("analogy-card.schema.json").iter_errors(card))
    assert any(list(error.absolute_path) == ["rights_and_attribution", "patent_or_prior_art_status"] for error in errors)
