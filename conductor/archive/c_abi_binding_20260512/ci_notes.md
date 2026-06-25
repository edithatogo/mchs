# CI and Build Notes: C ABI Binding

The C ABI preview surface is not production-ready. Keep CI conservative until the
header, exported symbols, and fixture parity checks are deterministic across
platforms.

## Current stance

- Do not add a required C ABI workflow until header generation and symbol checks
  are reproducible on clean runners.
- Keep the committed header and Rust crate as the reviewable preview surface.
- Treat the scalar acute 2025 entry point as implemented only for valid
  pointer-shaped calls that delegate to `nwau-core`; invalid pointers and any
  future unvalidated entry points must fail closed.

## Future CI gate commands

The minimum future gate should include:

```bash
cd rust && cargo fmt --all --check
cd rust && cargo clippy --all-targets --all-features -- -D warnings
cd rust && cargo test
```

When header generation is introduced, add:

```bash
cbindgen --config rust/crates/nwau-c-abi/cbindgen.toml \
  --crate nwau-c-abi \
  --output rust/crates/nwau-c-abi/include/nwau_abi.h
git diff --exit-code rust/crates/nwau-c-abi/include/nwau_abi.h
```

## ABI compatibility expectations

- Diff committed headers and exported symbols for every release candidate.
- Fail CI on removed symbols, reordered public fields, enum ordinal changes, or
  ownership-semantic changes inside the same ABI major version.
- Record ABI version macros and runtime version query results in compatibility
  tests.

## Fixture parity expectations

- C ABI outputs must match the shared golden fixtures for every calculator that
  becomes exposed through the ABI before production or public-readiness claims.
- Until parity exists for a new calculator entry point, that entry point should
  fail closed with an explicit unsupported or unimplemented status.

## Memory and error-path tests

- Test null pointer handling, caller-owned output storage, borrowed string
  views, status-message lifetimes, and invalid status codes.
- Add sanitizer or valgrind-style checks once allocated outputs and release
  functions exist.

## Platform matrix

- Start with Linux and macOS.
- Add Windows once the export macro and dynamic-linking story is validated.
- Keep platform claims conservative until all matrix legs run the same ABI and
  fixture checks.
