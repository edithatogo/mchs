# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `Open VSX / Visual Studio Marketplace` for existing `mchs-tools` publication.
    - [x] Capture registry URL/API response or absence evidence. Open VSX returned HTTP 404 `Extension not found` from `https://open-vsx.org/api/edithatogo/mchs-tools` with `Accept: application/json` on 2026-05-26; Visual Studio Marketplace returned HTTP 404 for the item page and 0 extensions from Gallery `extensionquery`. The earlier Open VSX HTTP 406 was a probe-header issue, not publication evidence.
    - [x] Compare discovered version against `0.1.0`.
    - [x] Update `language-registry-submissions.contract.json` status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Discovery' (Protocol in workflow.md)

## Phase 2: Preparation

- [x] Task: Prepare registry-specific package metadata.
    - [x] Confirm package name, ownership, license, README, keywords, repository URL, and support policy.
    - [x] Remove placeholder/example/private flags that block publication.
    - [x] Replace scaffold-only helper behavior with concrete VS Code commands for registry-gate status, contract navigation, roadmap navigation, and gated publish-command copying.
    - [x] Build the package artifact using the registry-native pack command.
    - [x] Capture checksum/SBOM/provenance where supported.
- [x] Task: Conductor - Automated Review and Checkpoint 'Preparation' (Protocol in workflow.md)

## Phase 3: Submission

- [x] Task: Assemble Open VSX and Visual Studio Marketplace access steps.
    - [x] Create a track-local access checklist with the agreement, publisher, token, and publish steps.
    - [x] Link the shared runbook back to the track-local checklist.
- [x] Task: Submit to `Open VSX / Visual Studio Marketplace` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR. Visual Studio Marketplace is published and public; Open VSX API also returns `edithatogo.mchs-tools` version `0.1.0`.
    - [x] Capture submission URL, version, owner, and review state. Chrome evidence on 2026-06-13 showed Open VSX Access Tokens available for `edithatogo`; a fresh token was generated, `ovsx publish` returned that `edithatogo.mchs-tools 0.1.0` is already published, the public Open VSX API verified version `0.1.0`, and the fresh token was deleted afterwards.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md)

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation. Visual Studio Marketplace Gallery API returns `edithatogo.mchs-tools` version `0.1.1`; Open VSX API returns `edithatogo/mchs-tools` latest version `0.1.1` and still exposes version `0.1.0` in `allVersions`.
    - [x] Record immutable URL/API response/checksum for both publications.
    - [x] Mark track complete only if both required destinations are published or the remaining Open VSX destination is explicitly rescoped.
- [x] Follow-up: synchronize latest Visual Studio Marketplace publication.
    - [x] Prepare the local `mchs-tools-0.1.1.vsix` Marketplace-sync artifact.
    - [x] Confirm the Marketplace publisher surface exposes version `0.1.1`.
    - [x] Re-query Marketplace Gallery API and update evidence once both destinations expose latest version `0.1.1`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md)
