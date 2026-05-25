# MATLAB Interop Numerical Analytics Workflow Notes

## Overview

MATLAB users consume shared-core calculator outputs through file exchange
(CSV/Parquet/MAT) or CLI invocation (`system()` / `!`). The repository does not
maintain MATLAB `.m` files containing funding formulas or calculation routines.

## Recommended workflows

### 1. CLI invocation (primary)

```matlab
[status, cmdout] = system('mchs-calc --calculator nwau --pricing-year 2026 --output results.csv');
T = readtable('results.csv');
```

Use for:
- One-off or batch calculator runs from the MATLAB command window.
- Automated scripts where the CLI is available on PATH.
- Cross-platform workflows (macOS, Linux, Windows with PATH configuration).

### 2. CSV file import (primary)

```matlab
T = readtable('results.csv');
```

Use for:
- Re-analyzing pre-computed outputs generated outside MATLAB.
- Sharing results with teams that do not use the CLI directly.
- Zero-build integration; no add-ons required.

### 3. Parquet file import (alternative)

```matlab
T = parquetread('results.parquet');
```

Use for:
- Large tabular datasets where columnar storage improves I/O.
- Users with the MATLAB Parquet toolbox (R2019b+).

### 4. MAT exchange (fallback)

```matlab
load('results.mat');
```

Use for:
- Native MATLAB users who prefer `.mat` format.
- Archiving processed results alongside MATLAB analysis scripts.
- MATLAB-only downstream toolboxes (Statistics, Optimization, etc.).

### 5. C ABI MEX (future path)

Documented but not implemented. Would require:
- A Rust `cdylib` build exposing the calculator ABI.
- MATLAB `mex` configuration matching the Rust compiler toolchain.
- `loadlibrary` / `calllib` for in-process execution.

## Supported calculators

All calculators supported by the shared core are accessible through the
file-import and CLI-invocation modes:

- acute
- adjust
- community_mh
- ed
- mh
- outpatients
- subacute

## Provenance and diagnostics

- All file outputs include provenance columns readable in MATLAB as table
  variables.
- CLI invocation captures diagnostic output visible in the MATLAB command
  window or redirectable to a log file.
- Provenance metadata supports traceability from MATLAB tables back to
  shared-core execution.

## Limitations

- MATLAB does not execute calculator logic. All computation happens in the
  shared core before file exchange.
- CLI invocation on Windows requires PATH or full binary path configuration.
- Parquet requires R2019b+ with Parquet support files; CSV is the recommended
  portable format.
- No MATLAB App Designer apps or Live Scripts containing funding formulas are
  maintained in this repository.

## Privacy

- All committed MATLAB example manifests and test files are synthetic.
- Real IHACPA pricing data or patient-level extracts are never committed as
  MATLAB examples.
- The `fixture_gate` column distinguishes synthetic examples from local-only
  real data.

## When to use MATLAB interop vs. other bindings

Use MATLAB interop when:
- The consumer is a numerical modeller, educator, or legacy MATLAB analyst.
- The workflow requires MATLAB toolboxes (Statistics, Optimization, etc.)
  for post-processing.
- The team standardises on MATLAB for teaching or research workflows.

Prefer CLI/file interop or native bindings when:
- The consumer does not use MATLAB.
- The integration needs sub-second or in-process calculator calls.
- The deployment target is fully automated (no MATLAB license).
- The consumer needs a language-agnostic integration surface.

## References

- `contracts/matlab-interop-binding/matlab-interop-binding.contract.json`:
  Full MATLAB interop binding contract.
- `contracts/matlab-interop-binding/binding_strategy.md`:
  Binding strategy decision and rationale.
- `bindings/matlab/examples/`:
  MATLAB `.m` skeletons showing CLI invocation and file import patterns.
