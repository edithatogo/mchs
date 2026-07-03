# Rust MCP Core Migration Plan

## Phase 0: Contract Hardening Pre-Phase

- [ ] Task: Pin MCP comparison and schema contracts
    - [ ] Define the numeric tolerance and rounding policy for acute 2025 MCP parity checks.
    - [ ] Name the schema parity source for MCP requests, responses, diagnostics, and provenance fields.
    - [ ] Name the unsupported diagnostic codes for unsupported calculators, years, tools, and response formats.
- [ ] Task: Pin MCP support-status wording
    - [ ] Define support-status wording for Rust canary, Rust opt-in, Python default, and Rust default.
    - [ ] Confirm wording separates Python stdio transport from Rust-backed formula runtime.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Contract Hardening Pre-Phase' (Protocol in workflow.md)

## Phase 1: MCP Contract Inventory and Dispatcher Design

- [ ] Task: Inventory MCP tools, resources, and registry-facing metadata
    - [ ] List current tool names, resource identifiers, schemas, examples, diagnostics, and package metadata.
    - [ ] Map each MCP surface to its existing Python implementation and contract files.
    - [ ] Identify which surfaces depend on CLI migration work and which can use the Rust core directly.
- [ ] Task: Define the Rust-backed MCP dispatcher boundary
    - [ ] Specify request validation, schema conversion, Rust core invocation, and response shaping.
    - [ ] Specify unsupported-surface diagnostics and fallback rules.
    - [ ] Document that the Python stdio transport may remain during transition but is not the formula runtime.
    - [ ] Specify that promoted formula execution uses the Rust-backed dispatcher.
    - [ ] State that MCP should reuse the CLI runtime policy and parity fixtures but must not shell out to the CLI unless a later implementation decision records that boundary explicitly.
- [ ] Task: Pin acute 2025 as the first Rust-backed implementation slice
    - [ ] Link the slice to existing Rust canary/kernel evidence.
    - [ ] Reuse the CLI migration fixture scope for acute 2025.
    - [ ] Record non-acute calculators, non-2025 years, and unvalidated MCP tools or formats as follow-on coverage.
- [ ] Task: Conductor - Automated Review and Checkpoint 'MCP Contract Inventory and Dispatcher Design' (Protocol in workflow.md)

## Phase 2: Red Tests for MCP Parity

- [ ] Task: Add failing MCP dispatcher tests
    - [ ] Cover successful calculation and validation tool calls for promoted fixtures.
    - [ ] Cover unsupported calculator/year requests, malformed inputs, and diagnostics.
    - [ ] Assert response schemas remain compatible with the existing MCP contract.
- [ ] Task: Add MCP-to-CLI parity tests
    - [ ] Compare MCP tool outputs with Rust-backed CLI outputs for the same canonical fixtures.
    - [ ] Ensure tests fail before MCP uses the Rust-backed dispatcher.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Red Tests for MCP Parity' (Protocol in workflow.md)

## Phase 3: Implement Rust-Backed MCP Execution

- [ ] Task: Wire MCP tools to the Rust-backed dispatcher
    - [ ] Route promoted calculation and validation requests through Rust-backed execution.
    - [ ] Preserve tool names, response shapes, and machine-readable diagnostics.
    - [ ] Remove or quarantine duplicated formula logic from MCP-specific code paths.
- [ ] Task: Implement compatibility and fallback controls
    - [ ] Keep the stdio transport stable for existing registry consumers.
    - [ ] Return explicit unsupported diagnostics where Rust coverage is incomplete.
    - [ ] Align runtime-selection behaviour with the CLI migration track without making CLI shell-out the implicit architecture.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Implement Rust-Backed MCP Execution' (Protocol in workflow.md)

## Phase 4: Evidence, Documentation, and Registry Claim Hygiene

- [ ] Task: Produce MCP migration evidence
    - [ ] Commit MCP conformance logs or generated parity reports.
    - [ ] Update support-status and registry documentation to reflect the validated runtime path.
    - [ ] Record all remaining Python-only or unsupported MCP surfaces as explicit gaps.
- [ ] Task: Run release-quality MCP validation
    - [ ] Run MCP contract tests, Rust tests, and the relevant CLI parity command.
    - [ ] Verify documentation does not overclaim hosted, Docker, or full-Rust runtime status.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Evidence, Documentation, and Registry Claim Hygiene' (Protocol in workflow.md)
