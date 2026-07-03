# Plan: Formula ONNX Export Validation

## Phase 1: Export Contract and Validation
- [x] Task: Define the optional ONNX export contract and unsupported-node boundaries.
    - [x] Add failing tests for parity evaluation, unsupported nodes, and docs wording.
    - [x] Add a deterministic export plan representation for formula documents.
    - [x] Keep ONNX optional and fail closed when the dependency is absent.

## Phase 2: Export Implementation and Review
- [x] Task: Implement serialization, parity checking, and package exports.
    - [x] Implement ONNX export helpers for supported numeric formula programs.
    - [x] Expose the export and parity helpers through package exports.
    - [x] Update calculator docs to describe the optional non-canonical ONNX boundary.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Export Implementation and Review' (Protocol in workflow.md)
