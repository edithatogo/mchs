# Rust CLI Runtime Boundary

This note defines the runtime contract for the first CLI migration slice.

## Runtime Status Wording

| Status | Meaning |
| --- | --- |
| Python default | The public CLI defaults to the existing Python calculator path. This remains the supported default until a release gate records a default-runtime change. |
| Rust canary | Rust kernels and Python bindings exist for selected calculations, but they are not the default CLI runtime. |
| Rust opt-in | A user may request Rust with `--runtime rust` or `NWAU_RUNTIME=rust` for validated surfaces only. Unsupported requests fail closed. |
| Rust default | A future state that requires published parity, diagnostics, and release evidence. This track does not claim that state. |

## Runtime Selection

`--runtime python|rust|auto` is the user-facing selector for calculation commands.
`NWAU_RUNTIME` is a CI and automation override. An explicit `--runtime` option takes
precedence over `NWAU_RUNTIME`.

The default runtime is `python`. `auto` is conservative during migration: it may use
Python fallback unless a later promotion gate records a wider Rust default.

## First Supported Rust Slice

The first Rust-backed CLI slice is:

- command: `acute`
- pricing year: `2025`
- input format: CSV
- output format: CSV to stdout or a file
- implementation: `nwau_py.calculators.acute.calculate_acute_rust_2025`

Non-acute calculators, non-2025 pricing years, non-CSV formats, and unvalidated
output modes remain Python-only until separate evidence promotes them.

## Parity Contract

Acute 2025 CLI parity compares the Python-backed CLI output and Rust-backed CLI
output against the golden fixture set in `tests/fixtures/golden/acute_2025`.
Numeric parity uses `rtol=1e-4` and `atol=1e-4`; no CLI-specific rounding is
introduced beyond the existing CSV output behaviour.

Schema parity sources:

- CLI command and file contract: `contracts/interop/cli-file-interop.contract.json`
- CLI schema: `contracts/interop/cli-file-interop.schema.json`
- acute 2025 golden input and expected output: `tests/fixtures/golden/acute_2025`
- acute 2025 reference pack: `tests/data/2025`

## Diagnostics

Rust runtime requests fail closed with stable diagnostic codes:

| Code | Condition |
| --- | --- |
| `MCHS-CLI-RUNTIME-INVALID` | `--runtime` or `NWAU_RUNTIME` is not `python`, `rust`, or `auto`. |
| `MCHS-CLI-RUST-UNSUPPORTED` | Rust is requested for an unsupported command, year, format, or output mode. |
| `MCHS-CLI-RUST-UNAVAILABLE` | Rust is requested for a supported surface but the Rust extension cannot be loaded. |

Python fallback is allowed only for the default Python runtime and the transitional
`auto` runtime. It is not allowed when the user explicitly requests `rust`.
