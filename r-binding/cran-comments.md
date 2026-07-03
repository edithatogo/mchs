## Test environments

* local macOS aarch64, R 4.6.0
* 2026-06-13 temp-directory `R CMD build` and `R CMD check --as-cran`: 1 NOTE

## R CMD check results

0 errors | 0 warnings | 0 notes for `R CMD check --no-manual`.

`R CMD check --as-cran` produced 1 NOTE:

* CRAN incoming feasibility reports this as a new submission. Maintainer is `Dylan Mordaunt <dylan.mordaunt@vuw.ac.nz>` for CRAN confirmation.

Latest `--as-cran` checked artifact was built from `r-binding` on 2026-06-13.

## Submission notes

This is a new submission.

`nwauR` is a thin R wrapper around the separately distributed `nwau-py`
Python command line interface. The R package does not reimplement funding
formulas and does not bundle proprietary or licensed calculator inputs.

Python is treated as an external system requirement. Tests avoid requiring a
working `nwau-py` installation on CRAN infrastructure and validate wrapper
behavior that is independent of external calculator data.
