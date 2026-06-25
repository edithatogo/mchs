# Plan: Release Workflow Validation

## Phase 1: Workflow Audit
- [x] Task: Review workflow syntax and outputs.
    - [x] Check release tag/version outputs.
    - [x] Check coverage extraction.
    - [x] Check SBOM fallback.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Workflow Audit' (Protocol in workflow.md)

## Phase 2: Workflow Fixes
- [x] Task: Apply workflow fixes.
    - [x] Fix broken outputs.
    - [x] Fix invalid shell interpolation.
    - [x] Align release artefacts with evidence bundle schema.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Workflow Fixes' (Protocol in workflow.md)

## Phase 3: Validation
- [x] Task: Validate workflows.
    - [x] Run local YAML/static checks where possible.
    - [x] Record remaining GitHub-only validation.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Validation' (Protocol in workflow.md)
