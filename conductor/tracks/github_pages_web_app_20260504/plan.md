# Plan: GitHub Pages Public Demo Readiness

## Phase 1: Demo Architecture and Boundary [checkpoint: c762b81]

- [x] Task: Write checks for static deployment assumptions [c762b81]
    - [x] Verify build output can be served from GitHub Pages
    - [x] Verify demo mode depends only on synthetic fixtures and public contract metadata
    - [x] Verify no server-only calculation dependency is required for demo mode
- [x] Task: Document web architecture [c762b81]
    - [x] Define contract-driven UI capabilities
    - [x] Define privacy-safe demo data workflow
    - [x] Define the secure service boundary for any future real-data workflow outside GitHub Pages
- [x] Task: Conductor - User Manual Verification 'Demo Architecture and Boundary' (Protocol in workflow.md) [c762b81]

## Phase 2: Demo Shell [checkpoint: c762b81]

- [x] Task: Write UI smoke tests [c762b81]
    - [x] Verify calculator/year selection from metadata
    - [x] Verify synthetic fixture execution or display
    - [x] Verify real-data entry points are absent from the Pages demo
- [x] Task: Build demo shell [c762b81]
    - [x] Add GitHub Pages build/deploy path
    - [x] Add fixture-backed demonstration workflow
    - [x] Consume public contract metadata for supported calculators and fields
- [x] Task: Conductor - User Manual Verification 'Demo Shell' (Protocol in workflow.md) [c762b81]

## Phase 3: Secure Real-Data Boundary [checkpoint: c762b81]

- [x] Task: Write boundary checks for real-data workflows [c762b81]
    - [x] Verify real-data requests are routed to a secured service boundary
    - [x] Verify the Pages demo does not expose upload or persistence paths for patient data
- [x] Task: Document real-data service boundary [c762b81]
    - [x] Define how the secure service boundary validates contracts and fixture parity
    - [x] Define how the boundary integrates with the public API contract and golden fixtures
- [x] Task: Conductor - User Manual Verification 'Secure Real-Data Boundary' (Protocol in workflow.md) [c762b81]
