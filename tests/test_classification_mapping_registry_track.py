from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, cast

import pytest
from click.testing import CliRunner

from nwau_py.cli.main import cli as _cli

ROOT = Path(__file__).resolve().parents[1]
TRACK = (
    ROOT
    / "conductor"
    / "archive"
    / "classification_mapping_registry_enrichment_20260703"
)
DOCS = ROOT / "nwau_py" / "docs" / "calculators.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def test_track_metadata_and_plan_record_the_classification_mapping_contract():
    metadata = _read_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    index = _read_text(TRACK / "index.md")

    assert metadata["track_id"] == "classification_mapping_registry_enrichment_20260703"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert metadata["publication_status"] == "not-applicable"
    assert metadata["github_issue_number"] == 205
    assert metadata["github_issue_url"].endswith("/issues/205")
    assert "stream/year/classification compatibility" in metadata["support_scope"]
    assert "local-only mapping hooks" in metadata["primary_contract"]
    assert "Classification Mapping Registry Enrichment" in spec
    assert "single shared source of truth" in spec
    assert "Phase 1: Shared Classification Registry Contract" in plan
    assert "Phase 2: Local Hooks, CLI Exposure, and Docs" in plan
    assert "GitHub Issue #205" in index


def test_public_classification_registry_records_are_public_metadata_only() -> None:
    from nwau_py.classification_mapping_registry import (
        get_classification_mapping_record,
        list_classification_mapping_records,
    )

    records = list_classification_mapping_records()
    assert {record.system for record in records} == {
        "ar_drg",
        "aecc",
        "udg",
        "tier_2",
        "amhcc",
    }
    assert {record.stream for record in records} == {
        "admitted_acute",
        "emergency_department",
        "emergency_service",
        "admitted_non_acute",
        "community_mental_health",
    }

    ar_drg = get_classification_mapping_record("ar_drg", "2026")
    assert ar_drg is not None
    assert ar_drg.support_status == "blocked_licensed"
    assert ar_drg.public_asset.kind == "public-metadata"
    assert ar_drg.public_asset.restricted is False
    assert ar_drg.public_asset.local_path_hint is None
    assert ar_drg.public_asset.source_refs
    assert ar_drg.local_hooks

    aecc = get_classification_mapping_record("AECC", "2026")
    assert aecc is not None
    assert aecc.support_status == "source_available"
    assert aecc.public_asset.kind == "public-metadata"
    assert aecc.local_hooks == ()


def test_classification_registry_fails_closed_for_stream_and_version_mismatches() -> (
    None
):
    from nwau_py.classification_mapping_registry import (
        ClassificationMappingRegistryError,
        ensure_classification_mapping_compatibility,
        validate_classification_mapping_compatibility,
    )

    result = validate_classification_mapping_compatibility(
        "admitted_acute",
        "ar_drg",
        "2026",
        version="v11.0",
    )
    assert result.compatible is False
    assert "expects v12.0" in (result.reason or "")

    with pytest.raises(
        ClassificationMappingRegistryError, match=re.escape("expects v12.0")
    ):
        ensure_classification_mapping_compatibility(
            "admitted_acute",
            "ar_drg",
            "2026",
            version="v11.0",
        )

    stream_result = validate_classification_mapping_compatibility(
        "emergency_department",
        "ar_drg",
        "2026",
        version="v12.0",
    )
    assert stream_result.compatible is False
    assert "not available for stream" in (stream_result.reason or "")


def test_local_mapping_hook_placeholders_validate_without_restricted_payloads() -> None:
    from nwau_py.classification_mapping_registry import (
        ClassificationMappingRegistryError,
        build_classification_local_hook_reference,
        ensure_classification_local_hook_compatibility,
        validate_classification_local_hook_compatibility,
    )

    hook = build_classification_local_hook_reference(
        hook_id="ar-drg-local-command-placeholder",
        system="ar_drg",
        stream="admitted_acute",
        pricing_year="2026",
        reference_type="local_command",
        status="placeholder",
        command="ar-drg-grouper --input in.json --output out.json",
        local_path_hint="archive/ihacpa/raw/2026/licensed/ar_drg/grouper/",
        source_refs=(
            "https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system",
        ),
        notes=("placeholder only",),
    )

    assert hook.status == "placeholder"
    assert hook.license_boundary == "local-only"
    assert hook.local_path_hint and "archive/ihacpa/raw/2026" in hook.local_path_hint

    validation = validate_classification_local_hook_compatibility(hook)
    assert validation.compatible is True
    assert validation.record is not None

    with pytest.raises(
        ClassificationMappingRegistryError,
        match="licensed content",
    ):
        ensure_classification_local_hook_compatibility(
            build_classification_local_hook_reference(
                hook_id="bad-hook",
                system="ar_drg",
                stream="admitted_acute",
                pricing_year="2026",
                reference_type="local_command",
                status="placeholder",
                command=None,
                local_path_hint=None,
                source_refs=(
                    "https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system",
                ),
                notes=("missing local path",),
            )
        )


def test_classification_registry_cli_lists_support_status_and_validates() -> None:
    runner = CliRunner()

    list_result = runner.invoke(
        cast(Any, _cli),
        ["classification", "registry", "list", "--year", "2026"],
    )
    assert list_result.exit_code == 0, list_result.output
    listing = json.loads(list_result.output)
    assert {record["stream"] for record in listing["records"]} == {
        "admitted_acute",
        "emergency_department",
        "emergency_service",
        "admitted_non_acute",
        "community_mental_health",
    }
    assert any(
        record["support_status"] == "blocked_licensed" for record in listing["records"]
    )

    validate_result = runner.invoke(
        cast(Any, _cli),
        [
            "classification",
            "registry",
            "validate-compatibility",
            "--stream",
            "admitted_acute",
            "--system",
            "ar_drg",
            "--year",
            "2026",
            "--version",
            "v12.0",
        ],
    )
    assert validate_result.exit_code == 0, validate_result.output
    validated = json.loads(validate_result.output)
    assert validated["support_status"] == "blocked_licensed"
    assert validated["compatible"] is True


def test_drg_derivation_docs_state_the_local_only_boundary() -> None:
    docs = _read_text(DOCS)

    for phrase in [
        "AR-DRG v12.0",
        "classification preflight validator",
        "local licensed tooling or precomputed DRG values",
        "does not claim parity validation",
    ]:
        assert phrase in docs
