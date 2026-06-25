# Plan: Generated Artifact Retention Policy

## Phase 1: Artifact Classes

- [x] Task: Define retention classes.
    - [x] Define source, generated-ignore, release-attachment, evidence-allowed, external-archive, and local-only.
    - [x] Map known build outputs and package artifacts to the classes.
    - [x] Define requirements for evidence artifacts.
- [x] Task: Conductor - User Manual Verification 'Artifact Classes' (Protocol in workflow.md)

## Phase 2: Validation Policy

- [x] Task: Add blocked pattern coverage.
    - [x] Block tracked cache and build directories.
    - [x] Block unmanaged browser logs and temporary package outputs.
    - [x] Allow explicitly owned evidence artifacts.
- [x] Task: Conductor - User Manual Verification 'Validation Policy' (Protocol in workflow.md)

## Phase 3: Reconciliation

- [x] Task: Reconcile current artifacts.
    - [x] Classify Power Platform exports and evidence files.
    - [x] Classify VSIX, MATLAB, Stata, and other package artifacts.
    - [x] Record cleanup or retention follow-up for each artifact class.
- [x] Task: Conductor - User Manual Verification 'Reconciliation' (Protocol in workflow.md)
