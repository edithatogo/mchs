# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `conda-forge` for existing `nwau-py` publication.
    - [x] Capture registry URL/API response or absence evidence.
    - [x] Compare discovered version against `0.2.2`.
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

- [x] Task: Submit to `conda-forge` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR.
    - [x] Capture submission URL, version, owner, and review state.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md).

## Phase 4: Publication Evidence

- [~] Task: Verify external publication. Pending conda-forge acceptance.
    - [x] Query public registry after propagation. 2026-07-03 Anaconda API query still returns 404 for `conda-forge/nwau-py`; conda-forge noarch repodata contains no `nwau-py` entries. `1597c33`
    - [x] Record immutable URL/API response/checksum.
    - [ ] Mark track complete only if publication or accepted-review evidence exists. Publication is not claimed; PR #33452 checks are green at `bffc5bf1a85389dc695adfd96c87bf2413f4db25` and maintainer review/merge remain pending.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md). Pending publication evidence.
