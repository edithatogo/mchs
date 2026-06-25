# Strategy: Pricing-Year Diff Tooling

## Contract

The track defines the review surface under the installed CLI entrypoint:

- `funding-calculator diff-year <from-year> <to-year>`

The command compares pricing-year manifests and surfaces changes in constants,
weights, adjustment parameters, classification versions, source artifacts, and
validation status in markdown and JSON.

## Evidence surfaces

Completion is anchored to these repository surfaces:

- The installed `funding-calculator diff-year <from-year> <to-year>` command
- The pricing-year manifest schema and comparison rules in
  `conductor/archive/reference_data_manifest_schema_20260512`
- The track-local spec, plan, index, metadata, and CI notes in this directory
- Fixture-backed diff examples for changed, unchanged, missing, and newly
  introduced values

## Implementation posture

- Keep the diff deterministic and review-first.
- Summarize large tables by stream and changed keys rather than dumping raw
  rows by default.
- Distinguish source-data changes from implementation changes.
- Fail closed on missing manifests, unsupported years, or unreadable fixture
  artifacts.
- Do not claim release readiness from a diff alone.

## Review outcome

The track is aligned to the installed `funding-calculator` naming and the
completion record now names concrete evidence surfaces for a later completion
decision.
