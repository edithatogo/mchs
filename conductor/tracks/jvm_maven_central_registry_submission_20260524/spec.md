# JVM Maven Central Registry Submission

## Overview

Track discovery, local preparation, submission, and publication evidence for the Maven Central registry without overclaiming publication.

## Registry

- Ecosystem: `Kotlin/Scala/JVM`
- Registry: `Maven Central`
- Package candidate: `io.github.edithatogo:mchs`
- Version candidate: `0.1.0`
- Local surface: `bindings/jvm/build.gradle.kts`
- Current status: `jvm_module_build_verified_pending_central_namespace_signing_and_release`

## Functional Requirements

- Query the public registry or authoritative submission system for existing package/version evidence.
- Record absence, submission, or publication evidence in the language registry contract.
- Prepare registry-specific metadata or artifacts only from committed package surfaces.
- Submit only through an authenticated, authorized publisher account or upstream review workflow.
- Keep external legal, credential, maintainer-review, and propagation blockers explicit.

## Current Blocker

Minimal JVM module, Maven publishing metadata, credential-safe Central Portal repository wiring, and in-memory signing wiring are checked in and local build passed; namespace verification, signing key material, publish credentials, publish validation, and authenticated release remain pending.

## Evidence

- Submission URL: not applicable or not yet available.
- Contract source: `contracts/language-registry-submissions/language-registry-submissions.contract.json`
- External gate roadmap: `docs/roadmaps/language-registry-external-gates.md`

## Acceptance Criteria

- Track context exists for the contract's `jvm_maven_central_registry_submission_20260524` reference.
- Current status and blocker language match the checked-in language registry contract.
- Publication is claimed only when public registry evidence verifies the target version.

## Out of Scope

- Accepting CLAs, publisher agreements, or legal terms on behalf of a contributor.
- Inventing credentials, namespace ownership, API keys, or registry maintainer approval.
- Claiming publication from local artifacts alone.
