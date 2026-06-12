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

- [x] Task: Submit to `crates.io` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available. `cargo publish --dry-run --allow-dirty --locked --manifest-path rust/crates/nwau-core/Cargo.toml` packaged and verified `nwau-core v0.1.0`, reached upload, then aborted because this was a dry run.
    - [x] Publish or open the required upstream PR. Public crates.io API verifies `nwau-core@0.1.0`.
    - [x] Capture submission URL, version, owner, and review state. `https://crates.io/api/v1/crates/nwau-core/0.1.0` reports version `0.1.0`, created `2026-05-25T13:59:23.536614Z`, checksum `c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547`, and `yanked=false`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md).

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation. `https://crates.io/api/v1/crates/nwau-core` reports newest version `0.1.0`.
    - [x] Record immutable URL/API response/checksum. Version API checksum is `c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547`.
    - [x] Mark track complete only if publication or accepted-review evidence exists. Publication is verified. Revoke or rotate the crates.io token because it passed through browser automation during setup.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md).
