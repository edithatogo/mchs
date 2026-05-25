# C/C++ vcpkg and Conan Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `C/C++ ABI`
- Registry: `vcpkg / ConanCenter`
- Package candidate: `nwau-c-abi`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/rust/crates/nwau-c-abi/Cargo.toml`
- Current status: `prepared_pending_vcpkg_conan_submission_prs`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally with caveat. A vcpkg port manifest and Conan recipe exist, the C ABI crate builds locally, and `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-c-abi/Cargo.toml` now verifies successfully by downloading `nwau-core v0.1.0` from crates.io. The remaining blockers are complete vcpkg portfile/Conan recipe packaging, local or CI validation for those registry formats, and upstream PR/review workflows.

## Preparation Evidence

- vcpkg discovery: `https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/nwau-c-abi/vcpkg.json` returned `404 Not Found`.
- ConanCenter reachability: `https://center2.conan.io/v1/ping` returned HTTP 200.
- vcpkg port: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
- Conan recipe: `microcosting_healthservices/packaging/conan/conanfile.py`
- Build command: `cargo build`
- Build result: `Finished dev profile for nwau-c-abi v0.1.0`
- Local fix: added `version = "0.1.0"` to the `nwau-core` path dependency.
- Cargo package command: `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-c-abi/Cargo.toml`
- Cargo package result: packaged 6 files, downloaded `nwau-core v0.1.0` from crates.io during verification, and compiled `nwau-c-abi v0.1.0`.
- Remaining external blocker: complete vcpkg portfile/Conan recipe packaging and submit vcpkg/ConanCenter PRs for review.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
