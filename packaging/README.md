# Packaging readiness

This directory tracks the local readiness state for downstream package
submission.

## C ABI registry readiness policy

- `nwau-core` is published on crates.io, so vcpkg and ConanCenter readiness
  can treat the Rust core as an external dependency rather than an unpublished
  local-only crate.
- `nwau-c-abi` is locally validated for archive-based Conan and vcpkg overlay
  packaging, but not yet published to vcpkg or ConanCenter.
- Upstream registry submissions are open. Publication still requires
  maintainer review/merge, ConanCenter job approval, vcpkg Rust/Cargo
  toolchain policy resolution, and Microsoft CLA acceptance by the authorized
  contributor.

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

- Current vcpkg and Conan files are local readiness scaffolds mirrored from the
  submitted upstream PRs where practical.
- The vcpkg scaffold now uses `vcpkg_download_distfile` against the dedicated
  `nwau-c-abi-v0.1.0` source archive instead of a full repository archive,
  maps vcpkg triplets to Rust targets, honors `VCPKG_LIBRARY_LINKAGE`, and
  installs a `nwau-c-abi::nwau-c-abi` CMake config target.
- The Conan scaffold uses `conandata.yml`, an archive-based `source()` flow,
  a native `test_package`, Release/Debug Cargo profile mapping, and
  static/shared artifact separation.
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
  the submitted upstream PR has registry version metadata generated in the
  vcpkg checkout.
- ConanCenter `test_package` harness exists under `packaging/conan/test_package`
  and has been mirrored to the upstream ConanCenter PR branch.
- vcpkg usage guidance exists under `packaging/vcpkg/ports/nwau-c-abi/usage`.
- Wait for ConanCenter maintainer job approval and review.
- Resolve vcpkg Rust/Cargo toolchain policy or move to an accepted
  self-contained artifact strategy; current vcpkg CI images do not provide
  `cargo` for all tested triplets and vcpkg has no first-class Rust/Cargo
  acquisition helper.
- Microsoft CLA acceptance is a legal contributor action and is not performed
  by automation.

## Local blockers

- No crates.io publication blocker remains for `nwau-core`.
- Conan `conandata.yml` points at the minimal immutable source archive and
  records its SHA256.
- Archive-based Conan and vcpkg overlay validations pass locally; upstream
  publication still requires registry review/merge.

## Local validation commands

Run these from the repository root when the external toolchains are available.
They are intentionally non-publishing checks: they exercise the local recipe
and port definitions without pushing anything upstream.

- Conan recipe:
  - `conan create packaging/conan --build=missing`
  - `conan create packaging/conan -o 'nwau-c-abi/*:shared=True' --build=missing`
- vcpkg port:
  - `vcpkg install nwau-c-abi --overlay-ports=packaging/vcpkg/ports`

## Current validation evidence

- `conan create packaging/conan --build=missing` passed with Conan 2.28.1 on
  macOS armv8/apple-clang 21, including download from the dedicated `source-r2`
  archive and the CMake consumer `test_package`.
- `conan create packaging/conan -o 'nwau-c-abi/*:shared=True' --build=missing`
  passed with Conan 2.28.1 on macOS armv8/apple-clang 21 and packaged the
  shared `.dylib` variant.
- `/tmp/vcpkg/vcpkg install nwau-c-abi --overlay-ports=packaging/vcpkg/ports`
  passed for `nwau-c-abi:arm64-osx@0.1.0` using the dedicated `source-r2`
  archive, installing header, release/debug static libraries, generated CMake
  config, usage text, and copyright.
- vcpkg fork commit `58ff86fe` updates the upstream PR branch with target-aware
  Cargo invocation, linkage-aware artifact installation, generated CMake config
  target, Android exclusion, and regenerated version metadata.
- Upstream PRs are open at `https://github.com/microsoft/vcpkg/pull/51965`
  and `https://github.com/conan-io/conan-center-index/pull/30262`; no upstream
  publication is claimed until those registry workflows accept/merge.
