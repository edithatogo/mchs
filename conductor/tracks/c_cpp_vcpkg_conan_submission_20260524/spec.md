# C/C++ vcpkg and Conan Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `C/C++ ABI`
- Registry: `vcpkg / ConanCenter`
- Package candidate: `nwau-c-abi`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/rust/crates/nwau-c-abi/Cargo.toml`
- Current status: `submitted_pending_upstream_review_and_vcpkg_rust_toolchain_policy`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Repo-side readiness is resolved for the submitted archive-based package
artifacts. The crates.io dependency blocker is resolved, the C ABI crate builds
locally, and `cargo package --allow-dirty --locked --manifest-path
rust/crates/nwau-c-abi/Cargo.toml` verifies by downloading `nwau-core v0.1.0`
from crates.io. The dedicated C ABI source archive, vcpkg overlay port,
ConanCenter recipe layout, and native consumer smoke tests have all been
validated locally.

Remaining blockers:

- vcpkg PR `https://github.com/microsoft/vcpkg/pull/51965` is submitted, but
  vcpkg CI fails on platforms where `cargo` is absent. Current vcpkg
  infrastructure has no first-class Rust/Cargo acquisition helper for ports, so
  the upstream path is blocked on vcpkg Rust toolchain policy or a decision to
  accept Cargo as an external host prerequisite.
- vcpkg also has a Microsoft CLA check queued. The CLA is a legal acceptance
  step and must be completed by the authorized contributor, not by automation.
- ConanCenter PR `https://github.com/conan-io/conan-center-index/pull/30262`
  is submitted. Local static and shared validations pass; upstream CI is
  waiting on maintainer job-scheduler approval before publication can be
  claimed.

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
- Dedicated source archive: `https://github.com/edithatogo/mchs/releases/download/nwau-c-abi-v0.1.0/nwau-c-abi-0.1.0-source-r2.tar.gz`
- Dedicated source archive SHA-256: `e42c7948828a7ea8b581782817a342db577588d9398ba683b34c45ca49ef2bf1`
- Dedicated source archive SHA-512: `eda962cc2f2569f87b8c21f600e3f5abce0c46f98bf587b410e42d72c5ffe73ec717d6bc3a78ffa4009cf6c0f07edd532a86ddf54cf1eb5199c555980ddddabc`
- ConanCenter validation: `conan create recipes/nwau-c-abi/all --version=0.1.0 --build=missing` passed from the ConanCenter fork branch.
- ConanCenter shared validation: `conan create recipes/nwau-c-abi/all --version=0.1.0 -o 'nwau-c-abi/*:shared=True' --build=missing` passed from the ConanCenter fork branch.
- ConanCenter review cleanup: fork commit `0e7d9052` changes the C smoke test pointer comparison from `0` to `NULL`; commit `d3a07060` switches the test_package runner to `self.cpp.build.bindir` for multi-config and Windows portability; commit `657c7a31` adds explicit Cargo profile and shared/static library-pattern helpers for the remaining live Copilot review threads; static and shared `conan create` validations passed before the final explicit-helper cleanup, and `657c7a31` passed `python3 -m py_compile` plus `git diff --check`.
- Local Conan validation: `conan create packaging/conan --build=missing` and `conan create packaging/conan -o 'nwau-c-abi/*:shared=True' --build=missing` passed from the MCHS clean push clone.
- vcpkg overlay validation: `/tmp/vcpkg/vcpkg install nwau-c-abi --overlay-ports=packaging/vcpkg/ports` passed for `arm64-osx` after the target-aware/linkage-aware port update, installing the generated CMake config target plus release/debug static libraries.
- vcpkg fork update: commit `58ff86fe` adds Rust target-triple mapping, honors `VCPKG_LIBRARY_LINKAGE`, installs `nwau-c-abi::nwau-c-abi`, excludes Android, and regenerates version metadata.
- vcpkg upstream PR: `https://github.com/microsoft/vcpkg/pull/51965`.
- ConanCenter upstream PR: `https://github.com/conan-io/conan-center-index/pull/30262`.
- Remaining external blocker: upstream review/merge and vcpkg Rust/Cargo
  toolchain policy; no public vcpkg or ConanCenter publication is claimed yet.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
