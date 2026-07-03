# Rust CLI Core Migration Evidence

Scope: `rust_cli_core_migration_20260703`

## Implemented Behaviour

- Added `--runtime python|rust|auto` to the `acute`, `ed`, and `non-admitted`
  calculation commands.
- Added `NWAU_RUNTIME` as an automation override. Explicit CLI options take
  precedence over the environment.
- Preserved Python as the default runtime.
- Routed `acute --year 2025 --runtime rust` through
  `nwau_py.calculators.acute.calculate_acute_rust_2025`.
- Added fail-closed Rust diagnostics:
  - `MCHS-CLI-RUNTIME-INVALID`
  - `MCHS-CLI-RUST-UNSUPPORTED`
  - `MCHS-CLI-RUST-UNAVAILABLE`

## Validation Evidence

Focused tests:

```text
uv run pytest -q tests/test_rust_cli_core_migration.py tests/test_cli.py tests/test_rust_acute_binding.py
12 passed, 4 skipped
```

The skipped tests are optional live Rust-extension binding and CLI parity tests
guarded when the extension is unavailable in the local Python environment.

Rust core and C ABI tests:

```text
cargo test -p nwau-core -p nwau-c-abi
36 passed
```

Full Rust workspace note:

```text
cargo test
```

The full workspace run passed `nwau-core`, `nwau-c-abi`, and Rust integration
tests before failing when the local `nwau-py` test binary attempted to load
`libpython3.13.dylib`. That is an environment dynamic-library blocker for the
Python extension test binary, not a failure in the acute 2025 Rust core tests.

## Support Claim

This evidence supports an opt-in Rust-backed CLI path for acute 2025 only. It
does not claim Rust default status, full SAS parity across all calculators, ED
Rust support, non-admitted Rust support, Parquet runtime support, or all-year
Rust support.

## Residual Gaps

- ED and non-admitted remain Python-only.
- Non-2025 pricing years remain Python-only for Rust CLI purposes.
- Parquet and non-CSV runtime paths are not implemented by the current Click
  commands.
- Rust default promotion still requires broader fixture coverage and release
  evidence beyond this track.
