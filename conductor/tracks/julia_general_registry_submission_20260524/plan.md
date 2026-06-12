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

- [x] Task: Submit `NationalWeightedActivityUnitWrapper` to `General registry` using an authenticated publisher workflow. Superseded `NwauCore` registry PR #156236 is retained as evidence but is not expected to merge.
    - [x] Use dry-run or validation mode first where available.
    - [x] Open the required upstream PR for `NationalWeightedActivityUnitWrapper`: `https://github.com/JuliaRegistries/General/pull/156254`.
    - [x] Capture active submission evidence: repository `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`; trigger issue `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1`; tag `v0.1.0`; commit `56ddec5ae29513e80717d4625f82c024a211c949`; PR head `bb63b2a81ec2ded2c5675f09fb6cd63128f10a07`; UUID `58dad789-f56a-4ab3-a66f-c15139bf9cbe`; checks successful.
    - [x] Capture superseded submission URL, version, owner, and review state. PR `https://github.com/JuliaRegistries/General/pull/156236` is open; registry consistency and treecheck passed. README/naming feedback was answered, then reviewer follow-up accepted abandoning `NwauCore` and re-registering as `NationalWeightedActivityUnitWrapper`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md). General PR #156254 merged successfully and publication is verified.

## Phase 4: Publication Evidence

- [x] Task: Verify external publication. General PR #156254 merged and the registry publication is verified.
    - [x] Query public registry before replacement registration. Current JuliaHub query for `NationalWeightedActivityUnitWrapper` returned 404 Not Found at discovery time; superseded `NwauCore` also returned 404 Not Found.
    - [x] Record active PR evidence. General PR `https://github.com/JuliaRegistries/General/pull/156254`; repository `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`; trigger issue `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1`; tag `v0.1.0`; commit `56ddec5ae29513e80717d4625f82c024a211c949`; PR head `bb63b2a81ec2ded2c5675f09fb6cd63128f10a07`; UUID `58dad789-f56a-4ab3-a66f-c15139bf9cbe`; checks successful; mergedAt `2026-05-28T15:34:44Z`.
    - [x] Record immutable superseded PR evidence. General PR `https://github.com/JuliaRegistries/General/pull/156236`; repository `https://github.com/edithatogo/NwauCore.jl`; tag `v0.1.0`; README update commit `f42f440`; review response `https://github.com/JuliaRegistries/General/pull/156236#issuecomment-4534757948`; rename response `https://github.com/JuliaRegistries/General/pull/156236#issuecomment-4534823787`; reviewer follow-up `https://github.com/JuliaRegistries/General/pull/156236#issuecomment-4534836505`.
    - [x] Mark track complete only after General registry merge/publication evidence exists. Publication is verified by the merged registry PR.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md). Publication evidence is verified upstream.
