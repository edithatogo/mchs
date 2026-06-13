# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `Open VSX / Visual Studio Marketplace` for existing `mchs-tools` publication.
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

- [x] Task: Submit to `Open VSX / Visual Studio Marketplace` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [~] Publish refreshed extension packages after README correction. Open VSX workflow run https://github.com/edithatogo/mchs/actions/runs/27455601114 published `edithatogo.mchs-tools` v0.1.0 after namespace creation and OVSX_PAT configuration; Visual Studio Marketplace public gallery query returns `edithatogo.mchs-tools` v0.1.0. Version `0.1.1` now updates the packaged README; Open VSX workflow run https://github.com/edithatogo/mchs/actions/runs/27457810800 published `edithatogo.mchs-tools` v0.1.1, but public API propagation still returned v0.1.0 immediately afterward; Visual Studio Marketplace `0.1.1` republish is blocked until `VSCE_PAT` is configured.
    - [x] Capture submission URL, version, owner, and review state. Open VSX URL: https://open-vsx.org/extension/edithatogo/mchs-tools; Open VSX API returned version `0.1.0` with timestamp `2026-06-13T03:46:01.067824Z`; Visual Studio Marketplace returned publisher `edithatogo`, extension `mchs-tools`, version `0.1.0`, last updated `2026-06-12T12:04:06.657Z`.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md). Pending refreshed `0.1.1` publication evidence after README correction.

## Phase 4: Publication Evidence

- [~] Task: Verify external publication.
    - [~] Query public registry after propagation. Open VSX workflow evidence verifies `0.1.1` publication, but public API propagation still returned `0.1.0` immediately afterward. Visual Studio Marketplace verifies `0.1.0`; refreshed `0.1.1` Marketplace publication is pending `VSCE_PAT`.
    - [x] Record immutable URL/API response/checksum for `0.1.0`; record `0.1.1` after republish.
    - [ ] Mark track complete only after refreshed `0.1.1` publication evidence exists for the claimed registry surfaces.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md). Pending refreshed publication evidence.
