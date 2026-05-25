# Rust crates.io Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Rust`
- Registry: `crates.io`
- Package candidate: `nwau-core`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/rust/crates/nwau-core/Cargo.toml`
- Current status: `prepared_pending_crates_token_and_cargo_publish`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally. `nwau-core` is package-ready and `cargo package --allow-dirty` verified successfully. The remaining blocker is external credentials: no crates.io token is available locally, and `cargo owner --list nwau-core` returned `no token found, please run cargo login`.

## Preparation Evidence

- Public registry discovery: `https://crates.io/api/v1/crates/nwau-core` returned crate absence evidence.
- Local package command: `cargo package --allow-dirty`
- Package result: `Packaged 16 files, 107.8KiB (25.2KiB compressed)`
- Verification result: `Compiling nwau-core v0.1.0` and `Finished dev profile`
- Remaining external blocker: crates.io authentication token is not configured.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
