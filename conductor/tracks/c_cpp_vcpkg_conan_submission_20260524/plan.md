# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `vcpkg / ConanCenter` for existing `nwau-c-abi` publication.
    - [x] Capture registry URL/API response or absence evidence.
    - [x] Compare discovered version against `0.1.0`.
    - [x] Update `language-registry-submissions.contract.json` status.
- [x] Task: Conductor - Automated Review and Checkpoint 'Discovery' (Protocol in workflow.md)

## Phase 2: Preparation

- [x] Task: Prepare registry-specific local/private preview package metadata.
    - [x] Confirm package name, ownership, license, README, keywords, repository URL, and support policy.
    - [x] Remove placeholder-only wording while preserving private-preview and publication gates.
    - [x] Build the C ABI package artifact with Cargo packaging verification.
    - [x] Capture checksum/SBOM/provenance where supported.
    - [x] Re-run `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-c-abi/Cargo.toml` after `nwau-core@0.1.0` publication; verification now resolves `nwau-core` from crates.io and compiles `nwau-c-abi`.
    - [x] Run `conan inspect packaging/conan/conanfile.py` and `conan create packaging/conan --build=missing`; Conan packages the exported C ABI sources locally.
    - [x] Run `python -m json.tool packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`; vcpkg manifest JSON parses locally.
    - [x] Bootstrap vcpkg under `/tmp/mchs-vcpkg-validation` and run overlay install for `nwau-c-abi:arm64-osx`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Preparation' (Protocol in workflow.md)

## Phase 3: Submission

- [x] Task: Assemble vcpkg and ConanCenter upstream PR steps.
    - [x] Create a track-local upstream PR checklist with the vcpkg version update and ConanCenter `conandata.yml` requirements.
    - [x] Link the shared runbook back to the track-local checklist.
- [ ] Task: Submit to `vcpkg / ConanCenter` using upstream PR/review workflows. Dependency blocker resolved; Conan create and vcpkg overlay-port validation pass locally.
    - [x] Use dry-run or validation mode first where available.
    - [x] Run vcpkg overlay-port validation in an environment with vcpkg installed.
    - [x] Open the vcpkg PR and capture the upstream policy outcome: `https://github.com/microsoft/vcpkg/pull/51965` closed unmerged because vcpkg does not currently support Rust library ports.
    - [x] Open the ConanCenter PR and capture review state: `https://github.com/conan-io/conan-center-index/pull/30262` is open after portability fixes.
    - [ ] Complete the ConanCenter CLA/recheck gate and wait for job scheduler/maintainer review.
    - [ ] Revisit vcpkg only if upstream Rust-library support appears or the C ABI distribution design changes.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md)

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication.
    - [ ] Query public registry after propagation.
    - [ ] Record immutable URL/API response/checksum.
    - [ ] Mark track complete only if publication or accepted-review evidence exists.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md)
