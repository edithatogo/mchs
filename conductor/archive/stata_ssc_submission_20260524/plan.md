# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `SSC / Stata package distribution` for existing `mchs-stata-interop` publication.
    - [x] Capture registry URL/API response or absence evidence.
    - [x] Compare discovered version against `0.1.0`.
    - [x] Update `language-registry-submissions.contract.json` status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Discovery' (Protocol in workflow.md)

## Phase 2: Preparation

- [x] Task: Prepare registry-specific package metadata.
    - [x] Confirm package name, ownership, license, README, keywords, repository URL, and support policy.
    - [x] Remove placeholder/example/private flags that block publication.
    - [x] Build the ado/help/pkg review archive for SSC maintainer submission.
    - [x] Capture checksum and archive contents evidence.
    - [x] Validate archive contents with focused regression coverage.
- [x] Task: Conductor - Automated Review and Checkpoint 'Preparation' (Protocol in workflow.md)

## Phase 3: Submission

- [x] Task: Submit to `SSC / Stata package distribution` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR. Initial SSC email was sent to `baum@bc.edu`; maintainer feedback has been received.
    - [x] Capture submission URL, version, owner, and review state.
    - [x] Apply maintainer feedback locally. Added author/contact information to `mchs.sthlp` and rebuilt the SSC review archive.
    - [x] Do not send corrected archive: public SSC/RePEc installability evidence was captured before any approved corrected-archive follow-up was needed.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md)

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation.
    - [x] Record immutable URL/API response/checksum.
    - [x] Mark track complete only if publication or accepted-review evidence exists.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md)
