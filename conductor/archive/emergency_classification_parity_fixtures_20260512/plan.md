# Plan: Emergency Classification Parity Fixtures

## Phase 1: Fixture Schema
- [x] Task: Define emergency classification fixture schema and provenance fields.
    - [x] Include raw source fields, expected UDG/AECC, stream, pricing year, mapping version, transition-registry reference, fixture type, and expected NWAU-relevant outputs.
    - [x] Define synthetic versus local official fixture handling, local-only redaction rules, and provenance preservation for grouper-derived inputs.
- [x] Task: Normalize the track metadata and index summary.
    - [x] Set the explicit primary contract, dependency chain, completion evidence, publication status, validation status, licensing caveats, and evidence surfaces.
    - [x] Mirror the same governance fields in the index summary.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Governance Contract and Fixture Schema' (Protocol in workflow.md)

## Phase 2: Fixture Validation
- [x] Task: Add fixture loader and compatibility tests.
    - [x] Reject incompatible UDG/AECC, pricing-year, stream, mapping-version, and grouper-version combinations.
    - [x] Support precomputed, derived, and transition-period workflows only when registry and mapping provenance exists.
    - [x] Verify downstream emergency NWAU behavior for the declared pricing year.
    - [x] Preserve the no invented crosswalk rule and local-only licensed reference handling.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Fixture Validation' (Protocol in workflow.md)

## Phase 3: Documentation
- [x] Task: Document emergency classification fixture creation and validation workflow.
    - [x] Explain UDG-era, AECC-era, transition-year, mapping-dependent, and grouper-dependent fixture handling.
    - [x] Add safe synthetic examples and local-only licensed reference caveats.
    - [x] Summarize completion evidence and evidence surfaces.
    - [x] Describe validation surfaces: schema, compatibility, behavior, and docs checks.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation' (Protocol in workflow.md)
