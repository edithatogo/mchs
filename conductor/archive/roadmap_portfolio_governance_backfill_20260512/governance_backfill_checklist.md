# Governance Backfill Checklist

## Purpose

Backfill governance metadata (class, current state, primary contract,
dependencies, completion evidence, publication status) for every active and
archived Conductor track. This prevents inaccurate completion claims and
clarifies the real state of each track before broad implementation proceeds.

## Active Tracks

### Source Archive and Provenance Registry

- **Class:** source-discovery
- **Current State:** complete
- **Primary Contract:** source acquisition and manifest policy
- **Dependencies:** none
- **Completion Evidence:** archive manifest, provenance docs, restore policy
- **Publication Status:** not-applicable
- **Notes:** Already complete; registry metadata matches durable evidence.

### Cross-Language Golden Test Suite

- **Class:** validator
- **Current State:** complete
- **Primary Contract:** golden fixture schema and cross-engine runner
- **Dependencies:** source archive manifest
- **Completion Evidence:** fixture contracts, runner tests, golden fixture examples
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### Python Tooling and CI Modernization

- **Class:** governance
- **Current State:** complete
- **Primary Contract:** Python tooling matrix, CI pipeline, lint/type/coverage gates
- **Dependencies:** source archive, validation fixture shape
- **Completion Evidence:** CI workflows, pre-commit config, coverage reports
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### Calculator Core Abstraction and Validation Models

- **Class:** governance
- **Current State:** complete
- **Primary Contract:** calculator boundary API, parameter models, provenance metadata
- **Dependencies:** validation evidence, CI coverage
- **Completion Evidence:** typed models, boundary tests, schema definitions
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### Public Calculator API Contract

- **Class:** data-contract
- **Current State:** complete
- **Primary Contract:** versioned input/output schema
- **Dependencies:** calculator core abstractions, golden fixtures
- **Completion Evidence:** schema files, conformance tests, contract docs
- **Publication Status:** published
- **Notes:** Already complete.

### Arrow and Polars Data Bundle Migration

- **Class:** data-contract
- **Current State:** complete
- **Primary Contract:** Arrow/Parquet data bundle format
- **Dependencies:** calculator core abstractions, stable validation fixtures
- **Completion Evidence:** data bundle migration docs, Arrow schema tests
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### GitHub Pages Web App Prototype

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** browser demo prototype with synthetic-data boundary
- **Dependencies:** public API contract, validation fixtures, governance rules
- **Completion Evidence:** GitHub Pages deployment, demo app docs
- **Publication Status:** published
- **Notes:** Already complete.

### C# Calculation Engine and Power Platform Adapter

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** C# engine and Power Platform adapter
- **Dependencies:** public API contract, golden fixtures
- **Completion Evidence:** C# engine tests, Power Platform solution docs
- **Publication Status:** published-with-gaps
- **Notes:** Already complete.

### Release and Supply-Chain Governance

- **Class:** publication
- **Current State:** complete
- **Primary Contract:** release policy, signed artifacts, supply-chain controls
- **Dependencies:** CI, validation evidence, contract stability
- **Completion Evidence:** release.yml, publish.yml, dependency automation
- **Publication Status:** published
- **Notes:** Already complete.

### Starlight Documentation Site and Versioning

- **Class:** governance
- **Current State:** complete
- **Primary Contract:** Starlight docs platform and versioning model
- **Dependencies:** public contracts, validation vocabulary, GitHub Pages rules
- **Completion Evidence:** docs-site deployment, versioning docs, migration guide
- **Publication Status:** published
- **Notes:** Archived track; already complete.

### Ecosystem Standards and Language Readiness

- **Class:** governance
- **Current State:** complete
- **Primary Contract:** standards assessment and readiness report
- **Dependencies:** contracts, fixtures, governance, docs, Power Platform boundary
- **Completion Evidence:** standards assessment docs, readiness reports
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### Rust Core Architecture and Calculator Abstraction

