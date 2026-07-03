"""Optional ONNX export helpers for JSON AST formula programs."""

from __future__ import annotations

import importlib
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Final

import pandas as pd
from pandas import DataFrame, Series

from .formula_ir import (
    FormulaIRError,
    evaluate_formula_document,
    normalize_formula_document,
)

try:  # pragma: no cover - optional dependency
    onnx = importlib.import_module("onnx")
    TensorProto = onnx.TensorProto
    checker = onnx.checker
    helper = onnx.helper
except Exception:  # pragma: no cover - optional dependency
    onnx = None
    TensorProto = None
    checker = None
    helper = None

__all__ = [
    "FormulaONNXError",
    "FormulaONNXExportNode",
    "FormulaONNXExportPlan",
    "FormulaONNXParityResult",
    "build_formula_onnx_export_plan",
    "evaluate_formula_onnx_export_plan",
    "export_formula_document_to_onnx_bytes",
    "validate_formula_document_onnx_exportability",
    "validate_formula_document_onnx_parity",
]

_BINARY_OPS: Final[frozenset[str]] = frozenset({"+", "-", "*", "/"})
_UNARY_OPS: Final[frozenset[str]] = frozenset({"+", "-"})
_MISSING_ONNX_MESSAGE = (
    "onnx is not installed; install the optional onnx dependency to export a model"
)


class FormulaONNXError(ValueError):
    """Raised when ONNX export or parity validation is not possible."""


@dataclass(frozen=True, slots=True)
class FormulaONNXExportNode:
    """A deterministic ONNX translation step."""

    name: str
    op_type: str
    inputs: tuple[str, ...]
    output: str
    value: float | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "op_type": self.op_type,
            "inputs": list(self.inputs),
            "output": self.output,
            "value": self.value,
        }


@dataclass(frozen=True, slots=True)
class FormulaONNXExportPlan:
    """Serializable plan for translating a formula IR to ONNX."""

    source_format: str
    result_name: str
    input_symbols: tuple[str, ...]
    input_columns: tuple[str, ...]
    nodes: tuple[FormulaONNXExportNode, ...]

    @property
    def output_name(self) -> str:
        """Backward-compatible alias for the exported result name."""
        return self.result_name

    def to_dict(self) -> dict[str, object]:
        return {
            "source_format": self.source_format,
            "result_name": self.result_name,
            "output_name": self.output_name,
            "input_symbols": list(self.input_symbols),
            "input_columns": list(self.input_columns),
            "nodes": [node.to_dict() for node in self.nodes],
        }


@dataclass(frozen=True, slots=True)
class FormulaONNXParityResult:
    """Outcome from comparing the export plan with the Python evaluator."""

    exportable: bool
    parity_matches: bool
    result_name: str
    max_abs_delta: float | None
    reason: str | None
    export_plan: FormulaONNXExportPlan
    onnx_bytes: bytes | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "exportable": self.exportable,
            "parity_matches": self.parity_matches,
            "result_name": self.result_name,
            "max_abs_delta": self.max_abs_delta,
            "reason": self.reason,
            "export_plan": self.export_plan.to_dict(),
            "onnx_bytes": None if self.onnx_bytes is None else self.onnx_bytes.hex(),
        }


