"""JSON AST helpers for calculator formula programs."""

from __future__ import annotations

import ast as py_ast
import re
from collections.abc import Mapping, Sequence
from typing import Any, cast

import pandas as pd
from pandas import DataFrame, Series

__all__ = [
    "FormulaIRError",
    "build_formula_program_from_steps",
    "evaluate_formula_document",
    "normalize_formula_document",
    "render_formula_program_steps",
    "validate_formula_program",
]

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_BINARY_OPS = {
    py_ast.Add: "+",
    py_ast.Sub: "-",
    py_ast.Mult: "*",
    py_ast.Div: "/",
}
_UNARY_OPS = {
    py_ast.UAdd: "+",
    py_ast.USub: "-",
}


class FormulaIRError(ValueError):
    """Raised when a formula JSON AST document is malformed or unsupported."""


def _require_string(value: Any, *, field: str) -> str:
    if not isinstance(value, str):
        raise FormulaIRError(f"{field} must be a string")
    if not value:
        raise FormulaIRError(f"{field} must not be blank")
    if value.strip() != value:
        raise FormulaIRError(f"{field} must not contain leading or trailing whitespace")
    return value


def _require_identifier(value: Any, *, field: str) -> str:
    text = _require_string(value, field=field)
    if not _IDENTIFIER_RE.fullmatch(text):
        raise FormulaIRError(f"{field} must be a valid identifier")
    return text


