# Plan: Release Boundary Control Plane

## Phase 1: Release Boundary Model

- [x] Task: Define release fields.
    - [x] Add version source, release target, workflow, registry state, evidence boundary, and external gate class.
    - [x] Require immutable evidence for published claims.
    - [x] Require explicit blockers for submitted or blocked states.
- [x] Task: Conductor - User Manual Verification 'Release Boundary Model' (Protocol in workflow.md)

## Phase 2: Claim Reconciliation

- [x] Task: Reconcile public claims.
    - [x] Compare README package status with package surface registry state.
    - [x] Compare support matrix and docs with registry evidence.
    - [x] Record external gates separately from local implementation readiness.
- [x] Task: Conductor - User Manual Verification 'Claim Reconciliation' (Protocol in workflow.md)

## Phase 3: Validation

- [x] Task: Add release-boundary tests.
    - [x] Assert every surface has a release boundary.
    - [x] Assert blocked or submitted surfaces name an external gate.
    - [x] Assert publication claims use evidence links.
- [x] Task: Run focused validation.
    - [x] Run `uv run pytest tests/test_repository_topology_governance.py`.
    - [x] Run `uv run python scripts/validate_repository_topology.py`.
- [x] Task: Conductor - User Manual Verification 'Validation' (Protocol in workflow.md)
