from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
ACTIVE_WORKSTREAMS = ROOT / "conductor" / "active-workstreams.md"
REVIEW_TEMPLATE = ROOT / "conductor" / "templates" / "review-template.md"
SUPPORT_SCHEMA = ROOT / "contracts" / "support" / "support-status.schema.json"
SUPPORT_MATRIX = ROOT / "contracts" / "support" / "support-matrix.json"
EVIDENCE_SCHEMA = ROOT / "contracts" / "release" / "evidence-bundle.schema.json"
EVIDENCE_PASS = (
    ROOT / "tests" / "fixtures" / "governance" / "release-evidence.pass.json"
)
SURFACE_RELATIONSHIP = (
    ROOT / "contracts" / "surfaces" / "api-mcp-openai-relationship.json"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return cast(dict[str, Any], json.loads(_read(path)))


def test_active_workstreams_and_review_template_define_handoff_protocol():
    active = _read(ACTIVE_WORKSTREAMS)
    template = _read(REVIEW_TEMPLATE)

    assert "Parallel-agent notice" in active
    assert "Cline/deepseek" in active
    assert "stage only owned files" in active
    assert "Rust implementation and generated contracts" in active

    for heading in [
        "Files changed",
        "Contract impact",
        "Validation",
        "Unresolved blockers",
        "Handoff",
    ]:
        assert heading in template


def test_support_matrix_enforces_deferred_and_historical_statuses():
    schema = _json(SUPPORT_SCHEMA)
    matrix = _json(SUPPORT_MATRIX)
    statuses = schema["properties"]["status"]["enum"]
    entries = {entry["id"]: entry for entry in matrix["entries"]}

    for status in [
        "unsupported",
        "blocked",
        "planned",
        "canary",
        "opt_in",
        "release_candidate",
        "ga",
        "no_new_development",
        "historical",
    ]:
        assert status in statuses

    for entry_id in [
        "language.scala-spark",
        "language.swift",
        "language.go",
        "language.matlab",
    ]:
        assert entries[entry_id]["status"] == "no_new_development"
        assert entries[entry_id]["ready_for_implementation"] is False

    assert entries["surface.sql-duckdb"]["status"] == "historical"
    assert entries["surface.sql-duckdb"]["ready_for_implementation"] is False
    assert entries["runtime.rust-core"]["ready_for_implementation"] is True


def test_release_evidence_schema_and_fixture_require_ga_blockers():
    schema = _json(EVIDENCE_SCHEMA)
    fixture = _json(EVIDENCE_PASS)

    for field in [
        "release_id",
        "git_commit",
        "git_tag",
        "packages",
        "supported_scope",
        "source_manifests",
        "schema_versions",
        "fixture_results",
        "parity_reports",
        "coverage",
        "sbom",
        "security",
        "provenance",
        "known_limitations",
        "rollback",
    ]:
        assert field in schema["required"]
        assert field in fixture

    assert fixture["coverage"]["actual"] >= fixture["coverage"]["threshold"]


def test_api_mcp_openai_relationship_keeps_logic_in_rust_core():
    relationship = _json(SURFACE_RELATIONSHIP)

    assert relationship["canonical_logic_owner"] == "rust-core"

    by_surface = {item["surface"]: item for item in relationship["relationships"]}
    assert by_surface["http-api"]["role"] == "domain transport"
    assert by_surface["mcp"]["role"] == "agent transport"
    assert by_surface["openai-tool-adapter"]["role"] == "generated tool adapter"
    assert by_surface["openai-tool-adapter"]["emulates_llm_endpoint"] is False

    for item in relationship["relationships"]:
        assert item["owns_calculator_logic"] is False
        assert item["schema_source"] == "contracts/canonical"

    assert "must not claim to emulate an LLM endpoint" in " ".join(
        relationship["rules"]
    )
