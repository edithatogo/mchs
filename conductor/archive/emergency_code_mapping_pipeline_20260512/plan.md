# Plan: Emergency Code Mapping Pipeline

## Scope Notes
- Limit work to versioned mapping bundles, provenance metadata, registry-gated applicability, validation surfaces, and documentation.
- Do not invent a UDG-to-AECC crosswalk or imply that one exists without explicit source evidence.
- Treat licensing on source manuals and mapping tables as a first-class constraint; capture provenance and license caveats rather than redistributing restricted content.
- Keep completion contingent on observable evidence in the repository.
- Keep the track metadata aligned with the governing fields: primary contract, dependencies, completion evidence, publication status, validation status, licensing caveats, and evidence surfaces.

## Phase 1: Mapping Bundle Schema
- [x] Task: Normalize the track metadata and index entry.
    - [x] Add the explicit primary contract, transition-registry dependency, completion evidence, publication status, validation status, licensing caveats, and evidence surfaces.
    - [x] Ensure the index summary mirrors the same governance fields without implying unsupported production mapping.
- [x] Task: Define emergency mapping-bundle schema and provenance fields.
    - [x] Include explicit source-field names, target classification family, table version, pricing years, checksums, provenance, and validation status.
    - [x] Define unknown, unmapped, deprecated, invalid, and era-incompatible diagnostics.
    - [x] Record the required local official or locally validated mapping reference fields.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Mapping Bundle Schema' (Protocol in workflow.md)

## Phase 2: Mapping Engine and Tests
- [x] Task: Implement table-driven emergency mapping and diagnostics.
    - [x] Add tests for mapped, unmapped, invalid, deprecated, unknown, and incompatible-year cases.
    - [x] Preserve raw and mapped fields for audit output.
    - [x] Enforce no-invented-crosswalk behavior when a bundle row or declared reference is missing.
    - [x] Link mapping selection to the UDG/AECC transition registry without inferring era boundaries.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Mapping Engine and Tests' (Protocol in workflow.md)

## Phase 3: Documentation
- [x] Task: Document emergency mapping workflow and future-table onboarding.
    - [x] Include dry-run data-quality review examples.
    - [x] Clarify when official or locally validated mapping sources are required.
    - [x] Document mapping-bundle semantics, source fields, and registry linkage.
    - [x] Describe validation surfaces and the no-invented-crosswalk caveat.
    - [x] Include the licensing caveats and evidence surfaces required before the track can be considered complete.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation' (Protocol in workflow.md)
