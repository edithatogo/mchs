# Specification: Coding-Set Version Registry

## Overview
Create a machine-readable registry for coding and classification sets used by IHACPA pricing years. This registry is the durable source of truth for version compatibility, pricing-year applicability, stream applicability, and licensing boundaries consumed by validation and classifier tracks.

The registry covers the classification families already called out in the project governance and validation matrix:
AR-DRG, AECC, UDG, Tier 2, AMHCC, ICD-10-AM, ACHI, and ACS.

## Functional Requirements
- Record coding-set names, versions, release dates, effective dates, applicable pricing years, stream applicability, licensing status, and source basis.
- Separate public metadata from restricted or locally supplied artifacts so licensed products are not redistributed by accident.
- Link pricing-year manifests and compatibility matrices to registry entries.
- Add validators that reject incompatible coding-set versions for a selected pricing year or stream.
- Document where users must obtain licensed classification products and what local-only inputs must never be committed.

## Non-Functional Requirements
- Do not redistribute licensed coding products unless permitted.
- Registry entries must distinguish public metadata from restricted code lists or groupers.
- Version compatibility must be explicit and testable.
- Registry records should be conservative and fail closed when the source basis or license boundary is unclear.

## Acceptance Criteria
- Registry includes all classification families currently relevant to the package.
- Pricing-year validators and classification input checks can resolve expected coding-set versions from the registry.
- Docs explain public versus licensed/restricted artifacts and the local-only handling rules for licensed products.
- Registry entries are consistent with the conservative year-by-year matrix already published in `classification_input_validation_20260512`.
