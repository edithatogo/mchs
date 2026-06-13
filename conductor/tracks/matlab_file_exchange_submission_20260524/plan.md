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
    - [x] Build the package artifact using the registry-native pack command.
    - [x] Capture checksum/SBOM/provenance where supported.
- [x] Task: Conductor - Automated Review and Checkpoint 'Preparation' (Protocol in workflow.md)

## Phase 3: Submission

- [x] Task: Submit to `MATLAB File Exchange` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR. Public File Exchange listing verified at `https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop`.
    - [x] Capture submission URL, version, owner, and review state.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md)

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation. File Exchange page returned HTTP 200 on 2026-06-14.
    - [x] Record immutable URL/API response/checksum. URL and page title are recorded in the registry contract and metadata; bundle SHA-256 remains recorded.
    - [x] Mark track complete only if publication or accepted-review evidence exists.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md)
