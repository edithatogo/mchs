from __future__ import annotations

import importlib.util
import json
import shutil
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
SPEC = importlib.util.spec_from_file_location("fixture_runner_acute", ACUTE_PATH)
assert SPEC is not None and SPEC.loader is not None
acute = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(acute)

FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "golden"
MANIFEST = FIXTURE_ROOT / "acute_2025" / "manifest.json"


def _load_weights(ref_dir: Path, year: str = "2025") -> pd.DataFrame:
    weights = pd.read_csv(Path("tests/data") / "nep25_aa_price_weights.csv")
    weights["DRG"] = weights["DRG"].str.strip("b'")
    return weights


def _calculator_map():
    return {
        "acute": (
            acute.calculate_acute,
            acute.AcuteParams(),
            "NWAU25",
        )
    }


def _copy_fixture_pack(src: Path, dest: Path, fixture_id: str) -> Path:
    shutil.copytree(src, dest)
    manifest_path = dest / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["fixture_id"] = fixture_id
    provenance = manifest["provenance"]
    provenance["notes"] = [*provenance["notes"], "cloned for runner coverage"]
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def test_discover_fixture_packs_finds_the_acute_pack():
    packs = fixtures.discover_fixture_packs(FIXTURE_ROOT)
    assert [pack.manifest.fixture_id for pack in packs] == ["acute_2025"]


def test_iter_fixture_cases_generates_runner_neutral_case():
    pack = fixtures.load_fixture_pack(MANIFEST)
    cases = fixtures.iter_fixture_cases([pack], calculator_map=_calculator_map())
    assert len(cases) == 1
    case = cases[0]
    assert case.fixture_id == "acute_2025"
    assert case.provenance_label.startswith("fixture=acute_2025")
    assert case.result_column == "NWAU25"
    assert case.parity_type == "output parity"


def test_fixture_case_params_generate_stable_pytest_ids():
    pack = fixtures.load_fixture_pack(MANIFEST)
    case = fixtures.iter_fixture_cases([pack], calculator_map=_calculator_map())[0]

    params = fixtures.fixture_case_params([case])

    assert len(params) == 1
    assert params[0].id == "acute_2025[acute]/NWAU25/output_parity"


def test_iter_fixture_pytest_params_generate_case_ids():
    pack = fixtures.load_fixture_pack(MANIFEST)
    case = fixtures.iter_fixture_cases([pack], calculator_map=_calculator_map())[0]

    params = fixtures.iter_fixture_pytest_params([case])

    assert len(params) == 1
    assert params[0].id == "acute_2025"
    assert params[0].values[0] is case


def test_iter_fixture_pytest_params_from_root_uses_manifest_metadata(tmp_path):
    root = tmp_path / "golden"
    _copy_fixture_pack(FIXTURE_ROOT / "acute_2025", root / "acute_2025", "acute_2025")

    params = fixtures.iter_fixture_pytest_params_from_root(
        root,
        calculator_map=_calculator_map(),
    )

    assert len(params) == 1
    assert params[0].id == "acute_2025"
    case = params[0].values[0]
    assert isinstance(case, fixtures.FixtureCase)
    assert case.fixture_id == "acute_2025"
    assert case.pack.manifest.cross_language_ready is True
    assert case.pack.manifest.privacy_classification == "synthetic"
    assert case.pack.manifest.source_basis.kind == "synthetic_sample"


def test_iter_fixture_pytest_params_from_root_skips_unready_packs(tmp_path):
    root = tmp_path / "golden"
    valid_pack = root / "acute_2025"
    invalid_pack = root / "acute_2025_unready"
    _copy_fixture_pack(FIXTURE_ROOT / "acute_2025", valid_pack, "acute_2025")
    _copy_fixture_pack(FIXTURE_ROOT / "acute_2025", invalid_pack, "acute_2025_unready")

    manifest_path = invalid_pack / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["cross_language_ready"] = False
    manifest["privacy_classification"] = "restricted"
    manifest["source_basis"]["kind"] = "manual_spreadsheet"
    manifest["precision"]["tolerance"]["absolute"] = -0.1
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    params = fixtures.iter_fixture_pytest_params_from_root(
        root,
        calculator_map=_calculator_map(),
    )

    assert [param.id for param in params] == ["acute_2025"]
    assert [param.values[0].fixture_id for param in params] == ["acute_2025"]