- **Class:** governance
- **Current State:** complete
- **Primary Contract:** Rust core architecture document
- **Dependencies:** public contracts, Arrow bundle guidance, golden fixtures
- **Completion Evidence:** Rust workspace scaffold, architecture docs
- **Publication Status:** future-only
- **Notes:** Already complete.

### Rust Acute 2025 Proof of Concept with Python Bindings

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** Rust-backed acute 2025 canary with Python opt-in
- **Dependencies:** Rust core architecture, acute golden fixtures, Python packaging
- **Completion Evidence:** Rust canary code, Python binding tests, fixture parity
- **Publication Status:** unpublished
- **Notes:** Already complete.

### Multi-Surface Binding and Delivery Roadmap

- **Class:** governance
- **Current State:** complete
- **Primary Contract:** binding delivery sequencing plan
- **Dependencies:** Rust core architecture, POC results, public contracts
- **Completion Evidence:** binding roadmap docs
- **Publication Status:** not-applicable
- **Notes:** Already complete; roadmap-only.

### Rust CI, Pre-Commit, and Supply-Chain Hardening

- **Class:** publication
- **Current State:** complete
- **Primary Contract:** Rust CI and supply-chain controls
- **Dependencies:** Python CI, release governance, docs-site workflow
- **Completion Evidence:** Rust CI workflows, Rust-specific pre-commit hooks
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### Documentation, Release, and Public Readiness

- **Class:** publication
- **Current State:** complete
- **Primary Contract:** public-readiness assessment and conservative docs
- **Dependencies:** Rust core, binding roadmap, Starlight, validation vocabulary
- **Completion Evidence:** readiness docs, release status docs
- **Publication Status:** published-with-gaps
- **Notes:** Already complete.

### Modernization Foundation

- **Class:** governance
- **Current State:** complete-with-gaps
- **Primary Contract:** coordination umbrella
- **Dependencies:** all focused tracks
- **Completion Evidence:** sequencing and governance context
- **Publication Status:** not-applicable
- **Notes:** Coordination only; retained for context. No active work.

### Power Platform ALM App Setup and Delivery

- **Class:** publication
- **Current State:** complete
- **Primary Contract:** Power Platform ALM scaffold
- **Dependencies:** Power Platform boundary docs
- **Completion Evidence:** solution files, deployment workflow docs
- **Publication Status:** published
- **Notes:** Archived.

### Power BI and Power Platform CLI Tooling

- **Class:** publication
- **Current State:** complete
- **Primary Contract:** CLI tooling setup and version checks
- **Dependencies:** Power Platform ALM app setup
- **Completion Evidence:** tooling setup docs, version checks
- **Publication Status:** published
- **Notes:** Archived.

### IHACPA Source Archive Gap Closure and Restore Validation

- **Class:** source-discovery
- **Current State:** complete
- **Primary Contract:** SAS artifact recovery and restore validation
- **Dependencies:** source archive manifesting
- **Completion Evidence:** gap records, restore validation tests
- **Publication Status:** not-applicable
- **Notes:** Archived.

### IHACPA Feature Incorporation and Calculator Coverage Roadmap

- **Class:** calculator
- **Current State:** complete
- **Primary Contract:** archive-to-calculator coverage mapping
- **Dependencies:** source archive inventory
- **Completion Evidence:** coverage matrix, parity gap analysis
- **Publication Status:** not-applicable
- **Notes:** Archived.

### IHACPA 2026-27 Support

- **Class:** calculator
- **Current State:** complete
- **Primary Contract:** 2026-27 NEP, specification, price-weight, calculator support
- **Dependencies:** source archive, contracts
- **Completion Evidence:** 2026-27 manifest, validation status
- **Publication Status:** published-with-gaps
- **Notes:** Already complete.

### Community Mental Health Calculator Support

- **Class:** calculator
- **Current State:** complete
- **Primary Contract:** community mental health and AMHCC calculator separation
- **Dependencies:** admitted mental health calculators
- **Completion Evidence:** stream separation docs, parity tests
- **Publication Status:** published
- **Notes:** Archived.

