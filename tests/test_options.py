import importlib.util
import sys
from pathlib import Path

import pytest

from nwau_py import compat as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

spec = importlib.util.spec_from_file_location(
    "outpatients",
    Path(__file__).resolve().parents[1] / "nwau_py" / "calculators" / "outpatients.py",
)
outpatients = importlib.util.module_from_spec(spec)
spec.loader.exec_module(outpatients)

DATA = pd.DataFrame(
    {
        "TIER2_CLINIC": [10.01],
        "SERVICE_DATE": [pd.Timestamp("2024-07-01")],
        "BIRTH_DATE": [pd.Timestamp("1990-01-01")],
        "PAT_MULTIPROV_FLAG": [0],
        "EST_ELIGIBLE_PAED_FLAG": [1],
    }
)


def test_clear_data_removes_cache(tmp_path, monkeypatch):
    pytest.skip("Cache clearing not supported without full dependencies")
    monkeypatch.chdir(tmp_path)
    cache_dir = Path(".cache")
    cache_dir.mkdir(exist_ok=True)
    (cache_dir / "dummy").write_text("x")

    def _load_csv(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
        df = pd.read_csv(
            Path(__file__).resolve().parent / "data" / "nep25_op_price_weights.csv"
        )
        return df.rename(columns={"tier2_clinic": "TIER2_CLINIC"})

    outpatients._load_weights = _load_csv  # monkeypatch without pytest fixture
    # ensure caching uses CSV to avoid optional parquet dependencies
    orig_loader = outpatients.load_sas_table

    def _load_csv_cache(path, **kw):
        return orig_loader(path, cache_format="csv", **kw)

    outpatients.load_sas_table = _load_csv_cache

    outpatients.calculate_outpatients(
        DATA.copy(),
        outpatients.OutpatientParams(clear_data=True, debug_mode=True),
        year="2025",
        ref_dir=Path("."),
    )
    assert not cache_dir.exists()
