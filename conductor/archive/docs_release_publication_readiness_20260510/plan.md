# Plan: Documentation, Release, and Public Readiness

## Phase 1: Starlight Architecture Content

- [x] Task: Write docs-site tests for Rust roadmap content [ee7ad94]
    - [x] Verify Starlight pages exist for Rust-core architecture and migration status
    - [x] Verify docs distinguish current validated Python behavior from intended Rust behavior
- [x] Task: Add public architecture docs [ee7ad94]
    - [x] Add Rust-core architecture, migration, and binding roadmap pages
    - [x] Link relevant Conductor governance docs into Starlight navigation
    - [x] Preserve conservative validation language
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Starlight Architecture Content' (Protocol in workflow.md) [ee7ad94]

## Phase 2: API and Reference Generation Plan [checkpoint: ee7ad94]

- [x] Task: Write tests for generated-reference planning [ee7ad94]
    - [x] Verify OpenAPI, schema, or generated reference plans are linked from docs
    - [x] Verify generated docs do not claim unsupported runtime parity
- [x] Task: Document generated reference strategy [ee7ad94]
    - [x] Define how public contracts, Rust API docs, Python docs, and WASM docs should surface
    - [x] Evaluate Starlight OpenAPI or equivalent integration only where it supports real public contracts
    - [x] Record documentation ownership for each language surface
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'API and Reference Generation Plan' (Protocol in workflow.md) [ee7ad94]

## Phase 3: Release Notes, Provenance, and Validation Status [checkpoint: ee7ad94]

- [x] Task: Write release-documentation tests [ee7ad94]
    - [x] Verify release policy covers Rust crates, Python wheels, WASM packages, and binding artifacts
    - [x] Verify validation status remains fixture-backed
- [x] Task: Update release and validation docs [ee7ad94]
    - [x] Define version relationships between package, core crate, data bundle, and binding packages
    - [x] Define release-note requirements for calculator behavior changes
    - [x] Document provenance and validation evidence expected for Rust-backed releases
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Release Notes, Provenance, and Validation Status' (Protocol in workflow.md) [ee7ad94]

## Phase 4: Public Repo Hygiene and Contributor Pathway [checkpoint: ee7ad94]

- [x] Task: Write tests for public-readiness documentation [ee7ad94]
    - [x] Verify contributor guidance names Python, docs, and future Rust quality gates
    - [x] Verify security, citation, license, and contribution expectations are present or gap-recorded
- [x] Task: Update public-readiness docs [ee7ad94]
    - [x] Add or update contributor pathway, security policy recommendation, citation guidance, and validation vocabulary links
    - [x] Record any unresolved public-readiness gaps as follow-on work
    - [x] Confirm GitHub Pages documentation remains the public docs front door
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Public Repo Hygiene and Contributor Pathway' (Protocol in workflow.md) [ee7ad94]
