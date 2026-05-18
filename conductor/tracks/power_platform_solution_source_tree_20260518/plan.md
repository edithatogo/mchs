# Plan: Power Platform Unpacked Solution Source Tree

## Phase 1: Solution Skeleton

- [x] Task: Initialize the solution source package
    - [x] Create solution metadata with unique name `mchs_alm_orchestration`
    - [x] Create publisher metadata
    - [x] Create environment variable and connection reference components
- [x] Task: Wire connector component into solution
    - [x] Include custom connector source assets
    - [x] Bind service endpoint via environment variable
    - [x] Bind auth via connection reference
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Solution Skeleton' (Protocol in workflow.md)

## Phase 2: Pack and Unpack Discipline

- [x] Task: Add pack/unpack scripts
    - [x] Use supported `pac solution pack` and `pac solution unpack` commands
    - [x] Separate unmanaged source from managed release artifact
    - [x] Ignore generated zip artifacts unless intentionally stored as release evidence
- [x] Task: Add structural checks
    - [x] Assert `Solution.xml` and `customizations.xml` exist after unpack
    - [x] Assert component names and versions match manifest
    - [x] Assert no formulas are embedded in app/flow assets
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Pack and Unpack Discipline' (Protocol in workflow.md)
