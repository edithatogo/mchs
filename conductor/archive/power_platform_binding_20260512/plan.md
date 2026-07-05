# Plan: Power Platform Binding

## Phase 1: Integration Contract [checkpoint: ab9f260]
- [x] Task: Define custom connector, service API, and managed solution contract.
    - [x] Align request/response schemas with shared calculator contracts.
    - [x] Define environment variables, connection references, and ALM requirements.
    - [x] Add `listMchsCalculatorCapabilities` and a checked calculator/year
      capability matrix so the app covers all declared calculator selectors
      across the full 2013-through-2026 archive horizon without hardcoded
      defaults.
    - [x] Add `power-platform/solution/app-surface.json` so the source app
      model loads capabilities, disables non-enabled states, validates before
      submit, and displays diagnostics without formula logic.
    - [x] Add `scripts/validate_power_platform_capabilities.py` as the local
      consistency gate for the matrix, app model, OpenAPI, examples, and
      contract operation IDs.
    - [x] Document strategy in [`binding_strategy.md`](./binding_strategy.md).
    - [x] Add machine-readable contract, OpenAPI, and synthetic validation
      examples under `contracts/power-platform/`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Integration Contract' (Protocol in workflow.md)
    [checkpoint: design]

## Phase 2: App and Flow Publication Path [checkpoint: ab9f260]
- [x] Task: Define publishable Power Platform artifact workflow.
    - [x] Package managed solution artifacts.
    - [x] Validate with solution checker and environment import/publish gates.
    - [x] Validate local contract artifacts without external Power Platform
      credentials using `tests/test_power_platform_binding_track.py`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: App and Flow Publication Path' (Protocol in workflow.md)
    [checkpoint: design]
