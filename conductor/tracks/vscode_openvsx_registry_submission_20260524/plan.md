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
    - [x] Publish to Open VSX and Visual Studio Marketplace. Open VSX workflow run https://github.com/edithatogo/mchs/actions/runs/27455601114 published `edithatogo.mchs-tools` v0.1.0 after namespace creation and OVSX_PAT configuration; Visual Studio Marketplace public gallery query returns `edithatogo.mchs-tools` v0.1.0.
    - [x] Capture submission URL, version, owner, and review state. Open VSX URL: https://open-vsx.org/extension/edithatogo/mchs-tools; Open VSX API returned version `0.1.0` with timestamp `2026-06-13T03:46:01.067824Z`; Visual Studio Marketplace returned publisher `edithatogo`, extension `mchs-tools`, version `0.1.0`, last updated `2026-06-12T12:04:06.657Z`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md). Evidence-only closure: public registry probes confirm publication; no generated VSIX artifact is committed.

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation.
    - [x] Record immutable URL/API response/checksum.
    - [x] Mark track complete only if publication or accepted-review evidence exists.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md).
