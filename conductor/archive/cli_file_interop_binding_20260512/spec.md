# Specification: CLI and File Interoperability Binding

## Overview
Provide a conservative language-neutral integration path through the CLI and Arrow/Parquet/CSV files. This supports R, Julia, SAS-adjacent workflows, Power Platform, notebooks, and institutional batch systems before native bindings are mature.

## Functional Requirements
- Define stable CLI commands for batch calculation and validation.
- Support Arrow/Parquet as preferred interchange and CSV as compatibility input/output.
- Emit structured diagnostics and provenance metadata.
- Add examples for shell, notebooks, and data-pipeline use.

## Acceptance Criteria
- CLI input/output contracts are versioned and documented.
- Golden fixtures validate file-based round trips.
- Docs explain when to use file interop instead of native bindings.
