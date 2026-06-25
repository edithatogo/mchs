# Python, Docs-Site, and Publication Readiness

## Python Package Readiness

The Python surface is the current authoritative implementation and the most
plausible candidate for pyOpenSci-style review.

Current readiness bar:

- `pyproject.toml` plus committed `uv.lock` with PEP 621-style metadata and a
  supported-Python declaration that matches the CI matrix.
- CI coverage across the supported Python matrix, with tests and coverage
  reporting visible on pull requests.
- `ruff` and `ty` as the active quality gates, with `mypy` treated as
  transitional comparator tooling only.
- Hypothesis, mutmut, and Scalene available for deeper validation without
  slowing the normal PR path.
- Documentation that explains install, usage, validation, and the supported
  calculator scope.
- Community and governance files such as `LICENSE`, `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, and `CITATION.cff` where publication readiness is
  being claimed.
- Transitional compatibility files clearly labeled as transitional rather than
  authoritative.

## Docs-Site Readiness

The docs site is an implemented public surface and should be treated as a
long-lived package-managed deliverable. The archived Starlight docs-site track
captures the completed implementation path and should be referenced when the
docs-site surface is evaluated:
[Starlight Documentation Site and Versioning](../archive/starlight_docs_site_20260506/spec.md).

Recommended improvements:

- Keep `docs-site/package-lock.json` committed and treat it as the current
  package-version evidence for the surface.
- Add manifest-level `packageManager` and `engines` pinning so the package
  manifest, not only the workflow, defines the supported build toolchain.
- Keep the GitHub Actions build, link-check, and deployment workflow
  reviewable and reproducible so GitHub Pages deployment readiness remains
  explicit.
- Keep Starlight plugins minimal and justified.
- Treat the docs site like a versioned release artifact rather than a loose
  markdown folder.

## Publication Readiness

If the project targets scientific-software publication or review venues:

- Add `CITATION.cff`.
- Add or verify `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`.
- Ensure the repository has a clear statement of need, public issue/PR
  workflow, and a license that meets venue expectations.
- Keep evidence-backed validation claims in release notes and docs.
- Consider JOSS-style publication readiness only when the citation,
  governance, documentation, and public-history prerequisites are complete.
