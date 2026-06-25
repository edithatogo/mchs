# Specification: AR-DRG Version Parity Fixtures

## Overview
Create a validation fixture strategy for AR-DRG version-specific behavior. Because AR-DRGs vary by version and are derived from coded episode data, the project needs fixture sets that prove version-compatible behavior for admitted acute NWAU calculations and any grouper integration.

## Contract
- The track defines a fixture contract for coded admitted episode inputs, expected AR-DRG outputs, and NWAU-relevant outputs or inputs needed to prove parity across versions.
- The fixture contract must record coding-set version, AR-DRG version, grouper version, pricing year, provenance, and whether the fixture is synthetic or local-only licensed reference data.
- Synthetic fixtures may be committed when they stay illustrative and do not embed restricted code tables, manuals, or proprietary grouper outputs.
- Licensed or reference fixtures may be used only as local user-supplied artifacts or redacted references; they must not be committed, mirrored, or redistributed through the repository.
- The track governs validation and fixture boundaries only; it does not provide licensed product content or replace the user's own licensing obligations.

## Functional Requirements
- Define fixture schema for coded admitted episodes, expected AR-DRG, and expected NWAU inputs/outputs.
- Support synthetic fixtures and user-supplied licensed/reference fixtures.
- Track fixture provenance, coding-set version, grouper version, and pricing year.
- Add tests for version-specific changes and invalid cross-version reuse.

## Evidence Surfaces
- `metadata.json` records the track contract, current state, and completion evidence expectations.
- `spec.md` defines the fixture contract, provenance fields, and the synthetic versus local-licensed boundary.
- `plan.md` stages the schema, compatibility checks, and documentation evidence.
- Fixture manifests and loader tests demonstrate version checks, provenance capture, and rejection of incompatible reuse.
- Documentation demonstrates how maintainers add safe synthetic fixtures and reference local-only licensed fixtures without redistributing restricted content.

## Non-Functional Requirements
- Synthetic fixtures must not contain restricted code tables beyond permissible illustrative values.
- Reference fixtures derived from licensed products must be local-only or redacted unless redistributable.
- Fixtures must support both precomputed AR-DRG and external-grouper workflows.
- No committed fixture output may include proprietary grouper results, licensed code tables, or redistributable source extracts unless the source license explicitly allows it.

## Acceptance Criteria
- Fixture schema captures ICD-10-AM/ACHI/ACS version, AR-DRG version, grouper version, and pricing year.
- Tests prevent reusing fixtures with incompatible versions.
- Docs explain how maintainers add safe synthetic and local licensed fixtures.
- Docs explain how admitted acute NWAU behavior is validated without committing proprietary outputs.

## Caveats
- Synthetic fixtures are for contract and regression coverage only; they should not be mistaken for licensed clinical or classification source data.
- Any licensed reference fixture must remain on the user's machine or in another local-only path that is not committed to the repository.
- The repository may record provenance and path placeholders for local licensed fixtures, but it must not include restricted content or derived tables that would enable redistribution.
- If a fixture cannot be validated because a required licensed artifact is missing, the failure should identify the missing category without exposing restricted contents.

## Source Evidence
- IHACPA AR-DRGs: https://www.ihacpa.gov.au/admitted-acute-care/ar-drg-classification-system
- IHACPA AR-DRG Version 12.0: https://www.ihacpa.gov.au/resources/ar-drg-version-120
