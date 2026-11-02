#!/usr/bin/env python3
"""B8 semantic checks for requirements, acceptance tests, delivery tasks and artifacts."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath
from typing import Any


def _rows_by_id(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {row.get(key): row for row in rows if isinstance(row, dict) and row.get(key)}


def _cycle_nodes(graph: dict[str, set[str]]) -> set[str]:
    """Return nodes participating in or reachable through a dependency cycle."""
    visiting: set[str] = set()
    visited: set[str] = set()
    cyclic: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> None:
        if node in visiting:
            try:
                cyclic.update(stack[stack.index(node):])
            except ValueError:
                cyclic.add(node)
            return
        if node in visited:
            return
        visiting.add(node)
        stack.append(node)
        for dependency in graph.get(node, set()):
            if dependency in graph:
                visit(dependency)
        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    return cyclic


def _safe_project_file(project_dir: Path, relative_path: str) -> tuple[Path | None, str | None]:
    """Resolve a relative artifact path without traversal or symlink escapes."""
    if not isinstance(relative_path, str) or not relative_path.strip():
        return None, "path is empty"
    if "\\" in relative_path:
        return None, "path must use POSIX separators"
    pure = PurePosixPath(relative_path)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        return None, "path must be a normalized relative path without traversal"
    if pure.as_posix() != relative_path:
        return None, "path must be normalized"

    root = project_dir.resolve()
    candidate = root.joinpath(*pure.parts)
    current = root
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            return None, "symlink paths are not accepted for project artifacts"
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(root)
    except (OSError, ValueError):
        return None, "path resolves outside the project workspace"
    if not candidate.is_file():
        return None, "file does not exist"
    return candidate, None


def _all_review_finding_ids(reviews: list[dict[str, Any]]) -> set[str]:
    found: set[str] = set()
    for review in reviews:
        if not isinstance(review, dict):
            continue
        for finding in review.get("findings", []):
            if isinstance(finding, dict) and finding.get("finding_id"):
                found.add(finding["finding_id"])
    return found


def _reference_lookup(
    *, sources: list[dict[str, Any]], claims: list[dict[str, Any]], assumptions: list[dict[str, Any]],
    decisions: list[dict[str, Any]], findings: list[dict[str, Any]], opportunities: list[dict[str, Any]],
    analogies: list[dict[str, Any]], nuts_runs: list[dict[str, Any]],
    artifacts: list[dict[str, Any]], tests: list[dict[str, Any]],
    reviews: list[dict[str, Any]], assumption_tests: list[dict[str, Any]],
    evaluation_results: list[dict[str, Any]],
) -> dict[str, set[str]]:
    return {
        "source": set(_rows_by_id(sources, "source_id")),
        "claim": set(_rows_by_id(claims, "claim_id")),
        "assumption": set(_rows_by_id(assumptions, "assumption_id")),
        "decision": set(_rows_by_id(decisions, "decision_id")),
        "research_finding": set(_rows_by_id(findings, "finding_id")),
        "opportunity": set(_rows_by_id(opportunities, "opportunity_id")),
        "analogy": set(_rows_by_id(analogies, "analogy_id")),
        "artifact": set(_rows_by_id(artifacts, "artifact_id")),
        "acceptance_test": set(_rows_by_id(tests, "test_id")),
        "assumption_test": set(_rows_by_id(assumption_tests, "test_id")),
        "nuts_run": set(_rows_by_id(nuts_runs, "run_id")),
        "evaluation_result": set(_rows_by_id(evaluation_results, "result_id")),
        "council_finding": _all_review_finding_ids(reviews),
    }


def _check_refs(
    refs: list[dict[str, Any]], lookup: dict[str, set[str]], label: str, errors: list[str]
) -> None:
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        kind, rid = ref.get("record_type"), ref.get("record_id")
        if kind == "external_requirement":
            if len(str(ref.get("note", "")).strip()) < 8:
                errors.append(f"{label}: external_requirement {rid} needs a note identifying its source or authority")
        elif kind in lookup and rid not in lookup[kind]:
            errors.append(f"{label}: missing {kind} reference {rid}")


def _validate_document_sections(project_dir: Path, artifacts_by_type: dict[str, dict[str, Any]], errors: list[str]) -> None:
    requirements = {
        "prd": [
            "executive summary", "problem and opportunity", "target users and use context",
            "jobs, needs, and user journeys", "goals and measurable outcomes", "non-goals and boundaries",
            "scope and release slices", "requirements and acceptance criteria", "success measures and release decision",
            "approval and limitations",
        ],
        "technical_design": [
            "purpose, design status, and scope", "system context and boundaries", "architecture overview",
            "components and responsibilities", "data model and lifecycle", "interfaces and contracts",
            "security, privacy, safety, and abuse cases", "reliability and failure handling",
            "accessibility and human factors", "observability and operations", "verification and test strategy",
            "alternatives and trade-offs", "technical risks, assumptions, and unresolved questions",
            "decisions and traceability", "approval and limitations",
        ],
        "build_plan": [
            "delivery objective and definition of done", "in-scope and excluded work", "work breakdown and ownership",
            "sequence, milestones, and dependency logic", "resources, estimates, and assumptions",
            "quality and verification plan", "risk reduction and contingency", "communication and handoff",
            "change control", "release readiness and approval",
        ],
        "demo_plan": [
            "demo objective and audience", "core scenario and story", "timed walkthrough",
            "proof points and evidence boundaries", "environment and prerequisites", "data, consent, privacy, and safety",
            "failure and fallback plan", "limitations and audience questions", "readiness and approval",
        ],
    }
    for artifact_type, required_headings in requirements.items():
        artifact = artifacts_by_type.get(artifact_type)
        if not artifact:
            continue
        path, reason = _safe_project_file(project_dir, artifact.get("path", ""))
        if reason or path is None:
            # The artifact validator reports the canonical path issue; avoid duplicate noise here.
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{artifact_type} artifact {artifact.get('artifact_id')}: cannot read Markdown: {exc}")
            continue
        headings = []
        for line in text.splitlines():
            match = re.match(r"^#{1,6}\s+(?:\d+\.\s*)?(.+?)\s*$", line)
            if match:
                headings.append(re.sub(r"\s+", " ", match.group(1)).strip().lower())
        for heading in required_headings:
            if not any(heading in actual for actual in headings):
                errors.append(f"{path.relative_to(project_dir).as_posix()}: missing required section heading '{heading}'")
        if artifact.get("status") == "approved":
            unresolved = re.search(r"\b(?:TBD|TODO|NOT APPROVED|NOT YET APPROVED)\b|\[fill in|\[describe|\[state|\[link", text, re.IGNORECASE)
            if unresolved:
                errors.append(f"{path.relative_to(project_dir).as_posix()}: approved artifact still contains an unresolved placeholder")



def _validate_document_traceability(
    project_dir: Path, artifacts_by_type: dict[str, dict[str, Any]],
    requirements: list[dict[str, Any]], build_tasks: list[dict[str, Any]],
    demo_plan: dict[str, Any] | None, errors: list[str],
) -> None:
    """Check that the human-readable handoff reflects the machine-readable ledgers."""
    checks: list[tuple[str, set[str]]] = []
    active_requirements = {
        row.get("requirement_id") for row in requirements if isinstance(row, dict)
        and row.get("status") not in {"rejected", "superseded"}
    }
    criteria = {
        criterion.get("criterion_id") for row in requirements if isinstance(row, dict)
        and row.get("status") not in {"rejected", "superseded"}
        for criterion in row.get("acceptance_criteria", []) if isinstance(criterion, dict)
    }
    if active_requirements or criteria:
        checks.append(("prd", active_requirements | criteria))
    approved_requirements = {
        row.get("requirement_id") for row in requirements if isinstance(row, dict)
        and row.get("status") == "approved"
    }
    if approved_requirements:
        checks.append(("technical_design", approved_requirements))

    task_ids = {
        row.get("task_id") for row in build_tasks if isinstance(row, dict)
        and row.get("status") != "cancelled"
    }
    task_requirements = {
        rid for row in build_tasks if isinstance(row, dict) and row.get("status") != "cancelled"
        for rid in row.get("requirement_ids", [])
    }
    if task_ids or task_requirements:
        checks.append(("build_plan", task_ids | task_requirements))

    demo_ids: set[str] = set()
    if isinstance(demo_plan, dict):
        for step in demo_plan.get("steps", []):
            if isinstance(step, dict):
                if step.get("step_id"):
                    demo_ids.add(step["step_id"])
                demo_ids.update(step.get("requirement_ids", []))
    if demo_ids:
        checks.append(("demo_plan", demo_ids))

    for artifact_type, identifiers in checks:
        artifact = artifacts_by_type.get(artifact_type)
        if not artifact:
            continue
        path, reason = _safe_project_file(project_dir, artifact.get("path", ""))
        if reason or path is None:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{artifact_type} document cannot be read for traceability check: {exc}")
            continue
        for identifier in sorted(value for value in identifiers if isinstance(value, str)):
            # Use identifier boundaries: REQ-001 must not accidentally match REQ-0010.
            pattern = rf"(?<![A-Za-z0-9_-]){re.escape(identifier)}(?![A-Za-z0-9_-])"
            if not re.search(pattern, text):
                errors.append(
                    f"{path.relative_to(project_dir).as_posix()}: missing machine-record reference {identifier}"
                )

def validate_b8_records(
    *, project_dir: Path, requirements: list[dict[str, Any]], acceptance_tests: list[dict[str, Any]],
    build_tasks: list[dict[str, Any]], artifacts: list[dict[str, Any]], demo_plan: dict[str, Any] | None,
    sources: list[dict[str, Any]], claims: list[dict[str, Any]], assumptions: list[dict[str, Any]],
    decisions: list[dict[str, Any]], findings: list[dict[str, Any]], opportunities: list[dict[str, Any]],
    analogies: list[dict[str, Any]], nuts_runs: list[dict[str, Any]],
    council_reviews: list[dict[str, Any]], assumption_tests: list[dict[str, Any]], evaluation_results: list[dict[str, Any]],
    artifact_ledger_present: bool, state: dict[str, Any] | None,
) -> list[str]:
    errors: list[str] = []
    req_by_id = _rows_by_id(requirements, "requirement_id")
    tests_by_id = _rows_by_id(acceptance_tests, "test_id")
    tasks_by_id = _rows_by_id(build_tasks, "task_id")
    artifacts_by_id = _rows_by_id(artifacts, "artifact_id")
    artifacts_by_type: dict[str, dict[str, Any]] = {}
    active_artifacts: dict[str, list[dict[str, Any]]] = {}
    for row in artifacts:
        if not isinstance(row, dict):
            continue
        artifact_type = row.get("artifact_type")
        if artifact_type in {"prd", "technical_design", "build_plan", "demo_plan", "demo_plan_data"} and row.get("status") not in {"superseded", "archived"}:
            active_artifacts.setdefault(artifact_type, []).append(row)
    for artifact_type, rows in active_artifacts.items():
        artifacts_by_type[artifact_type] = rows[-1]
        if len(rows) > 1:
            ids = ", ".join(str(row.get("artifact_id")) for row in rows)
            errors.append(
                f"Multiple active {artifact_type} artifacts are registered ({ids}); "
                "mark older versions superseded or archived."
            )
    lookup = _reference_lookup(
        sources=sources, claims=claims, assumptions=assumptions, decisions=decisions,
        findings=findings, opportunities=opportunities, analogies=analogies, nuts_runs=nuts_runs,
        artifacts=artifacts, tests=acceptance_tests, reviews=council_reviews,
        assumption_tests=assumption_tests, evaluation_results=evaluation_results,
    )
    source_by_id = _rows_by_id(sources, "source_id")
    claim_by_id = _rows_by_id(claims, "claim_id")
    finding_by_id = _rows_by_id(findings, "finding_id")

    # Artifact integrity: references must resolve to real files inside the workspace.
    seen_paths: dict[str, str] = {}
    for row_no, artifact in enumerate(artifacts, start=1):
        if not isinstance(artifact, dict):
            continue
        label = f"records/artifacts.jsonl:{row_no}"
        rel = artifact.get("path", "")
        path, reason = _safe_project_file(project_dir, rel)
        if reason:
            errors.append(f"{label}: unsafe or unavailable artifact path {rel!r}: {reason}")
        else:
            normalized = PurePosixPath(rel).as_posix()
            path_key = normalized.casefold()
            if path_key in seen_paths:
                errors.append(
                    f"{label}: path {normalized} collides with another artifact path "
                    f"registered by {seen_paths[path_key]} (case-insensitive check)"
                )
            else:
                seen_paths[path_key] = artifact.get("artifact_id", "unknown")
            digest = artifact.get("sha256")
            if digest and path:
                try:
                    actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
                except OSError as exc:
                    errors.append(f"{label}: cannot hash artifact {rel}: {exc}")
                else:
                    if actual_digest != digest:
                        errors.append(f"{label}: SHA-256 mismatch for {rel}; refresh the artifact record after an intentional change")
        for req_id in artifact.get("linked_requirement_ids", []):
            if req_id not in req_by_id:
                errors.append(f"{label}: missing requirement reference {req_id}")

    # Requirement provenance, scope consistency, dependencies and acceptance-test coverage.
    criterion_owner: dict[tuple[str, str], str] = {}
    req_graph: dict[str, set[str]] = {}
    supersession_graph: dict[str, set[str]] = {}
    test_coverage: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row_no, req in enumerate(requirements, start=1):
        if not isinstance(req, dict):
            continue
        label = f"records/requirements.jsonl:{row_no}"
        req_id = req.get("requirement_id")
        _check_refs(req.get("origin_refs", []), lookup, label, errors)
        origin_types = {x.get("record_type") for x in req.get("origin_refs", []) if isinstance(x, dict)}
        evidence_status = req.get("evidence_status")
        if evidence_status == "assumption" and "assumption" not in origin_types:
            errors.append(f"{label}: evidence_status=assumption requires a linked assumption record")
        if evidence_status in {"verified", "supported"} and not origin_types.intersection({"source", "claim", "research_finding"}):
            errors.append(f"{label}: {evidence_status} evidence requires an inspected source, claim, or research-finding origin")
        if evidence_status == "verified":
            strong_support = False
            for ref in req.get("origin_refs", []):
                if not isinstance(ref, dict):
                    continue
                if ref.get("record_type") == "source":
                    src = source_by_id.get(ref.get("record_id"), {})
                    assessment = src.get("assessment", {})
                    if (src.get("access_status") == "accessed" and src.get("validity_status") == "current"
                            and assessment.get("authority") == "high"):
                        strong_support = True
                elif ref.get("record_type") == "claim":
                    if claim_by_id.get(ref.get("record_id"), {}).get("evidence_status") == "supported":
                        strong_support = True
                elif ref.get("record_type") == "research_finding":
                    if finding_by_id.get(ref.get("record_id"), {}).get("evidence_label") in {"verified_primary", "supported_secondary", "measured"}:
                        strong_support = True
            if not strong_support:
                errors.append(f"{label}: verified evidence needs a current high-authority accessed source, supported claim, or verified/measured finding")
        if evidence_status == "supported":
            supported = False
            for ref in req.get("origin_refs", []):
                if not isinstance(ref, dict):
                    continue
                if ref.get("record_type") == "claim":
                    supported = supported or claim_by_id.get(ref.get("record_id"), {}).get("evidence_status") == "supported"
                elif ref.get("record_type") == "research_finding":
                    supported = supported or finding_by_id.get(ref.get("record_id"), {}).get("evidence_label") in {
                        "verified_primary", "supported_secondary", "measured"
                    }
                elif ref.get("record_type") == "source":
                    src = source_by_id.get(ref.get("record_id"), {})
                    authority = src.get("assessment", {}).get("authority")
                    supported = supported or (
                        src.get("access_status") == "accessed"
                        and src.get("validity_status") == "current"
                        and authority in {"medium", "high"}
                    )
            if not supported:
                errors.append(
                    f"{label}: supported evidence needs a current accessed medium/high-authority source, "
                    "a supported claim, or a verified/measured research finding"
                )
        if req.get("supersedes_requirement_id"):
            superseded_id = req["supersedes_requirement_id"]
            supersession_graph[req_id] = {superseded_id}
            if superseded_id not in req_by_id:
                errors.append(f"{label}: superseded requirement {superseded_id} not found")
            elif superseded_id == req_id:
                errors.append(f"{label}: a requirement cannot supersede itself")
        if (req.get("status") == "approved"
                and (req.get("mandatory") is True or req.get("requirement_type") in {"legal_regulatory", "mandatory_compliance"})
                and evidence_status not in {"verified", "supported"}):
            errors.append(f"{label}: mandatory or legal/compliance requirements cannot be approved on preliminary, assumed, or unknown evidence")
        if req.get("status") == "approved" and req.get("priority") == "wont":
            errors.append(f"{label}: a 'wont' priority requirement cannot be approved; reject or defer it explicitly")
        if (req.get("status") == "approved"
                and req.get("requirement_type") in {"legal_regulatory", "mandatory_compliance"}
                and req.get("mandatory") is not True):
            errors.append(f"{label}: an approved legal/compliance requirement must be explicitly marked mandatory")
        if (req.get("status") == "approved"
                and req.get("requirement_type") in {"legal_regulatory", "mandatory_compliance"}
                and evidence_status != "verified"):
            errors.append(f"{label}: legal/compliance approval requires verified evidence, not merely supported or assumed evidence")
        if evidence_status == "constraint" and not origin_types.intersection({"external_requirement", "decision", "source"}):
            errors.append(f"{label}: constraint evidence needs an external requirement, decision, or source origin")
        if req.get("status") == "approved" and req.get("release_scope") == "out_of_scope":
            errors.append(f"{label}: an approved requirement cannot be marked out_of_scope; defer/reject it or move it into scope")
        for criterion in req.get("acceptance_criteria", []):
            if not isinstance(criterion, dict):
                continue
            cid = criterion.get("criterion_id")
            criterion_key = (req_id, cid)
            if criterion_key in criterion_owner:
                errors.append(f"{label}: duplicate acceptance criterion ID {cid} within requirement {req_id}")
            else:
                criterion_owner[criterion_key] = req_id
        deps = set(req.get("depends_on", []))
        req_graph[req_id] = deps
        for dep in deps:
            if dep == req_id:
                errors.append(f"{label}: requirement cannot depend on itself")
            elif dep not in req_by_id:
                errors.append(f"{label}: missing requirement dependency {dep}")
            elif req.get("status") == "approved" and req_by_id[dep].get("status") != "approved":
                errors.append(f"{label}: approved requirement depends on unapproved requirement {dep}")
        for conflict in req.get("conflicts_with", []):
            if conflict == req_id:
                errors.append(f"{label}: requirement cannot conflict with itself")
            elif conflict not in req_by_id:
                errors.append(f"{label}: missing conflicting requirement {conflict}")
            else:
                counterpart = req_by_id[conflict]
                if req_id not in counterpart.get("conflicts_with", []):
                    errors.append(f"{label}: conflict with {conflict} must be recorded reciprocally")
                if req.get("status") == "approved" and counterpart.get("status") == "approved":
                    errors.append(f"{label}: conflicting requirements {req_id} and {conflict} cannot both be approved")

    for req_id, deps in req_graph.items():
        for dep in deps:
            if req_id in req_by_id.get(dep, {}).get("conflicts_with", []):
                errors.append(f"Requirement {req_id} both depends on and conflicts with {dep}")
    cyclic_requirements = _cycle_nodes(req_graph)
    for req_id in sorted(cyclic_requirements):
        errors.append(f"Requirement dependency cycle includes {req_id}")
    for req_id in sorted(_cycle_nodes(supersession_graph)):
        errors.append(f"Requirement supersession cycle includes {req_id}")

    # Acceptance tests must point to real criteria; only executed tests may claim results.
    for row_no, test in enumerate(acceptance_tests, start=1):
        if not isinstance(test, dict):
            continue
        label = f"records/acceptance-tests.jsonl:{row_no}"
        status = test.get("status")
        controls = test.get("participant_controls", {})
        if status in {"blocked", "cancelled"} and len(str(test.get("status_reason", "")).strip()) < 8:
            errors.append(f"{label}: status={status} requires a clear status_reason")
        if test.get("contains_identifiable_personal_data") is True:
            errors.append(f"{label}: identifiable personal data must not be stored in project test records")
        if test.get("involves_human_participants"):
            if not isinstance(controls, dict):
                errors.append(f"{label}: human-participant test requires participant_controls")
            else:
                consent = controls.get("consent_status")
                review = controls.get("ethics_review_disposition")
                if consent == "withdrawn" and status != "cancelled":
                    errors.append(f"{label}: withdrawn consent requires status=cancelled")
                if status == "ready" and consent != "obtained":
                    errors.append(f"{label}: human-participant test cannot be ready before consent is obtained")
                if status == "ready" and review not in {"approved", "not_required"}:
                    errors.append(f"{label}: human-participant test cannot be ready before local ethics/review disposition is resolved")
                if status in {"ready", "executed"} and review == "not_required" and len(str(controls.get("ethics_review_rationale", "")).strip()) < 12:
                    errors.append(f"{label}: not_required ethics disposition requires a rationale")
                if status == "executed":
                    if consent != "obtained":
                        errors.append(f"{label}: executed human-participant test requires obtained consent")
                    if review not in {"approved", "not_required"}:
                        errors.append(f"{label}: executed human-participant test requires approved or justified not_required review disposition")
        elif controls:
            if controls.get("consent_status") == "withdrawn" and status != "cancelled":
                errors.append(f"{label}: withdrawn consent requires status=cancelled")
        if status == "cancelled" and test.get("execution"):
            errors.append(f"{label}: cancelled test must not retain a completed execution result")
        if status != "executed" and test.get("execution"):
            errors.append(f"{label}: execution results are only permitted when status=executed")
        if status == "executed" and not test.get("execution"):
            errors.append(f"{label}: executed status requires a result, date, executor, evidence and limitations")
        if test.get("execution"):
            evidence_refs = test["execution"].get("evidence_refs", [])
            _check_refs(evidence_refs, lookup, f"{label}.execution", errors)
            if any(ref.get("record_type") == "acceptance_test" and ref.get("record_id") == test.get("test_id")
                   for ref in evidence_refs if isinstance(ref, dict)):
                errors.append(f"{label}: an acceptance test cannot cite itself as execution evidence")
        for cref in test.get("criterion_refs", []):
            if not isinstance(cref, dict):
                continue
            rid, cid = cref.get("requirement_id"), cref.get("criterion_id")
            req = req_by_id.get(rid)
            if not req:
                errors.append(f"{label}: missing requirement reference {rid}")
                continue
            criterion_ids = {c.get("criterion_id") for c in req.get("acceptance_criteria", []) if isinstance(c, dict)}
            if cid not in criterion_ids:
                errors.append(f"{label}: criterion {cid} is not defined by requirement {rid}")
            test_coverage.setdefault((rid, cid), []).append(test)

    for req in requirements:
        if not isinstance(req, dict) or req.get("status") != "approved":
            continue
        rid = req.get("requirement_id")
        for criterion in req.get("acceptance_criteria", []):
            if not isinstance(criterion, dict):
                continue
            cid = criterion.get("criterion_id")
            linked = test_coverage.get((rid, cid), [])
            eligible = [t for t in linked if t.get("status") not in {"blocked", "cancelled", "not_applicable"}]
            if not eligible:
                errors.append(f"Approved requirement {rid} criterion {cid} has no active linked acceptance-test specification")

    # Build task graph, execution readiness and coverage.
    task_graph: dict[str, set[str]] = {}
    for row_no, task in enumerate(build_tasks, start=1):
        if not isinstance(task, dict):
            continue
        label = f"records/build-tasks.jsonl:{row_no}"
        tid = task.get("task_id")
        deps = set(task.get("depends_on", []))
        if task.get("status") in {"blocked", "cancelled"} and len(str(task.get("status_reason", "")).strip()) < 8:
            errors.append(f"{label}: status={task.get('status')} requires a clear status_reason")
        task_graph[tid] = deps
        for dep in deps:
            if dep == tid:
                errors.append(f"{label}: task cannot depend on itself")
            elif dep not in tasks_by_id:
                errors.append(f"{label}: missing task dependency {dep}")
            elif task.get("sequence_index", 0) <= tasks_by_id[dep].get("sequence_index", 0):
                errors.append(f"{label}: sequence_index must be later than dependency {dep}")
            elif task.get("status") in {"ready", "in_progress", "completed"} and tasks_by_id[dep].get("status") != "completed":
                errors.append(f"{label}: task cannot be {task.get('status')} while dependency {dep} is not completed")
        for req_id in task.get("requirement_ids", []):
            if req_id not in req_by_id:
                errors.append(f"{label}: missing requirement reference {req_id}")
                continue
            linked_requirement = req_by_id[req_id]
            if linked_requirement.get("status") in {"rejected", "superseded"}:
                errors.append(f"{label}: task cannot deliver rejected/superseded requirement {req_id}")
            if (task.get("phase") in {"implementation", "integration", "release", "operations"}
                    and task.get("status") in {"ready", "in_progress", "completed"}
                    and linked_requirement.get("status") != "approved"):
                errors.append(f"{label}: {task.get('phase')} task cannot progress against unapproved requirement {req_id}")
        _check_refs(task.get("completion_evidence_refs", []), lookup, label, errors)
        if task.get("status") == "completed":
            refs = task.get("completion_evidence_refs", [])
            if not any(r.get("record_type") in {"artifact", "acceptance_test", "source"} for r in refs if isinstance(r, dict)):
                errors.append(f"{label}: completed task needs artifact, executed acceptance-test, or source evidence")
            for ref_obj in refs:
                if isinstance(ref_obj, dict) and ref_obj.get("record_type") == "acceptance_test":
                    linked_test = tests_by_id.get(ref_obj.get("record_id"), {})
                    if linked_test.get("status") != "executed" or linked_test.get("execution", {}).get("outcome") != "pass":
                        errors.append(f"{label}: completion evidence acceptance test {ref_obj.get('record_id')} is not an executed passing test")
    for tid in sorted(_cycle_nodes(task_graph)):
        errors.append(f"Build-task dependency cycle includes {tid}")

    planned_req_ids = {
        rid for task in build_tasks if isinstance(task, dict) and task.get("status") != "cancelled"
        for rid in task.get("requirement_ids", [])
    }
    for req in requirements:
        if (isinstance(req, dict) and req.get("status") == "approved"
                and req.get("release_scope") in {"mvp", "post_mvp"}
                and req.get("requirement_id") not in planned_req_ids):
            errors.append(f"Approved in-scope requirement {req.get('requirement_id')} has no build task")

    # Artifact references in earlier-stage records now resolve to indexed files.
    # Legacy workspaces without an artifact ledger remain readable; the migration warning
    # explains that artifact resolution becomes enforceable once the B8 ledger is initialized.
    def walk_artifact_refs(value: Any, label: str) -> None:
        if isinstance(value, dict):
            if value.get("record_type") == "artifact":
                artifact_id = value.get("record_id")
                if artifact_ledger_present and artifact_id not in artifacts_by_id:
                    errors.append(f"{label}: missing artifact reference {artifact_id}")
            for key, child in value.items():
                walk_artifact_refs(child, f"{label}.{key}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk_artifact_refs(child, f"{label}[{index}]")

    artifact_reference_groups = [
        ("records/council-reviews.jsonl", council_reviews),
        ("records/decisions.jsonl", decisions),
        ("records/assumption-tests.jsonl", assumption_tests),
        ("evaluations/results.jsonl", evaluation_results),
    ]
    for filename, rows in artifact_reference_groups:
        for row_no, row in enumerate(rows, start=1):
            walk_artifact_refs(row, f"{filename}:{row_no}")

    # The structured JSON demo plan and human-readable script are linked, not competing sources.
    if artifact_ledger_present:
        structured_demo_artifact = artifacts_by_type.get("demo_plan_data")
        if demo_plan is not None and not structured_demo_artifact:
            errors.append("records/artifacts.jsonl: demo-plan.json must be registered as a demo_plan_data artifact")
        elif structured_demo_artifact and structured_demo_artifact.get("path") != "demo-plan.json":
            errors.append("records/artifacts.jsonl: demo_plan_data artifact must point to demo-plan.json")
    if demo_plan is not None and demo_plan.get("status") == "approved":
        if artifacts_by_type.get("demo_plan", {}).get("status") != "approved":
            errors.append("demo-plan.json: approved status requires an approved DEMO_PLAN.md artifact")
        if artifacts_by_type.get("demo_plan_data", {}).get("status") != "approved":
            errors.append("demo-plan.json: approved status requires an approved structured demo-plan.json artifact")
    if demo_plan is not None and demo_plan.get("status") != "approved":
        for artifact_type in ("demo_plan", "demo_plan_data"):
            if artifacts_by_type.get(artifact_type, {}).get("status") == "approved":
                errors.append(f"demo-plan.json: status is {demo_plan.get('status')} but {artifact_type} artifact is marked approved")

    # Demo claims must preserve the difference between a live result and an illustration.
    if demo_plan is not None:
        if state and demo_plan.get("project_id") != state.get("project_id"):
            errors.append("demo-plan.json: project_id does not match project.json")
        seen_demo_step_ids: set[str] = set()
        for row_no, step in enumerate(demo_plan.get("steps", []), start=1):
            if not isinstance(step, dict):
                continue
            step_id = step.get("step_id")
            if step_id in seen_demo_step_ids:
                errors.append(f"demo-plan.json: duplicate demo step ID {step_id}")
            elif step_id:
                seen_demo_step_ids.add(step_id)
            for rid in step.get("requirement_ids", []):
                if rid not in req_by_id:
                    errors.append(f"demo-plan.json: steps[{row_no}]: missing requirement reference {rid}")
                elif req_by_id[rid].get("status") in {"rejected", "superseded"}:
                    errors.append(f"demo-plan.json: steps[{row_no}]: cannot demonstrate rejected/superseded requirement {rid}")
        for row_no, claim in enumerate(demo_plan.get("demo_claims", []), start=1):
            if not isinstance(claim, dict):
                continue
            refs = claim.get("evidence_refs", [])
            _check_refs(refs, lookup, f"demo-plan.json:demo_claims[{row_no}]", errors)
            if claim.get("claim_strength") in {"demonstrated", "measured"} and not refs:
                errors.append(f"demo-plan.json:demo_claims[{row_no}]: demonstrated/measured claim requires evidence references")
            if claim.get("claim_strength") == "demonstrated":
                passed = any(
                    ref.get("record_type") == "acceptance_test"
                    and tests_by_id.get(ref.get("record_id"), {}).get("status") == "executed"
                    and tests_by_id.get(ref.get("record_id"), {}).get("execution", {}).get("outcome") == "pass"
                    for ref in refs if isinstance(ref, dict)
                )
                artifact_evidence = any(ref.get("record_type") == "artifact" for ref in refs if isinstance(ref, dict))
                if not passed and not artifact_evidence:
                    errors.append(f"demo-plan.json:demo_claims[{row_no}]: demonstrated claim needs a passing acceptance test or inspectable artifact")
                if artifact_evidence:
                    reviewed_artifact = any(
                        ref.get("record_type") == "artifact"
                        and artifacts_by_id.get(ref.get("record_id"), {}).get("status") in {"reviewed", "approved"}
                        for ref in refs if isinstance(ref, dict)
                    )
                    if not passed and not reviewed_artifact:
                        errors.append(
                            f"demo-plan.json:demo_claims[{row_no}]: artifact-only demonstration evidence "
                            "must reference an artifact with reviewed or approved status"
                        )
            if claim.get("claim_strength") == "measured":
                measured_evidence = any(
                    ref.get("record_type") == "research_finding"
                    and finding_by_id.get(ref.get("record_id"), {}).get("evidence_label") == "measured"
                    for ref in refs if isinstance(ref, dict)
                )
                for ref in refs:
                    if not isinstance(ref, dict) or ref.get("record_type") != "acceptance_test":
                        continue
                    linked_test = tests_by_id.get(ref.get("record_id"), {})
                    if (linked_test.get("status") != "executed"
                            or linked_test.get("execution", {}).get("outcome") != "pass"):
                        continue
                    measurement_specific = linked_test.get("test_type") == "performance"
                    for criterion_ref in linked_test.get("criterion_refs", []):
                        if not isinstance(criterion_ref, dict):
                            continue
                        linked_requirement = req_by_id.get(criterion_ref.get("requirement_id"), {})
                        for criterion in linked_requirement.get("acceptance_criteria", []):
                            if (isinstance(criterion, dict)
                                    and criterion.get("criterion_id") == criterion_ref.get("criterion_id")
                                    and criterion.get("verification_method") in {"measurement", "usability_test"}):
                                measurement_specific = True
                    result_refs = linked_test.get("execution", {}).get("evidence_refs", [])
                    inspectable_result = any(
                        (result_ref.get("record_type") == "artifact"
                         and artifacts_by_id.get(result_ref.get("record_id"), {}).get("status") in {"reviewed", "approved"})
                        or (result_ref.get("record_type") == "research_finding"
                            and finding_by_id.get(result_ref.get("record_id"), {}).get("evidence_label") == "measured")
                        for result_ref in result_refs if isinstance(result_ref, dict)
                    )
                    measured_evidence = measured_evidence or (measurement_specific and inspectable_result)
                if not measured_evidence:
                    errors.append(
                        f"demo-plan.json:demo_claims[{row_no}]: measured claim requires a research finding explicitly labelled measured, "
                        "or a passing measurement/performance test with inspectable reviewed/approved result evidence"
                    )
        if demo_plan.get("status") == "approved" and not demo_plan.get("steps"):
            errors.append("demo-plan.json: approved demo plan must contain at least one walkthrough step")
        if demo_plan.get("status") == "not_applicable" and (demo_plan.get("steps") or demo_plan.get("demo_claims")):
            errors.append("demo-plan.json: not_applicable demo plan must not contain walkthrough steps or demo claims")

    _validate_document_sections(project_dir, artifacts_by_type, errors)
    _validate_document_traceability(project_dir, artifacts_by_type, requirements, build_tasks, demo_plan, errors)

    # Completed workflow stages need their corresponding artifact disposition.
    if isinstance(state, dict):
        completed = set(state.get("completed_stages", []))
        gate_map = {
            "P7": ("prd",),
            "P8": ("technical_design",),
            # P9 is not a bypass around product/technical approval: its own exit
            # reference requires the PRD and applicable design to be approved.
            "P9": ("prd", "technical_design", "build_plan", "demo_plan"),
        }
        for stage, artifact_types in gate_map.items():
            if stage not in completed:
                continue
            if stage == "P8" and "P7" not in completed:
                errors.append("state.json: P8 is marked complete but prerequisite stage P7 is not complete")
            if stage == "P9":
                for prerequisite in ("P7", "P8"):
                    if prerequisite not in completed:
                        errors.append(f"state.json: P9 is marked complete but prerequisite stage {prerequisite} is not complete")
            for artifact_type in artifact_types:
                artifact = artifacts_by_type.get(artifact_type)
                acceptable = artifact and artifact.get("status") == "approved"
                if artifact_type == "demo_plan" and demo_plan and demo_plan.get("status") == "not_applicable":
                    acceptable = True
                if not acceptable:
                    errors.append(f"state.json: {stage} is marked complete but {artifact_type} is not approved or explicitly not applicable")

    return errors
