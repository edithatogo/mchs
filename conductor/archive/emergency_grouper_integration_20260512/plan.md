# Plan: Emergency Grouper Integration

## Phase 1: Governance Contract and Compatibility
- [x] Task: Define the emergency grouper interface, provenance model, and publication boundary.
    - [x] Support precomputed, command, service, and file-exchange modes.
    - [x] Resolve era selection and compatibility through `emergency_udg_aecc_transition_registry_20260512`.
    - [x] Describe how `emergency_code_mapping_pipeline_20260512` supplies versioned source-field mapping bundles.
    - [x] Record licensing caveats and evidence surfaces in the track summary.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Interface Design' (Protocol in workflow.md)

## Phase 2: Adapter Prototype and Validation
- [x] Task: Add a mock emergency classifier adapter and tests.
    - [x] Test success, unmapped, failed tool, and incompatible-version cases.
    - [x] Preserve input/output provenance records.
    - [x] Fail closed when registry, mapping, or license constraints are violated.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Adapter Prototype' (Protocol in workflow.md)

## Phase 3: Documentation and Publication Readiness
- [x] Task: Document emergency classifier workflows and local tool setup.
    - [x] Explain precomputed UDG/AECC versus package-mediated derivation.
    - [x] Include privacy and licensing caveats.
    - [x] Summarize completion evidence and evidence surfaces for review and publication tracking.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation' (Protocol in workflow.md)
