# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `General registry` for existing `NwauCore` publication.
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

- [x] Task: Submit to `General registry` using an authenticated publisher workflow. Registry PR submitted; review feedback answered.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR. Registrator opened replacement General PR `https://github.com/JuliaRegistries/General/pull/156236`.
    - [x] Capture submission URL, version, owner, and review state. PR is open; registry consistency and treecheck passed. README/naming feedback was answered with a `[noblock]` PR comment after adding README documentation in package repo commit `f42f440`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md). Pending General merge; if reviewers require the README update inside the tagged registration payload, re-registration is needed.

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication. Pending General merge and registry propagation.
    - [x] Query public registry after propagation. Current JuliaHub query returns 404 Not Found.
    - [x] Record immutable URL/API response/checksum. General PR `https://github.com/JuliaRegistries/General/pull/156236`; repository `https://github.com/edithatogo/NwauCore.jl`; tag `v0.1.0`; README update commit `f42f440`; review response `https://github.com/JuliaRegistries/General/pull/156236#issuecomment-4534757948`.
    - [ ] Mark track complete only after General registry PR/merge evidence exists. Publication is not claimed.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md). Pending publication evidence.
