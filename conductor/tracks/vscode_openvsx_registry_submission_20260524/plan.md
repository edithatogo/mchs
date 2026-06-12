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
- [ ] Task: Submit to `Open VSX / Visual Studio Marketplace` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [ ] Publish or open the required upstream PR. Open VSX is blocked by Eclipse Foundation password login/agreement recognition and token creation; Visual Studio Marketplace publisher `edithatogo` exists with Owner role, but PAT creation and authenticated VSIX publish remain pending.
    - [x] Capture submission URL, version, owner, and review state. The user reports the Eclipse Foundation Open VSX Publisher Agreement is completed; Eclipse account `edithatogo` is now connected with GitHub account `edithatogo`, and Open VSX GitHub login succeeds. Open VSX Access Tokens still reports no signed Publisher Agreement and Log in with Eclipse reaches an Eclipse Foundation username/password prompt. Visual Studio Marketplace shows publisher `edithatogo` with Owner role and no uploaded extensions in the current Microsoft session.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md)

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication.
    - [x] Query public registry after propagation. The deterministic Open VSX and Visual Studio Marketplace public probes confirm `mchs-tools` is not listed.
    - [ ] Record immutable URL/API response/checksum.
    - [ ] Mark track complete only if publication or accepted-review evidence exists.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md)
