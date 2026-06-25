# Standards Matrix: Ecosystem Language Readiness

This file records the 2026-05-07 repository surface inventory and the decision
criteria implied by the ecosystem-readiness specification. It is intentionally
conservative: implemented surfaces are separated from architecture-only or
missing surfaces, and package/version-management claims stay limited to what
was present in the repository snapshot.

Later binding, registry, and package-surface ownership tracks supersede this
matrix where they provide newer implementation or publication evidence.

## Current Repository Surfaces

| Surface | Current repository artifacts | Package/version management today | SOTA fit for the ecosystem | Gap or next decision |
|---|---|---|---|---|
| Python package and CLI | `pyproject.toml`, `uv.lock`, `requirements.txt`, `requirements-dev.txt`, `ty.toml`, `mypy.ini`, `renovate.json`, `.github/workflows/*.yml` | `uv` with a committed lockfile is the authoritative package manager; dependency groups separate runtime, test, coverage, typing, property, mutation, profiling, and docs concerns | Good snapshot baseline, though transitional files still exist | Keep the locked `uv` workflow as the source of truth and retire transitional packaging files when migration is complete |
| docs-site | `docs-site/package.json`, `docs-site/package-lock.json`, `.github/workflows/docs-site.yml` | npm lockfile plus GitHub Actions build/link-check/deploy workflow; Node is pinned in workflow rather than in the package manifest | Reasonable current baseline with GitHub Pages readiness evidence, but not fully SOTA because version policy lives outside the package manifest | Add manifest-level `packageManager` and `engines` pinning if the docs site remains a long-lived surface; see the archived Starlight docs-site track for the completed implementation path |
| C# calculation engine | Architecture/boundary documentation only; no executable implementation surface found | No solution, project, or NuGet manifests found | Not ready | Need executable solution/project files, SDK pinning, NuGet strategy, deterministic builds, Source Link, and fixture parity before any readiness claim |
| Power Platform adapter | Orchestration-only architecture/boundary documentation; no executable implementation surface found | No solution or package artifacts found | Not ready | Need solution packaging, managed solution ALM, and a secure service boundary backed by the C# engine before readiness claims |
| R package or wrapper | No package artifacts found | None | Not ready | Decide wrapper versus full port only after shared contract and fixture parity are established |
| Julia package or kernel complete-with-gaps prototype | No package artifacts found | None | Not ready | Default to a wrapper-first or kernel-prototype path; consider a full port only if shared contract parity exists and Julia-native demand or performance need is proven |
| Health interoperability standards | Documentation-only standards guidance | None | Not applicable as an implementation surface | Treat ICD-10-AM, ACHI, ACS, AR-DRG, HL7 v2, FHIR, and IHE as standards guidance until a separate connector or PAS integration track exists |

## Standards and Decision Criteria

| Surface | Minimum standards expected | Decision rule |
|---|---|---|
| Python | `pyproject.toml` plus `uv.lock`, pinned CI, coverage reporting, docs, validation tooling, and release/governance evidence | Treat as the current authoritative implementation surface while the transitional compatibility files remain clearly labeled |
| docs-site | `package.json` plus `package-lock.json`, workflow-pinned Node/npm, reproducible build/deploy, and link validation; manifest-level `packageManager` and `engines` are an improvement item | Treat as implemented and GitHub Pages-ready, but keep manifest-level version pinning as an improvement item and align with the archived Starlight track |
| C# | `.sln`/`.csproj`, `global.json`, NuGet/package strategy, Source Link, deterministic builds, symbols, and shared fixture parity | Defer until executable parity and packaging evidence exist |
| Power Platform | Solution files, ALM/promotion workflow, custom connector boundary, and a secure service-backed calculation boundary that remains orchestration-only | Defer until the C# engine and solution packaging are in place |
| R | Standard R package structure with `DESCRIPTION`, `NAMESPACE`, `R/`, and `tests/testthat/`; `roxygen2`, `testthat`, `pkgdown`, CRAN-style checks, and reverse-dependency awareness | Defer or treat as wrapper-only unless a port is justified by usage demand and parity evidence |
| Julia | `Project.toml`, `Manifest.toml`, `src/<Package>.jl`, `test/runtests.jl`, `test/Project.toml` when appropriate, `Documenter.jl`, `Registrator`, `TagBot`, `[compat]`, CI coverage, and registry-ready packaging conventions | Prefer wrapper-first or kernel-prototype delivery; treat a full port as justified only when Julia-native demand, benchmark evidence, and fixture parity all exist |
| Health interoperability | ICD-10-AM, ACHI, ACS, AR-DRG, HL7 v2, FHIR R4/R5 watch-list, IHE PAM/PDQ/PIX/PIXm/PDQm/PMIR, openEHR watch-list, CDA watch-list | Treat as advisory standards guidance until a separate implementation track defines connector or PAS scope |

## Scope Notes

- Python and docs-site were the only language/package surfaces with concrete
  manifests in this snapshot.
- C#, Power Platform, R, and Julia were represented by track documentation or
  architecture notes only in this snapshot; later tracks may supersede this
  inventory.
- The matrix is a dated snapshot inventory, not a promise of future support.
- The matrix distinguishes implemented, documented-only, missing, and deferred surfaces.
- The docs-site entry should be interpreted together with the archived Starlight
  docs-site track: [Starlight Documentation Site and Versioning](../archive/starlight_docs_site_20260506/spec.md).
- Package/version management evidence precedes any language readiness claim.
- For Julia specifically, the ecosystem bar is: standard package layout,
  explicit compat bounds, coverage-bearing tests, package docs, registry-ready
  metadata, and release automation before any readiness claim is made.
- A Julia kernel is only worth considering if it can stay behind the shared
  public contract and fixture layer; a full port is only worth considering if
  a Julia-native audience justifies maintaining a second calculator source of
  truth.
