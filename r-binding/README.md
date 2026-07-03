# nwauR

`nwauR` is a minimal R wrapper around the authoritative `nwau_py` Python
calculator CLI. It does not reimplement the funding formulas in R. Instead it
passes CSV input to Python, lets the existing calculator run, and reads the
resulting CSV back into R.

This keeps the R surface lightweight and conservative while preserving a
single source of truth for the calculation logic.

## What this package provides

- `nwau_calculate()` for generic batch execution
- `nwau_acute()`, `nwau_ed()`, and `nwau_non_admitted()` convenience helpers
- `nwau_diagnose()` for CLI-oriented validation diagnostics
- `nwau_cli_contract()` for probing the shared CLI/file interop contract
- `validate_nwau_input()` for checking data frame or CSV handoff inputs before
  launching Python

## Requirements

- R 4.1 or newer
- Python 3 with the `nwau_py` package available on the selected interpreter
- The archived calculator data under `archive/sas/<YEAR>/`

The wrapper defaults to `python3` and the module `nwau_py.cli.main`. Override
either with R options:

```r
options(nwau.python = "/path/to/python")
options(nwau.module = "nwau_py.cli.main")
```

## Local development

From the repository root, load the package from the `r-binding/` directory:

```r
devtools::load_all("r-binding")
```

Or install it locally:

```r
install.packages("r-binding", repos = NULL, type = "source")
```

## Example

The repo includes a synthetic acute fixture at
`tests/fixtures/golden/acute_2025/input.csv`.

```r
library(nwauR)

acute_input <- "tests/fixtures/golden/acute_2025/input.csv"
acute_output <- nwau_acute(acute_input, year = 2025)
diagnostic <- nwau_diagnose(acute_input, year = 2025)
```

The returned `acute_output` is the Python-produced result CSV parsed into an R
data frame. Any validation failures come from the existing Python CLI.

## CLI/file boundary

The R adapter performs only boundary checks needed for reliable handoff:

- data frame inputs must have named columns
- file inputs must be existing `.csv` files
- output paths must target `.csv` files in existing directories
- successful CLI runs must produce a non-empty output CSV

Use `nwau_cli_contract()` to inspect the Python CLI/file contract exposed by
`python -m nwau_py.cli.main interop contract`.

## Boundary

This package is intentionally wrapper-only.

- Formula logic stays in Python
- Input validation stays in Python
- R is only responsible for file handoff, process invocation, and result loading
