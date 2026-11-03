from datetime import date

import pytest

from nwau_py.calculators.relative_stay import StayStratum
from nwau_py.calculators.stay_benchmarks import (
    DatedStay,
    calculate_stay_report,
    load_benchmarks,
)

HEADER = "kind,start_year,edition,stratum,expected_days,source\n"
FIRST = "pricing_alos,2025,11.0,801B,8.3,NEP25 Appendix H\n"
SECOND = "pricing_alos,2026,12.0,801B,9.4,NEP26 Appendix H\n"


def test_boundary_and_pool(tmp_path):
    path = tmp_path / "series.csv"
    path.write_text(HEADER + FIRST + SECOND + "rsi,2026,12.0,801B,7,synthetic RSI\n")
    registry = load_benchmarks(path)
    june = DatedStay(date(2026, 6, 30), "11.0", StayStratum("801B", 10, 100))
    july = DatedStay(date(2026, 7, 1), "12.0", StayStratum("801B", 20, 160))
    report = calculate_stay_report([june, july], registry, kind="pricing_alos")
    assert report.kind == "pricing_alos"
    assert report.annual[2025].index == pytest.approx(100 / 83)
    assert report.annual[2026].index == pytest.approx(160 / 188)
    assert report.pooled.index == pytest.approx(260 / 271)
    assert (
        calculate_stay_report([july], registry, kind="rsi").pooled.expected_days == 140
    )
    with pytest.raises(ValueError, match="No matching"):
        calculate_stay_report([june], registry, kind="rsi")
    with pytest.raises(ValueError, match="No matching"):
        calculate_stay_report(
            [DatedStay(july.separation_date, "11.0", july.stay)],
            registry,
            kind="pricing_alos",
        )


@pytest.mark.parametrize(
    "extra", [FIRST, FIRST.replace("11.0", "12.0"), SECOND.replace("9.4", "nan")]
)
def test_invalid_registry(tmp_path, extra):
    path = tmp_path / "series.csv"
    path.write_text(HEADER + FIRST + extra)
    with pytest.raises(ValueError):
        load_benchmarks(path)
