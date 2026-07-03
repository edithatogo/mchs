# Implementation Plan

## Phase 1: Optional Export Contract Tests

- [ ] Task: Add failing tests for numeric AST export, evaluator parity, and unsupported-operation rejection.
- [ ] Task: Define optional dependency and CI behavior for ONNX validation.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Optional Export Contract Tests' (Protocol in workflow.md)

## Phase 2: Exporter and Validator

- [ ] Task: Implement ONNX exporter for supported numeric AST nodes.
- [ ] Task: Implement optional ONNX runtime parity validation.
- [ ] Task: Ensure default runtime paths do not import optional ONNX dependencies.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Exporter and Validator' (Protocol in workflow.md)

## Phase 3: Documentation and Validation

- [ ] Task: Document ONNX scope, unsupported operations, and non-canonical status.
- [ ] Task: Run focused ONNX-optional, formula, lint, typing, and stub-detector checks.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation and Validation' (Protocol in workflow.md)
