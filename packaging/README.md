# Packaging readiness

This directory tracks the local readiness state for downstream package
submission.

## C ABI registry readiness policy

- `nwau-core` is published on crates.io, so vcpkg and ConanCenter readiness
  can treat the Rust core as an external dependency rather than an unpublished
  local-only crate.
- `nwau-c-abi` is locally validated for archive-based Conan and vcpkg overlay
  packaging, but not yet published to vcpkg or ConanCenter.
- Upstream registry submissions still require PR preparation, registry-native
  version metadata, and maintainer review/merge.

## Version and source-tag policy

- `rust/crates/nwau-c-abi/Cargo.toml` package version, `nwau_abi.h` ABI
  constants, Rust ABI constants, release notes, and registry manifests must
  either match exactly or document package-version versus ABI-version
  semantics.
- The current package and ABI version are aligned at `0.1.0`.
- Generate the minimal source archive with
  `packaging/scripts/build-nwau-c-abi-source-archive.sh 0.1.0 dist`.
- The source archive must contain `LICENSE`, `rust/Cargo.toml`,
  `rust/Cargo.lock`, `rust/crates/nwau-core`, `rust/crates/nwau-c-abi`,
  `rust/crates/nwau-py`, and `rust/crates/nwau-c-abi/include/nwau_abi.h`.
- Record archive checksums required by downstream registries: SHA512 for vcpkg
  and Conan `conandata.yml` checksums for ConanCenter.

## Overlay-to-archive roadmap

- Current vcpkg and Conan files are local readiness scaffolds.
- The vcpkg scaffold now uses `vcpkg_download_distfile` against the dedicated
  `nwau-c-abi-v0.1.0` source archive instead of a full repository archive.
- The Conan scaffold uses `conandata.yml`, an archive-based `source()` flow,
  and a native `test_package`; mirror or adapt that layout in the upstream
  ConanCenter index repository before submission.
- Do not claim upstream registry publication until review/merge evidence exists.

## Local scope

- `packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
- `packaging/vcpkg/ports/nwau-c-abi/usage`
- `packaging/vcpkg/versions/baseline.json`
- `packaging/vcpkg/versions/n-/nwau-c-abi.json`
- `packaging/conan/conanfile.py`
- `packaging/scripts/build-nwau-c-abi-source-archive.sh`

These remain local scaffolds for the `nwau-c-abi` C ABI package. The checked-in
vcpkg and Conan files are draft readiness artifacts, not accepted upstream
registry recipes.

## Remaining external submission steps

- Draft vcpkg registry version metadata exists under `packaging/vcpkg/versions`;
  replace the placeholder git tree with the upstream vcpkg tree hash during
  submission.
- ConanCenter `test_package` harness exists under `packaging/conan/test_package`;
  mirror or adapt it in the upstream ConanCenter index repository as required
  by reviewer policy.
- vcpkg usage guidance exists under `packaging/vcpkg/ports/nwau-c-abi/usage`.
- Submit upstream PRs to vcpkg and ConanCenter, then wait for review and
  registry acceptance.

## Local blockers

- No crates.io publication blocker remains for `nwau-core`.
- Conan `conandata.yml` points at the minimal immutable source archive and
  records its SHA256.
- Archive-based Conan and vcpkg overlay validations pass locally; upstream
  submission still requires registry PR preparation and review.

## Local validation commands

Run these from the repository root when the external toolchains are available.
They are intentionally non-publishing checks: they exercise the local recipe
and port definitions without pushing anything upstream.

- Conan recipe:
  - `conan create packaging/conan --build=missing`
  - `conan test packaging/conan/test_package nwau-c-abi/0.1.0`
- vcpkg port:
  - `vcpkg install nwau-c-abi --overlay-ports=packaging/vcpkg/ports`

## Current validation evidence

- `conan create packaging/conan --build=missing` passed with Conan 2.28.1 on
  macOS armv8/apple-clang 21, including download from the dedicated `source-r2`
  archive and the CMake consumer `test_package`.
- `/tmp/vcpkg/vcpkg install nwau-c-abi --overlay-ports=packaging/vcpkg/ports`
  passed for `nwau-c-abi:arm64-osx@0.1.0` using the dedicated `source-r2`
  archive, installing header, release/debug static libraries, release/debug
  dylibs, usage text, and copyright.
- The remaining work is upstream PR preparation/review, including replacing
  draft vcpkg `git-tree` metadata with the value generated in the upstream
  vcpkg registry checkout.
