# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `Maven Central` for existing `io.github.edithatogo:mchs-jvm-bindings` publication.
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
    - [x] Run Central Portal POM metadata validation.
    - [x] Generate binary, sources, and javadoc jars locally.
    - [x] Add a fail-closed readiness report for namespace, publisher credential, and PGP signing gates.
- [x] Task: Conductor - Automated Review and Checkpoint 'Preparation' (Protocol in workflow.md)

## Phase 3: Submission

- [ ] Task: Submit to `Maven Central` using an authenticated publisher workflow. Namespace is verified and Publisher API upload works; blocked by Central public-key discovery, release, and public metadata propagation.
    - [x] Use dry-run or validation mode first where available.
    - [x] Confirm `checkSigningConfiguration` fails closed without signing credentials, so release mode cannot be mistaken for a credential-free publish.
    - [ ] Publish or open the required upstream PR. Pending Central validation success and release.
    - [x] Capture submission URL, version, owner, and review state. Maven metadata URL returned HTTP 404/no publication again on 2026-06-12; Publisher API deployments `89d0d2a9-91c6-4994-9f8e-fdd34bb501d0`, `fccefc51-9ccb-4466-8f85-8a47bc16cf3c`, and `7ced6d47-59ee-40fb-9c9b-09b1aa9f8491` uploaded successfully but failed validation because Central could not discover public key `BB03C82343A653EE44BD5CDA9DF6B142F065199E`.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md). Blocked until Central validates the public key, then release and public metadata evidence are available.

## Phase 4: Publication Evidence

- [ ] Task: Verify external publication. Pending Maven Central release.
    - [x] Query public registry after propagation. Current metadata URL returned HTTP 404 on 2026-06-12.
    - [ ] Record immutable URL/API response/checksum. Pending publication.
    - [ ] Mark track complete only if publication or accepted-review evidence exists. Publication is not claimed.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md). Pending publication evidence.
