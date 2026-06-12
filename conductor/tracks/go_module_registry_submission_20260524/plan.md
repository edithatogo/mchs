# Implementation Plan

## Phase 1: Discovery

- [x] Task: Query `Go module proxy/pkg.go.dev` for existing module publication.
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

- [x] Task: Submit to `Go module proxy/pkg.go.dev` using an authenticated publisher workflow.
    - [x] Use dry-run or validation mode first where available.
    - [x] Publish or open the required upstream PR. Go module proxy lists `v0.1.0`.
    - [x] Capture submission URL, version, owner, and review state. `https://proxy.golang.org/github.com/edithatogo/mchs/bindings/go/@v/list` returns `v0.1.0`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Submission' (Protocol in workflow.md).

## Phase 4: Publication Evidence

- [x] Task: Verify external publication.
    - [x] Query public registry after propagation. Go module proxy returns `v0.1.0`.
    - [x] Record immutable URL/API response/checksum for the Go module proxy.
    - [x] Mark track complete only if pkg.go.dev indexing or equivalent final publication evidence exists. pkg.go.dev exposes version `0.1.0`.
- [x] Task: Conductor - Automated Review and Checkpoint 'Publication Evidence' (Protocol in workflow.md).
