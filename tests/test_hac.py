import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pytest

from nwau_py.groupers.hac import flag_hacs
from nwau_py.utils import RA_VERSION

YEARS = [y for y in sorted(RA_VERSION.keys()) if int(y) >= 2025]


@pytest.mark.parametrize("year", YEARS)
def test_hac_a020_maps_to_c03(year):
    if year != "2025":
        pytest.skip("HAC data only verified for 2025")
    flags = flag_hacs(["A020"], edition="07", year=year)
    assert flags.get("hac032c03_flag") == 1
    assert flags.get("hac032_flag") == 1


@pytest.mark.parametrize("year", YEARS)
def test_hac_t810_maps_to_c04(year):
    if year != "2025":
        pytest.skip("HAC data only verified for 2025")
    flags = flag_hacs(["T810"], edition="07", year=year)
    assert flags.get("hac032c04_flag") == 1


@pytest.mark.parametrize("year", YEARS)
def test_hac_multiple_codes(year):
    if year != "2025":
        pytest.skip("HAC data only verified for 2025")
    flags = flag_hacs(["A020", "T810"], edition="07", year=year)
    assert flags.get("hac032c03_flag") == 1
    assert flags.get("hac032c04_flag") == 1
    assert flags.get("hac032_flag") == 1


def test_hac_empty_and_mapping():
    from nwau_py.groupers.hac import count_hac_diagnoses, load_hac_mapping

    df = load_hac_mapping("07", year="2025")
    assert df is not None

    counts = count_hac_diagnoses(["NONEXISTENT_CODE_XYZ"], edition="07", year="2025")
    assert all(v == 0 for v in counts.values())
