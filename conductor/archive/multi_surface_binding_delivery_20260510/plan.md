# Plan: Multi-Surface Binding and Delivery Roadmap

## Phase 1: Binding Matrix and Adapter Contract

- [x] Task: Write tests for binding matrix coverage
    - [x] Verify Python, R, Julia, C#, Rust, Go, and TypeScript are covered
    - [x] Verify each surface is classified as implemented, planned, deferred, or advisory
    - [x] Verify adapters are documented as thin wrappers over the Rust core
- [x] Task: Create the binding matrix
    - [x] Record recommended tools and risks for each language
    - [x] Define stable ABI, Arrow, WASM, and service-boundary options
    - [x] Record sequencing after Rust/Python parity
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Binding Matrix and Adapter Contract' (Protocol in workflow.md) [9141601]

## Phase 2: TypeScript/WASM and GitHub Pages Delivery

- [x] Task: Write tests for browser delivery boundaries
    - [x] Verify GitHub Pages remains synthetic/demo-only
    - [x] Verify TypeScript/WASM plans consume generated or shared contracts
    - [x] Verify no real-data upload workflow is introduced
- [x] Task: Document TypeScript and GitHub Pages delivery
    - [x] Define wasm-bindgen or wasm-pack evaluation criteria
    - [x] Define fixture-backed browser parity workflow
    - [x] Update web architecture and docs-site guidance
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'TypeScript/WASM and GitHub Pages Delivery' (Protocol in workflow.md) [31f8af0]

## Phase 3: Streamlit and Service/API Delivery

- [x] Task: Write tests for hosted delivery boundaries
    - [x] Verify Streamlit is documented as a Python-hosted analyst surface
    - [x] Verify service/API pathways preserve public contracts and privacy rules
- [x] Task: Document Streamlit and service delivery
    - [x] Define local/demo Streamlit workflow and data constraints
    - [x] Define secure service boundary options for real-data workflows
    - [x] Define observability and logging limits for sensitive fields
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'Streamlit and Service/API Delivery' (Protocol in workflow.md) [ecb6f48]

## Phase 4: R, Julia, C#, Go, and Power Platform Packaging Plans

- [x] Task: Write tests for downstream packaging guidance
    - [x] Verify R, Julia, C#, and Go plans name binding options and blockers
    - [x] Verify Power Platform consumes a service or custom connector only
- [x] Task: Document downstream packaging plans
    - [x] Evaluate extendr for R, jlrs or Julia ccall for Julia, and ABI or service wrappers for C# and Go
    - [x] Define package/versioning expectations for each surface
    - [x] Define when each surface can claim parity or release readiness
- [x] Task: Conductor - Automated Review and Checkpoint via conductor-review, auto-fix, and auto-progress 'R, Julia, C#, Go, and Power Platform Packaging Plans' (Protocol in workflow.md) [3676064]
