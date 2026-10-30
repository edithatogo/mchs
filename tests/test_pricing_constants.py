from datetime import date

from nwau_py.pricing_constants import (
    NEC26,
    NEC26_SOURCE,
    NEC_BY_YEAR,
    NEP26,
    NEP26_SOURCE,
    NEP_BY_YEAR,
    get_nec,
    get_nep,
    get_supported_pricing_years,
)


def test_nep26_value():
    assert NEP26 == 7418
    assert NEP_BY_YEAR["2026"] == 7418
    assert get_nep("2026") == 7418
    assert NEP26_SOURCE.resource_url.endswith(
        "/resources/national-efficient-price-determination-2026-27"
    )
    assert NEP26_SOURCE.published_on == date(2026, 3, 11)


def test_nep25_value():
    assert NEP_BY_YEAR["2025"] == 7258
    assert get_nep("2025") == 7258


def test_get_nep_unknown_year():
    assert get_nep("2024") is None
    assert get_nep("1999") is None


def test_get_nec_defaults():
    """NEC is only published as headline components for 2026-27."""
    assert NEC_BY_YEAR["2025"] is None
    assert get_nec("2025") is None


def test_nec26_components():
    assert NEC26.fixed_cost_dollars == 3_127_000
    assert NEC26.variable_cost_per_nwau == 8_003
    assert NEC26.in_scope_hospitals == 364
    assert get_nec("2026") == NEC26
    assert NEC26_SOURCE.resource_url.endswith(
        "/resources/national-efficient-cost-determination-2026-27"
    )
    assert NEC26_SOURCE.published_on == date(2026, 3, 11)


def test_get_supported_years():
    years = get_supported_pricing_years()
    assert "2025" in years
    assert "2026" in years
    assert years == sorted(years)


def test_get_nep_returns_int():
    assert isinstance(get_nep("2026"), int)


def test_packaged_prices_match_canonical_manifests():
    import json
    from pathlib import Path

    import yaml

    root = Path(__file__).resolve().parents[1]
    packaged = json.loads((root / "nwau_py/data/pricing_constants.json").read_text())
    for year, record in packaged.items():
        manifest = yaml.safe_load(
            (root / "reference-data" / year / "manifest.yaml").read_text()
        )
        assert record == {
            key: manifest["constants"]["nep"][key] for key in ["value", "source_url"]
        }
