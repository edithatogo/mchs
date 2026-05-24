from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from nwau_py.ar_drg_grouper import (
    ARDRGGrouperError,
    ARDRGGrouperVersionWindow,
    build_ar_drg_external_reference,
    build_ar_drg_group_record_from_reference,
    build_ar_drg_precomputed_group_record,
    ensure_ar_drg_grouper_compatibility,
    hash_ar_drg_grouping_payload,
    validate_ar_drg_grouper_compatibility,
)

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "ar_drg_grouper_integration_20260512"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = ROOT / "contracts" / "ar-drg-icd-mapping-registry"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def _window_2026() -> ARDRGGrouperVersionWindow:
    return ARDRGGrouperVersionWindow(
        pricing_year="2026",
        ar_drg_version="v12.0",
        icd_10_am_version="12th edition",
        achi_version="12th edition",
        acs_version="12th edition",
    )


def test_ar_drg_grouper_track_contract_and_docs_are_complete() -> None:
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        TRACK / "review.md",
        TRACKS,
        CONTRACT / "ar-drg-icd-mapping-registry.contract.json",
        CONTRACT / "examples" / "precomputed-ar-drg-input.json",
        CONTRACT / "examples" / "external-local-grouper-references.json",
        CONTRACT / "examples" / "diagnostics.json",
        CONTRACT / "examples" / "license-boundary.json",
    ]:
        assert path.exists(), path

    metadata = _read_json(TRACK / "metadata.json")
    tracks = _read_text(TRACKS)
    spec = _read_text(TRACK / "spec.md")
    contract = _read_json(CONTRACT / "ar-drg-icd-mapping-registry.contract.json")

    assert metadata["status"] == "complete"
    assert metadata["current_state"] == "implemented-interface-contract"
    assert metadata["publication_status"] == "not-ready"
    assert "nwau_py.ar_drg_grouper" in metadata["primary_contract"]
    assert "- [x] **Track: AR-DRG Grouper Integration**" in tracks
    assert "precomputed AR-DRG inputs" in spec
    assert "does not reimplement proprietary grouping logic" in spec
    assert contract["registry_entry_types"][1]["id"] == "precomputed_input_record"


def test_precomputed_ar_drg_group_record_validates_versions_and_provenance() -> None:
    digest = hash_ar_drg_grouping_payload({"episode": "synthetic", "drg": "I03A"})
    record = build_ar_drg_precomputed_group_record(
        "I03A",
        year="2026",
        ar_drg_version="v12.0",
        icd_10_am_version="12th edition",
        achi_version="12th edition",
        acs_version="12th edition",
        input_sha256=digest,
        episode_id="synthetic-episode-1",
        generated_at="2026-05-13T00:00:00+00:00",
        notes=("precomputed locally",),
    )

    assert record.drg == "I03A"
    assert record.episode_id == "synthetic-episode-1"
    assert record.provenance.source_mode == "precomputed"
    assert record.provenance.external_reference_id is None
    assert record.provenance.input_sha256 == digest


def test_external_grouper_reference_supports_local_only_metadata() -> None:
    reference = build_ar_drg_external_reference(
        reference_id="local-command-placeholder",
        reference_type="local_command",
        command="ar-drg-grouper --input in.json --output out.json",
        local_path_hint="./licensed/ar-drg-grouper/README.local.md",
        supported_versions=(_window_2026(),),
        notes=("user supplied licensed grouper",),
    )

    assert reference.status == "unresolved"
    assert reference.license_boundary == "local-only"
    assert reference.supported_years() == ("2026",)

    result = validate_ar_drg_grouper_compatibility("2026", reference=reference)
    assert result.compatible is True
    assert result.declared_versions["ar_drg"] == "v12.0"

    digest = hash_ar_drg_grouping_payload({"external": "synthetic"})
    grouped = build_ar_drg_group_record_from_reference(
        "I03A",
        year="2026",
        reference=reference,
        input_sha256=digest,
        grouper_version="v12.0-local",
        generated_at="2026-05-13T00:00:00+00:00",
    )
    assert grouped.provenance.source_mode == "external-reference"
    assert grouped.provenance.external_reference_id == "local-command-placeholder"


def test_grouper_integration_fails_closed_for_missing_and_mismatched_versions() -> None:
    missing = validate_ar_drg_grouper_compatibility(
        "2026",
        ar_drg_version="v12.0",
        icd_10_am_version="12th edition",
        achi_version=None,
        acs_version="12th edition",
    )
    assert missing.compatible is False
    assert "missing declared version" in (missing.reason or "")

    mismatch = validate_ar_drg_grouper_compatibility(
        "2026",
        ar_drg_version="v11.0",
        icd_10_am_version="12th edition",
        achi_version="12th edition",
        acs_version="12th edition",
    )
    assert mismatch.compatible is False
    assert "expected 'v12.0'" in (mismatch.reason or "")

    with pytest.raises(ARDRGGrouperError, match=re.escape("expected 'v12.0'")):
        ensure_ar_drg_grouper_compatibility(
            "2026",
            ar_drg_version="v11.0",
            icd_10_am_version="12th edition",
            achi_version="12th edition",
            acs_version="12th edition",
        )


def test_external_reference_requires_local_resolution_details() -> None:
    with pytest.raises(ARDRGGrouperError, match="command string"):
        build_ar_drg_external_reference(
            reference_id="bad-command",
            reference_type="local_command",
            command=None,
            supported_versions=(_window_2026(),),
        )

    unsupported = build_ar_drg_external_reference(
        reference_id="old-window",
        reference_type="local_command",
        command="ar-drg-grouper --input in.json",
        supported_versions=(
            ARDRGGrouperVersionWindow(
                pricing_year="2025",
                ar_drg_version="v11.0",
                icd_10_am_version="12th edition",
                achi_version="12th edition",
                acs_version="12th edition",
            ),
        ),
    )
    result = validate_ar_drg_grouper_compatibility("2026", reference=unsupported)
    assert result.compatible is False
    assert "does not declare" in (result.reason or "")


def test_contract_examples_are_metadata_only_and_local_only() -> None:
    precomputed = _read_json(CONTRACT / "examples" / "precomputed-ar-drg-input.json")
    external = _read_json(
        CONTRACT / "examples" / "external-local-grouper-references.json"
    )
    diagnostics = _read_json(CONTRACT / "examples" / "diagnostics.json")

    assert precomputed["privacy"]["contains_phi"] is False
    assert "proprietary grouping rules" in json.dumps(precomputed).lower()
    assert all(
        item["license_boundary"] == "local-only" for item in external["references"]
    )
    assert diagnostics["diagnostics"]["status"] == "pass"
