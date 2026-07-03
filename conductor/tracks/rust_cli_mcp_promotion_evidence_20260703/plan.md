# Rust CLI/MCP Promotion Evidence Plan

## Phase 1: Promotion Matrix and Evidence Standard

- [ ] Task: Define the Rust runtime promotion matrix
    - [ ] List calculators, pricing years, CLI commands, MCP tools, input formats, output formats, and diagnostics.
    - [ ] Assign each surface to Rust-default, Rust-opt-in, Python-only, unsupported, or blocked.
    - [ ] Link each promoted surface to fixture, command, and validation evidence.
- [ ] Task: Define the default-runtime decision rule
    - [ ] State the minimum evidence required to switch CLI defaults.
    - [ ] State the minimum evidence required to switch MCP defaults.
    - [ ] Record rollback and support-policy requirements.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Promotion Matrix and Evidence Standard' (Protocol in workflow.md)

## Phase 2: Cross-Surface CI and Conformance Gates

- [ ] Task: Add release-grade conformance commands
    - [ ] Wire Rust test, Python compatibility, CLI parity, and MCP parity checks into one documented validation path.
    - [ ] Ensure failures identify the affected calculator, pricing year, surface, and fixture.
    - [ ] Keep the gate non-interactive and suitable for CI.
- [ ] Task: Add fail-closed promotion report generation
    - [ ] Generate or maintain a report that refuses broad Rust-default claims when evidence is incomplete.
    - [ ] Include Python-only and unsupported surfaces explicitly.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Cross-Surface CI and Conformance Gates' (Protocol in workflow.md)

## Phase 3: Documentation and Runtime Decision

- [ ] Task: Update user-facing runtime documentation
    - [ ] Update README, CLI docs, MCP docs, and support-status material to match the promotion matrix.
    - [ ] Document runtime selection, rollback, and residual Python dependencies.
    - [ ] Remove or rewrite any stale wording that implies broader Rust coverage than the evidence supports.
- [ ] Task: Record the default-runtime decision
    - [ ] Decide whether CLI and MCP move to Rust-default, remain Rust-opt-in, or stay Python-default.
    - [ ] Commit the decision record with links to CI and parity evidence.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Documentation and Runtime Decision' (Protocol in workflow.md)

## Phase 4: Closeout and Handoff

- [ ] Task: Verify project and Conductor status alignment
    - [ ] Update active tracks, project-board references, release notes, and support matrices.
    - [ ] Confirm no active track or registry row overclaims the migration state.
    - [ ] Record follow-on work for unported calculators or non-CLI/MCP adapters.
- [ ] Task: Run final release-quality validation
    - [ ] Run the documented conformance gate and relevant docs checks.
    - [ ] Archive promotion evidence if the Conductor workflow requires it after review.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Closeout and Handoff' (Protocol in workflow.md)
