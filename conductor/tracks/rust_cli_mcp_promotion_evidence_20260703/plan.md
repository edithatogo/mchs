# Rust CLI/MCP Promotion Evidence Plan

## Phase 1: Promotion Matrix and Evidence Standard

- [x] Task: Define the Rust runtime promotion matrix
    - [x] List calculators, pricing years, CLI commands, MCP tools, input formats, output formats, and diagnostics.
    - [x] Assign each surface to Rust-default, Rust-opt-in, Python-only, unsupported, or blocked.
    - [x] Link each promoted surface to fixture, command, and validation evidence.
- [x] Task: Define the default-runtime decision rule
    - [x] State the minimum evidence required to switch CLI defaults.
    - [x] State the minimum evidence required to switch MCP defaults.
    - [x] Record rollback and support-policy requirements.
- [x] Task: Conductor - Automated Review and Checkpoint 'Promotion Matrix and Evidence Standard' (Protocol in workflow.md)

## Phase 2: Cross-Surface CI and Conformance Gates

- [x] Task: Add release-grade conformance commands
    - [x] Wire Rust test, Python compatibility, CLI parity, and MCP parity checks into one documented validation path.
    - [x] Ensure failures identify the affected calculator, pricing year, surface, and fixture.
    - [x] Keep the gate non-interactive and suitable for CI.
- [x] Task: Add fail-closed promotion report generation
    - [x] Generate or maintain a report that refuses broad Rust-default claims when evidence is incomplete.
    - [x] Include Python-only and unsupported surfaces explicitly.
- [x] Task: Conductor - Automated Review and Checkpoint 'Cross-Surface CI and Conformance Gates' (Protocol in workflow.md)

## Phase 3: Documentation and Runtime Decision

- [x] Task: Update user-facing runtime documentation
    - [x] Update README, CLI docs, MCP docs, and support-status material to match the promotion matrix.
    - [x] Document runtime selection, rollback, and residual Python dependencies.
    - [x] Remove or rewrite any stale wording that implies broader Rust coverage than the evidence supports.
- [x] Task: Record the default-runtime decision
    - [x] Decide whether CLI and MCP move to Rust-default, remain Rust-opt-in, or stay Python-default.
    - [x] Commit the decision record with links to CI and parity evidence.
- [x] Task: Conductor - Automated Review and Checkpoint 'Documentation and Runtime Decision' (Protocol in workflow.md)

## Phase 4: Closeout and Handoff

- [x] Task: Verify project and Conductor status alignment
    - [x] Update active tracks, project-board references, release notes, and support matrices.
    - [x] Confirm no active track or registry row overclaims the migration state.
    - [x] Record follow-on work for unported calculators or non-CLI/MCP adapters.
- [x] Task: Run final release-quality validation
    - [x] Run the documented conformance gate and relevant docs checks.
    - [x] Archive promotion evidence if the Conductor workflow requires it after review.
- [x] Task: Conductor - Automated Review and Checkpoint 'Closeout and Handoff' (Protocol in workflow.md)
