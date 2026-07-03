from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from nwau_py.calculators.formula_ir import normalize_formula_document
from nwau_py.calculators.formula_onnx import (
    FormulaONNXError,
    build_formula_onnx_export_plan,
    evaluate_formula_onnx_export_plan,
    export_formula_document_to_onnx_bytes,
    validate_formula_document_onnx_parity,
)
from nwau_py.calculators.funding_formula import calculate_funding, load_formula

ROOT = Path(__file__).resolve().parents[1]
LEGACY_FORMULA = ROOT / "excel_calculator" / "data" / "formula.json"
DOCS = ROOT / "nwau_py" / "docs" / "calculators.md"


def test_formula_onnx_export_plan_matches_python_parity() -> None:
    formula = normalize_formula_document(load_formula(LEGACY_FORMULA))
    frame = pd.DataFrame(
        [
            {
                column: idx + 1
                for idx, column in enumerate(formula["variables"].values())
            }
        ]
    )

    plan = build_formula_onnx_export_plan(formula)
    parity = validate_formula_document_onnx_parity(frame, formula)
    plan_output = evaluate_formula_onnx_export_plan(frame, plan)
    python_output = calculate_funding(frame, formula)

    assert plan.output_name == "NWAU25"
    assert parity.exportable is True
    assert parity.parity_matches is True
    pd.testing.assert_series_equal(plan_output, python_output, check_dtype=False)


def test_formula_onnx_export_bytes_requires_optional_dependency(monkeypatch) -> None:
    formula = normalize_formula_document(load_formula(LEGACY_FORMULA))
    monkeypatch.setattr("nwau_py.calculators.formula_onnx.onnx", None)

    with pytest.raises(FormulaONNXError, match="onnx"):
        export_formula_document_to_onnx_bytes(formula)


def test_formula_onnx_docs_state_optional_boundary() -> None:
    docs = DOCS.read_text(encoding="utf-8")

    assert "optional ONNX export" in docs
    assert "ONNX is not canonical" in docs


def test_unsupported_formula_nodes_fail_onnx_export_validation() -> None:
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

    with pytest.raises(FormulaONNXError, match="unsupported"):
        build_formula_onnx_export_plan(formula)
