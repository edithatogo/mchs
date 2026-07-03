# Plan: IHACPA Source/License Audit Automation

## Phase 1: Draft Package Contract
- [x] Task: Define the review-only audit package shape and renderers.
    - [x] Add failing tests for the audit package, track scaffold text, and GitHub issue draft.
    - [x] Verify the outputs do not embed restricted assets or overclaim validation.
    - [x] Keep the scanner manifest as the source of truth for draft generation.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Draft Package Contract' (Protocol in workflow.md)

## Phase 2: CLI Integration and Docs
- [x] Task: Add the audit package CLI surface and reusable writers.
    - [x] Expose the audit package through the installed `funding-calculator` entrypoint.
    - [x] Update source-scanner contract fixtures or docs to mention the audit package workflow.
    - [x] Preserve review-only behavior for licensed or restricted source material.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: CLI Integration and Docs' (Protocol in workflow.md)
