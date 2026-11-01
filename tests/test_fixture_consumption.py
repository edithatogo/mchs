from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

import numpy as np
import pytest

from nwau_py import compat as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import nwau_py.fixtures as fixtures

PYREADSTAT = types.ModuleType("pyreadstat")
PYREADSTAT.ReadstatError = Exception
PYREADSTAT._readstat_parser = types.SimpleNamespace(PyreadstatError=Exception)
sys.modules.setdefault("pyreadstat", PYREADSTAT)

ACUTE_PATH = (
    Path(__file__).resolve().parents[1] / "nwau_py" / "calculators" / "acute.py"
)
SPEC = importlib.util.spec_from_file_location("fixture_acute", ACUTE_PATH)
assert SPEC is not None and SPEC.loader is not None
acute = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(acute)


FIXTURE_MANIFEST = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "golden"
    / "acute_2025"
    / "manifest.json"
)
BASE = Path("tests/data")


def _load_weights(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
    weights = pd.read_csv(BASE / "nep25_aa_price_weights.csv")
    weights["DRG"] = weights["DRG"].str.strip("b'")
    return weights


def _load_pack():
    pack = fixtures.load_fixture_pack(FIXTURE_MANIFEST)
    assert pack.manifest.schema_version == "1.0"
    assert pack.manifest.fixture_id == "acute_2025"
    assert pack.manifest.calculator == "acute"
    assert pack.manifest.pricing_year == "2025"
    assert pack.manifest.service_stream == "admitted acute"
    assert pack.manifest.cross_language_ready is True
    assert pack.manifest.privacy_classification == "synthetic"
    assert pack.manifest.source_basis.kind == "synthetic_sample"
    assert pack.manifest.source_basis.input_source.endswith("acute_input.csv")
    assert pack.manifest.source_basis.expected_output_source.endswith(
        "acute_expected.csv"
    )
    return pack


def _calculate_from_fixture(monkeypatch, pack):
    input_df = fixtures.read_payload_frame(pack, "input")

    monkeypatch.setattr(acute, "_load_price_weights", _load_weights)

    result = acute.calculate_acute(
        input_df,
        acute.AcuteParams(),
        year=pack.manifest.pricing_year,
        ref_dir=BASE / pack.manifest.pricing_year,
    )
    expected_df = fixtures.read_payload_frame(pack, "expected_output")
    return result, expected_df


def test_acute_fixture_pack_output_parity(monkeypatch):
    pack = _load_pack()
    result, expected_df = _calculate_from_fixture(monkeypatch, pack)
    case = fixtures.FixtureCase(
        pack=pack,
        calculator=acute.calculate_acute,
        calculator_params=acute.AcuteParams(),
        result_column="NWAU25",
        parity_type="output parity",
    )

    fixtures.assert_fixture_case_output(case, result, expected_df)

    assert np.allclose(
        result["NWAU25"].to_numpy(),
        expected_df["NWAU25"].to_numpy(),
        rtol=pack.manifest.precision.tolerance.relative,
        atol=pack.manifest.precision.tolerance.absolute,
    ), case.provenance_label


def test_acute_fixture_pack_regression_parity_uses_manifest_provenance():
    pack = _load_pack()
    assert pack.manifest.provenance["created_from"] == (
        "tests/data/acute_input.csv and tests/data/acute_expected.csv"
    )
    assert "synthetic fixture pack" in pack.manifest.provenance["notes"][0].lower()
    assert pack.manifest.payloads["input"].row_count == len(
        fixtures.read_payload_frame(pack, "input")
    )
    assert pack.manifest.payloads["expected_output"].row_count == len(
        fixtures.read_payload_frame(pack, "expected_output")
    )
    assert pack.manifest.precision.tolerance.absolute == pytest.approx(0.0001)
    assert pack.manifest.precision.tolerance.relative == pytest.approx(0.0001)
