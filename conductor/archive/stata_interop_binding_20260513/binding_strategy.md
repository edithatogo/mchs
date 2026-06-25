# Binding Strategy: Stata Interoperability

## Decision

Use a file-based exchange and CLI invocation strategy for Stata
interoperability. Stata users read pre-computed calculator outputs as CSV or
Parquet and invoke the shared-core CLI through the `mchs.ado` adapter, which
uses Stata's `shell` boundary. No Stata formula port (`.do` files with
calculator logic) is created.

This follows the polyglot Rust core roadmap and reuses the CLI/file interop
contract established by the shared core.

## Rationale

- Stata is widely used in Australian health-economics for costing studies,
  NWAU analysis, and NHCDC reporting. A Stata formula port would duplicate
  calculator logic and split validation effort.
- CSV and Parquet interchange is already supported by the CLI/file contract
  and is natively readable in Stata via `import delimited` or the `parquet`
  Stata package.
- CLI invocation from Stata (`mchs run ...`) gives a zero-build path for Stata
  users who already run the shared-core CLI.
- Stata's `frame` and `frames` commands can hold pre-computed results for
  comparison against existing Stata costing scripts.
- No Stata SSC publication is needed for local adapter validation. Package
  publication is a later registry decision.

## Contract shape

### Integration modes

| Mode          | Consumer                    | Transport       | Notes                            |
|---------------|-----------------------------|-----------------|----------------------------------|
| File import   | Stata `import delimited`    | CSV             | Primary mode; zero-dependency    |
| File import   | Stata `parquet` package     | Parquet         | Requires `ssc install parquet`   |
| CLI invocation| `mchs run` / Stata `shell`   | CLI stdout/json | Cross-platform; thin Stata adapter |
| DTA exchange  | Stata `save`/`use`          | .dta            | Native format for Stata users    |

### CSV/Parquet schema contract

Stata reads the same CSV and Parquet schemas produced by the CLI/file interop
track:

- `contract_version` — pinned calculator contract version
- `calculator_id` — public calculator identifier
- `pricing_year` — target IHACPA pricing year
- `input_schema` — structured input columns matching the calculator contract
- `output_schema` — computed output columns with diagnostic flags
- `provenance` — shared-core version, source archive hash, generation timestamp
- `fixture_gate` — declared synthetic-only or local-only gate

### CLI invocation pattern (Stata)

```stata
mchs run using "acute_input.csv", calculator(acute) year(2025) output("results.csv") replace import clear
mchs validate
```

### DTA export workflow

When Stata-native analysis is required, the shared-core CLI can export Parquet
or CSV that Stata saves as `.dta` for downstream use. The shared core does not
write `.dta` directly.

## Supported calculators

All calculators exposed through the CLI/file interop track are accessible from
Stata. No Stata-specific calculator packaging is required.

## Limitations

- Stata does not execute calculator logic. All computation happens in the
  shared core before file exchange.
- CLI invocation from Stata on Windows requires PATH configuration. The
  `winexec` command may need full binary paths.
- The `parquet` Stata package is community-maintained and version-dependent.
  CSV is the recommended portable format.
- The repository maintains only a thin Stata `.ado` adapter for file import,
  CLI invocation, and boundary validation. No Stata `.ado` file, Mata
  function, or SSC package contains formula logic.

## Versioning

- Stata interop workflows pin to the CLI/file interop contract version for
  file schemas.
- Output files declare `contract_version` and `pricing_year` as metadata
  columns for Stata frame matching.
- No separate Stata interop version is needed.

## Diagnostics and provenance

- File outputs include full provenance columns readable in Stata as string
  variables.
- CLI invocation captures diagnostic output that Stata users can review
  in the Stata results window or redirect to a log file.
- Provenance metadata supports traceability from Stata frames back to shared
  core execution.

## Privacy and synthetic examples

- All committed Stata example manifests and test CSV files are synthetic.
- Real IHACPA pricing data or patient-level extracts are never committed as
  Stata examples.
- The `fixture_gate` column distinguishes synthetic examples from local-only
  real data.

## When to use Stata interop vs. native bindings

Use Stata interop when:
- the consumer is a health-economics or policy analyst working in Stata
- the workflow compares shared-core results against existing Stata scripts
- the team standardises on Stata for costing-study analysis

Prefer CLI/file interop or native bindings when:
- the consumer does not use Stata
- the integration needs sub-second or in-process calculator calls
- the deployment target is fully automated (no interactive Stata session)

## Readiness bar

- This track remains transport-only: Stata code validates the file/CLI
  boundary and delegates every calculation to the shared core.
- Interop workflows are documented and validated against shared golden
  fixtures where those fixtures are available.
- Do not claim Stata package publication until a CSV-import or CLI-invocation
  example has registry-owner evidence beyond synthetic fixtures.
