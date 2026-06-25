# Track r_binding_20260512 Context

- [Strategy](./strategy.md)
- [CI Notes](./ci_notes.md)
- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)

## Current State

- Initial strategy selects a thin R wrapper over the shared CLI with CSV file
  interchange today and Arrow/Parquet as the later large-batch target.
- `r-binding/` contains a minimal `nwauR` package scaffold with wrapper-only
  helpers, `testthat` guardrails, and minimal Rd documentation.
- The R layer shells out to `python -m nwau_py.cli.main`; it does not duplicate
  formula logic, adjustment logic, or validation rules.
- R Markdown/Quarto tutorial documentation uses synthetic fixture data and
  avoids CRAN-readiness claims.
- Local `R CMD check --no-manual --no-build-vignettes r-binding` passed with
  only the standard source-directory NOTE.
