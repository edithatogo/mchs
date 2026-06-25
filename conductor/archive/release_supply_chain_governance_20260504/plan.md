# Plan: Release and Supply-Chain Governance

## Phase 1: Release Model [checkpoint: a00e550]

- [x] Task: Write checks for release metadata [a00e550]
    - [x] Validate package version, data bundle version, source checksum set, and validation status
    - [x] Validate evidence-backed parity records for release claims
    - [x] Record lockfile revision used for the build
    - [x] Verify release notes can identify calculator behavior changes
- [x] Task: Define release policy [a00e550]
    - [x] Distinguish code releases from data bundle releases
    - [x] Define when validation status changes require release notes
    - [x] Note dependency on the Python Tooling and CI Modernization track
- [x] Task: Conductor - User Manual Verification 'Release Model' (Protocol in workflow.md) [a00e550]

## Phase 2: Supply-Chain Controls [checkpoint: a00e550]

- [x] Task: Write CI checks for source and dependency integrity [a00e550]
    - [x] Verify source checksums before extraction
    - [x] Verify dependency lockfiles and pinned tool versions
    - [x] Ensure provenance manifests are read from the tracked location, not ignored raw storage
    - [x] Ensure locked installs are used in release validation
- [x] Task: Add supply-chain governance plan [a00e550]
    - [x] Define SBOM generation
    - [x] Define signed release artifacts
    - [x] Define Renovate package rules for calculator-impacting dependencies
- [x] Task: Conductor - User Manual Verification 'Supply-Chain Controls' (Protocol in workflow.md) [a00e550]
