# Plan: Power Platform Unpacked Solution Source Tree

## Phase 1: Solution Skeleton

- [ ] Task: Initialize the solution source package
    - [ ] Create solution metadata with unique name `mchs_alm_orchestration`
    - [ ] Create publisher metadata
    - [ ] Create environment variable and connection reference components
- [ ] Task: Wire connector component into solution
    - [ ] Include custom connector source assets
    - [ ] Bind service endpoint via environment variable
    - [ ] Bind auth via connection reference
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Solution Skeleton' (Protocol in workflow.md)

## Phase 2: Pack and Unpack Discipline

- [ ] Task: Add pack/unpack scripts
    - [ ] Use supported `pac solution pack` and `pac solution unpack` commands
    - [ ] Separate unmanaged source from managed release artifact
    - [ ] Ignore generated zip artifacts unless intentionally stored as release evidence
- [ ] Task: Add structural checks
    - [ ] Assert `Solution.xml` and `customizations.xml` exist after unpack
    - [ ] Assert component names and versions match manifest
    - [ ] Assert no formulas are embedded in app/flow assets
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Pack and Unpack Discipline' (Protocol in workflow.md)
