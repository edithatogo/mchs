# Julia Readiness

## Recommendation

Use a wrapper-first or kernel-prototype strategy by default. A full Julia port
should only be considered if Julia-native demand, benchmark evidence, and
shared-fixture parity justify a second calculator source of truth.

## Minimum Readiness Bar

- `Project.toml` with explicit `[compat]` bounds.
- `Manifest.toml` for reproducible environments.
- Standard package layout with `src/<Package>.jl`.
- `test/runtests.jl` and coverage-bearing tests.
- `Documenter.jl` docs.
- Registry-ready metadata, release automation, and CI.

## Gate

Do not claim a Julia release path until the package or kernel can consume the
shared calculator contract and fixtures, and pass registry-quality CI.

