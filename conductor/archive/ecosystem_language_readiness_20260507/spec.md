# Specification: Ecosystem Language and Community Readiness

## Goal

Create a dated repository-surface inventory and standards matrix that records
the package/version-management state as of 2026-05-07 for Python and docs-site,
the then-missing R/Julia/C#/Power Platform artifacts, and the decision criteria
implied by the ecosystem-readiness spec.

The project already has strong Python, fixture, provenance, and documentation
foundations. This track captures where those foundations are actually backed by
manifests and lockfiles today, where they are only described in architecture
docs, and what minimum standards would be required before any future language
surface could be described as ready.

## Snapshot Boundary

This track is an early ecosystem readiness snapshot. Later binding,
publication, and package-surface tracks supersede its inventory rows when they
provide newer implementation or registry evidence.

- Python was the only executable calculator package surface in this snapshot.
- Python packaging uses `pyproject.toml` plus `uv.lock`; `requirements*.txt`
  and `mypy.ini` remain transitional artifacts.
- The docs-site is an npm-managed Astro/Starlight surface with `package.json`
  and `package-lock.json`, and its current GitHub Pages workflow already
  provides build, link-check, and deployment evidence. The Node version policy
  still lives in the workflow rather than the package manifest.
- No R package, Julia package, C# solution/project, NuGet configuration, or
  Power Platform solution artifact existed in this snapshot.
- Existing C# and Power Platform material is architecture and boundary
  documentation, not executable implementation.
- Power Platform is treated as an orchestration surface only; calculation
  logic must remain behind a secure C# service boundary.
- Health standards are documented separately as advisory guidance rather than
  implementation evidence.
- The matrix must stay conservative and distinguish snapshot evidence from
  intended future direction.

## Standards and Decision Criteria

- **Python**: PyPA-style metadata and lockfile discipline, clear CI coverage,
  validation tooling, public documentation, citation metadata, and
  publication/community readiness criteria such as pyOpenSci where appropriate.
- **docs-site**: npm package metadata, lockfile discipline, manifest-level version
  pinning through `packageManager` and `engines`, reproducible build and
  deployment checks, and reviewable GitHub Pages delivery. See the
  archived Starlight track for the completed docs-site implementation path:
  [Starlight Documentation Site and Versioning](../archive/starlight_docs_site_20260506/spec.md).
  The docs-site maturity bar includes manifest-level version pinning.
- **C#**: solution/project layout, SDK pinning, NuGet strategy, deterministic
  builds, Source Link, symbols, and shared-fixture parity before any readiness
  claim.
- **Power Platform**: solution packaging, managed ALM, custom connector
  boundary, and a secure service-backed calculation layer while remaining
  orchestration-only before any calculation parity claim.
- **R**: wrapper or package decisions should wait for shared-contract parity
  and an rOpenSci/CRAN-style evidence base.
- **Julia**: wrapper, prototype, or package decisions should wait for shared-
  contract parity, package layout, `[compat]` bounds, and registry-ready
  evidence.
- **Health standards**: ICD-10-AM, ACHI, ACS, AR-DRG, HL7 v2, FHIR R4, IHE,
  and watch-list items remain advisory until a connector or PAS track is
  created.

## Decision Model

The roadmap must preserve the following order:

- Repository evidence precedes any statement about readiness.
- Package/version management evidence precedes any language readiness claim.
- Shared public contracts and golden fixtures precede any non-Python
  implementation claim.
- Docs-site versioning and deployment evidence must be separated from the
  Python package surface.
- The docs-site surface should be judged against the archived Starlight track
  while the snapshot npm/package-lock evidence and GitHub Pages workflow remain
  the evidence recorded here.
- C# engine packaging precedes any Power Platform calculation-parity claim.
- R and Julia remain wrapper, prototype, or deferred options unless parity and
  community evidence justify a fuller surface.

## Acceptance Criteria

- A standards matrix exists for the current repository surfaces.
- The matrix distinguishes implemented, documented-only, missing, and deferred
  surfaces.
- The matrix records the package/version-management approach for Python and
  docs-site.
- The matrix records the missing C#, Power Platform, R, and Julia artifacts.
- The matrix states the minimum standards or decision criteria for each
  surface.
- Guardrail tests verify the matrix file, the track docs, and the registry
  entry.

## Out Of Scope

- Implementing any R, Julia, C#, or Power Platform surface.
- Changing calculator behavior.
- Broadening validation claims beyond current repository evidence.
