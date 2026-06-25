# R Ecosystem Readiness

## Recommendation

Use a wrapper-first strategy by default. A full R port should only be
considered if there is sustained demand for R-native workflows or a
distribution need that cannot be met by wrapping the authoritative engine.

## Minimum Readiness Bar

- Standard R package structure with roxygen2 documentation.
- pkgdown site for package and vignette documentation.
- testthat-based tests covering success paths, error paths, warnings, messages,
  and edge cases.
- Clean `R CMD check` across the supported operating systems relevant to the
  package behavior.
- Reverse-dependency checks before releases once downstream consumers exist.
- Specific, evidence-backed validation claims only.

## Community Expectations

- Include `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md` guidance.
- Keep authorship, licensing, and governance clear.
- Treat reverse dependencies as a release concern, not an afterthought.

## Port Gate

Do not claim an R release path until the package or wrapper can consume the
shared calculator contract or authoritative engine, run shared golden fixtures
or equivalent contract tests, and pass release-quality CI.
