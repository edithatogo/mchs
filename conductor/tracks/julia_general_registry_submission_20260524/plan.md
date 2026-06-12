# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `General registry` for existing `NationalWeightedActivityUnitWrapper` publication.
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

- [x] Task: Submit to `General registry` using an authenticated publisher workflow. Replacement registry PR submitted, merged, and registry files verified.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR. Registrator opened replacement General PR `https://github.com/JuliaRegistries/General/pull/156254`.
    - [x] Capture submission URL, version, owner, and review state. PR merged on 2026-05-28T15:34:44Z after registry consistency, treecheck, AutoMerge, and AutoMerge-stopwatch checks passed. Superseded PRs are closed, and the reviewer `[noblock]` nation-scope clarification was answered for Australia's NWAU context.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md).

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation. JuliaHub still returns 404, but Julia General raw registry files return HTTP 200.
    - [x] Record immutable URL/API response/checksum. General PR `https://github.com/JuliaRegistries/General/pull/156254`; repository `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`; tag `v0.1.0`; commit `56ddec5ae29513e80717d4625f82c024a211c949`; UUID `58dad789-f56a-4ab3-a66f-c15139bf9cbe`; registry git-tree-sha1 `bb22d4bd44689549064bd441092fd540b5d852cf`.
    - [x] Mark track complete only after General registry PR/merge evidence exists. Publication is claimed from merged General registry raw-file evidence.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md).
