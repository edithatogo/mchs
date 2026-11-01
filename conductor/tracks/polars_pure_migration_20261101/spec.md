# Specification: Pure Polars Migration & Pandas Decommissioning

## Objective
Drop the `pandas` dependency completely from `nwau_py`, standardizing the entire tabular pipeline on native Polars (`pl.DataFrame`, `pl.LazyFrame`) and Arrow. Retain `narwhals` exclusively at outer library boundaries to accept heterogeneous caller objects without depending directly on `pandas`.

## Requirements
1. **Zero Pandas Footprint:**
   - Remove `pandas` from `dependencies` in `pyproject.toml` and synchronize `uv.lock`.
   - Replace every `import pandas as pd` across `nwau_py/calculators/`, `nwau_py/groupers/`, `nwau_py/data/`, and `nwau_py/bundles.py` with native Polars expressions.
2. **Clarification of SAS Macro Terminology:**
   - Confirm that historical mentions of `xarray` in the repo refer strictly to SAS macro arrays (`array DDXARRAY &DIAG_PREFIX:;`) and that no Python `xarray` dependency exists or should ever be introduced.
3. **LazyFrame & Streaming Execution:**
   - Weight table lookups and adjustment joins must evaluate lazily via Polars expressions to avoid memory allocations on large cohort batches.
   - Parquet read and write paths must use native Polars streaming writers.
4. **Validation:**
   - Run the complete 820-test pytest suite in an environment where `pandas` is not installed or unimported, ensuring 100% parity against SAS golden fixtures.
