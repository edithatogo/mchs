# Specification: Classification Mapping Registry Enrichment

## Overview
Enrich the public classification metadata available to the repository so the toolchain can reason about stream/year/classification compatibility without duplicating hardcoded matrices in multiple places. The registry must stay conservative: public metadata is allowed, licensed mapping content is not.

## Contract
- The registry must treat the classification stream, pricing year, expected version, required fields, and licensing boundary as first-class metadata.
- Compatibility checks must fail closed when a stream/year/classification combination is unsupported or mismatched.
- AR-DRG mapping hooks may describe local-only usage, but they must not redistribute grouping logic or proprietary table content.
- Public fixtures must remain loadable without licensed assets being present on disk.
- Docs and command-line output must make the AR-DRG derivation boundary explicit: precomputed DRG values or local licensed tooling are required for executable grouping, while the repo only records metadata and placeholders.

## Functional Requirements
- Provide a single shared source of truth for supported classification systems, required fields, streams, and year/version bindings.
- Surface public classification metadata for AR-DRG, AECC, UDG, Tier 2, and AMHCC.
- Provide fail-closed validation helpers for stream/year/version combinations.
- Provide local-only mapping hook placeholders for AR-DRG that validate structure but never bundle restricted content.
- Make the registry consumable from the CLI and library surface without requiring licensed assets.

## Non-Functional Requirements
- No proprietary mapping tables or grouping logic may be committed.
- Public metadata must remain machine-readable and deterministic.
- The registry should stay aligned with the existing classification validation helpers instead of introducing a parallel matrix.
- The new surface should be easy to extend when additional supported years are added.

## Acceptance Criteria
- The registry exposes public metadata for supported classification systems and the stream each one serves.
- Validation rejects incompatible stream/year/classification combinations.
- Local AR-DRG hook placeholders validate without requiring licensed file contents.
- Existing classification validation continues to use the shared source of truth.
- Documentation states that AR-DRG derivation depends on precomputed values or licensed local tooling, not bundled grouping logic.

## Out of Scope
- Redistributing ICD-10-AM, ACHI, ACS, or AR-DRG licensed tables.
- Implementing proprietary grouping logic.
- Loading or executing external licensed tooling.
- Adding new classification families beyond the current admitted acute, emergency, non-admitted, and mental-health surfaces.

## Source Evidence
- IHACPA admitted acute care: https://www.ihacpa.gov.au/health-care/classification/admitted-acute-care
- IHACPA AR-DRGs: https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system
- IHACPA emergency care classification pages:
  - https://www.ihacpa.gov.au/health-care/classification/emergency-care/aecc
  - https://www.ihacpa.gov.au/health-care/classification/emergency-care/udg
- IHACPA non-admitted care and mental health classifier pages are recorded in the existing repository guidance and remain metadata-only here.
