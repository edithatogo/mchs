# Plan: Public Calculator API Contract

## Phase 1: Contract Shape [checkpoint: 3a18dc5]

- [x] Task: Write tests for calculator capability metadata [3a18dc5]
    - [x] Verify supported years, inputs, outputs, parameters, and validation status
    - [x] Verify unsupported combinations produce structured errors
    - [x] Verify numeric precision and versioned contract identifiers
- [x] Task: Define public contract schema [3a18dc5]
    - [x] Add versioning policy
    - [x] Add error model and validation response model
    - [x] Add explicit input, output, and parameter schema shapes
- [x] Task: Conductor - User Manual Verification 'Contract Shape' (Protocol in workflow.md) [3a18dc5]

## Phase 2: API and CLI Alignment [checkpoint: 3a18dc5]

- [x] Task: Write tests aligning CLI and Python API outputs [3a18dc5]
    - [x] Use the same contract definitions
    - [x] Cover errors and successful calculations
- [x] Task: Refactor one calculator surface to contract-backed behavior [3a18dc5]
    - [x] Preserve existing public behavior where documented
    - [x] Add deprecation notes where behavior must change
    - [x] Keep adapter responsibilities limited to parsing, validation, orchestration, and formatting
- [x] Task: Conductor - User Manual Verification 'API and CLI Alignment' (Protocol in workflow.md) [3a18dc5]

## Phase 3: Generation Readiness [checkpoint: 3a18dc5]

- [x] Task: Write checks for OpenAPI and C# model generation compatibility [3a18dc5]
    - [x] Validate enum naming and numeric precision
    - [x] Validate schema examples
- [x] Task: Document generation pathway [3a18dc5]
    - [x] Define how web and C# adapters consume contracts
    - [x] Define contract compatibility rules
    - [x] Define how the calculator core publishes contract-ready metadata
- [x] Task: Conductor - User Manual Verification 'Generation Readiness' (Protocol in workflow.md) [3a18dc5]
