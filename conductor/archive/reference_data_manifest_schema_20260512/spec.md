# Specification: Reference Data Manifest Schema

## Overview
Define a machine-readable manifest schema for each IHACPA pricing year so formulae, parameters, source files, coding-set versions, and validation status can be incorporated consistently over time.

## Functional Requirements
- Add a versioned manifest format under `reference-data/<year>/manifest.yaml` or an equivalent canonical path.
- Represent source artifacts with URLs, local paths, publication dates, retrieval dates, hashes, and license/provenance notes.
- Represent NEP/NEC constants, stream price weights, adjustment parameters, coding-set versions, and validation status.
- Add typed Python models for loading and validating manifests.
- Document the lifecycle from `source-discovered` to `validated`.

## Non-Functional Requirements
- Manifest validation must be strict and deterministic.
- Missing artifacts must be represented as explicit gaps, not silently omitted.
- Schema evolution must be versioned.

## Acceptance Criteria
- Example manifests exist for pinned years `2026` and `2025`; do not rely on
  time-relative "current year" wording in tests or docs.
- Invalid manifests fail with actionable diagnostics.
- Docs explain required fields and validation statuses.
