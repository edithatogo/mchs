# nwauR

`nwauR` is a lightweight R wrapper around the separately distributed `nwau-py`
calculator CLI. It does not reimplement the funding formulas in R. Instead it
passes CSV input to Python, lets the existing calculator run, and reads the
resulting CSV back into R.

This keeps the R surface lightweight and conservative while preserving a
single source of truth for the calculation logic.

## What this package provides

- `nwau_calculate()` for generic batch execution
- `nwau_acute()`, `nwau_ed()`, and `nwau_non_admitted()` convenience helpers
- `nwau_diagnose()` for CLI-oriented validation diagnostics

## Requirements

- R 4.1 or newer
- Python 3.10 or newer with the `nwau-py` package available on the selected interpreter
- Calculator reference data supplied separately through the Python package or
  the `params` argument. Licensed source data is not bundled with this R
  package.

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

Run CRAN-oriented checks from the repository root:

```sh
R CMD build r-binding
R CMD check --as-cran nwauR_0.1.0.tar.gz
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

## Boundary

This package is intentionally wrapper-only.

- Formula logic stays in Python
- Input validation stays in Python
- R is only responsible for file handoff, process invocation, and result loading
