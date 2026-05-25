# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `vcpkg / ConanCenter` for existing `nwau-c-abi` publication.
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
    - [x] Re-run `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-c-abi/Cargo.toml` after `nwau-core@0.1.0` publication; verification now resolves `nwau-core` from crates.io and compiles `nwau-c-abi`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Preparation' (Protocol in workflow.md)

## Phase 2.5: C ABI packaging readiness hardening

- [ ] Task: Align C ABI version/source policy.
    - [ ] Decide whether package version and ABI version must match for `0.1.0`, or document package-version versus ABI-version semantics.
    - [ ] Align `Cargo.toml`, `nwau_abi.h`, Rust ABI constants, registry manifests, and release notes before tagging.
    - [ ] Create or nominate an immutable C ABI source tag and record required archive contents.
- [ ] Task: Convert local vcpkg scaffold into archive-ready port design.
    - [ ] Replace placeholder `REF` and `SHA512` values with immutable source metadata.
    - [ ] Add `supports` and usage expectations.
    - [ ] Define clean vcpkg validation commands and expected artifacts.
- [ ] Task: Convert local Conan scaffold into ConanCenter-ready recipe design.
    - [ ] Add `conandata.yml` source/checksum plan.
    - [ ] Add `test_package` expectation for a native C/C++ consumer.
    - [ ] Define CCI layout and local `conan create` validation expectations.
- [ ] Task: Document shared native consumer smoke test.
    - [ ] Include or link `nwau_abi.h`.
    - [ ] Link `nwau_c_abi`.
    - [ ] Call `nwau_abi_version_*` and `nwau_abi_status_message`.
    - [ ] Avoid clinical/private data fixtures.

## Phase 3: Submission

- [ ] Task: Submit to `vcpkg / ConanCenter` using upstream PR/review workflows. Dependency blocker resolved; portfile/recipe packaging remains.
    - [ ] Use dry-run or validation mode first where available.
    - [ ] Publish or open the required upstream PR.
    - [ ] Capture submission URL, version, owner, and review state.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md)

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication.
    - [ ] Query public registry after propagation.
    - [ ] Record immutable URL/API response/checksum.
    - [ ] Mark track complete only if publication or accepted-review evidence exists.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md)
