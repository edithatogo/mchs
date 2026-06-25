# Rust crates.io Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Rust`
- Registry: `crates.io`
- Package candidate: `nwau-core`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/rust/crates/nwau-core/Cargo.toml`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Published and verified. `nwau-core` is package-ready, `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-core/Cargo.toml` verified successfully, `cargo publish --dry-run --allow-dirty --locked --manifest-path rust/crates/nwau-core/Cargo.toml` reached the dry-run upload abort, and the public crates.io API verifies `nwau-core@0.1.0`. The browser-created publish token was revoked and the GitHub Actions `CARGO_REGISTRY_TOKEN` secret was deleted after verification.

## Preparation Evidence

- Public registry discovery: `https://crates.io/api/v1/crates/nwau-core` returned crate absence evidence.
- Local package command: `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-core/Cargo.toml`
- Package result: `Packaged 16 files, 107.8KiB (25.2KiB compressed)`
- Verification result: `Compiling nwau-core v0.1.0` and `Finished dev profile`
- Publish dry-run command: `cargo publish --dry-run --allow-dirty --locked --manifest-path rust/crates/nwau-core/Cargo.toml`
- Publish dry-run result: packaged and verified `nwau-core v0.1.0`, reached upload, then aborted because this was a dry run.
- Workflow clean-checkout note: `cargo package --locked` without `--allow-dirty` fails in the dirty worktree; the GitHub workflow can publish only after the Rust crate state is committed and pushed to the workflow ref.
- Publication evidence: `https://crates.io/api/v1/crates/nwau-core/0.1.0` returned version `0.1.0`, checksum `c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547`, and `yanked=false`.
- Credential cleanup: crates.io token `mchs-github-actions-publish` was revoked and GitHub Actions secret `CARGO_REGISTRY_TOKEN` was deleted after verification.
- Remaining external blocker: none for crates.io.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