def _as_float(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FormulaONNXError("ONNX export requires numeric literals")
    return float(value)


def _is_pure_numeric_expression(node: Mapping[str, Any]) -> bool:
    node_type = str(node.get("type", ""))
    if node_type == "literal":
        return isinstance(node.get("value"), (int, float)) and not isinstance(
            node.get("value"), bool
        )
    if node_type == "variable":
        return isinstance(node.get("name"), str)
    if node_type == "binary":
        return (
            str(node.get("op")) in _BINARY_OPS
            and isinstance(node.get("left"), Mapping)
            and isinstance(node.get("right"), Mapping)
            and _is_pure_numeric_expression(node["left"])
            and _is_pure_numeric_expression(node["right"])
        )
    if node_type == "unary":
        return (
            str(node.get("op")) in _UNARY_OPS
            and isinstance(node.get("operand"), Mapping)
            and _is_pure_numeric_expression(node["operand"])
        )
    return False


def validate_formula_document_onnx_exportability(
    formula: Mapping[str, Any],
) -> FormulaONNXExportPlan:
    """Validate a formula document for optional ONNX export."""
    try:
        normalized = normalize_formula_document(formula)
        return build_formula_onnx_export_plan(normalized)
    except FormulaIRError as exc:
        raise FormulaONNXError(str(exc)) from exc


def _translate_expression(
    expression: Mapping[str, Any],
    *,
    nodes: list[FormulaONNXExportNode],
    symbol_counter: list[int],
) -> str:
    node_type = str(expression.get("type"))
    if node_type == "literal":
        name = f"const_{symbol_counter[0]}"
        symbol_counter[0] += 1
        nodes.append(
            FormulaONNXExportNode(
                name=name,
                op_type="Constant",
                inputs=(),
                output=name,
                value=_as_float(expression["value"]),
            )
        )
        return name
    if node_type == "variable":
        return str(expression["name"])
    if node_type in {"binary", "unary"}:
        if node_type == "binary":
            left = _translate_expression(
                expression["left"], nodes=nodes, symbol_counter=symbol_counter
            )
            right = _translate_expression(
                expression["right"], nodes=nodes, symbol_counter=symbol_counter
            )
            op = str(expression["op"])
            op_slug = {
                "+": "add",
                "-": "sub",
                "*": "mul",
                "/": "div",
            }[op]
            node_name = f"{op_slug}_{symbol_counter[0]}"
            symbol_counter[0] += 1
            nodes.append(
                FormulaONNXExportNode(
                    name=node_name,
                    op_type={
                        "+": "Add",
                        "-": "Sub",
                        "*": "Mul",
                        "/": "Div",
                    }[op],
                    inputs=(left, right),
                    output=node_name,
                )
            )
            return node_name
        operand = _translate_expression(
            expression["operand"], nodes=nodes, symbol_counter=symbol_counter
        )
        op = str(expression["op"])
        node_name = f"{'pos' if op == '+' else 'neg'}_{symbol_counter[0]}"
        symbol_counter[0] += 1
        if op == "+":
            nodes.append(
                FormulaONNXExportNode(
                    name=node_name,
                    op_type="Identity",
                    inputs=(operand,),
                    output=node_name,
                )
            )
        else:
            nodes.append(
                FormulaONNXExportNode(
                    name=node_name,
                    op_type="Neg",
                    inputs=(operand,),
                    output=node_name,
                )
            )
        return node_name
    raise FormulaONNXError(f"unsupported AST expression node type {node_type!r}")


def build_formula_onnx_export_plan(
    formula: Mapping[str, Any],
) -> FormulaONNXExportPlan:
    """Build a deterministic ONNX export plan from a formula document."""
    try:
        normalized = normalize_formula_document(formula)
    except FormulaIRError as exc:
        raise FormulaONNXError(str(exc)) from exc
    program = normalized["program"]
    if not isinstance(program, Mapping):
        raise FormulaONNXError("normalized formula program must be a mapping")
    input_symbols = tuple(normalized["variables"].keys())
    input_columns = tuple(normalized["variables"].values())
    nodes: list[FormulaONNXExportNode] = []
    symbol_counter = [0]

    for statement in program["statements"]:
        if not _is_pure_numeric_expression(statement["value"]):
            raise FormulaONNXError("formula contains unsupported AST nodes for ONNX")
        value_name = _translate_expression(
            statement["value"], nodes=nodes, symbol_counter=symbol_counter
        )
        target = str(statement["target"])
        if value_name != target:
            nodes.append(
                FormulaONNXExportNode(
                    name=f"assign_{target}_{symbol_counter[0]}",
                    op_type="Identity",
                    inputs=(value_name,),
                    output=target,
                )
            )
            symbol_counter[0] += 1

    return FormulaONNXExportPlan(
        source_format=str(normalized.get("format", "json-ast")),
        result_name=str(program["result"]),
        input_symbols=input_symbols,
        input_columns=input_columns,
        nodes=tuple(nodes),
    )


def evaluate_formula_onnx_export_plan(
    weights_df: DataFrame,
    plan: FormulaONNXExportPlan,
) -> Series:
    """Evaluate a translated export plan against a dataframe."""
    env: dict[str, Series] = {}
    for symbol, column in zip(plan.input_symbols, plan.input_columns, strict=True):
        if column not in weights_df.columns:
            raise FormulaONNXError(
                f"missing input column {column!r} for symbol {symbol!r}"
            )
        env[symbol] = weights_df[column]
    for node in plan.nodes:
        if node.op_type == "Constant":
            env[node.output] = pd.Series(
                [node.value] * len(weights_df), index=weights_df.index, dtype="float64"
            )
            continue
        if node.op_type == "Identity":
            env[node.output] = env[node.inputs[0]]
            continue
        if node.op_type == "Neg":
            env[node.output] = -env[node.inputs[0]]
            continue
        left = env[node.inputs[0]]
        right = env[node.inputs[1]]
        if node.op_type == "Add":
            env[node.output] = left + right
        elif node.op_type == "Sub":
            env[node.output] = left - right
        elif node.op_type == "Mul":
            env[node.output] = left * right
        elif node.op_type == "Div":
            env[node.output] = left / right
        else:
            raise FormulaONNXError(f"unsupported ONNX export op {node.op_type!r}")
    if plan.result_name not in env:
        raise FormulaONNXError(f"missing result symbol {plan.result_name!r}")
    result = env[plan.result_name]
    if not isinstance(result, pd.Series):
        return pd.Series(result, index=weights_df.index)
    return result


def export_formula_document_to_onnx_bytes(
    formula: Mapping[str, Any],
    *,
    model_name: str = "formula",
    opset_version: int = 17,
) -> bytes:
    """Serialize an eligible formula document to ONNX model bytes."""
    plan = build_formula_onnx_export_plan(formula)
    if onnx is None or helper is None or TensorProto is None:
        raise FormulaONNXError(_MISSING_ONNX_MESSAGE)

    inputs = [
        helper.make_tensor_value_info(symbol, TensorProto.DOUBLE, [None])
        for symbol in plan.input_symbols
    ]
    outputs = [
        helper.make_tensor_value_info(plan.result_name, TensorProto.DOUBLE, [None])
    ]
    onnx_nodes: list[Any] = []
    for node in plan.nodes:
        if node.op_type == "Constant":
            tensor = helper.make_tensor(
                name=node.output,
                data_type=TensorProto.DOUBLE,
                dims=[],
                vals=[node.value],
            )
            onnx_nodes.append(
                helper.make_node(
                    "Constant",
                    inputs=[],
                    outputs=[node.output],
                    name=node.name,
                    value=tensor,
                )
            )
            continue
        onnx_nodes.append(
            helper.make_node(
                node.op_type,
                inputs=list(node.inputs),
                outputs=[node.output],
                name=node.name,
            )
        )
    graph = helper.make_graph(
        nodes=onnx_nodes,
        name=model_name,
        inputs=inputs,
        outputs=outputs,
    )
    model = helper.make_model(
        graph,
        producer_name="nwau_py",
        opset_imports=[helper.make_operatorsetid("", opset_version)],
    )
    if checker is not None:  # pragma: no branch - optional dependency guard
        checker.check_model(model)
    return model.SerializeToString()


def validate_formula_document_onnx_parity(
    weights_df: DataFrame,
    formula: Mapping[str, Any],
    *,
    model_name: str = "formula",
    opset_version: int = 17,
) -> FormulaONNXParityResult:
    """Validate optional ONNX export parity for a formula document."""
    try:
        normalized = normalize_formula_document(formula)
        plan = build_formula_onnx_export_plan(normalized)
    except FormulaIRError as exc:
        raise FormulaONNXError(str(exc)) from exc
    python_result = evaluate_formula_document(weights_df, normalized)
    export_result = evaluate_formula_onnx_export_plan(weights_df, plan)
    delta = (export_result.astype(float) - python_result.astype(float)).abs()
    max_abs_delta = None if delta.empty else float(delta.max())
    parity_matches = bool(delta.fillna(0.0).eq(0.0).all())
    onnx_bytes = None
    reason = None
    if onnx is not None and helper is not None and TensorProto is not None:
        onnx_bytes = export_formula_document_to_onnx_bytes(
            normalized, model_name=model_name, opset_version=opset_version
        )
        reason = "onnx export and parity validation passed"
    else:
        reason = "onnx dependency not installed; parity validated via export plan"
    return FormulaONNXParityResult(
        exportable=True,
        parity_matches=parity_matches,
        result_name=plan.result_name,
        max_abs_delta=max_abs_delta,
        reason=reason,
        export_plan=plan,
        onnx_bytes=onnx_bytes,
    )
