# Rust CLI Surface Inventory

This inventory records the CLI surfaces considered by the Rust CLI core
migration track.

## Public Commands

| Command | Options | Input | Output | Python implementation | Rust status |
| --- | --- | --- | --- | --- | --- |
| `acute` | `--output`, `--runtime`, `--year`, `--params` | CSV path | CSV stdout or file | `nwau_py.calculators.calculate_acute` | Rust opt-in for year `2025` through `calculate_acute_rust_2025` |
| `ed` | `--output`, `--runtime`, `--year`, `--params` | CSV path | CSV stdout or file | `nwau_py.calculators.calculate_ed` | Python-only; `--runtime rust` fails closed |
| `non-admitted` | `--output`, `--runtime`, `--year`, `--params` | CSV path | CSV stdout or file | `nwau_py.calculators.calculate_outpatients` | Python-only; `--runtime rust` fails closed |
| `interop contract` | none | none | JSON stdout | `contracts/interop/cli-file-interop.contract.json` | Contract inspection only |
| `validate-year` | `--json/--text` | repository reference-data manifests | text or JSON stdout | `nwau_py.reference_validation` | Python-only governance command |
| `diff-year` | `--json/--text` | repository reference-data manifests | text or JSON stdout | `nwau_py.reference_validation` | Python-only governance command |
| `coding-set registry list` | `--year`, `--metadata-only/--include-restricted` | registry metadata | JSON stdout | `nwau_py.classification_registry` | Python-only metadata command |
| `coding-set registry validate-compatibility` | `--entry`, `--year`, `--version` | registry metadata | JSON stdout | `nwau_py.classification_registry` | Python-only metadata command |
| `sources scan` | source scan options | source pages and manifests | JSON/text output | `nwau_py.sources` | Python-only evidence command |
| `sources add-year` | year and source options | source pages and manifests | manifest files | `nwau_py.sources` | Python-only evidence command |

The calculation commands retain the shared classification preflight:

- `acute` validates `ar_drg`
- `ed` validates `aecc`
- `non-admitted` validates `tier_2`

## File Contracts

The migration preserves the current CLI/file contract:

- contract bundle: `contracts/interop/cli-file-interop.contract.json`
- schema: `contracts/interop/cli-file-interop.schema.json`
- diagnostics fields: `severity`, `code`, `message`, `path`
- acute fixture pack: `tests/fixtures/golden/acute_2025`

The interop contract advertises CSV and Parquet at the contract level. The
current Click entry points exercised by this track accept CSV paths and emit
CSV only. Parquet and additional output modes are not promoted to Rust support
by this track.

## Runtime Policy

Calculation commands expose `--runtime python|rust|auto`. The runtime default is
Python unless `NWAU_RUNTIME` is set. Explicit CLI options take precedence over
the environment. `auto` is a transitional mode and may use Python fallback.

`--runtime rust` is accepted only for `acute --year 2025` with CSV input and CSV
output. Unsupported Rust requests emit `MCHS-CLI-RUST-UNSUPPORTED`; a missing
Rust extension emits `MCHS-CLI-RUST-UNAVAILABLE`.

## Rust API Needed

The first slice uses the existing Python binding over the Rust kernel:

- `nwau_py.calculators.acute.calculate_acute_rust_2025`
- `nwau_py.rust_bridge.calculate_acute_2025_row`
- `rust/crates/nwau-core` acute 2025 kernel functions

Follow-on migration requires Rust kernels and binding adapters for ED,
non-admitted, governance validation, and any promoted Parquet/file-contract
surface before those commands can move beyond Python-only status.
