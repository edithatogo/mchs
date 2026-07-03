# Plan: IHACPA Source/License Audit Automation

## Phase 1: Draft Package Contract
- [~] Task: Define the review-only audit package shape and renderers.
    - [~] Add failing tests for the audit package, track scaffold text, and GitHub issue draft.
    - [ ] Verify the outputs do not embed restricted assets or overclaim validation.
    - [ ] Keep the scanner manifest as the source of truth for draft generation.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Draft Package Contract' (Protocol in workflow.md)

## Phase 2: CLI Integration and Docs
- [ ] Task: Add the audit package CLI surface and reusable writers.
    - [ ] Expose the audit package through the installed `funding-calculator` entrypoint.
    - [ ] Update source-scanner contract fixtures or docs to mention the audit package workflow.
    - [ ] Preserve review-only behavior for licensed or restricted source material.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: CLI Integration and Docs' (Protocol in workflow.md)
