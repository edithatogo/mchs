# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `MATLAB File Exchange` for existing `mchs-matlab-interop` publication.
    - [x] Capture registry URL/API response or absence evidence.
    - [x] Compare discovered version against `0.1.0`.
    - [x] Update `language-registry-submissions.contract.json` status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Discovery' (Protocol in workflow.md)

## Phase 2: Preparation

- [x] Task: Prepare registry-specific package metadata.
    - [x] Confirm package name, ownership, license, README, keywords, repository URL, and support policy.
    - [x] Remove placeholder/example/private flags that block publication.
    - [x] Build the source upload artifact for manual File Exchange review.
    - [x] Capture checksum and archive contents evidence.
    - [x] Validate archive contents with focused regression coverage.
- [x] Task: Conductor - Automated Review and Checkpoint 'Preparation' (Protocol in workflow.md)

## Phase 3: Submission

- [ ] Task: Submit to `MATLAB File Exchange` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [ ] Publish or open the required upstream PR.
    - [x] Capture submission URL, version, owner, and review state.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md)

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication.
    - [ ] Query public registry after propagation.
    - [ ] Record immutable URL/API response/checksum.
    - [ ] Mark track complete only if publication or accepted-review evidence exists.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md)
