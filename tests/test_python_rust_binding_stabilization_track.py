"""Track-level tests for Python Rust binding stabilization."""

# ruff: noqa: E402

from __future__ import annotations

import builtins
import sys
import types
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PYREADSTAT: Any = types.ModuleType("pyreadstat")
PYREADSTAT.ReadstatError = Exception
PYREADSTAT._readstat_parser = types.SimpleNamespace(PyreadstatError=Exception)
sys.modules.setdefault("pyreadstat", PYREADSTAT)

import nwau_py.calculators.acute as acute
import nwau_py.fixtures as fixtures
import nwau_py.rust_bridge as rust_bridge

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "python_rust_binding_stabilization_20260512"
TRACK_DIR = ROOT / "conductor" / "tracks" / TRACK_ID
if not TRACK_DIR.exists():
    TRACK_DIR = ROOT / "conductor" / "archive" / TRACK_ID
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "golden" / "acute_2025"
MANIFEST = FIXTURE_ROOT / "manifest.json"
INPUT_CSV = FIXTURE_ROOT / "input.csv"
EXPECTED_CSV = FIXTURE_ROOT / "expected.csv"
WEIGHTS_CSV = ROOT / "tests" / "data" / "nep25_aa_price_weights.csv"
REF_DIR = ROOT / "tests" / "data" / "2025"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_weights(*_args, **_kwargs) -> pd.DataFrame:
    weights = pd.read_csv(WEIGHTS_CSV)
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


def test_track_docs_cover_opt_in_fallback_golden_fixtures_and_maturin_ci():
    spec = _read(TRACK_DIR / "spec.md").lower()
    plan = _read(TRACK_DIR / "plan.md").lower()
    package_readme = _read(ROOT / "nwau_py" / "README.md").lower()
    package_docs = _read(ROOT / "nwau_py" / "docs" / "calculators.md").lower()
    workflow = _read(ROOT / ".github" / "workflows" / "pr-ci.yml").lower()

    assert "opt-in" in spec
    assert "fallback behavior" in spec
    assert "share golden fixtures" in spec
    assert "maturin" in spec
    assert "maturin" in plan
    assert "golden fixtures" in plan
    assert "import failures" in plan
    assert "rust-backed opt-in path" in package_readme
    assert "default\npython calculator path" in package_readme
    assert "opt-in rust-backed acute 2025 adapter" in package_docs
    assert "uv run --with maturin maturin build --release" in workflow
    assert "pip install --no-deps" in workflow
    assert '  - "3.10"' in workflow
    assert '  - "3.14"' in workflow


def test_default_acute_execution_stays_on_the_pure_python_path(monkeypatch):
    monkeypatch.setattr(acute, "_load_price_weights", _load_weights)

    def _fail_if_called(*_args, **_kwargs):
        raise AssertionError("default acute execution should not touch the Rust hook")

    monkeypatch.setattr(acute, "_rust_calculate_acute_2025_row", _fail_if_called)

    input_df = pd.read_csv(INPUT_CSV)
    expected = pd.read_csv(EXPECTED_CSV)["NWAU25"].to_numpy()

    result = acute.calculate_acute(
        input_df,
        acute.AcuteParams(),
        year="2025",
        ref_dir=REF_DIR,
    )

    assert list(input_df.columns) == list(result.columns[: len(input_df.columns)])
    assert "NWAU25" in result.columns
    assert result["NWAU25"].to_numpy() == pytest.approx(expected, rel=1e-4, abs=1e-4)


def test_rust_opt_in_execution_matches_the_acute_golden_fixture_pack(monkeypatch):
    pack, case = _fixture_case()
    monkeypatch.setattr(acute, "_load_price_weights", _load_weights)

    input_df = fixtures.read_payload_frame(pack, "input")
    expected_df = fixtures.read_payload_frame(pack, "expected_output")

    python_result = acute.calculate_acute(
        input_df,
        acute.AcuteParams(),
        year=pack.manifest.pricing_year,
        ref_dir=REF_DIR,
    )
    rust_result = acute.calculate_acute_rust_2025(
        input_df,
        acute.AcuteParams(),
        year=pack.manifest.pricing_year,
        ref_dir=REF_DIR,
    )

    fixtures.assert_fixture_case_output(case, rust_result, expected_df)
    assert rust_result["NWAU25"].to_numpy() == pytest.approx(
        expected_df["NWAU25"].to_numpy(), rel=1e-4, abs=1e-4
    )
    assert rust_result["NWAU25"].to_numpy() == pytest.approx(
        python_result["NWAU25"].to_numpy(), rel=1e-4, abs=1e-4
    )


def test_missing_rust_extension_reports_a_clear_import_error(monkeypatch):
    monkeypatch.setattr(rust_bridge, "_candidate_extension_paths", lambda: [])

    original_import = builtins.__import__

    def _blocked_import(
        name: str,
        globals: Mapping[str, object] | None = None,
        locals: Mapping[str, object] | None = None,
        fromlist: tuple[str, ...] | list[str] = (),
        level: int = 0,
    ) -> object:
        if name == "nwau_py._rust" or (level == 1 and "_rust" in fromlist):
            raise ImportError("simulated missing compiled extension")
        return original_import(name, globals, locals, fromlist, level)

    def _raise_missing_extension() -> None:
        exc = ModuleNotFoundError("No module named 'nwau_py._rust'")
        exc.name = "nwau_py._rust"
        raise exc

    monkeypatch.setattr(
        rust_bridge,
        "_load_installed_extension",
        _raise_missing_extension,
    )
    monkeypatch.setattr(rust_bridge, "_candidate_extension_paths", lambda: [])
    monkeypatch.setattr(builtins, "__import__", _blocked_import)

    with pytest.raises(
        ImportError, match=r"Rust extension nwau_py\._rust is not available"
    ):
        rust_bridge.load_rust_extension()
