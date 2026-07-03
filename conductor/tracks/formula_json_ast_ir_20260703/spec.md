# Specification: Formula JSON AST IR

## Overview
Add JSON AST as the canonical structured representation for calculator formulas, while preserving compatibility with the current legacy step-based `formula.json` shape. The new IR must support evaluator parity for the current funding formula, reject unsupported operations clearly, and keep formula logic out of ad hoc string evaluation paths.

## Contract
- Formula documents must be loadable as JSON AST programs with explicit nodes for literals, variables, assignments, unary operators, and binary operators.
- Legacy `variables` plus `steps` formula files may continue to load, but the AST representation is the canonical structured form.
- Evaluators must operate on deterministic data structures and return the same outputs as the current funding formula for supported arithmetic programs.
- Unsupported or malformed AST nodes must fail closed with explicit validation errors.
- The AST track must not introduce Mojo runtime dependencies; ONNX export remains the responsibility of the dependent ONNX track.

## Functional Requirements
- Define a JSON AST formula program model for calculator expressions.
- Add validation for AST structure, node types, and required fields.
- Add an evaluator that can execute supported AST programs against tabular inputs.
- Keep the existing formula loader usable with legacy formula files while allowing AST-native fixtures.
- Provide parity tests showing the AST evaluator matches the current formula output.

## Non-Functional Requirements
- The IR must be deterministic, machine-readable, and easy to diff in review.
- Unsupported node types must not be silently ignored or coerced.
- The IR should remain small enough to reuse across Python loaders, future bindings, and schema exports.
- Formula logic must remain single-sourced rather than duplicated across loaders or adapters.

## Acceptance Criteria
- Canary formula bundles can be expressed as JSON AST fixtures.
- AST evaluator results match the existing funding formula outputs for supported arithmetic programs.
- Invalid AST nodes or unsupported operators fail validation with clear errors.
- Docs explain the JSON AST IR boundary and state that Mojo is not adopted for this track.

## Out of Scope
- ONNX export or runtime execution.
- Mojo adoption or benchmark-driven runtime switching.
- Rewriting calculator math into a second independent implementation.
- Redistributing proprietary formula sources or restricted tables.

## Source Evidence
- GitHub issue: https://github.com/edithatogo/mchs/issues/207
- Current formula contract: `excel_calculator/data/formula.json`
- Roadmap notes: `ROADMAP.md`
