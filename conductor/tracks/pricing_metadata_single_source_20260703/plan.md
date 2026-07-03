# Implementation Plan

## Phase 1: Contract and Tests

- [~] Task: Identify all pricing metadata sources and duplicate NEP/NEC constants.
- [ ] Task: Add failing tests for NEP25, NEP26, missing metadata, and support-state generation.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Contract and Tests' (Protocol in workflow.md)

## Phase 2: Manifest-Backed Runtime

- [ ] Task: Implement manifest-backed pricing metadata loading behind the existing public APIs.
- [ ] Task: Remove or generate duplicate hardcoded constants and update callers.
- [ ] Task: Update validation and diff tooling to use canonical metadata.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Manifest-Backed Runtime' (Protocol in workflow.md)

## Phase 3: Documentation and Release Evidence

- [ ] Task: Regenerate or update support documentation from canonical metadata.
- [ ] Task: Run focused tests, stub detector, typing, linting, and affected docs checks.
- [ ] Task: Record residual source-only gaps without claiming validation.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation and Release Evidence' (Protocol in workflow.md)
