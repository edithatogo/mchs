"""Tests for the community mental health calculator module."""

import numpy as np
import pandas as pd

from nwau_py.calculators.community_mh_calculator import (
    CommunityMHCalculator,
    CommunityMHParams,
    calculate_community_mh,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_cmty_weights() -> pd.DataFrame:
    """Return fake community price weight data matching the SAS table schema."""
    return pd.DataFrame(
        {
            "AMHCC": ["2001", "2002"],
            "_cmty_fixed_pw": [0.0, 0.0],
            "_cmty_sc_pat_pw": [0.10, 0.15],
            "_cmty_sc_nopat_pw": [0.05, 0.08],
        }
    )


DATA = pd.DataFrame(
    {
        "AMHCC": ["2001", "2002", "2001"],
        "SC_PAT_PUB": [1, 2, 0],
        "SC_NOPAT_PUB": [0, 1, 3],
    }
)


# ---------------------------------------------------------------------------
# Params
# ---------------------------------------------------------------------------


def test_params_defaults():
    """CommunityMHParams should have sensible defaults."""
    p = CommunityMHParams()
    assert p.debug_mode is False


# ---------------------------------------------------------------------------
# Calculator
# ---------------------------------------------------------------------------


def test_calculate_community_mh_basic():
    """Basic community mental health calculation returns expected NWAU."""
    result = calculate_community_mh(
        DATA.copy(),
        CommunityMHParams(debug_mode=True),
        cmty_weights=_mock_cmty_weights(),
    )
    # Row 0: 1*0.10 + 0*0.05 = 0.10
    # Row 1: 2*0.15 + 1*0.08 = 0.38
    # Row 2: 0*0.10 + 3*0.05 = 0.15
    expected = [0.10, 0.38, 0.15]
    assert np.allclose(result["_w01"].values, expected)
    assert np.allclose(result["NWAU25"].values, expected)


def test_calculate_community_mh_no_service_contacts():
    """Zero service contacts should result in zero NWAU."""
    df = pd.DataFrame(
        {
            "AMHCC": ["2001"],
            "SC_PAT_PUB": [0],
            "SC_NOPAT_PUB": [0],
        }
    )
    result = calculate_community_mh(
        df, CommunityMHParams(), cmty_weights=_mock_cmty_weights()
    )
    assert result["NWAU25"].iloc[0] == 0.0


def test_calculate_community_mh_negative_contacts_clamped():
    """The calculator should not produce negative NWAU."""
    df = pd.DataFrame(
        {
            "AMHCC": ["2001"],
            "SC_PAT_PUB": [-1],
            "SC_NOPAT_PUB": [0],
        }
    )
    result = calculate_community_mh(
        df, CommunityMHParams(), cmty_weights=_mock_cmty_weights()
    )
    assert result["NWAU25"].iloc[0] >= 0


def test_calculate_community_mh_debug_mode():
    """Debug mode retains intermediate columns."""
    result = calculate_community_mh(
        DATA.copy(),
        CommunityMHParams(debug_mode=True),
        cmty_weights=_mock_cmty_weights(),
    )
    assert "_w01" in result.columns


def test_calculate_community_mh_debug_off():
    """Non-debug mode drops intermediate columns."""
    result = calculate_community_mh(
        DATA.copy(),
        CommunityMHParams(debug_mode=False),
        cmty_weights=_mock_cmty_weights(),
    )
    assert "_w01" not in result.columns


def test_calculator_class_api():
    """The CommunityMHCalculator class provides a top-level run method."""
    calc = CommunityMHCalculator()
    result = calc.run(DATA.copy(), CommunityMHParams(debug_mode=True))
    assert "NWAU25" in result.columns


def test_calculator_class_with_custom_weights():
    """The calculator can accept custom weight frames."""
    calc = CommunityMHCalculator()
    result = calc.run(
        DATA.copy(),
        CommunityMHParams(),
        cmty_weights=_mock_cmty_weights(),
    )
    assert np.allclose(result["NWAU25"].values, [0.10, 0.38, 0.15])


def test_calculate_community_mh_different_years():
    """The calculator produces output for the NWAU column of the given year."""
    result = calculate_community_mh(
        DATA.copy(),
        CommunityMHParams(),
        year="2024",
        cmty_weights=_mock_cmty_weights(),
    )
    assert "NWAU24" in result.columns
    assert "NWAU25" not in result.columns
