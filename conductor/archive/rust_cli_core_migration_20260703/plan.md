# Rust CLI Core Migration Plan

## Phase 0: Contract Hardening Pre-Phase

- [x] Task: Pin CLI comparison and schema contracts
    - [x] Define the numeric tolerance and rounding policy for acute 2025 CLI parity checks.
    - [x] Name the schema parity source for CLI input, output, diagnostics, and provenance fields.
    - [x] Name the unsupported diagnostic codes for unsupported calculators, years, formats, and output modes.
- [x] Task: Pin CLI support-status wording
    - [x] Define support-status wording for Rust canary, Rust opt-in, Python default, and Rust default.
    - [x] Confirm wording separates current default behaviour from intended Rust migration state.
- [x] Task: Conductor - Automated Review and Checkpoint 'Contract Hardening Pre-Phase' (Protocol in workflow.md)

## Phase 1: CLI Surface Inventory and Migration Boundary

- [x] Task: Inventory public CLI commands and file contracts
    - [x] List current command names, options, input formats, output formats, exit codes, and diagnostics.
    - [x] Map each command to the Python implementation modules and existing contract files.
    - [x] Record the Rust core API surface needed by each command.
- [x] Task: Define runtime-selection and fallback policy
    - [x] Specify `--runtime python|rust|auto` as the user-facing runtime selector.
    - [x] Document that the default runtime remains `python` until promotion evidence records a default change.
    - [x] Specify `NWAU_RUNTIME` as an internal or CI override and state that the explicit CLI `--runtime` option takes precedence.
    - [x] Specify fail closed behaviour when `--runtime rust` is requested for unsupported calculators, years, formats, or output modes.
    - [x] Document when Python fallback is permitted during transition.
- [x] Task: Pin acute 2025 as the first Rust-backed implementation slice
    - [x] Link the slice to existing Rust canary/kernel evidence.
    - [x] Record non-acute calculators, non-2025 years, and unvalidated formats as follow-on coverage.
- [x] Task: Conductor - Automated Review and Checkpoint 'CLI Surface Inventory and Migration Boundary' (Protocol in workflow.md)

## Phase 2: Red Tests for Rust-Backed CLI Parity

- [x] Task: Add failing CLI parity tests
    - [x] Add golden-fixture tests comparing Python and Rust-backed CLI outputs.
    - [x] Cover success, unsupported-surface, malformed-input, and diagnostics cases.
    - [x] Include the promoted acute 2025 fixture set before any follow-on coverage expands.
- [x] Task: Add CI command coverage for Rust-backed CLI execution
    - [x] Define a narrow non-interactive command suitable for PR CI.
    - [x] Ensure tests fail before the Rust-backed execution path is implemented.
- [x] Task: Conductor - Automated Review and Checkpoint 'Red Tests for Rust-Backed CLI Parity' (Protocol in workflow.md)

## Phase 3: Implement Rust-Backed CLI Execution

- [x] Task: Wire CLI calculation and validation calls to the Rust core
    - [x] Route supported calculator requests through Rust-backed bindings or process boundaries.
    - [x] Preserve existing CLI schemas, diagnostics, and exit codes.
    - [x] Avoid duplicating formula logic in CLI-specific adapters.
- [x] Task: Implement unsupported-surface handling
    - [x] Return explicit unsupported diagnostics when Rust is requested outside validated coverage.
    - [x] Preserve Python fallback only where the runtime-selection policy allows it.
- [x] Task: Conductor - Automated Review and Checkpoint 'Implement Rust-Backed CLI Execution' (Protocol in workflow.md)

## Phase 4: Evidence, Documentation, and Release Readiness

- [x] Task: Produce CLI migration evidence
    - [x] Commit parity reports, command logs, or generated artifacts that prove promoted coverage.
    - [x] Update support-status documentation and README runtime wording.
    - [x] Record residual Python-only surfaces as explicit gaps.
- [x] Task: Run release-quality validation
    - [x] Run Python CLI tests, Rust tests, and formatting/lint checks relevant to the changed surfaces.
    - [x] Confirm documentation does not overclaim Rust default status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Evidence, Documentation, and Release Readiness' (Protocol in workflow.md)
