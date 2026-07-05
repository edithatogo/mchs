# Plan: Parallel Valuation Outputs

## Phase 1: Output Contract
- [x] Task: Define parallel valuation output schema.
    - [x] Add HWAU-only output.
    - [x] Add national, state, local, and discounted valuation outputs.
    - [x] Add provenance per valuation.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Output Contract' (Protocol in workflow.md)

## Phase 2: Surface Integration
- [x] Task: Add parallel output support to required surfaces.
    - [x] CLI/file.
    - [x] HTTP API.
    - [x] MCP.
    - [x] OpenAI tool adapter.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Surface Integration' (Protocol in workflow.md)

## Phase 3: Validation
- [x] Task: Add parallel valuation fixtures and tests.
    - [x] Test national, state, local, and discounted outputs.
    - [x] Test missing schedule and unsupported jurisdiction behavior.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validation' (Protocol in workflow.md)

## Phase 4: Runtime Registry API [checkpoint: 3e3f83f]
- [x] Task: Implement the runtime price registry and parallel valuation helper.
    - [x] Add public-safe national, state, local, discounted, missing, and blocked rows.
    - [x] Preserve provenance and support status for valuation outputs.
- [x] Task: Add archive evidence for the runtime valuation contract.
    - [x] Record `nwau_py/price_registry.py`, `nwau_py/nsw_funding_model.py`, and the archive tests.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Runtime Registry API' (Protocol in workflow.md)
