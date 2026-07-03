# Implementation Plan

## Phase 1: IR Contract Tests

- [ ] Task: Define AST schema requirements and add failing schema validation tests.
- [ ] Task: Add failing evaluator parity tests for supported arithmetic, conditionals, rounding, nulls, and table lookup declarations.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: IR Contract Tests' (Protocol in workflow.md)

## Phase 2: Evaluator and Bundle Integration

- [ ] Task: Implement AST models, validation, and Python evaluator.
- [ ] Task: Convert existing canary formula records to AST fixtures while preserving provenance.
- [ ] Task: Update formula bundle tooling to prefer AST over raw strings where available.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Evaluator and Bundle Integration' (Protocol in workflow.md)

## Phase 3: Documentation and Validation

- [ ] Task: Document AST operators, provenance, null/rounding policy, and unsupported operations.
- [ ] Task: Run focused formula, bundle, lint, typing, and stub-detector checks.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation and Validation' (Protocol in workflow.md)
