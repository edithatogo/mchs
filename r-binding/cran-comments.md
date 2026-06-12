## Test environments

* local macOS aarch64, R 4.6.0
* 2026-06-12 temp-directory `R CMD build` and `R CMD check --no-manual`: OK
* 2026-06-12 temp-directory `R CMD build` and `R CMD check --as-cran`: 2 NOTEs

## R CMD check results

0 errors | 0 warnings | 0 notes for `R CMD check --no-manual`.

`R CMD check --as-cran` produced 2 NOTEs:

* CRAN incoming feasibility reports this as a new submission.
* Local HTML validation was skipped because the installed `tidy` is not recent
  enough for HTML validation.

Latest `--as-cran` checked artifact SHA-256:

`a081781f26e2652bc085e0e852399a180ac6a2187684e8c0cec5d8448b80e9cc`

## Submission notes

This is a new submission.

`nwauR` is a thin R wrapper around the separately distributed `nwau-py`
Python command line interface. The R package does not reimplement funding
formulas and does not bundle proprietary or licensed calculator inputs.

Python is treated as an external system requirement. Tests avoid requiring a
working `nwau-py` installation on CRAN infrastructure and validate wrapper
behavior that is independent of external calculator data.