def _require_numeric(value: Any, *, field: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FormulaIRError(f"{field} must be numeric")
    return value


def _normalize_variables(value: Any) -> dict[str, str]:
    if not isinstance(value, Mapping) or not value:
        raise FormulaIRError("formula variables must be a non-empty mapping")
    return {
        _require_identifier(key, field="variable name"): _require_string(
            column, field=f"variable column for {key!r}"
        )
        for key, column in value.items()
    }


def _validate_expression(node: Any) -> dict[str, Any]:
    if not isinstance(node, Mapping):
        raise FormulaIRError("AST expression nodes must be mappings")
    node_type = _require_string(node.get("type"), field="expression type")
    if node_type == "literal":
        return {
            "type": "literal",
            "value": _require_numeric(node.get("value"), field="literal value"),
        }
    if node_type == "variable":
        return {
            "type": "variable",
            "name": _require_identifier(node.get("name"), field="variable name"),
        }
    if node_type == "binary":
        op = _require_string(node.get("op"), field="binary op")
        if op not in {"+", "-", "*", "/"}:
            raise FormulaIRError(f"unsupported binary operator {op!r}")
        return {
            "type": "binary",
            "op": op,
            "left": _validate_expression(node.get("left")),
            "right": _validate_expression(node.get("right")),
        }
    if node_type == "unary":
        op = _require_string(node.get("op"), field="unary op")
        if op not in {"+", "-"}:
            raise FormulaIRError(f"unsupported unary operator {op!r}")
        return {
            "type": "unary",
            "op": op,
            "operand": _validate_expression(node.get("operand")),
        }
    raise FormulaIRError(f"unsupported AST expression node type {node_type!r}")


def _validate_statement(node: Any) -> dict[str, Any]:
    if not isinstance(node, Mapping):
        raise FormulaIRError("AST statements must be mappings")
    node_type = _require_string(node.get("type"), field="statement type")
    if node_type != "assign":
        raise FormulaIRError(f"unsupported AST statement type {node_type!r}")
    return {
        "type": "assign",
        "target": _require_identifier(node.get("target"), field="assignment target"),
        "value": _validate_expression(node.get("value")),
    }


def validate_formula_program(program: Any) -> dict[str, Any]:
    """Validate a JSON AST formula program and return a normalized copy."""
    if not isinstance(program, Mapping):
        raise FormulaIRError("formula program must be a mapping")
    if _require_string(program.get("type"), field="program type") != "program":
        raise FormulaIRError("formula program type must be 'program'")
    statements = program.get("statements")
    if not isinstance(statements, Sequence) or isinstance(statements, (str, bytes)):
        raise FormulaIRError("formula program statements must be a sequence")
    if not statements:
        raise FormulaIRError("formula program statements must not be empty")
    normalized_statements = [_validate_statement(statement) for statement in statements]
    result = _require_identifier(program.get("result"), field="program result")
    return {
        "type": "program",
        "result": result,
        "statements": normalized_statements,
    }


def build_formula_program_from_steps(steps: Sequence[str]) -> dict[str, Any]:
    """Convert legacy assignment strings into a canonical JSON AST program."""
    if not isinstance(steps, Sequence) or isinstance(steps, (str, bytes)):
        raise FormulaIRError("formula steps must be a sequence")
    statements: list[dict[str, Any]] = []
    for raw_step in steps:
        step = _require_string(raw_step, field="formula step")
        if "=" not in step:
            raise FormulaIRError(f"formula step is missing assignment syntax: {step!r}")
        target_text, expr_text = step.split("=", 1)
        target = _require_identifier(target_text.strip(), field="assignment target")
        expr = _python_expression_to_ast(expr_text.strip())
        statements.append({"type": "assign", "target": target, "value": expr})
    if not statements:
        raise FormulaIRError("formula steps must not be empty")
    return {
        "type": "program",
        "result": statements[-1]["target"],
        "statements": statements,
    }


def _python_expression_to_ast(expr_text: str) -> dict[str, Any]:
    try:
        expr = py_ast.parse(expr_text, mode="eval")
    except SyntaxError as exc:
        raise FormulaIRError(f"invalid formula expression {expr_text!r}") from exc
    return _python_node_to_ast(expr.body)


def _python_node_to_ast(node: py_ast.AST) -> dict[str, Any]:
    if isinstance(node, py_ast.Constant):
        return {
            "type": "literal",
            "value": _require_numeric(node.value, field="literal value"),
        }
    if isinstance(node, py_ast.Name):
        return {
            "type": "variable",
            "name": _require_identifier(node.id, field="variable name"),
        }
    if isinstance(node, py_ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BINARY_OPS:
            raise FormulaIRError(f"unsupported binary operator {op_type.__name__!r}")
        if op_type is py_ast.Add:
            op = "+"
        elif op_type is py_ast.Sub:
            op = "-"
        elif op_type is py_ast.Mult:
            op = "*"
        else:
            op = "/"
        return {
            "type": "binary",
            "op": op,
            "left": _python_node_to_ast(node.left),
            "right": _python_node_to_ast(node.right),
        }
    if isinstance(node, py_ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise FormulaIRError(f"unsupported unary operator {op_type.__name__!r}")
        op = "+" if op_type is py_ast.UAdd else "-"
        return {
            "type": "unary",
            "op": op,
            "operand": _python_node_to_ast(node.operand),
        }
    raise FormulaIRError(f"unsupported formula expression node {type(node).__name__!r}")


def _render_expression(node: Mapping[str, Any]) -> str:
    node_type = _require_string(node.get("type"), field="expression type")
    if node_type == "literal":
        return repr(node["value"])
    if node_type == "variable":
        return str(node["name"])
    if node_type == "binary":
        left = _render_expression(cast(Mapping[str, Any], node["left"]))
        right = _render_expression(cast(Mapping[str, Any], node["right"]))
        return f"({left} {node['op']} {right})"
    if node_type == "unary":
        operand = _render_expression(cast(Mapping[str, Any], node["operand"]))
        return f"({node['op']}{operand})"
    raise FormulaIRError(f"unsupported AST expression node type {node_type!r}")


def render_formula_program_steps(program: Mapping[str, Any]) -> list[str]:
    """Render a formula program back into legacy assignment strings."""
    validated = validate_formula_program(program)
    return [
        f"{statement['target']} = {_render_expression(statement['value'])}"
        for statement in validated["statements"]
    ]


def normalize_formula_document(formula: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize a formula document to the canonical JSON AST representation."""
    if not isinstance(formula, Mapping):
        raise FormulaIRError("formula document must be a mapping")
    normalized = dict(formula)
    normalized["variables"] = _normalize_variables(normalized.get("variables"))

    if "program" in normalized:
        program = validate_formula_program(normalized["program"])
    elif "steps" in normalized:
        program = build_formula_program_from_steps(normalized["steps"])
    else:
        raise FormulaIRError("formula document must include program or steps")
    normalized["program"] = program
    normalized["steps"] = render_formula_program_steps(program)
    normalized.setdefault("format", "json-ast")
    normalized.setdefault("version", 1)
    return normalized


def _evaluate_expression(
    node: Mapping[str, Any],
    env: Mapping[str, Any],
) -> Any:
    node_type = _require_string(node.get("type"), field="expression type")
    if node_type == "literal":
        return node["value"]
    if node_type == "variable":
        name = str(node["name"])
        if name not in env:
            raise FormulaIRError(f"unknown formula variable {name!r}")
        return env[name]
    if node_type == "binary":
        left = _evaluate_expression(cast(Mapping[str, Any], node["left"]), env)
        right = _evaluate_expression(cast(Mapping[str, Any], node["right"]), env)
        op = node["op"]
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            return left / right
        raise FormulaIRError(f"unsupported binary operator {op!r}")
    if node_type == "unary":
        operand = _evaluate_expression(cast(Mapping[str, Any], node["operand"]), env)
        op = node["op"]
        if op == "+":
            return +operand
        if op == "-":
            return -operand
        raise FormulaIRError(f"unsupported unary operator {op!r}")
    raise FormulaIRError(f"unsupported AST expression node type {node_type!r}")


def evaluate_formula_document(
    weights_df: DataFrame,
    formula: Mapping[str, Any],
) -> Series:
    """Evaluate a formula document against a weights dataframe."""
    normalized = normalize_formula_document(formula)
    env: dict[str, Any] = {
        symbol: weights_df[column]
        for symbol, column in normalized["variables"].items()
    }
    for statement in normalized["program"]["statements"]:
        env[statement["target"]] = _evaluate_expression(statement["value"], env)
    result = env[normalized["program"]["result"]]
    if isinstance(result, pd.Series):
        return result
    return pd.Series([result] * len(weights_df), index=weights_df.index)
