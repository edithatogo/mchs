# Formula JSON AST IR

## Overview

Formula strings are not enough for cross-runtime validation, generation, or audit. The project needs a canonical JSON AST formula IR that can be evaluated, diffed, validated, and optionally lowered to other runtimes.

## Requirements

- Define a JSON AST schema for arithmetic, comparisons, conditionals, rounding, coalescing, constants, variables, and declared table lookups.
- Preserve formula provenance, units, rounding/null policy, stream/year applicability, and source references.
- Implement a Python evaluator and validation fixtures for existing formula bundles.
- Reject unsupported operations explicitly instead of interpreting arbitrary strings.
- Keep the IR language-neutral and compatible with future Rust and binding consumers.

## Acceptance Criteria

- Existing canary formula bundles can be represented as JSON AST fixtures.
- Evaluator parity tests match existing formula outputs for supported operations.
- Invalid or unsupported AST nodes fail with schema-level errors.
- Documentation explains the IR contract and why Mojo is out of scope.

## Out of Scope

- ONNX export, except as a dependent track.
- Replacing all formulas before parity evidence exists.
- Mojo implementation.