### Classification Input Validation

- **Class:** validator
- **Current State:** complete
- **Primary Contract:** stream-specific classification version matrices
- **Dependencies:** source archive, contracts
- **Completion Evidence:** classification matrix, validation tests
- **Publication Status:** published
- **Notes:** Already complete.

### Costing-Study Tutorials and Examples

- **Class:** costing
- **Current State:** complete
- **Primary Contract:** synthetic costing-study tutorials
- **Dependencies:** contract stability, validation gates
- **Completion Evidence:** tutorial docs, synthetic examples
- **Publication Status:** published
- **Notes:** Already complete.

### Historical IHACPA Coverage Audit

- **Class:** audit
- **Current State:** complete
- **Primary Contract:** historical coverage verification report
- **Dependencies:** source archive inventory
- **Completion Evidence:** historical coverage table, gap records
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### Python Rust Binding Stabilization

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** stable pyo3/maturin Python binding
- **Dependencies:** Rust core, public API contract
- **Completion Evidence:** binding tests, opt-in documentation
- **Publication Status:** unpublished
- **Notes:** Already complete.

### R Binding

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** R language binding
- **Dependencies:** Rust core, contracts
- **Completion Evidence:** R binding setup, contract tests
- **Publication Status:** unpublished
- **Notes:** Already complete.

### Julia Binding

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** Julia language binding
- **Dependencies:** Rust core, contracts
- **Completion Evidence:** Julia binding setup, interop tests
- **Publication Status:** unpublished
- **Notes:** Already complete.

### TypeScript and WebAssembly Binding

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** TS/WASM browser binding with synthetic-data boundary
- **Dependencies:** Rust core, contracts
- **Completion Evidence:** WASM binding setup, demo tests
- **Publication Status:** unpublished
- **Notes:** Already complete.

### C ABI Binding

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** stable C ABI for institutional embedding
- **Dependencies:** core schemas, calculator parity
- **Completion Evidence:** C ABI header, interop tests
- **Publication Status:** unpublished
- **Notes:** Already complete.

### CLI and File Interoperability Binding

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** Arrow/Parquet/CSV CLI and file contract
- **Dependencies:** Rust core, contracts
- **Completion Evidence:** CLI tooling, file format tests
- **Publication Status:** unpublished
- **Notes:** Already complete.

### Reference Data Manifest Schema

- **Class:** data-contract
- **Current State:** complete
- **Primary Contract:** machine-readable pricing-year manifest schema
- **Dependencies:** source archive, contracts
- **Completion Evidence:** schema definition, pinned examples, manifest files
- **Publication Status:** published
- **Notes:** Already complete.

### IHACPA Source Scanner

- **Class:** source-discovery
- **Current State:** complete
- **Primary Contract:** source discovery and manifest automation
- **Dependencies:** source archive policy
- **Completion Evidence:** scanner tooling, draft manifests
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### Pricing-Year Validation Gates

- **Class:** validator
- **Current State:** complete
- **Primary Contract:** `funding-calculator validate-year` gate
- **Dependencies:** manifest schema, validation vocabulary, roadmap governance
- **Completion Evidence:** CLI command, strategy docs, CI notes
- **Publication Status:** not-ready
- **Notes:** Already complete.

### Pricing-Year Diff Tooling

- **Class:** validator
- **Current State:** complete
- **Primary Contract:** `funding-calculator diff-year` comparison tool
- **Dependencies:** pricing-year manifest schema
- **Completion Evidence:** CLI command, diff examples, strategy docs
- **Publication Status:** not-ready
- **Notes:** Already complete.

### Coding-Set Version Registry

- **Class:** data-contract
- **Current State:** complete
- **Primary Contract:** versioned coding-set compatibility registry
- **Dependencies:** classification input validation, source archive
- **Completion Evidence:** registry data, strategy docs, CI notes
- **Publication Status:** published
- **Notes:** Already complete.

### Formula and Parameter Bundle Pipeline

