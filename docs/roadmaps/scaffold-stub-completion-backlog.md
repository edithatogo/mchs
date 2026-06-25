# Scaffold and Stub Completion Backlog

Roadmap snapshot: 2026-05-24.

This document is the support-state companion for the Scaffold and Stub
Completion Backlog track. It does not mark scaffolded work as complete. It
records how unfinished surfaces should be named until implementation,
validation, documentation, and release evidence exist.

## Product Versus Scaffold

| Surface | Current evidence | Public claim |
| --- | --- | --- |
| Python package and Python calculator runtime | Published `nwau-py`, CLI entry point, Python calculator modules, 2024 and 2025 validation claims scoped in README | Real product for the declared Python runtime scope |
| Python CLI/file execution | `funding-calculator` and `python -m nwau_py.cli.main` paths exist | Real product for current Python workflows; not proof of a stable branded cross-language CLI contract |
| MCP stdio server | Local server code and registry metadata exist | Preview/local-use surface unless release and registry evidence are linked |
| Rust core | Local Rust workspace with acute 2025 canary kernel and bindings | Canary/preview implementation, not GA |
| C ABI | Local header and extern functions for acute 2025 shape | Preview scaffold over the Rust canary, not stable ABI support |
| TypeScript/WASM | npm publication evidence for `@edithatogo/mchs-wasm-binding 0.1.0` plus tested JavaScript adapter for WASM exports | Preview adapter; publication does not prove deterministic Rust WASM runtime support |
| Go, C#/.NET, Kotlin/Native, Scala/Spark, Swift, Stata, MATLAB | Local boundary adapters plus contracts/tests | Private/deferred adapters unless each surface has runtime, owner, packaging, and release evidence |
| R, Julia, Power Platform | Track specs, contracts, and/or local private surfaces | Planned, canary, or deferred until implementation and release evidence are complete |
| Registry submissions other than PyPI and confirmed MCP evidence | Submission plans or manifests without public registry pages | Not published until immutable registry evidence exists |

## Inventory Labels

These labels are backlog labels, not public support statuses:

| Label | Use | Required public mapping |
| --- | --- | --- |
| `real-product` | Implementation is usable in the declared scope and has validation evidence | `ga`, `preview`, or `opt_in`, depending on default support |
| `scaffold-only` | Files exist to reserve structure, contracts, examples, or packaging shape | `planned`, `deferred`, or `blocked` |
| `roadmap-only` | Intent exists only in docs or Conductor tracks | `planned`, `deferred`, or `no_new_development` |
| `complete-with-gaps` | Prior completion claim exists but evidence is incomplete | `blocked`, `canary`, or `preview` until gaps close |
| `not-ready` | Implementation may exist, but release, parity, or support gates are missing | `blocked`, `canary`, `preview`, or `planned` |
| `future-only` | Useful future direction with no active implementation owner | `deferred` or `no_new_development` |
| `quarantined` | Retained for reference but should not be linked as a supported surface | `historical` or `unsupported` |

Public docs should use the canonical statuses from
[Support Status Matrix](./schemas/support-status-matrix.md). Backlog labels may
appear only where the document is explicitly about remediation work.

## Current Completion Risks

- Completed-track metadata can outrun implementation evidence when a track has
  specs, contracts, and examples but no executable surface.
- Registry submission files can look like publication evidence before a public
  registry page exists.
- Thin language-adapter scaffolds can be mistaken for working packages.
- Synthetic examples and local-only licensed placeholders can be mistaken for
  parity fixtures.
- Rust canary code can be mistaken for Rust GA if docs do not name the stream,
  year, and runtime path.
- Support matrices can drift from README package tables and Starlight pages.

## Completion Evidence Gate

An item may move out of scaffold status only when all of these are true:

- Implementation files exist in the owned surface.
- Tests or documented validation commands cover the declared behavior.
- Documentation names the exact runtime, surface, stream, year, and limits.
- Support status is updated with the narrowest truthful canonical state.
- Registry or release claims link to immutable external evidence when the claim
  is about publication.
- Adapters prove they call the Rust core, Python baseline, or approved
  service/file contract instead of duplicating formula logic.

## Current Detector Baseline

As of 2026-05-26, the repo-local detector command is available at
`conductor/scripts/stub_detector.py` and the current scan reports zero
unresolved findings:

```bash
python conductor/scripts/stub_detector.py --root . --json
```

The remaining uses of `scaffold`, `placeholder`, and related wording are
retained where they describe deferred support states, local-only licensed asset
references, or governance rules. They are not treated as completion evidence.

## Next Actions

1. Keep the no-stub detector baseline at zero unresolved findings.
2. Map any new finding to `real-product`, `scaffold-only`, `roadmap-only`,
   `complete-with-gaps`, `not-ready`, `future-only`, or `quarantined`.
3. Reconcile known overclaim candidates before widening the inventory:
   `mcp_server_registry_submission_20260516`, `rust_core_ga_20260513`, and
   `rust_core_ga_post_cline_review_20260513`.
4. For retained scaffolds, create bounded follow-on implementation work with
   owner, evidence gate, validation command, and support-state update.
5. Keep README, Starlight support docs, and support matrices synchronized.
