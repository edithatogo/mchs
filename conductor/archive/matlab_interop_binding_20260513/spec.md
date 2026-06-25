# Specification: MATLAB Interoperability

## Overview
Define MATLAB interoperability for numerical, simulation, teaching, and legacy
analytics consumers. MATLAB should consume file, CLI, service, or C ABI
boundaries and must not duplicate formula logic.

## Functional Requirements
- Compare MAT/CSV/Parquet, CLI/service, and C ABI interop.
- Preserve diagnostics, provenance, and validation status in MATLAB-readable outputs.
- Document toolbox publication only after fixture and platform gates pass.

## Acceptance Criteria
- MATLAB interop strategy is selected and documented.
- Examples validate against shared fixtures.
- Formula logic remains single-sourced outside MATLAB scripts.
