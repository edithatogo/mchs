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

- [x] Task: Submit to `Maven Central` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [x] Confirm `checkSigningConfiguration` fails closed without signing credentials, so release mode cannot be mistaken for a credential-free publish.
    - [x] Publish or open the required upstream PR. Publisher API deployment `5fb01ae9-2609-4284-9427-5830e08bcbb5` validated after keyserver propagation and was published with HTTP 204.
    - [x] Capture submission URL, version, owner, and review state. Maven metadata URL returned HTTP 200 and exposes `0.1.0`; public POM and JAR URLs return HTTP 200.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md).

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation. Current metadata URL returned HTTP 200 on 2026-06-12 and exposes latest/release/version `0.1.0`.
    - [x] Record immutable URL/API response/checksum. Public JAR SHA-256 is `2f499b78d06317fd9bf2e343542b74043f163f127cd32db4651098f6ac6af49e`; public POM SHA-256 is `367e6a08a9d57ebd6d97d9fa14f1fe65fbfdf7fce882369ab8264996995c36c6`.
    - [x] Mark track complete only if publication or accepted-review evidence exists. Publication is verified on repo1.maven.org.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md).
