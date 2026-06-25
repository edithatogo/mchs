# Roadmap Governance

## Purpose

The roadmap is now larger than a linear implementation queue. It covers
calculator parity, future IHACPA releases, classification systems, cost
buckets, Rust-core migration, polyglot bindings, Power Platform, repository
publication, and recurring audits. This document defines how those tracks are
grouped, sequenced, audited, and promoted from roadmap intent to validated
delivery.

## Track Classes

Use these classes when creating or auditing tracks.

| Class | Purpose | Examples | Completion Evidence |
| --- | --- | --- | --- |
| `governance` | Define rules, contracts, templates, and audit cadence | abstraction doctrine, recurring audit templates | docs, checks, accepted policy |
| `source-discovery` | Find, archive, and manifest official sources | IHACPA scanner, historical coverage | source table, URLs, hashes, gap records |
| `data-contract` | Define reusable schemas and manifests | reference-data manifests, formula bundles, coding registries | typed models, fixtures, docs |
| `validator` | Prevent unsupported claims and incompatible inputs | pricing-year gates, classification validation | tests, CI checks, failure diagnostics |
| `calculator` | Implement or update calculation behavior | 2026-27 support, community mental health | source parity, output parity, docs |
| `classifier` | Handle derived classifications and groupers | AR-DRG, UDG/AECC, AMHCC | version registry, adapter tests, provenance |
| `costing` | Support costing-study and NHCDC/AHPCS workflows | cost buckets, NHCDC ingestion | public-safe data, tutorials, caveats |
| `binding` | Expose shared behavior in another language/surface | R, Julia, C#, Go, WASM, C ABI | contract tests, packaging status |
| `publication` | Release, package, and repository readiness | PyPI, conda, Pages, GitHub metadata | passing workflows, registry evidence |
| `audit` | Re-evaluate state and create remediation tracks | repo SOTA audit, IHACPA discovery audit | findings table, remediations |

## Required Track Metadata

Every new track should state:

- Track class.
- MoSCoW requirement IDs from `requirements.md`.
- Design references from `design.md`.
- Current state: `roadmap-only`, `scaffold-only`, `in-progress`,
  `complete-with-gaps`, or `complete`.
- Primary contract: API, schema, source manifest, validation gate, package,
  docs page, or audit report.
- Dependencies on prior tracks.
- Evidence required before completion.
- Publication status when the track affects released packages, docs, or apps.

Use this extended `metadata.json` shape for new tracks:

```json
{
  "track_id": "<track_id>",
  "type": "feature|bug|chore",
  "status": "new|in_progress|completed|cancelled",
  "track_class": "governance|source-discovery|data-contract|validator|calculator|classifier|costing|binding|publication|audit",
  "requirements": [
    "MUST-001"
  ],
  "design_refs": [
    "System Design#Architecture Overview"
  ],
  "current_state": "roadmap-only|scaffold-only|in-progress|complete-with-gaps|complete",
  "primary_contract": "<api|schema|source manifest|validation gate|package|docs page|audit report>",
  "dependencies": [
    "<track_id or artifact>"
  ],
  "completion_evidence": [
    "<tests|docs|workflow|package registry|release|manifest|audit report>"
  ],
  "publication_status": "not-applicable|future-only|unpublished|published|published-with-gaps",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "description": "<description>"
}
```

Legacy tracks that do not have these fields should be normalized by the
Roadmap Portfolio Governance Backfill track before broad completion claims are
made.

## Track Creation Checklist

Before adding a new track:

- Confirm whether an existing track already owns the work.
- Choose exactly one primary track class.
- State the current state honestly; roadmap content alone is
  `roadmap-only`.
- Reference the MoSCoW requirements and design sections affected by the track.
- Identify upstream dependencies and downstream consumers.
- Define the explicit contract being delivered.
- Define the evidence needed before the track can be marked complete.
- Identify whether publication, package release, docs deployment, or registry
  updates are part of completion.
- Add SAS parity and Excel formula parity requirements for pricing-year
  validation tracks where those sources are available.
- Add abstraction-boundary requirements for binding, app, classifier, and
  tutorial tracks.

## Dependency Order

Prefer this order unless a track explicitly documents why it can proceed
earlier:

1. Governance and abstraction doctrine.
2. Source discovery and archive manifesting.
3. Reference-data manifests and formula/parameter bundles.
4. Coding-set registries and licensed-product handling.
5. Validation gates and fixture schemas.
6. Calculator implementation or classifier/grouper adapters.
7. Cross-language contract tests.
8. Bindings and apps.
9. Documentation, tutorials, packages, releases, and publication.
10. Recurring audits and remediation tracks.

## Validation Ladder by Pricing Year

A pricing year should move through this ladder:

1. `discovered`: official sources are identified.
2. `archived`: sources are archived or explicitly gap-recorded.
3. `extracted`: SAS logic, Excel formulae, workbook tables, price weights, and
   supporting parameters are extracted into structured bundles where feasible.
4. `source-parity-checked`: implementation logic is compared with SAS and
   Excel formulae where available.
5. `fixture-parity-checked`: outputs are checked against official SAS/Excel or
   trusted reference outputs.
6. `cross-engine-checked`: Python, Rust, CLI, and released bindings agree on
   shared fixtures.
7. `validated`: evidence records are complete and linked from manifests/docs.

When SAS and Excel disagree, record the disagreement and identify the
authoritative source for the affected behavior.

## Recurring Audit Cadence

Run these recurring audits:

- IHACPA discovery audit: at least quarterly and after each NEP/NWAU release.
- Repository publication and SOTA audit: before every release and at least
  monthly while publication work is active.
- Conductor completion and contract audit: after major roadmap expansions and
  before claiming a milestone complete.
- Dependency and security review: whenever Renovate/Dependabot opens
  calculator-impacting updates.

## Completion Rules

A track must not be marked complete unless:

- The contract is explicit.
- The relevant requirements and design references are stated.
- The required evidence exists.
- Tests, docs, workflows, or registry records back the claim.
- Current-state and future-state language are separated.
- Publication claims are verified against the relevant registry or platform.
- `conductor-review` has run at phase and track boundaries with high-confidence
  fixes applied and validation rerun.

If only the roadmap, scaffold, or documentation exists, mark the track as
`roadmap-only` or `scaffold-only`, not complete.

## Archive Rules

Use `track-archive-policy.md` before moving tracks to `archive/`.

Completed tracks in `conductor/tracks/` should be audited before archival. A
track is archive-ready only when its metadata, spec, plan, review evidence,
validation evidence, documentation links, and publication status agree. Tracks
that are marked `[x]` but only contain scaffolds, stubs, generated placeholders,
or docs-only intent must be downgraded or given remediation tracks instead of
being archived.

## Remediation Rules

Audits should create remediation tracks when gaps are too large for immediate
fixes. High-confidence stale links, stale repo names, incorrect workflow paths,
and inaccurate claims should be fixed directly during the audit.
