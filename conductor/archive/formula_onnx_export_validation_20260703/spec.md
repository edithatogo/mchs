# Specification: Formula ONNX Export Validation

## Overview
Add an optional ONNX export and validation path for pure numeric JSON AST formula programs. ONNX must remain a derived artifact, not the canonical formula source. The Python JSON AST evaluator stays the source of truth, and the ONNX path must fail closed on unsupported nodes.

## Contract
- Formula documents remain canonical as JSON AST programs in `nwau_py.calculators.formula_ir`.
- ONNX export is optional and must not be required at install time.
- Only pure numeric arithmetic subgraphs may be exported.
- Unsupported AST nodes, table lookups, or provenance-bearing operations must be rejected.
- Exported models must be validated for parity against the Python evaluator when the optional dependency is available.

## Functional Requirements
- Build a deterministic export plan from normalized formula documents.
- Translate supported arithmetic nodes into ONNX-compatible operations.
- Provide optional model serialization helpers for local workflows.
- Expose parity validation that compares exported execution against Python evaluation.
- Document the boundary between canonical JSON AST formulas and derived ONNX artifacts.

## Non-Functional Requirements
- The export path must be deterministic and easy to review.
- The code must avoid hard dependencies on ONNX for normal installs and tests.
- Unsupported nodes must raise explicit errors rather than falling back silently.
- The design must keep future extension points open for alternative numeric exporters.

## Acceptance Criteria
- Supported formula fixtures can be translated into an ONNX export plan.
- Parity validation succeeds for pure numeric programs.
- Unsupported formula nodes fail closed with clear error messages.
- Docs state that ONNX is optional and non-canonical.

## Out of Scope
- Replacing the JSON AST formula IR.
- Treating ONNX as a canonical runtime format.
- Proving parity for non-numeric or provenance-bearing operations.
- Introducing Mojo dependencies.

## Source Evidence
- GitHub issue: https://github.com/edithatogo/mchs/issues/208
- Formula IR track: `conductor/archive/formula_json_ast_ir_20260703`
- Calculator docs: `nwau_py/docs/calculators.md`
