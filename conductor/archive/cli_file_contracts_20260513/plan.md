# Plan: CLI/File Contracts

## Phase 1: Command Contract
- [x] Task: Define command names, arguments, stdout/stderr behavior, and exit codes.
    - [x] Include schema, validate, run, explain, list, and diagnose commands.
    - [x] Require `--json` for machine-readable automation.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Command Contract' (Protocol in workflow.md)

## Phase 2: File Contract
- [x] Task: Define JSON manifest and Arrow/Parquet data contracts.
    - [x] Include batch input, batch output, diagnostics, and provenance files.
    - [x] Add round-trip validation fixtures.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: File Contract' (Protocol in workflow.md)

## Phase 3: Validation
- [x] Task: Add tests for exit codes, schemas, fixtures, and fail-closed behavior.
    - [x] Validate unsupported streams and years.
    - [x] Validate schema mismatch handling.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validation' (Protocol in workflow.md)
