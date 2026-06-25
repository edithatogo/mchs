# MATLAB interop adapter

This directory contains the published MATLAB interop adapter for
numerical, simulation, teaching, and legacy analytics consumers. It is ready
for source-bundle review and is published on MathWorks File Exchange as
version `0.1.0`.

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
- Implementing MATLAB-native formula engines beyond the published interop
  helper boundary

## Layout

- `mchs/`: MATLAB functions that validate file boundaries, import CSV/Parquet
  results, and invoke an external shared-core CLI
- `examples/`: MATLAB `.m` examples showing CLI invocation and file import
  patterns
- `matlab-interop-notes.md`: Numerical analytics workflow notes
- `mchs-matlab-interop-0.1.0.zip`: source upload bundle used for File
  Exchange publication and local replacement evidence

## File Exchange publication

The upload bundle includes the adapter functions, examples, notes, submission
metadata, README, and MIT license. It was published on 2026-06-13:

- File Exchange URL: <https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop>
- File Exchange id: `184067`
- Add-on UUID: `91133d3e-f475-413c-85bc-544188a60074`
- Version: `0.1.0`
- Bundle SHA-256: recorded in
  `conductor/tracks/matlab_file_exchange_submission_20260524/metadata.json`

Validate the local bundle from the repository root with:

```sh
unzip -l bindings/matlab/mchs-matlab-interop-0.1.0.zip
shasum -a 256 bindings/matlab/mchs-matlab-interop-0.1.0.zip
```

MATLAB/Octave are not installed in this local environment, so runtime execution
is not claimed here.

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
