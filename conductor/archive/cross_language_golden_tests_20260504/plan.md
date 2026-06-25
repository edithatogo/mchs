# Plan: Cross-Language Golden Test Suite

## Phase 1: Fixture Contract [checkpoint: 5956b7b]

- [x] Task: Write tests for fixture manifest schema and payload rules
    - [x] Validate calculator, pricing year, service stream, source basis, tolerance, rounding policy, and privacy classification
    - [x] Reject fixtures without provenance, schema version, or cross-language readiness metadata
- [x] Task: Define the fixture pack format
    - [x] Use a JSON manifest with Arrow/Parquet tabular payloads where practical
    - [x] Document precision, rounding policy, expected schema, and runner-neutral typing
- [x] Task: Conductor - User Manual Verification 'Fixture Contract' (Protocol in workflow.md) [5956b7b]

## Phase 2: Python Consumption [checkpoint: 5956b7b]

- [x] Task: Write tests that consume fixture packs through the shared manifest
    - [x] Cover the implemented acute_2025 pilot pack first
    - [x] Distinguish regression parity from output parity and preserve provenance in failures
- [x] Task: Add a fixture runner [0ed673f]
    - [x] Generate pytest cases from manifest metadata
    - [x] Validate privacy classification, tolerance, source basis, and cross-language readiness before execution
- [x] Task: Conductor - User Manual Verification 'Python Consumption' (Protocol in workflow.md) [5956b7b]

## Phase 3: Cross-Engine Readiness [checkpoint: 5956b7b]

- [x] Task: Write compatibility checks for C# and web consumption
    - [x] Verify naming, numeric precision, enum representation, and runner-neutral payload metadata
    - [x] Verify no Python-specific assumptions leak into the fixture pack
- [x] Task: Document the cross-engine parity workflow [5956b7b]
    - [x] Define how Python, C#, and web runners consume the same manifest and payloads
    - [x] Define the release-blocking criteria for fixture packs marked cross-language ready
- [x] Task: Conductor - User Manual Verification 'Cross-Engine Readiness' (Protocol in workflow.md) [5956b7b]
