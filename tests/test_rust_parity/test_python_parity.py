"""C1: Python baseline parity — Rust output matches Python reference output.

Tests that the Rust kernel (nwau-core) produces numerically identical
outputs to the Python reference calculator when consuming the same
synthetic golden fixtures (tests/fixtures/golden/).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

# Ensure the project root is on sys.path so nwau_py is importable
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import nwau_py.calculators.acute as acute  # noqa: E402
import nwau_py.fixtures as fixtures  # noqa: E402
from nwau_py.rust_bridge import load_rust_extension  # noqa: E402

GOLDEN_DIR = PROJECT_ROOT / "tests" / "fixtures" / "golden"
DATA_DIR = PROJECT_ROOT / "tests" / "data"
PYTHON_EXPOSED_RUST_CALCULATORS = {"acute"}
PYTHON_BLOCKED_RUST_CALCULATORS = {
    "subacute": (
        "Rust sub-acute has no Python Rust entrypoint; Python parity "
        "needs a source-backed fixture and explicit bridge entrypoint first."
    ),
}


def _golden_manifests() -> list[Path]:
    """Return a sorted list of manifest.json paths under tests/fixtures/golden/."""
    if not GOLDEN_DIR.is_dir():
        return []
    return sorted(GOLDEN_DIR.glob("*/manifest.json"))


@pytest.fixture(params=_golden_manifests(), ids=lambda p: p.parent.name)
def golden_fixture(request) -> tuple[fixtures.FixturePack, fixtures.FixtureCase]:
    """Yield (pack, case) for each golden fixture manifest.

    Each parameterised call loads the manifest, locates the corresponding
    Python calculator, and builds a FixtureCase.
    """
    manifest_path: Path = request.param
    pack = fixtures.load_fixture_pack(manifest_path)
    calculator_name = pack.manifest.calculator

    calculator_map: dict[str, callable] = {
        "acute": acute.calculate_acute_rust_2025,
    }

    calc_fn = calculator_map.get(calculator_name)
    if calc_fn is None:
        blocked_reason = PYTHON_BLOCKED_RUST_CALCULATORS.get(calculator_name)
        assert blocked_reason, (
            f"Golden fixture '{pack.manifest.fixture_id}' uses calculator "
            f"'{calculator_name}' without a Python-exposed Rust bridge or "
            "an explicit blocked Rust parity reason."
        )
        pytest.skip(blocked_reason)

    case = fixtures.FixtureCase(
        pack=pack,
        calculator=calc_fn,
        calculator_params=acute.AcuteParams(),
        result_column="NWAU25",
    )
    return pack, case


# ---------------------------------------------------------------------------
# Helper — load price weights
# ---------------------------------------------------------------------------


def _load_price_weights(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
    """Load reference price weights for the given pricing year."""
    import pandas as pd

    weights = pd.read_csv(Path("tests/data") / "nep25_aa_price_weights.csv")
    weights["DRG"] = weights["DRG"].astype(str).str.strip("b'")
    return weights


def _require_rust_extension_available() -> None:
    """Skip parity tests when the optional PyO3 extension is not built."""
    try:
        load_rust_extension()
    except ImportError as exc:
        pytest.skip(str(exc))


# ---------------------------------------------------------------------------
# Parity tests
# ---------------------------------------------------------------------------


def test_rust_output_matches_golden_expected(golden_fixture, monkeypatch):
    """Rust output must match the golden expected values within tolerance."""
    _require_rust_extension_available()
    pack, case = golden_fixture
    monkeypatch.setattr(acute, "_load_price_weights", _load_price_weights)

    input_df = fixtures.read_payload_frame(pack, "input")
    expected_df = fixtures.read_payload_frame(pack, "expected_output")

    rust_result = case.calculator(
        input_df,
        case.calculator_params,
        year=pack.manifest.pricing_year,
        ref_dir=DATA_DIR / pack.manifest.pricing_year,
    )

    fixtures.assert_fixture_case_output(case, rust_result, expected_df)

    tol = pack.manifest.precision.tolerance
    result_col = rust_result[case.result_column].to_numpy()
    expected_col = expected_df[case.result_column].to_numpy()
    assert result_col == pytest.approx(expected_col, rel=tol.relative, abs=tol.absolute)


def test_rust_output_matches_python_output(golden_fixture, monkeypatch):
    """Rust output must match the native Python output within tolerance."""
    _require_rust_extension_available()
    pack, case = golden_fixture
    monkeypatch.setattr(acute, "_load_price_weights", _load_price_weights)

    input_df = fixtures.read_payload_frame(pack, "input")

    python_calculator_map: dict[str, callable] = {
        "acute": acute.calculate_acute,
    }
    py_calc = python_calculator_map.get(pack.manifest.calculator)
    if py_calc is None:
        blocked_reason = PYTHON_BLOCKED_RUST_CALCULATORS.get(pack.manifest.calculator)
        assert blocked_reason, (
            f"Golden fixture '{pack.manifest.fixture_id}' uses calculator "
            f"'{pack.manifest.calculator}' without a Python reference mapping "
            "or an explicit blocked Rust parity reason."
        )
        pytest.skip(blocked_reason)

    python_result = py_calc(
        input_df,
        case.calculator_params,
        year=pack.manifest.pricing_year,
        ref_dir=DATA_DIR / pack.manifest.pricing_year,
    )
    rust_result = case.calculator(
        input_df,
        case.calculator_params,
        year=pack.manifest.pricing_year,
        ref_dir=DATA_DIR / pack.manifest.pricing_year,
    )

    tol = pack.manifest.precision.tolerance
    py_col = python_result[case.result_column].to_numpy()
    rs_col = rust_result[case.result_column].to_numpy()
    assert rs_col == pytest.approx(py_col, rel=tol.relative, abs=tol.absolute)


def test_all_golden_fixtures_have_python_exposed_rust_kernel_registered():
    """Every promoted golden fixture must have a Python-exposed Rust mapping."""
    available = PYTHON_EXPOSED_RUST_CALCULATORS
    for manifest_path in _golden_manifests():
        pack = fixtures.load_fixture_pack(manifest_path)
        assert pack.manifest.calculator in available, (
            f"Golden fixture '{pack.manifest.fixture_id}' uses calculator "
            f"'{pack.manifest.calculator}' which has no Python-exposed Rust kernel. "
            f"Registered: {available}"
        )


def test_subacute_rust_parity_is_blocked_until_python_entrypoint_and_fixture_exist():
    """Subacute Rust signals must not be treated as default Python parity."""
    import nwau_py.calculators as calculators
    import nwau_py.calculators.subacute as subacute

    manifest_calculators = {
        fixtures.load_fixture_pack(path).manifest.calculator
        for path in _golden_manifests()
    }

    assert PYTHON_BLOCKED_RUST_CALCULATORS["subacute"]
    assert "subacute" not in PYTHON_EXPOSED_RUST_CALCULATORS
    assert "subacute" not in manifest_calculators
    assert "calculate_subacute" in calculators.__all__
    assert "calculate_subacute_rust" not in calculators.__all__
    assert not hasattr(subacute, "calculate_subacute_rust")
    assert not hasattr(subacute, "calculate_subacute_rust_2025")


def test_blocked_rust_calculators_have_tracked_defer_reasons():
    assert set(PYTHON_BLOCKED_RUST_CALCULATORS) == {"subacute"}
    for calculator_name, reason in PYTHON_BLOCKED_RUST_CALCULATORS.items():
        assert calculator_name not in PYTHON_EXPOSED_RUST_CALCULATORS
        assert "fixture" in reason.lower()
        assert "entrypoint" in reason.lower()


def test_rust_parity_holds_under_input_variation(monkeypatch):
    """Randomised input variation must not break Rust/Python parity."""
    _require_rust_extension_available()
    import pandas as pd

    monkeypatch.setattr(acute, "_load_price_weights", _load_price_weights)

    n = 3

    input_df = pd.DataFrame(
        {
            "DRG": ["801A", "801A", "801A"],
            "LOS": [5.0, 10.0, 80.0],
            "ICU_HOURS": [0.0] * n,
            "ICU_OTHER": [0.0] * n,
            "PAT_SAMEDAY_FLAG": [False] * n,
            "PAT_PRIVATE_FLAG": [False] * n,
            "PAT_COVID_FLAG": [False] * n,
        }
    )

    params = acute.AcuteParams()
    ref_dir = DATA_DIR / "2025"

    python_result = acute.calculate_acute(
        input_df, params, year="2025", ref_dir=ref_dir
    )
    rust_result = acute.calculate_acute_rust_2025(
        input_df, params, year="2025", ref_dir=ref_dir
    )

    pd.testing.assert_series_equal(
        python_result["NWAU25"],
        rust_result["NWAU25"],
        check_names=False,
        atol=1e-4,
        rtol=1e-4,
    )
