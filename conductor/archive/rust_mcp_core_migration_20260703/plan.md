# Rust MCP Core Migration Plan

## Phase 0: Contract Hardening Pre-Phase

- [x] Task: Pin MCP comparison and schema contracts
    - [x] Define the numeric tolerance and rounding policy for acute 2025 MCP parity checks.
    - [x] Name the schema parity source for MCP requests, responses, diagnostics, and provenance fields.
    - [x] Name the unsupported diagnostic codes for unsupported calculators, years, tools, and response formats.
- [x] Task: Pin MCP support-status wording
    - [x] Define support-status wording for Rust canary, Rust opt-in, Python default, and Rust default.
    - [x] Confirm wording separates Python stdio transport from Rust-backed formula runtime.
- [x] Task: Conductor - Automated Review and Checkpoint 'Contract Hardening Pre-Phase' (Protocol in workflow.md)

## Phase 1: MCP Contract Inventory and Dispatcher Design

- [x] Task: Inventory MCP tools, resources, and registry-facing metadata
    - [x] List current tool names, resource identifiers, schemas, examples, diagnostics, and package metadata.
    - [x] Map each MCP surface to its existing Python implementation and contract files.
    - [x] Identify which surfaces depend on CLI migration work and which can use the Rust core directly.
- [x] Task: Define the Rust-backed MCP dispatcher boundary
    - [x] Specify request validation, schema conversion, Rust core invocation, and response shaping.
    - [x] Specify unsupported-surface diagnostics and fallback rules.
    - [x] Document that the Python stdio transport may remain during transition but is not the formula runtime.
    - [x] Specify that promoted formula execution uses the Rust-backed dispatcher.
    - [x] State that MCP should reuse the CLI runtime policy and parity fixtures but must not shell out to the CLI unless a later implementation decision records that boundary explicitly.
- [x] Task: Pin acute 2025 as the first Rust-backed implementation slice
    - [x] Link the slice to existing Rust canary/kernel evidence.
    - [x] Reuse the CLI migration fixture scope for acute 2025.
    - [x] Record non-acute calculators, non-2025 years, and unvalidated MCP tools or formats as follow-on coverage.
- [x] Task: Conductor - Automated Review and Checkpoint 'MCP Contract Inventory and Dispatcher Design' (Protocol in workflow.md)

## Phase 2: Red Tests for MCP Parity

- [x] Task: Add failing MCP dispatcher tests
    - [x] Cover successful calculation and validation tool calls for promoted fixtures.
    - [x] Cover unsupported calculator/year requests, malformed inputs, and diagnostics.
    - [x] Assert response schemas remain compatible with the existing MCP contract.
- [x] Task: Add MCP-to-CLI parity tests
    - [x] Compare MCP tool outputs with Rust-backed CLI outputs for the same canonical fixtures.
    - [x] Ensure tests fail before MCP uses the Rust-backed dispatcher.
- [x] Task: Conductor - Automated Review and Checkpoint 'Red Tests for MCP Parity' (Protocol in workflow.md)

## Phase 3: Implement Rust-Backed MCP Execution

- [x] Task: Wire MCP tools to the Rust-backed dispatcher
    - [x] Route promoted calculation and validation requests through Rust-backed execution.
    - [x] Preserve tool names, response shapes, and machine-readable diagnostics.
    - [x] Remove or quarantine duplicated formula logic from MCP-specific code paths.
- [x] Task: Implement compatibility and fallback controls
    - [x] Keep the stdio transport stable for existing registry consumers.
    - [x] Return explicit unsupported diagnostics where Rust coverage is incomplete.
    - [x] Align runtime-selection behaviour with the CLI migration track without making CLI shell-out the implicit architecture.
- [x] Task: Conductor - Automated Review and Checkpoint 'Implement Rust-Backed MCP Execution' (Protocol in workflow.md)

## Phase 4: Evidence, Documentation, and Registry Claim Hygiene

- [x] Task: Produce MCP migration evidence
    - [x] Commit MCP conformance logs or generated parity reports.
    - [x] Update support-status and registry documentation to reflect the validated runtime path.
    - [x] Record all remaining Python-only or unsupported MCP surfaces as explicit gaps.
- [x] Task: Run release-quality MCP validation
    - [x] Run MCP contract tests, Rust tests, and the relevant CLI parity command.
    - [x] Verify documentation does not overclaim hosted, Docker, or full-Rust runtime status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Evidence, Documentation, and Registry Claim Hygiene' (Protocol in workflow.md)
