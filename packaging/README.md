# Packaging readiness

This directory tracks the local readiness state for downstream package
submission.

## C ABI registry readiness policy

- `nwau-core` is published on crates.io, so vcpkg and ConanCenter readiness
  can treat the Rust core as an external dependency rather than an unpublished
  local-only crate.
- `nwau-c-abi` is not yet vcpkg or ConanCenter review-ready. Upstream registry
  submissions require an immutable source archive, coherent version metadata,
  consumer usage examples, and registry-native validation.

## Version and source-tag policy

- `rust/crates/nwau-c-abi/Cargo.toml` package version, `nwau_abi.h` ABI
  constants, Rust ABI constants, release notes, and registry manifests must
  either match exactly or document package-version versus ABI-version
  semantics.
- Prefer a dedicated immutable release tag for C ABI packaging, such as
  `nwau-c-abi-v0.1.0`, after version alignment.
- The source archive must contain `LICENSE`, `rust/Cargo.toml`,
  `rust/Cargo.lock`, `rust/crates/nwau-core`, `rust/crates/nwau-c-abi`, and
  `rust/crates/nwau-c-abi/include/nwau_abi.h`.
- Record archive checksums required by downstream registries: SHA512 for vcpkg
  and SHA256 or Conan `conandata.yml` checksums for ConanCenter.

## Overlay-to-archive roadmap

- Current vcpkg and Conan files are local readiness scaffolds.
- The vcpkg scaffold uses `vcpkg_from_github`, but the source reference and
  checksum still need to be replaced with reviewable immutable release
  metadata.
- The Conan scaffold still exports local source and must be converted to
  ConanCenter layout before submission.
- Do not submit upstream until archive-based builds pass from clean registry
  checkouts.

## Local scope

- `packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
- `packaging/conan/conanfile.py`

These remain local scaffolds for the `nwau-c-abi` C ABI package. The checked-in
vcpkg and Conan files are draft readiness artifacts, not accepted upstream
registry recipes.

## Remaining external submission steps

- The vcpkg port pins an immutable repository commit and archive hash; add
  vcpkg registry version metadata in the upstream vcpkg repository when it is
  ready for submission.
- Add the ConanCenter `test_package` harness and any required recipe layout
  changes in the upstream ConanCenter index repository.
- Add a vcpkg usage file or CMake/pkg-config consumer story.
- Run the required local and CI validation against the published
  `nwau-core` crate and the C ABI surface.
- Submit upstream PRs to vcpkg and ConanCenter, then wait for review and
  registry acceptance.

## Local blockers

- No crates.io publication blocker remains for `nwau-core`.
- Align or explicitly document package-version versus ABI-version semantics.
- Define the immutable C ABI source tag and archive checksum policy.
- Add a native C/C++ consumer smoke test that includes `nwau_abi.h`, links
  `nwau_c_abi`, and calls harmless version/status functions.
- Record clean archive-based vcpkg and Conan validation before upstream
  submissions.
- The remaining work is the missing upstream packaging submission flow and any
  validation those registries require.

## Local validation commands

Run these from the repository root when the external toolchains are available.
They are intentionally non-publishing checks: they exercise the local recipe
and port definitions without pushing anything upstream.

- Conan recipe:
  - `conan create packaging/conan --build=missing`
- vcpkg port:
  - `vcpkg install nwau-c-abi --overlay-ports=packaging/vcpkg/ports`

## Current validation blocker

- `conan` is not installed in this environment.
- `vcpkg` is not installed in this environment.
- Because both tools are missing, I could not advance beyond the static review
  of `packaging/conan/conanfile.py` and `packaging/vcpkg/ports/nwau-c-abi/`.
