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

- [x] Task: Submit to `NuGet` using an authenticated publisher workflow. Workflow dispatch succeeded; public listing pending.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR. `.github/workflows/publish-registry-packages.yml` was dispatched with `registry=nuget` in run `https://github.com/edithatogo/mchs/actions/runs/26404217645`.
    - [x] Capture submission URL, version, owner, and review state. NuGet returned `Created` and `Your package was pushed`; public flat-container still returned 404 after the initial propagation wait.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md). Submission completed; public listing verification pending.

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication. Pending NuGet validation/indexing propagation.
    - [ ] Query public registry after propagation. Current flat-container query still returns 404.
    - [x] Record immutable URL/API response/checksum. Workflow run `26404217645` succeeded and NuGet API accepted the package upload.
    - [ ] Mark track complete only if publication or accepted-review evidence exists. Publication is not claimed.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md). Pending publication evidence.
