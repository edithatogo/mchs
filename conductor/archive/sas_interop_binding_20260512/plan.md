# Plan: SAS Interoperability

## Phase 1: Governance Reclassification
- [x] Task: Reclassify SAS interoperability as private/no-new-development.
    - [x] Confirm no public SAS adapter surface exists in the repository.
    - [x] Keep existing local SAS-read workflows out of this track's public
      development scope.
    - [x] Record private/local reference-comparison policy in
      [`binding_strategy.md`](./binding_strategy.md).
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Governance Reclassification' (Protocol in workflow.md)
    [checkpoint: policy]

## Phase 2: Evidence and Validation
- [x] Task: Add explicit validation guardrails for the private SAS surface.
    - [x] Require comparison evidence to be synthetic or local/licensed.
    - [x] Block public adapter-readiness and publication claims.
    - [x] Keep proprietary SAS formula logic out of new code and docs.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Evidence and Validation' (Protocol in workflow.md)
    [checkpoint: validation]
