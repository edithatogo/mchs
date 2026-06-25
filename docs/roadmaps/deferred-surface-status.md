# Deferred Surface Status

Roadmap snapshot: checked against registry evidence through 2026-06-25.

This document defines how to describe surfaces that exist as specs,
contracts, examples, package manifests, or local scaffolds but are not
supported product surfaces.

## Support Vocabulary

Use canonical support states in public support documents:

| Status | Meaning for deferred surfaces |
| --- | --- |
| `planned` | Work is intended, but implementation or validation has not started. |
| `deferred` | Work is intentionally paused behind an explicit owner, audience, contract, parity, or release gate. |
| `blocked` | Work cannot advance because source, license, fixture, parity, implementation, or release evidence is missing. |
| `preview` | Local or pre-release implementation exists, but default support is not claimed. |
| `no_new_development` | Retained for traceability, with no active implementation path. |
| `historical` | Prior context retained; not an active product commitment. |
| `unsupported` | The project does not intend to support the surface in the declared scope. |

`private` is release-visibility vocabulary used by package and registry docs,
not a canonical support status. When a private scaffold appears in support
docs, map it to the narrowest truthful support state: usually `planned`,
`deferred`, `blocked`, or `no_new_development`.

`scaffold-only`, `roadmap-only`, `not-ready`, `future-only`, and
`complete-with-gaps` are remediation labels. They must be translated to one of
the canonical states above when used in README, Starlight docs, package
metadata, or registry-facing material.

## Current Deferred Surface Map

| Surface | Current public/release state | Reason | Next action |
| --- | --- | --- | --- |
| R | `planned`/`private` | Local CLI/file wrapper exists, but CRAN/release evidence and owner gates are unresolved | Keep as thin consumer of Rust core or file contract after Rust parity. |
| Julia | `preview` | Julia General publication evidence exists for `NationalWeightedActivityUnitWrapper 0.1.0`; runtime support remains limited to thin-adapter and fixture-parity scope | Keep fixture parity and packaging checks current before broader support claims. |
| C#/.NET | `preview` | NuGet publication evidence exists for `Mchs.Bindings.DotNet 0.1.0`; runtime support remains limited to the thin adapter contract | Keep wrapper thin and require repeatable signed package evidence for later releases. |
| Go | `no_new_development`/`private` | Local service and binding-file adapters exist, but cross-compilation and audience evidence remain unresolved | Do not promote until owner and end-to-end CI exist. |
| TypeScript/WASM | `preview` | npm publication evidence exists for `@edithatogo/mchs-wasm-binding 0.1.0`; deterministic Rust WASM runtime support remains separate | Keep browser/Node smoke tests and artifact release evidence current before broader support claims. |
| Kotlin/Native | `deferred`/`private` | File-boundary request validation exists, but native target ownership and release evidence are unresolved | Keep boundary-only until stable C ABI/service/file execution and target CI are proven. |
| Scala/Spark | `deferred`/`private` | Transport-boundary adapters exist, but live Spark/JVM fixture validation and owner evidence are missing | Keep boundary-only; no Spark formula logic. |
| Swift | `preview` | Swift Package Index publication evidence exists for `MCHSBind 0.1.0`; Apple-platform runtime support remains owner/audience and fixture gated | Keep platform fixtures, owner, and compatibility-build evidence separate from publication. |
| Stata | `preview` | SSC/RePEc publication evidence exists for package `mchs`; local Stata runtime validation is not claimed | Keep ado/do commands boundary-only and require Stata runtime proof for stronger support. |
| MATLAB | `preview` | MATLAB File Exchange publication evidence exists for add-on `184067`; local MATLAB/Octave runtime validation is not claimed | Keep numerical examples as contract consumers only and require runtime proof for stronger support. |
| SQL/DuckDB | `historical` unless reprioritized | Prior context exists but not an active GA dependency | Retain only as traceability until a new owner appears. |
| SAS interop | `private`/`no_new_development` | Licensed-source boundaries and no public artifact evidence | Keep exchange boundaries local-only. |
| Power Platform | `deferred`/`private` | Source-controlled connector contract exists, but tenant ALM and credentialed validation are external gates | Do not put formula logic in apps, flows, or expressions. |
| Web demos | `preview` | Demo surface is not a computation authority | Call shared artifacts or file contracts only. |
| Package registries without verified public evidence, including CRAN, conda-forge, vcpkg, and ConanCenter | `blocked` or `submitted_not_published` until registry pages exist | Submission files are not publication evidence | Link immutable registry pages before claiming publication. |

## Claim Rules

- A package manifest is not registry publication evidence.
- A contract schema is not implementation evidence.
- A synthetic fixture is not source parity evidence.
- A local-only placeholder is not redistributable data.
- A binding is complete only if it delegates to the shared core, Python
  baseline, or approved service/file contract.
- A surface cannot be more supported than the stream/year/runtime it calls.

## Next Actions

1. Keep the README package registry table as the public summary of registry
   claims.
2. Keep support-state docs synchronized with `contracts/support/support-matrix.json`
   and Starlight support pages.
3. For every deferred surface, name the unblocker: owner, audience, contract,
   fixture, CI, packaging, or registry evidence.
4. Promote surfaces only after validation commands and evidence links exist.
