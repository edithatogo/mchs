# Plan: Scaffold and Stub Completion Backlog

## Phase 1: Baseline Audit and State Map

- [x] Task: Capture the current no-stub detector baseline.
    - [x] Run `python conductor/scripts/stub_detector.py --root microcosting_healthservices --json`.
    - [x] Record every detector finding with owning track, claimed state, and missing evidence.
    - [x] Add regression tests or fixtures for any detector blind spots discovered during the audit.
- [x] Task: Inventory scaffold and non-final surfaces.
    - [x] Review bindings, contracts, Power Platform, WebAssembly, registry tracks, README claims, docs, and Conductor metadata.
    - [x] Classify each surface as promote-now, retain-as-non-final, or remove/quarantine.
    - [x] Record owners, dependencies, validation commands, and support-state vocabulary for each item.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Baseline Audit and State Map' (Protocol in workflow.md)
    - Evidence: `docs/roadmaps/scaffold-stub-completion-backlog.md`, `docs/roadmaps/deferred-surface-status.md`, `tests/test_scaffold_stub_completion_backlog_track.py`.

## Phase 2: State Mismatch Remediation

- [x] Task: Write failing tests for current completion overclaims.
    - [x] Assert that complete tracks cannot pass with missing implementation evidence.
    - [x] Assert that complete-with-gaps and scaffold-only tracks remain visible as non-final.
    - [x] Assert that registry/publication claims require immutable evidence links.
- [x] Task: Fix current detector findings.
    - [x] Reconcile MCP registry submission metadata with actual implementation evidence paths.
        - [x] Current detector finding: `mcp_server_registry_submission_20260516`.
    - [x] Reconcile Rust Core GA metadata with actual implementation evidence paths or downgrade its state.
        - [x] Current detector finding: `rust_core_ga_20260513`.
    - [x] Reconcile Rust Core GA post-review metadata with actual implementation evidence paths or downgrade its state.
        - [x] Current detector finding: `rust_core_ga_post_cline_review_20260513`.
- [x] Task: Rerun stub detector and targeted tests until the mismatch set is closed or explicitly marked incomplete.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: State Mismatch Remediation' (Protocol in workflow.md)
    - Evidence: `conductor/scripts/stub_detector.py`, `tests/test_stub_detector.py`, `conductor/tracks/rust_core_ga_20260513/metadata.json`, `conductor/tracks/rust_core_ga_post_cline_review_20260513/metadata.json`.

## Phase 3: Surface Completion Backlog

- [x] Task: Create or update follow-on implementation tracks for retained scaffolds.
    - [x] Language bindings: R, Julia, C#/.NET, Go, TypeScript/WASM, Kotlin/Native, Scala/Spark, Swift, Stata, MATLAB, SQL/DuckDB, SAS interop, and C ABI where still intended.
    - [x] Platform surfaces: Power Platform, GitHub Pages/API, MCP registries, package registries, and local service adapters.
    - [x] Data and classification surfaces: source manifests, formula bundles, mapping registries, groupers, and parity fixtures.
- [x] Task: Add completion gates to each follow-on track.
    - [x] Require implementation evidence.
    - [x] Require automated tests or documented validation evidence.
    - [x] Require docs and support-status updates.
    - [x] Require publication evidence before public registry claims.
- [x] Task: Update README, docs, and support matrices to distinguish real product from scaffold.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Surface Completion Backlog' (Protocol in workflow.md)
    - Evidence: existing registry-submission tracks dated `20260524`, `docs/roadmaps/scaffold-stub-completion-backlog.md`, `README.md`.

## Phase 4: Enforcement and Closeout

- [x] Task: Wire the no-stub detector into the strict quality gate if it is not already enforced everywhere needed.
    - [x] Add CI coverage for detector execution.
    - [x] Ensure generated examples and licensed local placeholders are excluded only through explicit policy.
    - [x] Ensure failures block archive eligibility and completion claims.
- [x] Task: Run full remediation validation.
    - [x] Run the stub detector.
    - [x] Run affected Conductor registry tests.
    - [x] Run support-status and docs checks affected by state changes.
- [x] Task: Publish a concise remediation report with completed items, retained scaffolds, removed/quarantined items, and remaining implementation tracks.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Enforcement and Closeout' (Protocol in workflow.md)
    - Evidence: `python conductor/scripts/stub_detector.py --root microcosting_healthservices --json` reports zero findings; `python -m pytest tests/test_stub_detector.py -q` reports 29 passing tests; `uv run pytest tests/test_tracks_registry.py tests/test_scaffold_stub_completion_backlog_track.py -q` passes.
