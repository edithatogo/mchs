# Plan: Repository Topology CI Gate

## Phase 1: Validator Core

- [x] Task: Implement topology checks.
    - [x] Detect nested `.git` directories below the canonical root.
    - [x] Detect gitlinks without matching `.gitmodules` sections.
    - [x] Detect package manifests missing from the ownership registry.
    - [x] Detect tracked generated artifacts.
- [x] Task: Add diagnostics.
    - [x] Print concise failures by default.
    - [x] Support `--json` output for automation.
    - [x] Support `--outer-root` for explicit wrapper validation.
- [x] Task: Conductor - User Manual Verification 'Validator Core' (Protocol in workflow.md)

## Phase 2: CI Wiring

- [x] Task: Wire PR CI.
    - [x] Run the validator after environment sync in the quality job.
    - [x] Keep it independent from package registry credentials.
    - [x] Ensure it runs before broader test jobs.
- [x] Task: Conductor - User Manual Verification 'CI Wiring' (Protocol in workflow.md)

## Phase 3: Tests and Evidence

- [x] Task: Add focused tests.
    - [x] Test valid repository registry state.
    - [x] Test broken outer gitlink detection with a synthetic fixture.
    - [x] Test generated artifact policy references.
- [x] Task: Run validation commands.
    - [x] Run `uv run pytest tests/test_repository_topology_governance.py`.
    - [x] Run `uv run python scripts/validate_repository_topology.py --json`.
- [x] Task: Conductor - User Manual Verification 'Tests and Evidence' (Protocol in workflow.md)
