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
    - [x] Publish refreshed extension packages after README correction. Open VSX workflow run https://github.com/edithatogo/mchs/actions/runs/27455601114 published `edithatogo.mchs-tools` v0.1.0 after namespace creation and OVSX_PAT configuration. Version `0.1.1` updates the packaged README; Open VSX workflow run https://github.com/edithatogo/mchs/actions/runs/27457810800 published `edithatogo.mchs-tools` v0.1.1, and the public Open VSX API verifies `0.1.1` with timestamp `2026-06-13T05:28:35.187880Z`. Visual Studio Marketplace `0.1.1` was uploaded manually through the publisher portal and the public Gallery API now verifies `0.1.1`.
    - [x] Capture submission URL, version, owner, and review state. Open VSX URL: https://open-vsx.org/extension/edithatogo/mchs-tools; Open VSX API returned version `0.1.0` with timestamp `2026-06-13T03:46:01.067824Z`; Visual Studio Marketplace returned publisher `edithatogo`, extension `mchs-tools`, version `0.1.0`, last updated `2026-06-12T12:04:06.657Z`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md).

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation. Open VSX public API verifies `0.1.1`. Visual Studio Marketplace Gallery API verifies `0.1.1` with VSIX SHA-256 `1d20feaa22e66978d5259dfb7b83467ed803a776d3fcb101792f2f164a2807ad`.
    - [x] Record immutable URL/API response/checksum for `0.1.1`.
    - [x] Mark track complete only after refreshed `0.1.1` publication evidence exists for the claimed registry surfaces.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md).
