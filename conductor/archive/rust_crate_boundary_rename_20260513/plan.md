# Plan: Rust Crate Boundaries and HWAU Rename

## Phase 1: Boundary Design
- [x] Task: Define target crate boundaries.
    - [x] Document contracts, core, CLI, MCP, API, Python, .NET, and WASM crates.
    - [x] Document C ABI as implementation boundary only.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Boundary Design' (Protocol in workflow.md)

## Phase 2: Rename Plan
- [x] Task: Define NWAU-to-HWAU migration path.
    - [x] Add compatibility aliases.
    - [x] Add deprecation notes.
    - [x] Add migration tests.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Rename Plan' (Protocol in workflow.md)

## Phase 3: Coordinated Implementation
- [x] Task: Coordinate with active Rust implementation agents.
    - [x] Avoid conflicting file edits.
    - [x] Stage only planned rename changes after implementation stabilizes.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Coordinated Implementation' (Protocol in workflow.md)
