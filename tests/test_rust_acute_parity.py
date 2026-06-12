"""Phase 4 parity and canary coverage for the acute 2025 Rust proof of concept."""

# ruff: noqa: I001

from __future__ import annotations

import sys
import types
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PYREADSTAT = types.ModuleType("pyreadstat")
PYREADSTAT.ReadstatError = Exception
PYREADSTAT._readstat_parser = types.SimpleNamespace(PyreadstatError=Exception)
sys.modules.setdefault("pyreadstat", PYREADSTAT)

import nwau_py.calculators.acute as acute  # noqa: E402
import nwau_py.fixtures as fixtures  # noqa: E402
from nwau_py import rust_bridge  # noqa: E402


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "golden" / "acute_2025"
MANIFEST = FIXTURE_ROOT / "manifest.json"


def _load_weights(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
    weights = pd.read_csv(Path("tests/data") / "nep25_aa_price_weights.csv")
    weights["DRG"] = weights["DRG"].astype(str).str.strip("b'")
    return weights


def _fixture_case() -> tuple[fixtures.FixturePack, fixtures.FixtureCase]:
    pack = fixtures.load_fixture_pack(MANIFEST)
    case = fixtures.FixtureCase(
        pack=pack,
        calculator=acute.calculate_acute_rust_2025,
        calculator_params=acute.AcuteParams(),
        result_column="NWAU25",
    )
    return pack, case


def _require_rust_extension() -> None:
    try:
        rust_bridge.load_rust_extension()
    except ImportError as exc:
        pytest.skip(f"optional Rust extension unavailable: {exc}")


def test_rust_and_python_match_the_acute_fixture_pack(monkeypatch):
    _require_rust_extension()
    pack, case = _fixture_case()
    monkeypatch.setattr(acute, "_load_price_weights", _load_weights)

    input_df = fixtures.read_payload_frame(pack, "input")
    expected_df = fixtures.read_payload_frame(pack, "expected_output")

    python_result = acute.calculate_acute(
        input_df,
        acute.AcuteParams(),
        year=pack.manifest.pricing_year,
        ref_dir=Path("tests/data") / pack.manifest.pricing_year,
    )
    rust_result = acute.calculate_acute_rust_2025(
        input_df,
        acute.AcuteParams(),
        year=pack.manifest.pricing_year,
        ref_dir=Path("tests/data") / pack.manifest.pricing_year,
    )

    fixtures.assert_fixture_case_output(case, rust_result, expected_df)
    assert rust_result["NWAU25"].to_numpy() == pytest.approx(
        expected_df["NWAU25"].to_numpy(), rel=1e-4, abs=1e-4
    )
    assert rust_result["NWAU25"].to_numpy() == pytest.approx(
        python_result["NWAU25"].to_numpy(), rel=1e-4, abs=1e-4
    )


def test_rust_failure_reports_include_provenance_and_tolerance(monkeypatch):
    _require_rust_extension()
    pack, case = _fixture_case()
    monkeypatch.setattr(acute, "_load_price_weights", _load_weights)

    input_df = fixtures.read_payload_frame(pack, "input")
    rust_result = acute.calculate_acute_rust_2025(
        input_df,
        acute.AcuteParams(),
        year=pack.manifest.pricing_year,
        ref_dir=Path("tests/data") / pack.manifest.pricing_year,
    )
    expected_df = fixtures.read_payload_frame(pack, "expected_output").copy()
    expected_df["NWAU25"] = expected_df["NWAU25"] + 1.0

    with pytest.raises(fixtures.FixtureManifestError) as exc_info:
        fixtures.assert_fixture_case_output(case, rust_result, expected_df)

    message = str(exc_info.value)
    assert "fixture=acute_2025" in message
    assert "calculator=acute" in message
    assert "exceeded tolerance" in message
    assert "abs=0.0001" in message
    assert "rel=0.0001" in message
