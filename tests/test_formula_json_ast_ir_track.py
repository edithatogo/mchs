from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from nwau_py.calculators.formula_ir import (
    FormulaIRError,
    normalize_formula_document,
)
from nwau_py.calculators.funding_formula import calculate_funding, load_formula

ROOT = Path(__file__).resolve().parents[1]
LEGACY_FORMULA = ROOT / "excel_calculator" / "data" / "formula.json"


def test_legacy_formula_normalizes_to_json_ast_program_and_matches_output() -> None:
    formula = load_formula(LEGACY_FORMULA)
    normalized = normalize_formula_document(formula)
    columns = list(formula["variables"].values())
    frame = pd.DataFrame([{column: idx + 1 for idx, column in enumerate(columns)}])

    legacy_output = calculate_funding(frame, formula)
    ast_output = calculate_funding(frame, normalized)

    assert normalized["program"]["type"] == "program"
    assert normalized["program"]["result"] == "NWAU25"
    pd.testing.assert_series_equal(
        legacy_output,
        ast_output,
        check_names=True,
        check_dtype=False,
    )


def test_ast_formula_fixture_round_trips_through_loader_and_evaluator(tmp_path) -> None:
    formula_path = tmp_path / "formula.json"
    payload = {
        "format": "json-ast",
        "version": 1,
        "variables": {"X": "A", "Y": "B"},
        "program": {
            "type": "program",
            "result": "OUT",
            "statements": [
                {
                    "type": "assign",
                    "target": "T1",
                    "value": {
                        "type": "binary",
                        "op": "+",
                        "left": {"type": "variable", "name": "X"},
                        "right": {"type": "literal", "value": 2},
                    },
                },
                {
                    "type": "assign",
                    "target": "OUT",
                    "value": {
                        "type": "binary",
                        "op": "*",
                        "left": {"type": "variable", "name": "T1"},
                        "right": {"type": "variable", "name": "Y"},
                    },
                },
            ],
        },
    }
    formula_path.write_text(json.dumps(payload), encoding="utf-8")

    loaded = load_formula(formula_path)
    result = calculate_funding(pd.DataFrame({"A": [3], "B": [10]}), loaded)

    assert loaded["program"]["result"] == "OUT"
    assert result.iloc[0] == 50


def test_invalid_json_ast_nodes_fail_closed() -> None:
    formula = {
        "variables": {"X": "A"},
        "program": {
            "type": "program",
            "result": "OUT",
            "statements": [
                {
                    "type": "assign",
                    "target": "OUT",
                    "value": {"type": "call", "name": "abs", "args": ["X"]},
                }
            ],
        },
    }

    try:
        normalize_formula_document(formula)
    except FormulaIRError as exc:
        assert "unsupported" in str(exc).lower()
    else:
        raise AssertionError("unsupported AST node should fail validation")


def test_empty_legacy_step_lists_fail_closed() -> None:
    formula = {"variables": {"X": "A"}, "steps": []}

    try:
        normalize_formula_document(formula)
    except FormulaIRError as exc:
        assert "must not be empty" in str(exc).lower()
    else:
        raise AssertionError("empty step lists should fail validation")


def test_docs_state_the_json_ast_boundary_and_mojo_non_adoption() -> None:
    docs = (ROOT / "nwau_py" / "docs" / "calculators.md").read_text(encoding="utf-8")

    assert "JSON AST" in docs
    assert "Mojo is not adopted" in docs
    assert "ONNX export stays with the dependent ONNX track" in docs