def test_run_fixture_case_and_assert_output_parity(monkeypatch):
    pack = fixtures.load_fixture_pack(MANIFEST)
    case = fixtures.iter_fixture_cases([pack], calculator_map=_calculator_map())[0]
    monkeypatch.setattr(acute, "_load_price_weights", _load_weights)

    result = fixtures.run_fixture_case(case)
    expected = fixtures.read_payload_frame(pack, "expected_output")
    fixtures.assert_fixture_case_output(case, result, expected)


def test_run_fixture_case_uses_manifest_year_and_payload_shape():
    pack = fixtures.load_fixture_pack(MANIFEST)
    input_df = fixtures.read_payload_frame(pack, "input")
    seen: dict[str, object] = {}

    def calculator_spy(
        calculator_input: pd.DataFrame,
        params,
        year: str,
    ) -> pd.DataFrame:
        seen["year"] = year
        seen["columns"] = tuple(calculator_input.columns)
        seen["rows"] = len(calculator_input)
        seen["params"] = params
        return pd.DataFrame({"NWAU25": np.zeros(len(calculator_input), dtype=float)})

    case = fixtures.FixtureCase(
        pack=pack,
        calculator=calculator_spy,
        calculator_params=object(),
        result_column="NWAU25",
    )

    result = fixtures.run_fixture_case(case)

    assert seen["year"] == pack.manifest.pricing_year
    assert seen["columns"] == tuple(input_df.columns)
    assert seen["rows"] == pack.manifest.payloads["input"].row_count
    assert seen["params"] is case.calculator_params
    assert list(result.columns) == ["NWAU25"]
    assert len(result) == pack.manifest.payloads["input"].row_count


def test_fixture_runner_executes_a_suite_of_cases(tmp_path):
    suite_root = tmp_path / "golden"
    _copy_fixture_pack(
        FIXTURE_ROOT / "acute_2025", suite_root / "acute_2025_a", "acute_2025_a"
    )
    _copy_fixture_pack(
        FIXTURE_ROOT / "acute_2025", suite_root / "acute_2025_b", "acute_2025_b"
    )
    packs = fixtures.discover_fixture_packs(suite_root)

    cases = fixtures.iter_fixture_cases(
        packs,
        calculator_map={
            "acute": (
                lambda calculator_input, params, year: pd.DataFrame(
                    {"NWAU25": np.zeros(len(calculator_input), dtype=float)}
                ),
                object(),
                "NWAU25",
            )
        },
    )

    runner = fixtures.FixtureRunner(
        execute_case=lambda case: pd.DataFrame(
            {"NWAU25": np.zeros(len(fixtures.read_payload_frame(case.pack, "input")))}
        )
    )
    results = runner.run_cases(cases)

    assert [case.fixture_id for case in cases] == ["acute_2025_a", "acute_2025_b"]
    assert [result.case.fixture_id for result in results] == [
        "acute_2025_a",
        "acute_2025_b",
    ]
    assert [list(result.result.columns) for result in results] == [
        ["NWAU25"],
        ["NWAU25"],
    ]
    assert [len(result.result) for result in results] == [
        fixtures.load_fixture_pack(suite_root / "acute_2025_a" / "manifest.json")
        .manifest.payloads["input"]
        .row_count,
        fixtures.load_fixture_pack(suite_root / "acute_2025_b" / "manifest.json")
        .manifest.payloads["input"]
        .row_count,
    ]


def test_assert_fixture_case_output_reports_tolerance_failures(monkeypatch):
    pack = fixtures.load_fixture_pack(MANIFEST)
    case = fixtures.iter_fixture_cases([pack], calculator_map=_calculator_map())[0]
    monkeypatch.setattr(acute, "_load_price_weights", _load_weights)

    result = fixtures.run_fixture_case(case)
    expected = fixtures.read_payload_frame(pack, "expected_output")
    if hasattr(expected, "with_columns"):
        import polars as pl

        expected = expected.with_columns((pl.col("NWAU25") + 1.0).alias("NWAU25"))
    else:
        expected = expected.copy()
        expected["NWAU25"] = expected["NWAU25"] + np.array([1.0, 1.0, 1.0])

    with pytest.raises(fixtures.FixtureManifestError):
        fixtures.assert_fixture_case_output(case, result, expected)
