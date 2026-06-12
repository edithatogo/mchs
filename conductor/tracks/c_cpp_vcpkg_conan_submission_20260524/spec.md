# C/C++ vcpkg and Conan Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare local/private preview package metadata if absent, submit only when package readiness and credentials are present, and record durable publication evidence only after upstream acceptance.

## Registry

- Ecosystem: `C/C++ ABI`
- Registry: `vcpkg / ConanCenter`
- Package candidate: `nwau-c-abi`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/rust/crates/nwau-c-abi/Cargo.toml`
- Current status: `submitted_conancenter_pending_cla_scheduler_review_vcpkg_deferred`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Prepared locally with caveat. A vcpkg port manifest and `portfile.cmake` exist, the C ABI crate builds and packages with Cargo, the Conan recipe passes `conan create packaging/conan --build=missing` from exported sources on macOS armv8, and a disposable vcpkg clone under `/tmp/mchs-vcpkg-validation` installs `nwau-c-abi:arm64-osx` from the local overlay port. This is local/private preview packaging evidence only. vcpkg PR `https://github.com/microsoft/vcpkg/pull/51965` was closed unmerged because vcpkg does not currently support Rust library ports. ConanCenter PR `https://github.com/conan-io/conan-center-index/pull/30262` is open after portability fixes; remaining blockers are CLA/recheck, job scheduler, maintainer review, and merge.

## Preparation Evidence

- vcpkg discovery: `https://raw.githubusercontent.com/microsoft/vcpkg/master/ports/nwau-c-abi/vcpkg.json` returned `404 Not Found`.
- ConanCenter reachability: `https://center2.conan.io/v1/ping` returned HTTP 200.
- vcpkg port: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
- vcpkg portfile: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/portfile.cmake`
- Conan recipe: `microcosting_healthservices/packaging/conan/conanfile.py`
- Build command: `cargo build`
- Build result: `Finished dev profile for nwau-c-abi v0.1.0`
- Local fix: added `version = "0.1.0"` to the `nwau-core` path dependency.
- Cargo package command: `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-c-abi/Cargo.toml`
- Cargo package result: packaged 6 files, 14.2KiB (4.2KiB compressed) and compiled `nwau-c-abi v0.1.0` during verification.
- Conan inspect command: `conan inspect packaging/conan/conanfile.py`
- Conan inspect result: Conan 2.28.1 parsed name/version/options/settings/package metadata.
- Conan create command: `conan create packaging/conan --build=missing`
- Conan create result: built `nwau-c-abi/0.1.0` from exported sources on macOS armv8 and packaged `LICENSE`, `nwau_abi.h`, `libnwau_c_abi.dylib`, and `libnwau_c_abi.a`.
- Conan package reference: `nwau-c-abi/0.1.0#54fd5d0abe08598387916b9bc960f74c:b8da06845b8444be84fc8e71e7354dc6f23831c8#711e388131e98c4a4f2449e8d3549768`
- vcpkg manifest validation: `python -m json.tool packaging/vcpkg/ports/nwau-c-abi/vcpkg.json` parsed successfully.
- vcpkg bootstrap command: `git clone --depth 1 https://github.com/microsoft/vcpkg.git /tmp/mchs-vcpkg-validation && /tmp/mchs-vcpkg-validation/bootstrap-vcpkg.sh -disableMetrics`
- vcpkg bootstrap result: bootstrapped vcpkg package management program version `2026-04-08-e0612b42ce44e55a0e630f2ee9d3c533a63d8bc1`.
- vcpkg overlay install command: `/tmp/mchs-vcpkg-validation/vcpkg install nwau-c-abi --overlay-ports=/Volumes/PortableSSD/GitHub/mchs/microcosting_healthservices/packaging/vcpkg/ports --triplet arm64-osx --clean-after-build --binarysource=clear`
- vcpkg overlay install result: installed `nwau-c-abi:arm64-osx@0.1.0` successfully with `include/nwau_abi.h`, `lib/libnwau_c_abi.a`, `debug/lib/libnwau_c_abi.a`, copyright, and SPDX metadata.
- Conan packaging metadata: recipe declares settings/options, explicit source export, Cargo build command, constrained header/library packaging, and CMake/pkg-config consumer metadata.
- Publication claim: no public vcpkg or ConanCenter publication is claimed.
- vcpkg submission: PR `https://github.com/microsoft/vcpkg/pull/51965` closed unmerged on 2026-05-26 because vcpkg does not currently support Rust library ports; keep as deferred upstream-policy evidence.
- ConanCenter submission: PR `https://github.com/conan-io/conan-center-index/pull/30262` is open; commit `c635b0f9d2f1619d9149e4fa964185658c063f5d` fixed test-package portability.
- Remaining external blocker: complete ConanCenter CLA/recheck and wait for job scheduler/maintainer review; vcpkg remains deferred until upstream policy supports Rust library ports or the distribution design changes.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for local/private preview package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Treating local vcpkg/Conan metadata as public registry publication.
- Claiming support for clinical/private data workflows from package publication.
