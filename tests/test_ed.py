import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest

from nwau_py.utils import RA_VERSION

YEARS = [y for y in sorted(RA_VERSION.keys()) if int(y) >= 2025]

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

spec = importlib.util.spec_from_file_location(
    "ed",
    Path(__file__).resolve().parents[1] / "nwau_py" / "calculators" / "ed.py",
)
if spec is None or spec.loader is None:
    raise RuntimeError("failed to load ED calculator module")
ed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ed)


DATA = pd.DataFrame(
    {
        "AECC": ["E0110A"],
        "Error_Code": [0],
        "COMPENSABLE_STATUS": [2],
        "DVA_STATUS": [2],
        "adj_indigenous": [0.0],
        "adj_remoteness": [0.0],
        "adj_treat_remoteness": [0.0],
        "FUNDSC": [1],
    }
)

EXPECTED = 0.2837


@pytest.mark.parametrize("year", YEARS)
def test_calculate_ed_matches_sas_weights(monkeypatch, year):
    weights = pd.DataFrame({"AECC": ["E0110A"], "AECC_pw": [EXPECTED]})

    def _load(
        ref_dir: Path, classification_option: int, year: str = "2025"
    ) -> pd.DataFrame:
        return weights.rename(columns={"aecc_pw": "AECC_pw"})

    monkeypatch.setattr(ed, "_load_weights", _load)

    result = ed.calculate_ed(
        DATA.copy(),
        ed.EDParams(classification_option=3, eligibility_option=2),
        year=year,
        ref_dir=Path("unused"),
    )
    assert result["NWAU25"].iloc[0] == pytest.approx(EXPECTED, rel=1e-4)


CALC_DIR = Path("archive/sas/NEP25_SAS_NWAU_calculator/calculators")


def test_ed_reference_loaders_decode_classification_tables(monkeypatch):
    calls: list[Path] = []

    def fake_read_sas(path):
        calls.append(Path(path))
        name = Path(path).name
        if "edudg" in name:
            return pd.DataFrame({"UDG": [b"UDG01"], "udg_pw": [0.5]})
        if "edaecc" in name:
            return pd.DataFrame({"AECC": [b"E0110A"], "AECC_pw": [0.75]})
        return pd.DataFrame({"UDG": [b"UDG02"], "map": [1]})

    monkeypatch.setattr(pd, "read_sas", fake_read_sas)

    udg = ed._load_weights(Path("ref"), classification_option=2, year="2025")
    aecc = ed._load_weights(Path("ref"), classification_option=3, year="2025")
    mapping = ed._load_udg_map(Path("ref"))

    assert udg.to_dict("records") == [{"UDG": "UDG01", "udg_pw": 0.5}]
    assert aecc.to_dict("records") == [{"AECC": "E0110A", "AECC_pw": 0.75}]
    assert mapping.to_dict("records") == [{"UDG": "UDG02", "map": 1}]
    assert len(calls) == 3


@pytest.mark.parametrize("year", YEARS)
def test_calculate_ed_aecc_basic(monkeypatch, year):
    weights = pd.read_sas(CALC_DIR / "nep25_edaecc_price_weights.sas7bdat")
    weights["AECC"] = weights["AECC"].str.decode("ascii")
    row = weights[weights["AECC"] == "E0110A"].iloc[0]

    def _load(
        ref_dir: Path, classification_option: int, year: str = "2025"
    ) -> pd.DataFrame:
        return weights

    monkeypatch.setattr(ed, "_load_weights", _load)

    df = pd.DataFrame(
        {
            "AECC": ["E0110A"],
            "COMPENSABLE_STATUS": [2],
            "DVA_STATUS": [2],
            "adj_indigenous": [0.0],
            "adj_remoteness": [0.0],
            "adj_treat_remoteness": [0.03],
        }
    )

    result = ed.calculate_ed(
        df,
        ed.EDParams(classification_option=3),
        year=year,
        ref_dir=Path("unused"),
    )

    expected = round(row["AECC_pw"] * 1.03, 8)
    assert result["GWAU25"].iloc[0] == pytest.approx(expected)
    assert result["NWAU25"].iloc[0] == pytest.approx(expected)
    assert result["Error_Code"].iloc[0] == 0


@pytest.mark.parametrize("year", YEARS)
def test_calculate_ed_udg_mapping_and_errors(monkeypatch, year):
    weights = pd.read_sas(CALC_DIR / "nep25_edudg_price_weights.sas7bdat")
    weights["UDG"] = weights["UDG"].str.decode("ascii")
    udg_pw = weights[weights["UDG"] == "UDG01"].iloc[0]["udg_pw"]

    def _load_map(ref_dir: Path) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "type_of_visit": [1],
                "triage_category": [1],
                "episode_end_status": [1],
                "UDG": ["UDG01"],
            }
        )

    def _load(
        ref_dir: Path, classification_option: int, year: str = "2025"
    ) -> pd.DataFrame:
        return weights.rename(columns={"udg_pw": "udg_pw"})

    monkeypatch.setattr(ed, "_load_weights", _load)
    monkeypatch.setattr(ed, "_load_udg_map", _load_map)

    df = pd.DataFrame(
        {
            "type_of_visit": [1, 1, 1],
            "triage_category": [1, 1, 1],
            "episode_end_status": [1, 9, 1],
            "COMPENSABLE_STATUS": [2, 2, 1],
            "DVA_STATUS": [2, 2, 2],
            "adj_treat_remoteness": [0.0, 0.0, 0.0],
        }
    )

    result = ed.calculate_ed(
        df,
        ed.EDParams(classification_option=1),
        year=year,
        ref_dir=Path("unused"),
    )

    expected = round(udg_pw, 6)
    assert result.loc[0, "GWAU25"] == pytest.approx(expected)
    assert result.loc[0, "Error_Code"] == 0
    assert result.loc[0, "NWAU25"] == pytest.approx(expected)

    assert result.loc[1, "Error_Code"] == 3
    assert result.loc[1, "NWAU25"] == 0

    assert result.loc[2, "Error_Code"] == 2
    assert result.loc[2, "NWAU25"] == 0
