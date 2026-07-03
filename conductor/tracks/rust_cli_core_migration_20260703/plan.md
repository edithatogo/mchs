# Rust CLI Core Migration Plan

## Phase 0: Contract Hardening Pre-Phase

- [ ] Task: Pin CLI comparison and schema contracts
    - [ ] Define the numeric tolerance and rounding policy for acute 2025 CLI parity checks.
    - [ ] Name the schema parity source for CLI input, output, diagnostics, and provenance fields.
    - [ ] Name the unsupported diagnostic codes for unsupported calculators, years, formats, and output modes.
- [ ] Task: Pin CLI support-status wording
    - [ ] Define support-status wording for Rust canary, Rust opt-in, Python default, and Rust default.
    - [ ] Confirm wording separates current default behaviour from intended Rust migration state.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Contract Hardening Pre-Phase' (Protocol in workflow.md)

## Phase 1: CLI Surface Inventory and Migration Boundary

- [ ] Task: Inventory public CLI commands and file contracts
    - [ ] List current command names, options, input formats, output formats, exit codes, and diagnostics.
    - [ ] Map each command to the Python implementation modules and existing contract files.
    - [ ] Record the Rust core API surface needed by each command.
- [ ] Task: Define runtime-selection and fallback policy
    - [ ] Specify `--runtime python|rust|auto` as the user-facing runtime selector.
    - [ ] Document that the default runtime remains `python` until promotion evidence records a default change.
    - [ ] Specify `NWAU_RUNTIME` as an internal or CI override and state that the explicit CLI `--runtime` option takes precedence.
    - [ ] Specify fail closed behaviour when `--runtime rust` is requested for unsupported calculators, years, formats, or output modes.
    - [ ] Document when Python fallback is permitted during transition.
- [ ] Task: Pin acute 2025 as the first Rust-backed implementation slice
    - [ ] Link the slice to existing Rust canary/kernel evidence.
    - [ ] Record non-acute calculators, non-2025 years, and unvalidated formats as follow-on coverage.
- [ ] Task: Conductor - Automated Review and Checkpoint 'CLI Surface Inventory and Migration Boundary' (Protocol in workflow.md)

## Phase 2: Red Tests for Rust-Backed CLI Parity

- [ ] Task: Add failing CLI parity tests
    - [ ] Add golden-fixture tests comparing Python and Rust-backed CLI outputs.
    - [ ] Cover success, unsupported-surface, malformed-input, and diagnostics cases.
    - [ ] Include the promoted acute 2025 fixture set before any follow-on coverage expands.
- [ ] Task: Add CI command coverage for Rust-backed CLI execution
    - [ ] Define a narrow non-interactive command suitable for PR CI.
    - [ ] Ensure tests fail before the Rust-backed execution path is implemented.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Red Tests for Rust-Backed CLI Parity' (Protocol in workflow.md)

## Phase 3: Implement Rust-Backed CLI Execution

- [ ] Task: Wire CLI calculation and validation calls to the Rust core
    - [ ] Route supported calculator requests through Rust-backed bindings or process boundaries.
    - [ ] Preserve existing CLI schemas, diagnostics, and exit codes.
    - [ ] Avoid duplicating formula logic in CLI-specific adapters.
- [ ] Task: Implement unsupported-surface handling
    - [ ] Return explicit unsupported diagnostics when Rust is requested outside validated coverage.
    - [ ] Preserve Python fallback only where the runtime-selection policy allows it.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Implement Rust-Backed CLI Execution' (Protocol in workflow.md)

## Phase 4: Evidence, Documentation, and Release Readiness

- [ ] Task: Produce CLI migration evidence
    - [ ] Commit parity reports, command logs, or generated artifacts that prove promoted coverage.
    - [ ] Update support-status documentation and README runtime wording.
    - [ ] Record residual Python-only surfaces as explicit gaps.
- [ ] Task: Run release-quality validation
    - [ ] Run Python CLI tests, Rust tests, and formatting/lint checks relevant to the changed surfaces.
    - [ ] Confirm documentation does not overclaim Rust default status.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Evidence, Documentation, and Release Readiness' (Protocol in workflow.md)
