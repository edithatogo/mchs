# MATLAB interop adapter

This directory contains a synthetic, non-published MATLAB interop adapter for
numerical, simulation, teaching, and legacy analytics consumers.

Scope:

- File import (CSV/Parquet) helpers for MATLAB `readtable`/`parquetread`
- CLI invocation helper for MATLAB `system()` / `!`
- Documented MAT-exchange workflow for MATLAB `save`/`load`
- C ABI MEX documented as a future path

Out of scope:

- Formula parsing and evaluation
- Calculator rule implementation or funding formulas
- MATLAB `.m` files containing calculation routines
- Repo-wide build or release wiring
- MATLAB toolbox release or Add-On Explorer submission

## Layout

- `mchs/`: MATLAB functions that validate file boundaries, import CSV/Parquet
  results, and invoke an external shared-core CLI
- `examples/`: MATLAB `.m` examples showing CLI invocation and file import
  patterns
- `matlab-interop-notes.md`: Numerical analytics workflow notes

## Usage

```matlab
% File import (primary mode)
T = importResultTable("results.csv");

% CLI invocation (primary mode)
run = invokeCli("mchs-calc", "CalculatorId", "nwau", "PricingYear", "2026", "OutputPath", "results.csv");
T = importResultTable(run.outputPath);
```

The interop only moves data across file or CLI boundaries. It does not compute
formula results or mutate formula expressions.
