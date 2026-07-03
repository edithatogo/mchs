# Formula ONNX Export Validation

## Overview

ONNX can be useful as an optional generated artifact for pure numeric formula subgraphs, but it should not replace JSON AST as the canonical source.

## Requirements

- Add optional ONNX export for supported numeric AST nodes only.
- Keep ONNX dependencies optional and outside the default runtime path.
- Validate exported models against the JSON AST evaluator on deterministic fixtures.
- Reject table lookups, provenance-only nodes, unsupported branching, or licensed-data-dependent operations.
- Document ONNX as an interoperability/performance artifact, not a source of truth.

## Acceptance Criteria

- Pure numeric AST fixtures export to ONNX and pass parity checks.
- Unsupported formula nodes fail with explicit diagnostics.
- Default installation and non-ONNX tests do not require ONNX dependencies.
- CI can run optional ONNX validation when the dependency group is installed.

## Out of Scope

- Making ONNX mandatory.
- Replacing Rust or Polars calculator paths.
- Exporting formulas that depend on proprietary assets.