- **Class:** data-contract
- **Current State:** complete
- **Primary Contract:** formula extraction and bundling pipeline
- **Dependencies:** reference-data manifest schema
- **Completion Evidence:** example manifests, pipeline docs
- **Publication Status:** published
- **Notes:** Already complete.

### AR-DRG ICD/ACHI/ACS Mapping Registry

- **Class:** classifier
- **Current State:** complete
- **Primary Contract:** version-specific AR-DRG mapping registry
- **Dependencies:** coding-set registry, source archive
- **Completion Evidence:** registry data, mapping tests
- **Publication Status:** published
- **Notes:** Already complete.

### AR-DRG Grouper Integration

- **Class:** classifier
- **Current State:** complete
- **Primary Contract:** precomputed and external AR-DRG grouper interface
- **Dependencies:** AR-DRG mapping registry
- **Completion Evidence:** grouper adapter, integration tests
- **Publication Status:** published-with-gaps
- **Notes:** Already complete.

### ICD-10-AM/ACHI/ACS Licensed Product Workflow

- **Class:** governance
- **Current State:** complete
- **Primary Contract:** licensed classification asset handling workflow
- **Dependencies:** source archive policy
- **Completion Evidence:** workflow docs, commit guard tests
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### AR-DRG Version Parity Fixtures

- **Class:** classifier
- **Current State:** complete
- **Primary Contract:** version-specific AR-DRG parity fixture validation
- **Dependencies:** AR-DRG grouper, mapping registry
- **Completion Evidence:** fixture tests, parity reports
- **Publication Status:** published
- **Notes:** Already complete.

### Emergency UDG/AECC Transition Registry

- **Class:** classifier
- **Current State:** complete
- **Primary Contract:** emergency classification transition registry
- **Dependencies:** coding-set registry
- **Completion Evidence:** registry docs, transition tests
- **Publication Status:** published
- **Notes:** Already complete.

### Emergency Code Mapping Pipeline

- **Class:** classifier
- **Current State:** complete
- **Primary Contract:** versioned emergency field mapping pipeline
- **Dependencies:** emergency transition registry
- **Completion Evidence:** mapping bundle tests
- **Publication Status:** published
- **Notes:** Already complete.

### Emergency Grouper Integration

- **Class:** classifier
- **Current State:** complete
- **Primary Contract:** UDG/AECC grouper interface
- **Dependencies:** emergency code mapping pipeline
- **Completion Evidence:** adapter tests, integration docs
- **Publication Status:** published-with-gaps
- **Notes:** Already complete.

### Emergency Classification Parity Fixtures

- **Class:** classifier
- **Current State:** complete
- **Primary Contract:** emergency classification parity fixture validation
- **Dependencies:** transition registry, mapping pipeline, grouper integration
- **Completion Evidence:** fixture tests, parity reports
- **Publication Status:** published
- **Notes:** Already complete.

### Abstraction Doctrine Enforcement

- **Class:** governance
- **Current State:** complete
- **Primary Contract:** explicit boundary enforcement across all surfaces
- **Dependencies:** all previous contracts
- **Completion Evidence:** boundary tests, enforcement docs
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### Polyglot Rust Core Roadmap

- **Class:** governance
- **Current State:** complete
- **Primary Contract:** Rust-core migration coordination
- **Dependencies:** Rust core architecture, binding delivery roadmap
- **Completion Evidence:** sequencing docs, coordination notes
- **Publication Status:** not-applicable
- **Notes:** Already complete.

### C#/.NET Binding

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** C#/.NET language binding
- **Dependencies:** Rust core, C ABI or service contract
- **Completion Evidence:** binding setup, interop tests
- **Publication Status:** unpublished
- **Notes:** Already complete.

### Go Binding

- **Class:** binding
- **Current State:** complete
- **Primary Contract:** Go language binding
- **Dependencies:** Rust core, contracts
- **Completion Evidence:** binding setup, interop tests
- **Publication Status:** unpublished
- **Notes:** Already complete.

### Java/JVM Binding

