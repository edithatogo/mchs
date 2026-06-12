from __future__ import annotations

import json
from pathlib import Path

import pytest

from nwau_py.reference_data import (
    ReferenceBundle,
    reference_bundle_root,
    resolve_reference_bundle,
)

SOURCE_PAGE_URL = "https://www.ihacpa.gov.au/health-care/pricing/nwau-calculators"
CREATED_FROM = "tests/data/acute_input.csv and tests/data/acute_expected.csv"


def _write_bundle(
    root: Path,
    *,
    year: str,
    calculator: str,
    bundle_id: str,
    source_artifact_id: str,
    source_page_url: str,
    checksum: str,
    provenance: dict[str, object] | None = None,
) -> Path:
    bundle_dir = root / year / calculator / bundle_id
    bundle_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "bundle_id": bundle_id,
        "calculator": calculator,
        "pricing_year": year,
        "manifest_path": str(bundle_dir / "manifest.json"),
        "source_artifact_id": source_artifact_id,
        "source_page_url": source_page_url,
        "checksum": checksum,
        "provenance": provenance
        or {
            "created_from": f"{calculator}-{year}",
            "notes": ["synthetic reference bundle for selection tests"],
        },
    }
    manifest_path = bundle_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (bundle_dir / "payload.csv").write_text("value\n1\n", encoding="utf-8")
    return manifest_path


def test_reference_bundle_resolver_selects_exact_year_calculator_and_bundle(tmp_path):
    manifest_path = _write_bundle(
        tmp_path,
        year="2025",
        calculator="acute",
        bundle_id="acute-2025-v1",
        source_artifact_id="ihacpa-acute-2025-sas",
        source_page_url=SOURCE_PAGE_URL,
        checksum="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    )
    _write_bundle(
        tmp_path,
        year="2025",
        calculator="acute",
        bundle_id="acute-2025-v2",
        source_artifact_id="ihacpa-acute-2025-sas",
        source_page_url=SOURCE_PAGE_URL,
        checksum="fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210",
    )

    bundle = resolve_reference_bundle(
        tmp_path,
        year="2025",
        calculator="acute",
        bundle_id="acute-2025-v1",
    )

    assert isinstance(bundle, ReferenceBundle)
    assert bundle.manifest_path == manifest_path
    assert bundle.bundle_id == "acute-2025-v1"
    assert bundle.calculator == "acute"
    assert bundle.pricing_year == "2025"
    assert bundle.source_artifact_id == "ihacpa-acute-2025-sas"
    assert bundle.source_page_url.endswith("/nwau-calculators")
    assert bundle.checksum.startswith("0123456789abcdef")
    assert bundle.provenance["created_from"] == "acute-2025"
    assert "synthetic reference bundle" in bundle.provenance["notes"][0]


def test_reference_bundle_resolver_requires_an_existing_bundle_directory(tmp_path):
    with pytest.raises(FileNotFoundError, match="year='2025'"):
        resolve_reference_bundle(tmp_path, year="2025", calculator="acute")


def test_reference_bundle_resolver_rejects_ambiguous_bundle_directories(tmp_path):
    _write_bundle(
        tmp_path,
        year="2025",
        calculator="acute",
        bundle_id="acute-2025-v1",
        source_artifact_id="ihacpa-acute-2025-sas",
        source_page_url=SOURCE_PAGE_URL,
        checksum="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    )
    _write_bundle(
        tmp_path,
        year="2025",
        calculator="acute",
        bundle_id="acute-2025-v2",
        source_artifact_id="ihacpa-acute-2025-sas",
        source_page_url=SOURCE_PAGE_URL,
        checksum="fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210",
    )

    with pytest.raises(ValueError, match="ambiguous reference bundle"):
        resolve_reference_bundle(tmp_path, year="2025", calculator="acute")


def test_reference_bundle_resolver_preserves_manifest_identity_metadata(tmp_path):
    _write_bundle(
        tmp_path,
        year="2025",
        calculator="acute",
        bundle_id="acute-2025-v1",
        source_artifact_id="ihacpa-acute-2025-sas",
        source_page_url=SOURCE_PAGE_URL,
        checksum="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        provenance={
            "created_from": CREATED_FROM,
            "notes": [
                "synthetic reference bundle for selection tests",
                "no patient-level data included",
            ],
        },
    )

    bundle = resolve_reference_bundle(
        tmp_path,
        year="2025",
        calculator="acute",
        bundle_id="acute-2025-v1",
    )

    assert bundle.bundle_id == "acute-2025-v1"
    assert bundle.calculator == "acute"
    assert bundle.pricing_year == "2025"
    assert bundle.source_artifact_id == "ihacpa-acute-2025-sas"
    assert bundle.provenance["created_from"] == CREATED_FROM
    assert bundle.provenance["notes"] == [
        "synthetic reference bundle for selection tests",
        "no patient-level data included",
    ]


def test_reference_bundle_root_returns_expected_directory():
    assert reference_bundle_root(
        Path("data/reference"),
        year="2025",
        calculator="acute",
    ) == Path("data/reference/2025/acute")


def test_reference_bundle_root_rejects_bad_year_and_calculator_labels():
    with pytest.raises(ValueError, match="leading or trailing whitespace"):
        reference_bundle_root(Path("data/reference"), year=" 2025", calculator="acute")
    with pytest.raises(ValueError, match="must not be blank"):
        reference_bundle_root(Path("data/reference"), year="2025", calculator="")


def test_reference_bundle_resolver_rejects_missing_explicit_bundle_id(tmp_path):
    root = tmp_path / "2025" / "acute"
    root.mkdir(parents=True)

    with pytest.raises(FileNotFoundError, match="bundle_id='missing'"):
        resolve_reference_bundle(
            tmp_path,
            year="2025",
            calculator="acute",
            bundle_id="missing",
        )


def test_reference_bundle_resolver_rejects_non_object_manifest(tmp_path):
    bundle_dir = tmp_path / "2025" / "acute" / "bad"
    bundle_dir.mkdir(parents=True)
    (bundle_dir / "manifest.json").write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="must be a JSON object"):
        resolve_reference_bundle(
            tmp_path,
            year="2025",
            calculator="acute",
            bundle_id="bad",
        )


def test_reference_bundle_resolver_rejects_manifest_identity_mismatches(tmp_path):
    manifest_path = _write_bundle(
        tmp_path,
        year="2025",
        calculator="acute",
        bundle_id="acute-2025-v1",
        source_artifact_id="ihacpa-acute-2025-sas",
        source_page_url=SOURCE_PAGE_URL,
        checksum="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    for key, value, match in [
        ("pricing_year", "2024", "year does not match"),
        ("calculator", "ed", "calculator does not match"),
        ("bundle_id", "other", "id does not match"),
    ]:
        candidate = dict(manifest)
        candidate[key] = value
        manifest_path.write_text(json.dumps(candidate), encoding="utf-8")

        with pytest.raises(ValueError, match=match):
            resolve_reference_bundle(
                tmp_path,
                year="2025",
                calculator="acute",
                bundle_id="acute-2025-v1",
            )

    candidate = dict(manifest)
    candidate["checksum"] = "not-a-sha"
    manifest_path.write_text(json.dumps(candidate), encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        resolve_reference_bundle(
            tmp_path,
            year="2025",
            calculator="acute",
            bundle_id="acute-2025-v1",
        )
