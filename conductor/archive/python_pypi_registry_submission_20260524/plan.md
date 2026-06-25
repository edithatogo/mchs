# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `PyPI` for existing `nwau-py` publication.
    - [x] Capture registry URL/API response or absence evidence. `https://pypi.org/project/nwau-py/0.2.2/` is the public package evidence.
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

- [x] Task: Submit to `PyPI` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR.
    - [x] Capture submission URL, version, owner, and review state. PyPI exposes `nwau-py 0.2.2`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md)

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation.
    - [x] Record immutable URL/API response/checksum.
    - [x] Mark track complete only if publication or accepted-review evidence exists. Publication is claimed from the public PyPI project/version URL.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md)
