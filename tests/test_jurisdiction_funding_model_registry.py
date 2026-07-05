from __future__ import annotations

from nwau_py import jurisdiction_funding_model_registry as funding_registry


def test_jurisdiction_registry_covers_all_states_with_explicit_statuses() -> None:
    registry = funding_registry.JurisdictionFundingModelRegistry.default()

    assert registry.list_available_years() == ["2025"]
    assert registry.list_available_jurisdictions("2025") == [
        "ACT",
        "NSW",
        "NT",
        "QLD",
        "SA",
        "TAS",
        "VIC",
        "WA",
    ]
    assert registry.list_support_statuses("2025") == {
        "ACT": funding_registry.JurisdictionFundingModelStatus.PUBLIC,
        "NSW": funding_registry.JurisdictionFundingModelStatus.PUBLIC,
        "NT": funding_registry.JurisdictionFundingModelStatus.BLOCKED,
        "QLD": funding_registry.JurisdictionFundingModelStatus.LOCAL_ONLY,
        "SA": funding_registry.JurisdictionFundingModelStatus.PUBLIC,
        "TAS": funding_registry.JurisdictionFundingModelStatus.BLOCKED,
        "VIC": funding_registry.JurisdictionFundingModelStatus.LOCAL_ONLY,
        "WA": funding_registry.JurisdictionFundingModelStatus.PUBLIC,
    }


def test_jurisdiction_registry_records_provenance_and_price_boundaries() -> None:
    registry = funding_registry.JurisdictionFundingModelRegistry.default()

    nsw = registry.require_record("NSW", "2025")
    vic = registry.require_record("VIC", "2025")
    wa = registry.require_record("WA", "2025")
    tas = registry.require_record("TAS", "2025")

    assert nsw.price_per_hwau == 5675
    assert nsw.source_term == "State Price per NWAU"
    assert "DNR" in nsw.provenance_notes[0]
    assert vic.price_per_hwau == 7600
    assert (
        vic.support_status is funding_registry.JurisdictionFundingModelStatus.LOCAL_ONLY
    )
    assert wa.price_per_hwau is None
    assert wa.support_status is funding_registry.JurisdictionFundingModelStatus.PUBLIC
    assert tas.price_per_hwau is None
    assert tas.support_status is funding_registry.JurisdictionFundingModelStatus.BLOCKED


def test_parallel_jurisdiction_valuation_selects_priced_rows_only() -> None:
    registry = funding_registry.JurisdictionFundingModelRegistry.default()
    valuations = registry.select_parallel_valuations(100.0)

    priced = {
        valuation.jurisdiction: valuation
        for valuation in valuations
        if valuation.funding is not None
    }
    blocked = {
        valuation.jurisdiction: valuation
        for valuation in valuations
        if valuation.funding is None
    }

    assert priced["NSW"].funding == 567500.0
    assert priced["VIC"].funding == 760000.0
    assert priced["QLD"].funding == 720000.0
    assert (
        blocked["WA"].support_status
        is funding_registry.JurisdictionFundingModelStatus.PUBLIC
    )
    assert (
        blocked["TAS"].support_status
        is funding_registry.JurisdictionFundingModelStatus.BLOCKED
    )


def test_package_level_helpers_fail_closed_for_unknown_row() -> None:
    registry = funding_registry.JurisdictionFundingModelRegistry.default()

    assert funding_registry.get_jurisdiction_funding_model_record(
        "NSW", "2025"
    ).source_term
    assert funding_registry.list_jurisdiction_funding_model_records("2025")

    try:
        registry.require_record("NSW", "2024")
    except funding_registry.JurisdictionFundingModelError as exc:
        assert "No jurisdiction funding model row" in str(exc)
    else:  # pragma: no cover - defensive assertion branch
        raise AssertionError("missing jurisdiction model should fail closed")
