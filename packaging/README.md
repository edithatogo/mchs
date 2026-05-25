# Packaging readiness

This directory tracks the local readiness state for downstream package
submission.

## Current assumption

- `nwau-core` is published on crates.io, so vcpkg and ConanCenter readiness
  can now treat the Rust core as an external, available dependency rather than
  an unpublished local-only crate.

## Local scope

- `packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
- `packaging/conan/conanfile.py`

These remain local scaffolds for the `nwau-c-abi` C ABI package. The checked-in
vcpkg and Conan files are draft readiness artifacts, not accepted upstream
registry recipes.

## Remaining external submission steps

- Replace the draft vcpkg `REF` and `SHA512` values with upstream-reviewable
  immutable source metadata, then add vcpkg registry version metadata in the
  upstream vcpkg repository.
- Add the ConanCenter `test_package` harness and any required recipe layout
  changes in the upstream ConanCenter index repository.
- Run the required local and CI validation against the published
  `nwau-core` crate and the C ABI surface.
- Submit upstream PRs to vcpkg and ConanCenter, then wait for review and
  registry acceptance.

## Local blockers

- No crates.io publication blocker remains for `nwau-core`.
- The remaining work is the missing upstream packaging submission flow and any
  validation those registries require.
