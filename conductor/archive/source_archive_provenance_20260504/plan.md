# Plan: Source Archive and Provenance Registry

## Phase 1: Manifest Contract [checkpoint: 23495cc]

- [x] Task: Write tests for archive manifest schema [23495cc]
    - [x] Validate required fields and status values
    - [x] Validate run context, schema version, and checksum algorithm fields
    - [x] Validate SHA-256 and byte-count handling
- [x] Task: Implement manifest schema helpers [23495cc]
    - [x] Add typed structures for source artifacts
    - [x] Add structured lifecycle fields for acquisition, extraction, implementation, and validation
    - [x] Add status normalization for IHACPA-hosted and Box-hosted assets
    - [x] Add a tracked provenance output path outside ignored raw storage
- [x] Task: Conductor - User Manual Verification 'Manifest Contract' (Protocol in workflow.md) [23495cc]

## Phase 2: Acquisition Workflow [checkpoint: 23495cc]

- [x] Task: Write tests for IHACPA page parsing [23495cc]
    - [x] Cover year grouping, Excel links, SAS links, and Box share links
    - [x] Use saved HTML fixtures rather than live network calls
- [x] Task: Harden archive acquisition script [23495cc]
    - [x] Add fixture-based parser tests
    - [x] Add checksum updates for existing local files and record verification state
    - [x] Capture acquisition command, script version, redirect chain, and source page snapshot metadata
    - [x] Add command documentation
- [x] Task: Conductor - User Manual Verification 'Acquisition Workflow' (Protocol in workflow.md) [23495cc]

## Phase 3: Storage Decision [checkpoint: 23495cc]

- [x] Task: Write storage policy checklist [23495cc]
    - [x] Compare Git LFS, GitHub release assets, and external object storage
    - [x] Define restore workflow, checksum verification, and manifest location
- [x] Task: Create final storage ADR [23495cc]
    - [x] Update ADR 0001 from proposed to accepted after decision
    - [x] Document how raw binaries are retrieved in CI or release workflows
- [x] Task: Conductor - User Manual Verification 'Storage Decision' (Protocol in workflow.md) [23495cc]
