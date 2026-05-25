# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `NuGet` for existing `Mchs.Bindings.DotNet` publication.
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

- [ ] Task: Submit to `NuGet` using an authenticated publisher workflow. Manual workflow exists; blocked by dispatch.
    - [x] Use dry-run or validation mode first where available.
    - [ ] Publish or open the required upstream PR. Pending dispatch of `.github/workflows/publish-registry-packages.yml` with `registry=nuget`.
    - [x] Capture submission URL, version, owner, and review state. The flat-container URL returned 404 and no public version exists; GitHub secret `NUGET_API_KEY` exists as of 2026-05-25T13:34:49Z; manual workflow exists.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md). Blocked until NuGet workflow dispatch.

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication. Pending authenticated NuGet push.
    - [ ] Query public registry after propagation. Current flat-container query returns 404.
    - [ ] Record immutable URL/API response/checksum. Pending publication.
    - [ ] Mark track complete only if publication or accepted-review evidence exists. Publication is not claimed.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md). Pending publication evidence.
