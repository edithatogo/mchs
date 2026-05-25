# Stata Interoperability Notes

## Health-Economics Workflow Context

These notes document how Stata users in Australian health-economics
settings can integrate shared-core calculator outputs without duplicating
calculator logic.

## Transport Modes

| Mode | Stata Command | Format | Dependency |
|------|---------------|--------|------------|
| File import | `import delimited` | CSV | None |
| File import | `parquet` | Parquet | `ssc install parquet` |
| CLI invocation | `mchs run` / `shell` | CLI stdout | `funding-calculator` on PATH |
| DTA exchange | `save` / `use` | .dta | None |

## CSV Schema Contract

The shared-core CLI produces CSV with the following columns:

- `contract_version` — pinned calculator contract version
- `calculator_id` — public calculator identifier
- `pricing_year` — target IHACPA pricing year
- `input_schema` — structured input columns
- `output_schema` — computed output columns with diagnostic flags
- `provenance` — shared-core version, source archive hash, timestamp
- `fixture_gate` — declared synthetic-only or local-only gate

## CLI Invocation from Stata

```stata
* Basic usage
mchs run using "acute_input.csv", calculator(acute) year(2025) output("acute_results.csv") replace import clear
mchs validate

* With specific calculator
local calc "acute"
local year 2025
mchs run using "`calc'_input.csv", calculator(`calc') year(`year') output("`calc'_`year'.csv") replace
mchs import using "`calc'_`year'.csv", clear
```

## DTA Export Workflow

After importing CSV/Parquet results into Stata:

```stata
* Save for downstream analysis
save results_2026.dta, replace

* Frame-based comparison
frame create expected
frame expected: import delimited using expected_2026.csv, clear
cf _all using expected, verbose
```

## Windows Considerations

- On Windows, `winexec` may need full binary paths:
  ```stata
  mchs run using "acute_input.csv", calculator(acute) year(2025) output("acute_results.csv") cli("C:\path\to\funding-calculator.exe") replace
  ```
- Ensure the shared-core binary directory is on the system PATH.

## Limitations

- The shared core does not write `.dta` files directly. Stata users
  export from CSV/Parquet after import.
- The `parquet` Stata package is community-maintained. CSV is the
  recommended portable format for reproducibility.
- The repository maintains a thin `.ado` file-boundary adapter only. No Stata
  calculator logic, formula port, or SSC package is maintained here.

## Privacy

- All example CSV/Parquet files and manifests in this repository are
  synthetic. Real IHACPA pricing data or patient-level extracts are
  never committed as Stata examples.
- Use the `fixture_gate` column to distinguish synthetic examples from
  local-only real data.
