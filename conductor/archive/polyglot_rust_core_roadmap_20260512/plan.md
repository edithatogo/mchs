# Plan: Polyglot Rust Core Roadmap

## Phase 1: Architecture and Sequencing
- [x] Task: Define the polyglot architecture and Rust-core promotion lifecycle.
    - [x] Specify Python baseline, Rust canary, Rust opt-in, and Rust default gates.
    - [x] Define dependencies across reference-data bundles, coding-set registries, classifiers, and bindings.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Architecture and Sequencing' (Protocol in workflow.md)

## Phase 2: Shared Contract and Fixture Gates
- [x] Task: Define shared cross-language contracts and binding conformance tests.
    - [x] Specify Arrow-compatible batch schemas, diagnostics, errors, provenance, and validation status.
    - [x] Define fixture gates every binding must pass before release.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Shared Contract and Fixture Gates' (Protocol in workflow.md)

## Phase 3: Packaging and Release Plan
- [x] Task: Define packaging and release expectations for each surface.
    - [x] Cover Python wheels, Rust crates, R packages, Julia packages, NuGet packages, Go modules, WASM/npm, JVM packages, C ABI artifacts, SQL/DuckDB integration, SAS interop, CLI/file interop, web demos, and Power Platform managed solutions.
    - [x] Define which artifacts are published now, experimental, or future-only.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Packaging and Release Plan' (Protocol in workflow.md)

## Phase 4: Documentation Integration
- [x] Task: Publish the polyglot roadmap in project and docs-site materials.
    - [x] Explain current Python-first status and Rust-core target state.
    - [x] Link binding, abstraction, source-manifest, formula-bundle, and validation-gate tracks.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4: Documentation Integration' (Protocol in workflow.md)
