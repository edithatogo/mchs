# JVM Maven Central Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Kotlin/Scala/JVM`
- Registry: `Maven Central`
- Package candidate: `io.github.edithatogo:mchs-jvm-bindings`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/bindings/jvm`
- Current status: `prepared_namespace_verified_pending_central_portal_credentials_signing_upload_and_release`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally. A private Gradle/Kotlin JVM package candidate builds successfully with `gradle -p bindings/jvm validateCentralPortalReadiness build`. The Sonatype Central Portal namespace `io.github.edithatogo` is verified. The remaining blockers are Central Portal publisher credentials, in-memory PGP signing key/password, keyserver/public-key discoverability, authenticated upload/release, and public Maven metadata evidence.

## Preparation Evidence

- Public registry discovery: Maven Central metadata probe for `io.github.edithatogo:mchs-jvm-bindings` returned HTTP 404/no publication.
- Build command: `gradle -p bindings/jvm validateCentralPortalReadiness build`
- Build result: `BUILD SUCCESSFUL`
- POM validation: `checkPomFileForMavenPublication` passed with required developer email/organization and SCM connection metadata.
- Generated artifacts: binary jar, sources jar, javadoc jar, Maven POM, and Gradle module metadata.
- Namespace verification: Sonatype Central Portal shows `io.github.edithatogo` as Verified after public GitHub repository verification with key `f7fztfn9vz`.
- Upload bundle: `build/mchs-jvm-bindings-0.1.0-central-bundle.zip` was generated with jar, sources jar, javadoc jar, POM, Gradle module metadata, signatures, and checksum sidecars; SHA-256 `d0024c9f97b6cc23081139948a6b22508b5a06e20f96b75dc9b07082d2e56f42`.
- Signing validation: local GPG signatures verify with key `9DF6B142F065199E` / `BB03C82343A653EE44BD5CDA9DF6B142F065199E` for `Dylan Mordaunt <d.a.mordaunt@gmail.com>`; supported keyserver upload now returns success and a clean temporary keyring can receive the key from `hkps://keyserver.ubuntu.com`, but Central validation still cannot discover the key by fingerprint.
- Local fix: Kotlin JVM toolchain lowered to Java 11 to match installed local JDK.
- Remaining external blocker: Central Portal publisher credentials, in-memory PGP signing key/password, keyserver/public-key discoverability, authenticated upload/release, and public metadata propagation.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
