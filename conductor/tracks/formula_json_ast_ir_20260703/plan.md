# Plan: Formula JSON AST IR

## Phase 1: JSON AST Contract and Validation
- [x] Task: Define the JSON AST formula program model and validation helpers.
    - [x] Add failing tests for AST node validation, unsupported operators, and legacy compatibility.
    - [x] Add failing tests for evaluator parity against the current funding formula.
    - [x] Add failing tests for public loader behavior and IR round-tripping.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: JSON AST Contract and Validation' (Protocol in workflow.md)

## Phase 2: Evaluator Integration, Fixtures, and Docs
- [x] Task: Implement AST evaluation, loader integration, and tracked fixtures.
    - [x] Implement the JSON AST evaluator and loader helpers.
    - [x] Add AST-backed formula fixtures and parity coverage.
    - [x] Update docs to explain the canonical AST IR and the Mojo/ONNX boundary.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Evaluator Integration, Fixtures, and Docs' (Protocol in workflow.md)
