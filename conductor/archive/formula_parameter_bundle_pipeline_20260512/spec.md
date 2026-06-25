# Specification: Formula and Parameter Bundle Pipeline

## Overview
Build a formal pipeline for extracting, normalizing, versioning, diffing, and validating future IHACPA formulae and parameters from official calculators, technical specifications, workbooks, and data tables.

## Evidence surfaces
- `reference-data/2026/manifest.yaml` records explicit source-only gaps for price-weight extraction, adjustment extraction, and publication-date uncertainty.
- `contracts/source-scanner/examples/add-year.draft-manifest.json` captures the synthetic add-year discovery contract and the price-weight gap in fixture form.
- `conductor/archive/reference_data_manifest_schema_20260512` defines the manifest shape this pipeline must satisfy.
- `conductor/tracks/end_to_end_validated_canary_20260512` depends on a formula and parameter bundle as part of the full lifecycle evidence package.

## Functional Requirements
- Define a versioned bundle format for formulas, weights, thresholds, adjustments, and stream-specific parameters.
- Add extraction steps from supported official formats such as SAS, Excel, CSV/XLSX tables, and manifest-linked artifacts.
- Add bundle provenance and validation evidence references.
- Add bundle loaders used by calculator modules instead of hidden globals.
- Add tests that compare bundle-loaded behavior to golden fixtures.

## Non-Functional Requirements
- Bundle changes must be reviewable and diffable.
- Formula representation must preserve traceability to source lines, sheets, or tables where practical.
- Source-discovered gaps must remain explicit until fixture evidence closes them.
- New bundles must remain unvalidated until fixture evidence passes.

## Acceptance Criteria
- At least one stream/year can load parameters from a versioned bundle.
- Bundle diffs identify formula and parameter changes.
- Docs explain how to add a future IHACPA release from source discovery through validation.
