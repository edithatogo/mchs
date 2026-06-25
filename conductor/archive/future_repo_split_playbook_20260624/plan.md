# Plan: Future Repo Split Playbook

## Phase 1: Eligibility Model

- [x] Task: Define split criteria.
    - [x] Require registry or maintenance evidence that a split is beneficial.
    - [x] Require stable shared contracts and release boundaries.
    - [x] Reject splits that only hide incomplete scaffold work.
- [x] Task: Conductor - User Manual Verification 'Eligibility Model' (Protocol in workflow.md)

## Phase 2: Extraction Procedure

- [x] Task: Define history-preserving extraction.
    - [x] Prefer `git subtree split` for path-based extraction.
    - [x] Preserve tags, license, README, CI, package manifest, and registry metadata.
    - [x] Add compatibility tests against shared contracts.
- [x] Task: Conductor - User Manual Verification 'Extraction Procedure' (Protocol in workflow.md)

## Phase 3: Continuity and Rollback

- [x] Task: Define post-split continuity.
    - [x] Preserve package names and version lineage.
    - [x] Update docs, registry metadata, and support status.
    - [x] Define rollback if CI or publication proof fails.
- [x] Task: Conductor - User Manual Verification 'Continuity and Rollback' (Protocol in workflow.md)
