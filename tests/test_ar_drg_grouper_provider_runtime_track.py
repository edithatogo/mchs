from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

from nwau_py.cli.main import cli as _cli

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "ar_drg_grouper_provider_runtime_20260703"
DOCS = ROOT / "nwau_py" / "docs" / "calculators.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def test_track_metadata_and_plan_record_provider_runtime_contract() -> None:
    metadata = _read_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    index = _read_text(TRACK / "index.md")

    assert metadata["track_id"] == "ar_drg_grouper_provider_runtime_20260703"
    assert metadata["status"] == "in_progress"
    assert metadata["github_issue_number"] == 206
    assert metadata["github_issue_url"].endswith("/issues/206")
    assert metadata["track_class"] == "classifier"
    assert "support-status reporting" in metadata["support_scope"]
    assert "provider runtime registry" in metadata["primary_contract"]
    assert "pluggable AR-DRG grouper providers" in spec
    assert "source_available" in spec
    assert "Phase 1: Provider Runtime Contract and Registry" in plan
    assert "Phase 2: Provider Output Validation, CLI Exposure, and Docs" in plan
    assert "GitHub Issue #206" in index


def test_provider_runtime_module_exposes_supported_profiles_and_fails_closed() -> None:
    import nwau_py.ar_drg_grouper_runtime as runtime
    from nwau_py.ar_drg_grouper import (
        ARDRGGrouperError,
        ARDRGGrouperVersionWindow,
        build_ar_drg_external_reference,
        build_ar_drg_precomputed_group_record,
        ensure_ar_drg_grouper_compatibility,
    )

    profiles = runtime.list_ar_drg_grouper_provider_profiles()
    assert [profile.provider_type for profile in profiles] == [
        "precomputed",
        "local_command",
        "local_service",
        "file_exchange",
        "container",
    ]
    assert {profile.support_status for profile in profiles} == {
        "source_available",
        "executable",
        "validated",
    }

    precomputed = runtime.validate_ar_drg_grouper_provider_compatibility(
        "precomputed",
        year="2026",
        ar_drg_version="v12.0",
        icd_10_am_version="12th edition",
        achi_version="12th edition",
        acs_version="12th edition",
    )
    assert precomputed.compatible is True
    assert precomputed.support_status == "source_available"

    reference = build_ar_drg_external_reference(
        reference_id="local-command-placeholder",
        reference_type="local_command",
        command="ar-drg-grouper --input in.json --output out.json",
        supported_versions=(
            ARDRGGrouperVersionWindow(
                pricing_year="2026",
                ar_drg_version="v12.0",
                icd_10_am_version="12th edition",
                achi_version="12th edition",
                acs_version="12th edition",
            ),
        ),
    )
    command_result = runtime.validate_ar_drg_grouper_provider_compatibility(
        "local_command",
        year="2026",
        reference=reference,
    )
    assert command_result.compatible is True
    assert command_result.support_status == "executable"

    missing = runtime.validate_ar_drg_grouper_provider_compatibility(
        "local_service",
        year="2026",
    )
    assert missing.compatible is False
    assert "requires a reference" in (missing.reason or "")

    unsupported = runtime.validate_ar_drg_grouper_provider_compatibility(
        "container",
        year="2026",
        container_image=None,
    )
    assert unsupported.compatible is False
    assert "container_image" in (unsupported.reason or "")

    with pytest.raises(ARDRGGrouperError, match=re.escape("v12.0")):
        ensure_ar_drg_grouper_compatibility(
            "2026",
            ar_drg_version="v11.0",
            icd_10_am_version="12th edition",
            achi_version="12th edition",
            acs_version="12th edition",
        )

    record = build_ar_drg_precomputed_group_record(
        "I03A",
        year="2026",
        ar_drg_version="v12.0",
        icd_10_am_version="12th edition",
        achi_version="12th edition",
        acs_version="12th edition",
        input_sha256="0" * 64,
        generated_at="2026-05-13T00:00:00+00:00",
    )
    provider_record = runtime.build_ar_drg_group_record_from_provider(
        "precomputed",
        record.drg,
        year="2026",
        ar_drg_version=record.provenance.ar_drg_version,
        icd_10_am_version=record.provenance.icd_10_am_version,
        achi_version=record.provenance.achi_version,
        acs_version=record.provenance.acs_version,
        input_sha256=record.provenance.input_sha256,
        generated_at="2026-05-13T00:00:00+00:00",
    )
    assert provider_record.provenance.source_mode == "precomputed"


def test_provider_runtime_cli_lists_statuses_and_validates() -> None:
    runner = CliRunner()

    list_result = runner.invoke(
        _cli,
        ["ar-drg", "provider", "list"],
    )
    assert list_result.exit_code == 0, list_result.output
    listing = json.loads(list_result.output)
    assert {row["provider_type"] for row in listing["records"]} == {
        "precomputed",
        "local_command",
        "local_service",
        "file_exchange",
        "container",
    }

    validate_result = runner.invoke(
        _cli,
        [
            "ar-drg",
            "provider",
            "validate-compatibility",
            "--provider-type",
            "precomputed",
            "--year",
            "2026",
            "--ar-drg-version",
            "v12.0",
            "--icd-10-am-version",
            "12th edition",
            "--achi-version",
            "12th edition",
            "--acs-version",
            "12th edition",
        ],
    )
    assert validate_result.exit_code == 0, validate_result.output
    validated = json.loads(validate_result.output)
    assert validated["support_status"] == "source_available"
    assert validated["compatible"] is True


def test_provider_runtime_docs_state_the_local_only_boundary() -> None:
    docs = _read_text(DOCS)

    for phrase in [
        "precomputed AR-DRG values",
        "local command, local service, file exchange, and optional container",
        "blocked_licensed",
        "provenance-bearing inputs",
    ]:
        assert phrase in docs
