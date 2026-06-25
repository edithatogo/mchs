# Plan: Rust Core Architecture and Calculator Abstraction

## Phase 1: Current-State Architecture Audit [checkpoint: c052777]

- [x] Task: Write tests for Rust architecture governance [2151123]
    - [x] Verify the tracks registry contains the Rust architecture roadmap in the expected order
    - [x] Verify architecture docs distinguish current Python behavior from intended Rust-core behavior
    - [x] Verify Power Platform remains orchestration-only
- [x] Task: Audit current calculator boundaries [43d4a0a]
    - [x] Map formulae, parameters, schemas, reference loading, provenance, and adapter responsibilities
    - [x] Identify remaining pandas-coupled execution paths
    - [x] Record where existing Arrow/Parquet bundles and golden fixtures already satisfy the target contract
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Current-State Architecture Audit' (Protocol in workflow.md) [43d4a0a]

## Phase 2: Rust-Core Target Architecture ADR [checkpoint: c357f5e]

- [x] Task: Write tests for the new ADR and documentation links [5b7fd22]
    - [x] Verify the ADR exists and is referenced from Conductor and Starlight navigation where appropriate
    - [x] Verify the ADR names Rust as the intended future core and Python as the current validated path
- [x] Task: Add the Rust-core architecture ADR [2151123]
    - [x] Define crate responsibilities, adapter boundaries, and promotion gates
    - [x] Record why Arrow-compatible batch contracts are primary
    - [x] Supersede the C#-engine-first assumption without removing Power Platform support
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Rust-Core Target Architecture ADR' (Protocol in workflow.md) [c357f5e]

## Phase 3: Contract and Schema Boundary Design [checkpoint: c3e2eb1]

- [x] Task: Write contract tests for boundary documentation [38dc15e]
    - [x] Verify formulae, parameters, schemas, bundles, provenance, and validation status are documented as separate concepts
    - [x] Verify adapters are prohibited from duplicating formula logic
- [x] Task: Update contract and boundary documents [2151123]
    - [x] Update public API contract guidance for Rust-backed batch execution
    - [x] Update C#, Power Platform, and web architecture docs to consume the Rust-core contract
    - [x] Document scalar helper limits and batch-first interface expectations
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Contract and Schema Boundary Design' (Protocol in workflow.md) [c3e2eb1]

## Phase 4: Migration and Promotion Policy [checkpoint: 5ccffec]

- [x] Task: Write migration policy tests [e067ef6]
    - [x] Verify Rust promotion requires golden fixture parity and explicit validation status
    - [x] Verify Python remains default until a calculator-specific promotion record exists
- [x] Task: Document calculator-by-calculator migration policy [e067ef6]
    - [x] Define canary, parity, performance, rollback, and release-note requirements
    - [x] Define how validation claims appear in docs and release metadata
    - [x] Update product and tech-stack docs only where the architecture materially changes them
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Migration and Promotion Policy' (Protocol in workflow.md) [5ccffec]
