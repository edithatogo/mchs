# Plan: CLI and File Interoperability Binding

## Phase 1: Versioned CLI/File Contract
- [x] Task: Define the versioned CLI commands and file contract.
    - [x] Specify Arrow/Parquet as the target interchange format and CSV as compatibility-only where safe.
    - [x] Document schema requirements, diagnostics, provenance, and contract-version behavior.
    - [x] State the privacy rule for synthetic or anonymized examples only.
    - [x] Add a machine-readable contract bundle and additive `interop contract` CLI command.
    - [x] Add schema/version regression tests for the contract bundle.
    - [x] Add synthetic-data and privacy guardrail tests for committed examples.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Versioned CLI/File Contract' (Protocol in workflow.md)

## Phase 2: Round-Trip Validation and Consumer Guidance
- [x] Task: Add file round-trip tests and language-neutral examples.
    - [x] Validate outputs against golden fixtures for Arrow/Parquet and any documented CSV path.
    - [x] Add guidance for when to use file interop instead of native bindings for R, Julia, Power Platform, notebooks, and batch systems.
    - [x] Add CI notes for the actual Python Click entrypoint and future Arrow/Parquet gates.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Round-Trip Validation and Consumer Guidance' (Protocol in workflow.md)
