# Specification: Stata Interoperability

## Overview
Define Stata interoperability for health economics and applied policy users.
Stata should use file, CLI, or service boundaries for costing studies and must
not contain a separate formula implementation.

## Functional Requirements
- Define CSV/Parquet/DTA exchange and CLI/service invocation patterns.
- Preserve diagnostics, provenance, and validation status in Stata-readable outputs.
- Document package publication only after fixture and reproducibility gates pass.

## Acceptance Criteria
- Stata interop strategy is selected and documented.
- Examples validate against shared fixtures.
- Formula logic remains single-sourced outside Stata scripts.
