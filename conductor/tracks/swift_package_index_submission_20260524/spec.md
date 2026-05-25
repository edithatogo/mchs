# Swift Package Index Submission

## Overview

Track discovery, local preparation, submission, and publication evidence for the Swift Package Index registry without overclaiming publication.

## Registry

- Ecosystem: `Swift`
- Registry: `Swift Package Index`
- Package candidate: `MCHSBind`
- Version candidate: `0.1.0`
- Local surface: `bindings/swift/Package.swift`
- Current status: `submitted_accepted_pending_spi_public_probe`

## Functional Requirements

- Query the public registry or authoritative submission system for existing package/version evidence.
- Record absence, submission, or publication evidence in the language registry contract.
- Prepare registry-specific metadata or artifacts only from committed package surfaces.
- Submit only through an authenticated, authorized publisher account or upstream review workflow.
- Keep external legal, credential, maintainer-review, and propagation blockers explicit.

## Current Blocker

Swift Package Index PackageList issue is closed as completed, repository publication metadata is fixed, but SPI public listing/version evidence is still blocked by public probe visibility.

## Evidence

- Submission URL: https://github.com/SwiftPackageIndex/PackageList/issues/13717
- Contract source: `contracts/language-registry-submissions/language-registry-submissions.contract.json`
- External gate roadmap: `docs/roadmaps/language-registry-external-gates.md`

## Acceptance Criteria

- Track context exists for the contract's `swift_package_index_submission_20260524` reference.
- Current status and blocker language match the checked-in language registry contract.
- Publication is claimed only when public registry evidence verifies the target version.

## Out of Scope

- Accepting CLAs, publisher agreements, or legal terms on behalf of a contributor.
- Inventing credentials, namespace ownership, API keys, or registry maintainer approval.
- Claiming publication from local artifacts alone.
