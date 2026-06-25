# Plan: Calculator Core Abstraction and Validation Models

## Phase 1: Contract Tests [checkpoint: 5191561]

- [x] Task: Write tests for contract-backed parameter and schema boundaries [5191561]
    - [x] Validate pricing-year selection against the public API contract
    - [x] Validate required input fields and output columns from the contract shape
    - [x] Validate explicit error shapes for invalid contract inputs
- [x] Task: Introduce calculator contract types [5191561]
    - [x] Add parameter, input, output, and provenance model concepts
    - [x] Keep behavior-compatible adapters for existing calculators
    - [x] Bind these types to the public API contract definitions
- [x] Task: Conductor - User Manual Verification 'Contract Tests and Boundary Shape' (Protocol in workflow.md) [5191561]

## Phase 2: Reference Data Boundaries [checkpoint: 5191561]

- [x] Task: Write tests for reference bundle resolution [5191561]
    - [x] Verify explicit bundle selection by year, calculator, and manifest identity
    - [x] Verify missing or mismatched bundles produce clear errors
- [x] Task: Implement reference data abstraction [5191561]
    - [x] Separate raw archive, extracted data, and runtime bundle locations
    - [x] Add provenance metadata to runtime resolution
    - [x] Make bundle selection deterministic from year, calculator, and manifest identity
    - [x] Keep acute and other calculators consuming resolved reference helpers instead of loading bundles inline
- [x] Task: Conductor - User Manual Verification 'Reference Bundle Boundaries' (Protocol in workflow.md) [5191561]

## Phase 3: Adapter Boundaries [checkpoint: 5191561]

- [x] Task: Write tests proving CLI and library paths share the same adapter helper and core behavior [5191561]
    - [x] Use shared fixtures
    - [x] Assert equivalent outputs
- [x] Task: Separate delivery adapters from calculator core [5191561]
    - [x] Define adapter responsibilities for CLI, Python API, web, and C#
    - [x] Document prohibited adapter behavior
    - [x] Keep adapter code limited to parsing, validation, orchestration, and formatting
    - [x] Reuse a shared adapter helper where CLI and library parity needs to stay aligned
- [x] Task: Conductor - User Manual Verification 'Adapter Boundaries' (Protocol in workflow.md) [5191561]
