# CI feasibility notes: R binding

Date: 2026-05-12

## Assessment

At this point, a full R CI workflow is not low-risk enough to add.

Current repository state now contains a minimal R package scaffold under
`r-binding/`:

- `DESCRIPTION`
- `NAMESPACE`
- `R/`
- `tests/testthat/`

There is still no pinned R dependency lockfile and no GitHub Actions R job.
That is intentional: a full `R CMD check` gate should wait until the CLI
installation path and fixture invocation story are stable enough for CI.

## Recommended stance

- Keep CI coverage conservative until the package dependency path is stable.
- Use Python text-contract tests and static R source scans now.
- Add workflow automation only after the package structure and CLI invocation
  path are stable enough to avoid brittle false failures.

## Safe future CI options

When the R binding is promoted beyond prototype status, prefer one of these
validation shapes:

1. Package-aware check job
   - Install R only after `DESCRIPTION` and `NAMESPACE` exist.
   - Run `R CMD check` or `devtools::check()` against a pinned dependency set.
   - Use `setup-r` or equivalent only when the package metadata is present.

2. Thin interface smoke test
   - Exercise a single CLI- or file-based entry point from R.
   - Keep the test fixture small and synthetic.
   - Avoid extendr or reticulate wiring until the binding choice is settled.

## Not recommended yet

- A workflow that unconditionally installs R packages on every push.
- A workflow that assumes CRAN/package manager availability for undeclared dependencies.
- A binding-specific check job before the R package surface is defined.

## Gate for adding CI

Add a real R workflow only after the binding has:

- a stable fixture set,
- an explicit dependency installation path,
- a reliable way to install or locate the shared CLI,
- and one successful local `R CMD check` run recorded in the track evidence.

## Local validation evidence

The prototype package was checked locally with:

```bash
R CMD check --no-manual --no-build-vignettes r-binding
```

Result: package install, namespace load/unload, Rd checks, and `testthat`
tests passed. The only remaining NOTE was the standard source-directory check
message: `Checking should be performed on sources prepared by R CMD build`.
