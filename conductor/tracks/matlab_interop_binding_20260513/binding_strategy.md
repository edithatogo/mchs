# Binding Strategy: MATLAB Interoperability

## Decision

Use a staged integration strategy for MATLAB consumers, initially targeting
file exchange (MAT/CSV/Parquet) and CLI invocation, with C ABI as a future
in-process MEX path. MATLAB users read pre-computed calculator outputs or
invoke the shared-core CLI from MATLAB via the `system()` or `!` command.
No MATLAB formula port (`.m` files with calculator logic) is created.

This follows the polyglot Rust core roadmap and reuses the C ABI and CLI/file
interop contracts established by the shared core.

## Rationale

- MATLAB is widely used in numerical simulation, teaching, and legacy health
  analytics. A MATLAB formula port would duplicate calculator logic and split
  validation effort.
- CSV and Parquet interchange is already supported by the CLI/file contract
  and is natively readable in MATLAB via `readtable` or the MATLAB Parquet
  toolbox.
- CLI invocation from MATLAB (`system('mchs-calc ...')`) gives a zero-build
  path for MATLAB users who already run the shared-core CLI.
- C ABI via MEX (Rust `cdylib` loaded with `loadlibrary` or MEX `calllib`)
  is viable for in-process execution but requires MATLAB compiler toolchain
  matching.
- `.mat` file exchange via MATLAB's `save`/`load` is a familiar workflow for
  existing MATLAB users.
- No MATLAB toolbox publication or Add-On Explorer submission is needed for
  local adapter validation. Toolbox publication is a later packaging decision.

## Contract shape

### Integration modes

| Mode          | Consumer                    | Transport         | Notes                              |
|---------------|-----------------------------|-------------------|------------------------------------|
| File import   | MATLAB `readtable`          | CSV / Parquet     | Primary mode; zero-build           |
| File import   | MATLAB `load`               | .mat              | Native for existing MATLAB users   |
| CLI invocation| MATLAB `system()` / `!`     | CLI stdout/json   | Cross-platform; no add-on          |
| C ABI         | MATLAB `loadlibrary`        | C .dylib/.so      | Future path; MEX matching required |

### CSV/Parquet schema contract

MATLAB reads the same CSV and Parquet schemas produced by the CLI/file interop
track:

- `contract_version` — pinned calculator contract version
- `calculator_id` — public calculator identifier
- `pricing_year` — target IHACPA pricing year
- `input_schema` — structured input columns matching the calculator contract
- `output_schema` — computed output columns with diagnostic flags
- `provenance` — shared-core version, source archive hash, generation timestamp
- `fixture_gate` — declared synthetic-only or local-only gate

### CLI invocation pattern (MATLAB)

```matlab
% Illustrative — not implemented here
[status, cmdout] = system('mchs-calc --calculator nwau --pricing-year 2026 --output results.csv');
T = readtable('results.csv');
```

### .mat export workflow

When MATLAB-native analysis is required, the shared-core CLI exports CSV or
Parquet that MATLAB loads and saves as `.mat` for downstream use. The shared
core does not write `.mat` directly.

## Supported calculators

All calculators exposed through the CLI/file interop track are accessible from
MATLAB. No MATLAB-specific calculator packaging is required.

## Limitations

- MATLAB does not execute calculator logic. All computation happens in the
  shared core before file exchange.
- CLI invocation from MATLAB on Windows requires PATH or full binary path
  configuration. On macOS and Linux, `system()` resolves PATH normally.
- C ABI MEX integration requires a Rust `cdylib` build and a MATLAB compiler
  (`mex`) configuration. This path is documented but not implemented in this
  track.
- The MATLAB Parquet toolbox requires R2019b or later with the Parquet
  support files. CSV is the recommended portable format.
- No MATLAB `.m` functions, classes, or App Designer apps containing formula
  logic are maintained in this repository.

## Versioning

- MATLAB interop workflows pin to the CLI/file interop contract version for
  file schemas.
- C ABI integration would pin to the C ABI contract version.
- No separate MATLAB interop version is needed.

## Diagnostics and provenance

- File outputs include full provenance columns readable in MATLAB as table
  variables.
- CLI invocation captures diagnostic output that MATLAB users can review
  in the command window or redirect to a log file.
- Provenance metadata supports traceability from MATLAB tables back to shared
  core execution.

## Privacy and synthetic examples

- All committed MATLAB example manifests and test files are synthetic.
- Real IHACPA pricing data or patient-level extracts are never committed as
  MATLAB examples.
- The `fixture_gate` column distinguishes synthetic examples from local-only
  real data.

## When to use MATLAB interop vs. other bindings

Use MATLAB interop when:
- the consumer is a numerical modeller, educator, or legacy MATLAB analyst
- the workflow requires MATLAB toolboxes (Statistics, Optimization, etc.) for
  post-processing
- the team standardises on MATLAB for teaching or research workflows

Prefer CLI/file interop or native bindings when:
- the consumer does not use MATLAB
- the integration needs sub-second or in-process calculator calls
- the deployment target is fully automated (no MATLAB license)
- the consumer needs a language-agnostic integration surface

## Readiness bar

- This track is adapter-ready for file/CLI boundary helpers and remains
  transport-only.
- Interop workflows are documented and validated against shared golden
  fixtures.
- Do not claim MATLAB toolbox publication until a CSV-import or CLI-invocation
  example has registry-owner evidence beyond synthetic fixtures.
