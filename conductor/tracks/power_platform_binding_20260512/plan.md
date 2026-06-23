# Plan: Power Platform Binding

## Phase 1: Integration Contract
- [x] Task: Define custom connector, service API, and managed solution contract.
    - [x] Align request/response schemas with shared calculator contracts.
    - [x] Define environment variables, connection references, and ALM requirements.
    - [x] Document strategy in [`binding_strategy.md`](./binding_strategy.md).
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Integration Contract' (Protocol in workflow.md)
    [checkpoint: design]

## Phase 2: App and Flow Publication Path
- [x] Task: Define publishable Power Platform artifact workflow.
    - [x] Package managed solution artifacts.
    - [x] Validate with solution checker and environment import/publish gates.
- [x] Task: Add local capability-discovery contract gates.
    - [x] Add `contracts/power-platform/power-platform-binding.contract.json`.
    - [x] Add `contracts/power-platform/custom-connector.openapi.yaml`.
    - [x] Add `power-platform/solution/app-surface.json`.
    - [x] Validate with `tests/test_power_platform_binding_track.py`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: App and Flow Publication Path' (Protocol in workflow.md)
    [checkpoint: design]
