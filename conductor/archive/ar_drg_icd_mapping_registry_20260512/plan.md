# Plan: AR-DRG ICD/ACHI/ACS Mapping Registry

## Phase 1: Contract and Relationship Model
- [x] Task: Define the registry contract for ICD-10-AM, ACHI, ACS, and AR-DRG version relationships.
    - [x] State the required metadata fields for code family, version, effective period, and pricing-year applicability.
    - [x] Separate public metadata, locally supplied licensed assets, and derived validation fixtures.
    - [x] Mark unsupported or ambiguous relationships as fail-closed cases.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Contract and Relationship Model' (Protocol in workflow.md)

## Phase 2: Registry Records and Compatibility Validation
- [x] Task: Add registry records and compatibility validation for admitted acute coding sets.
    - [x] Test compatible and incompatible ICD-10-AM, ACHI, ACS, and AR-DRG version combinations.
    - [x] Add local-path placeholders for licensed mapping assets without committing restricted content.
    - [x] Record the source basis for each compatibility rule and reject missing provenance.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Registry Records and Compatibility Validation' (Protocol in workflow.md)

## Phase 3: Documentation and Governance Notes
- [x] Task: Document AR-DRG derivation metadata and user-supplied table requirements.
    - [x] Explain why AR-DRG is version-specific and derived from ICD-10-AM/ACHI/ACS coded data.
    - [x] Link admitted acute validation to the expected coding-set version set and local file requirements.
    - [x] Call out the licensing boundary for any table families that must remain local-only.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Documentation and Governance Notes' (Protocol in workflow.md)
