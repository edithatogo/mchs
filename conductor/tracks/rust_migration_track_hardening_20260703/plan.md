# Rust Migration Track Hardening Plan

## Phase 1: Governance Normalization

- [~] Task: Normalize metadata for the Rust migration track set
    - [ ] Update CLI and MCP migration tracks to use `track_class: binding`, `current_state: roadmap-only`, and `publication_status: published-with-gaps`.
    - [ ] Update the promotion evidence track to use `track_class: validator`, `current_state: roadmap-only`, and `publication_status: future-only`.
    - [ ] Keep dependencies, primary contracts, and completion evidence explicit.
- [ ] Task: Add governance validation for new Rust migration track metadata
    - [ ] Extend an existing validator or add a focused test that rejects unknown track classes, unknown current states, and missing publication status.
    - [ ] Cover the three Rust migration track metadata files directly.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Governance Normalization' (Protocol in workflow.md)

## Phase 2: Runtime Boundary Decisions

- [ ] Task: Harden the CLI runtime-selection contract
    - [ ] Update the CLI migration spec and plan to define `--runtime python|rust|auto`.
    - [ ] Document Python as the default until promotion evidence changes the default.
    - [ ] Document `NWAU_RUNTIME` as an internal or CI override with explicit CLI options taking precedence.
    - [ ] Document fail-closed behaviour when `rust` is requested outside validated coverage.
- [ ] Task: Harden the MCP runtime boundary
    - [ ] Update the MCP migration spec and plan to distinguish Python stdio transport from formula runtime.
    - [ ] Require promoted MCP calculation behaviour to use a Rust-backed dispatcher.
    - [ ] State that MCP reuses CLI runtime policy and parity fixtures without implicitly shelling out to the CLI.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Runtime Boundary Decisions' (Protocol in workflow.md)

## Phase 3: First-Slice and Contract Hardening

- [ ] Task: Pin acute 2025 as the first migration slice
    - [ ] Update the CLI and MCP migration specs to make acute 2025 the first Rust-backed implementation slice.
    - [ ] Link the first slice to existing Rust canary/kernel evidence and Rust Core Continuation dependencies.
    - [ ] Record other calculators and years as follow-on coverage until their fixtures are ready.
- [ ] Task: Add contract-hardening pre-phases to CLI and MCP plans
    - [ ] Add numeric tolerance and rounding policy tasks.
    - [ ] Add schema parity source tasks.
    - [ ] Add unsupported diagnostic-code tasks.
    - [ ] Add support-status wording tasks for Rust canary, Rust opt-in, Python default, and Rust default.
- [ ] Task: Conductor - Automated Review and Checkpoint 'First-Slice and Contract Hardening' (Protocol in workflow.md)

## Phase 4: Status Alignment and Additional Track Improvements

- [ ] Task: Align Conductor registry and status matrix
    - [ ] Update `conductor/tracks.md` wording if needed to reflect hardened gates.
    - [ ] Update `conductor/status-matrix.json` if any status or recommended-next-track ordering changes.
    - [ ] Run the Conductor status-matrix validator.
- [ ] Task: Record additional track-quality improvements
    - [ ] Decide whether to update the reusable `conductor-newtrack` skill/template wording so it matches the repo's automated-review workflow.
    - [ ] Record whether a broader metadata-governance validator should cover all active tracks, not only the Rust migration set.
    - [ ] Record whether project-board synchronization should explicitly include the new hardening track.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Status Alignment and Additional Track Improvements' (Protocol in workflow.md)
