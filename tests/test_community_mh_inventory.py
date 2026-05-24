"""Tests for the community mental health calculator artifact inventory."""

from pathlib import Path

from nwau_py.calculators.community_mh_inventory import (
    CMTY_MH_ARTIFACTS,
    get_active_years,
    get_inventory_by_year,
    get_shadow_years,
)


def test_inventory_has_all_expected_years():
    """The inventory must cover NEP21 through NEP26."""
    years = sorted(a.year for a in CMTY_MH_ARTIFACTS)
    assert years == ["2021", "2022", "2023", "2024", "2025", "2026"]


def test_inventory_sas_templates_refer_to_existing_files():
    """Every SAS template path referenced in the inventory must exist."""
    for artifact in CMTY_MH_ARTIFACTS:
        for path in artifact.sas_templates:
            assert Path(path).exists(), (
                f"SAS template not found: {path} (year={artifact.year})"
            )


def test_inventory_sas_calculators_refer_to_existing_files():
    """Every SAS calculator path referenced in the inventory must exist."""
    for artifact in CMTY_MH_ARTIFACTS:
        for path in artifact.sas_calculators:
            assert Path(path).exists(), (
                f"SAS calculator not found: {path} (year={artifact.year})"
            )


def test_inventory_cmty_price_weights_refer_to_existing_files():
    """Every community price weights table must exist on disk."""
    for artifact in CMTY_MH_ARTIFACTS:
        for path in artifact.cmty_price_weights:
            assert Path(path).exists(), (
                f"Community price weights not found: {path} (year={artifact.year})"
            )


def test_inventory_adm_price_weights_refer_to_existing_files():
    """Every admitted price weights table must exist on disk."""
    for artifact in CMTY_MH_ARTIFACTS:
        for path in artifact.adm_price_weights:
            assert Path(path).exists(), (
                f"Admitted price weights not found: {path} (year={artifact.year})"
            )


def test_nep25_nep26_are_active_pricing():
    """NEP25 and NEP26 are active pricing years for community MH."""
    for year in ("2025", "2026"):
        art = next(a for a in CMTY_MH_ARTIFACTS if a.year == year)
        assert art.pricing_status == "active", f"{year} should be active"


def test_nep21_nep24_are_shadow_pricing():
    """NEP21 through NEP24 are shadow-pricing years for community mental
    health."""
    for artifact in CMTY_MH_ARTIFACTS:
        if artifact.year in ("2021", "2022", "2023", "2024"):
            assert artifact.pricing_status == "shadow", (
                f"Expected shadow pricing for year {artifact.year}"
            )


def test_nep22_has_excel_workbook():
    """NEP22 has a dedicated AMHCC shadow Excel workbook for community mental
    health."""
    nep22 = next(a for a in CMTY_MH_ARTIFACTS if a.year == "2022")
    assert len(nep22.excel_workbooks) >= 1
    for wb in nep22.excel_workbooks:
        path = Path(wb)
        assert path.suffix == ".xlsb"
        assert path.parts[:4] == ("archive", "ihacpa", "raw", "2022")
        assert "amhcc_shadow" in path.name


def test_nep26_has_excel_workbook():
    """NEP26 has a community MH Excel workbook in the raw archive."""
    nep26 = next(a for a in CMTY_MH_ARTIFACTS if a.year == "2026")
    assert len(nep26.excel_workbooks) >= 1
    for wb in nep26.excel_workbooks:
        path = Path(wb)
        assert path.suffix == ".xlsb"
        assert path.parts[:4] == ("archive", "ihacpa", "raw", "2026")
        assert "mental_health_activity_community" in path.name


def test_amhcc_prefix_convention_documented():
    """AMHCC prefix '1' = admitted, '2' = community."""
    for artifact in CMTY_MH_ARTIFACTS:
        assert artifact.amhcc_admitted_prefix == "1"
        assert artifact.amhcc_community_prefix == "2"


def test_all_artifacts_have_user_guide_field():
    """Every inventory entry must record user-guide availability."""
    for artifact in CMTY_MH_ARTIFACTS:
        assert isinstance(artifact.user_guide_available, bool)


def test_no_mh_calculator_before_nep21():
    """NEP13 through NEP20 do not have dedicated mental health calculators."""
    assert all(int(a.year) >= 2021 for a in CMTY_MH_ARTIFACTS)
    earliest = min(int(a.year) for a in CMTY_MH_ARTIFACTS)
    assert earliest == 2021, f"Expected earliest year 2021, got {earliest}"


def test_get_inventory_by_year_found():
    """get_inventory_by_year returns the correct artifact for known years."""
    for year in ("2025", "2026"):
        art = get_inventory_by_year(year)
        assert art is not None
        assert art.year == year
        assert art.pricing_status == "active"


def test_get_inventory_by_year_not_found():
    """get_inventory_by_year returns None for an unknown year."""
    assert get_inventory_by_year("2015") is None
    assert get_inventory_by_year("2099") is None


def test_get_active_years():
    """get_active_years returns only years with active pricing status."""
    active = get_active_years()
    assert "2025" in active
    assert "2026" in active
    assert all(y not in active for y in get_shadow_years())


def test_get_shadow_years():
    """get_shadow_years returns only years with shadow pricing status."""
    shadow = get_shadow_years()
    assert "2021" in shadow
    assert "2022" in shadow
    assert "2023" in shadow
    assert "2024" in shadow
    assert "2026" not in shadow
    assert "2025" not in shadow
    assert all(y not in shadow for y in get_active_years())
