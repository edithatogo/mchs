# Public Readiness

## Purpose

This document captures the contributor, security, and citation guidance that
must remain true for public publication and future Rust expansion.

## Contributor Path

- Use the current Python and docs workflow as the baseline contributor gate.
- Add Rust checks to the contributor path as soon as Rust changes are part of
  the active implementation surface.
- Keep the docs-site build and link validation in the public publishing path.

## Security Guidance

- Examples, screenshots, and docs content must stay synthetic or
  de-identified.
- Do not encourage patient-level uploads in browser workflows or public docs.
- Keep real-data workflows behind a secured service boundary.

## Citation Guidance

- Validation claims should cite the fixture pack, source artifact, or validation
  record that supports the claim.
- Prefer explicit calculator, year, and fixture identifiers.
- Avoid broad year-level claims when the evidence is calculator-specific.

## Public Repo Hygiene

- Keep the public docs front door on Starlight/GitHub Pages.
- Record unresolved public-readiness gaps as follow-on work when the required
  governance files are not yet present.
- Treat `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff`,
  and `SECURITY.md` as readiness items even when they are still missing.

## Maven Central Readiness

- Do not claim Maven Central readiness for JVM/Kotlin/Scala surfaces until the
  Central Portal namespace is registered, signing credentials are provisioned,
  and the repository contains the required Gradle publishing metadata.
- Required Gradle metadata includes `maven-publish`, `signing`, and the POM
  coordinates and descriptor fields needed for a publishable module.
- If those inputs are still absent, record the gap as a remaining blocker
  rather than as an implied publishing claim.