- **Class:** binding
- **Current State:** in-progress
- **Primary Contract:** JVM language binding
- **Dependencies:** Rust core, contracts
- **Completion Evidence:** binding setup, interop tests
- **Publication Status:** unpublished
- **Notes:** In progress; not yet complete.

### SQL and DuckDB Integration

- **Class:** binding
- **Current State:** roadmap-only
- **Primary Contract:** SQL/DuckDB table interface
- **Dependencies:** Rust core, data contracts
- **Completion Evidence:** SQL schema tests, integration tests
- **Publication Status:** future-only
- **Notes:** Roadmap only; no implementation yet.

### SAS Interoperability

- **Class:** binding
- **Current State:** roadmap-only
- **Primary Contract:** SAS import/export workflow
- **Dependencies:** Rust core, data contracts
- **Completion Evidence:** SAS interop tests
- **Publication Status:** future-only
- **Notes:** Roadmap only; no implementation yet.

### Power Platform Binding

- **Class:** binding
- **Current State:** roadmap-only
- **Primary Contract:** Power Platform managed solution connector
- **Dependencies:** Rust core, contracts, C# engine
- **Completion Evidence:** connector tests, deployment docs
- **Publication Status:** future-only
- **Notes:** Roadmap only; no implementation yet.

### Cost Bucket Registry

- **Class:** costing
- **Current State:** roadmap-only
- **Primary Contract:** public IHACPA/NHCDC cost bucket definitions
- **Dependencies:** source archive, reference data
- **Completion Evidence:** registry data, caveat docs
- **Publication Status:** future-only
- **Notes:** Roadmap only; no implementation yet.

### NHCDC Cost Report Ingestion

- **Class:** costing
- **Current State:** roadmap-only
- **Primary Contract:** public NHCDC cost report ingestion pipeline
- **Dependencies:** cost bucket registry
- **Completion Evidence:** ingestion tests, provenance docs
- **Publication Status:** future-only
- **Notes:** Roadmap only; no implementation yet.

### AHPCS Costing Process Model

- **Class:** costing
- **Current State:** roadmap-only
- **Primary Contract:** AHPCS costing process concept model
- **Dependencies:** NHCDC ingestion
- **Completion Evidence:** model docs, validation aid tests
- **Publication Status:** future-only
- **Notes:** Roadmap only; no implementation yet.

### Cost Bucket Analytics Tutorials

- **Class:** costing
- **Current State:** roadmap-only
- **Primary Contract:** synthetic cost bucket analytics tutorials
- **Dependencies:** cost bucket registry
- **Completion Evidence:** tutorial docs, synthetic examples
- **Publication Status:** future-only
- **Notes:** Roadmap only; no implementation yet.

## Stale or Inconsistent Registry Statuses

| Track | Registry Status | Actual State | Action |
| --- | --- | --- | --- |
| Roadmap Portfolio Governance Backfill | `roadmap-only` | In progress (this track) | Update to completed after backfill |
| Expert Panel Remediation | `roadmap-only` | In progress (this track) | Update to completed after remediation |
| End-to-End Validated Canary | `roadmap-only` | In progress (this track) | Update to completed after canary |
| Public Appropriate-Use Docs | `roadmap-only` | In progress (this track) | Update to completed after docs |
| Release Evidence Automation | `roadmap-only` | In progress (this track) | Update to completed after automation |
| Contract Schema Export | `roadmap-only` | In progress (this track) | Update to completed after export |
| Java/JVM Binding | `in-progress` | In progress | Consistent |
| SQL/DuckDB/SA/PowerPlatform/Cost/ NHCDC/AHPCS/Tutorials | `roadmap-only` | roadmap-only | Consistent |

## Actions Required

1. Update metadata.json for this track from `roadmap-only` to `completed` after backfill.
2. Ensure all completed tracks have `"status": "completed"` in metadata.json and consistent `current_state`.
3. Mark the 6 in-progress tracks complete in tracks.md after each is delivered.
4. Fix any stale links or workflow references discovered during this backfill.
