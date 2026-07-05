from __future__ import annotations

import pytest

from nwau_py.jurisdiction_price_sources import (
    JURISDICTIONS,
    JurisdictionPriceSourceIndex,
    JurisdictionPriceSourceStatus,
    SourceIndexError,
    get_jurisdiction_price_source,
    list_jurisdiction_price_sources,
    validate_price_source_coverage,
)


def test_default_source_index_covers_every_jurisdiction_for_2025() -> None:
    rows = list_jurisdiction_price_sources(financial_year="2025")

    assert {row.jurisdiction for row in rows} == set(JURISDICTIONS)
    assert all(row.financial_year == "2025" for row in rows)
    assert all(row.checksum for row in rows)
    assert all(row.source_url_or_path for row in rows)
    assert all(row.licence_status for row in rows)
    assert all(row.redistribution_status == "metadata_only" for row in rows)
    assert all(row.mapped_unit.startswith("HWAU") for row in rows)


def test_source_index_records_public_metadata_or_blocked_status_only() -> None:
    rows = list_jurisdiction_price_sources(financial_year="2025")
    statuses = {row.support_status for row in rows}

    assert statuses == {
        JurisdictionPriceSourceStatus.PUBLIC_METADATA,
        JurisdictionPriceSourceStatus.BLOCKED,
    }
    assert {
        row.jurisdiction
        for row in rows
        if row.support_status is JurisdictionPriceSourceStatus.BLOCKED
    } == {"NSW", "TAS", "NT"}
    assert {
        row.jurisdiction
        for row in rows
        if row.support_status is JurisdictionPriceSourceStatus.PUBLIC_METADATA
    } == {"VIC", "QLD", "WA", "SA", "ACT"}


def test_source_index_does_not_commit_price_values() -> None:
    for row in list_jurisdiction_price_sources(financial_year="2025"):
        serialised = row.to_dict()
        assert "price_per_hwau" not in serialised
        assert "not extracted" in row.price_term
        assert "numeric price extraction remains gated" in row.extraction_notes or (
            "No redistributable" in row.extraction_notes
        )


def test_source_index_fails_closed_for_missing_year_or_jurisdiction() -> None:
    index = JurisdictionPriceSourceIndex.default()

    with pytest.raises(SourceIndexError, match="No jurisdiction price source"):
        index.require_source("NSW", "2024")

    with pytest.raises(SourceIndexError, match="Missing jurisdiction price source"):
        index.validate_coverage(financial_year="2024")

    validate_price_source_coverage("2025")


def test_package_level_source_lookup_returns_expected_rows() -> None:
    qld = get_jurisdiction_price_source("QLD", "2025")
    act = get_jurisdiction_price_source("ACT", "2025")

    assert qld.source_unit == "QWAU"
    assert "Queensland-specific mapping validation" in qld.mapped_unit
    assert act.support_status is JurisdictionPriceSourceStatus.PUBLIC_METADATA
