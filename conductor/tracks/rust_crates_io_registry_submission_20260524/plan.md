# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `crates.io` for existing `nwau-core` publication.
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

- [ ] Task: Submit to `crates.io` using an authenticated publisher workflow. Manual workflow exists; blocked by token rotation and dispatch.
    - [x] Use dry-run or validation mode first where available.
    - [ ] Publish or open the required upstream PR. Pending dispatch of `.github/workflows/publish-registry-packages.yml` with `registry=cratesio` after token rotation.
    - [x] Capture submission URL, version, owner, and review state. `https://crates.io/api/v1/crates/nwau-core` returned crate absence; `cargo owner --list nwau-core` returned `no token found, please run cargo login`; GitHub secret `CARGO_REGISTRY_TOKEN` exists as of 2026-05-25T13:04:00Z; manual workflow exists.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md). Blocked until token rotation and crates.io workflow dispatch.

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication. Pending authenticated publication.
    - [ ] Query public registry after propagation. Current query returns no crate.
    - [ ] Record immutable URL/API response/checksum. Pending publication.
    - [ ] Mark track complete only if publication or accepted-review evidence exists. Publication is not claimed. Rotate the crates.io token before use because it passed through browser automation during setup.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md). Pending publication evidence.
