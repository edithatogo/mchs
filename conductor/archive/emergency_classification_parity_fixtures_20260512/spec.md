# Specification: Emergency Classification Parity Fixtures

## Overview
Create a validation fixture strategy for emergency classification behavior across UDG and AECC versions. Fixtures should prove classification compatibility, allowed transition behavior, and downstream emergency NWAU behavior for pricing years.

## Contract
- This track owns the metadata-only parity fixture contract for emergency classification workflows.
- The track depends on `emergency_udg_aecc_transition_registry_20260512` for era selection and pricing-year applicability, `emergency_code_mapping_pipeline_20260512` for versioned source-field mapping bundles, and `emergency_grouper_integration_20260512` for precomputed or externally derived grouper-dependent workflows.
- The track does not define, redistribute, or license emergency source tables, mapping tables, or grouper outputs.
- The track does not invent a UDG-to-AECC crosswalk, equivalence class, or silent fallback path.

## Governance and Evidence
- Publication status: `not-ready`
- Validation status: `not-validated`
- Licensing caveats: do not embed or redistribute licensed UDG, AECC, mapping, or grouper tables unless the source license explicitly permits it; keep local official and user-supplied reference fixtures outside the repository unless they are synthetic or otherwise redistributable; do not imply a crosswalk or fallback mapping that the source evidence does not support.
- Evidence surfaces: `metadata.json`, `spec.md`, `plan.md`, `index.md`, fixture manifests and loader tests, fixture workflow documentation, and review notes.

## Functional Requirements
- Define fixture schema for raw emergency source fields, expected UDG/AECC classification, pricing year, stream, and expected NWAU-relevant outputs.
- Support synthetic fixtures and user-supplied official/local reference fixtures.
- Track mapping table version, classifier version, pricing year, transition-registry reference, and validation status.
- Add tests that reject cross-version fixture reuse unless a declared transition mapping exists.

## Non-Functional Requirements
- Synthetic fixtures must avoid restricted mapping-table content unless redistributable.
- Local official fixtures must remain local-only or redacted unless licensed for redistribution.
- Fixtures must support both precomputed classification and derived classification workflows.
- Fixture output must preserve provenance for source fields, mapping references, and any declared grouper-derived inputs.

## Acceptance Criteria
- Fixture schema captures UDG/AECC version, source mapping version, transition-registry reference, pricing year, and stream.
- Tests prevent using UDG fixtures in AECC-only years and vice versa unless a declared transition mapping exists.
- Docs explain safe fixture creation, local-only licensed fixture handling, and validation workflow.

## Source Evidence
- IHACPA AECC: https://www.ihacpa.gov.au/health-care/classification/emergency-care/aecc
- IHACPA UDG: https://www.ihacpa.gov.au/health-care/classification/emergency-care/udg
