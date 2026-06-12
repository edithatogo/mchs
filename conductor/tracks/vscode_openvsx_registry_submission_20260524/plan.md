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

- [ ] Task: Submit to `Open VSX / Visual Studio Marketplace` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [ ] Publish or open the required upstream PR. Open VSX remains blocked by Eclipse OAuth Publisher Agreement completion and PAT creation; Visual Studio Marketplace is blocked by publisher/PAT access.
    - [x] Capture submission URL, version, owner, and review state. 2026-06-12 recheck rebuilt `integrations/vscode/mchs-tools-0.1.0.vsix` with SHA-256 `5ffcc870020787438e31e035e3a12fbea131f744d8647cd7d6367be7e05a717b`; `npx ovsx publish mchs-tools-0.1.0.vsix` reached the namespace PAT prompt for `edithatogo`; Open VSX still reports no Eclipse Foundation Open VSX Publisher Agreement attached. Eclipse account GitHub linking is present as `edithatogo`, but Open VSX requires Eclipse OAuth login to complete/sign the Publisher Agreement.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md)

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication.
    - [ ] Query public registry after propagation.
    - [ ] Record immutable URL/API response/checksum.
    - [ ] Mark track complete only if publication or accepted-review evidence exists.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md)
