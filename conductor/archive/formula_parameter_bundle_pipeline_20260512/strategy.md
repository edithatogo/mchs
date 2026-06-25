# Strategy: Formula and Parameter Bundle Pipeline

## Contract
This track defines a review-first pipeline for extracting, normalizing,
versioning, diffing, and validating formula and parameter bundles.

## Evidence surfaces
- `reference-data/2026/manifest.yaml` records explicit source-only gaps for
  price-weight extraction, adjustment extraction, and publication-date
  uncertainty.
- `contracts/source-scanner/examples/add-year.draft-manifest.json` captures the
  synthetic add-year discovery contract and the price-weight gap in fixture
  form.
- `conductor/archive/reference_data_manifest_schema_20260512` defines the
  manifest contract the bundle pipeline must feed.
- `conductor/tracks/end_to_end_validated_canary_20260512` depends on a formula
  and parameter bundle as part of the full lifecycle evidence package.

## Implementation posture
- Treat source-discovered gaps as first-class until extraction evidence closes
  them.
- Preserve bundle provenance and line, sheet, or table traceability whenever
  the source format supports it.
- Keep bundle serialization deterministic and reviewable.
- Fail closed on missing source links, unsupported formats, or unreadable
  fixtures.
- Do not claim production readiness from manifest shape alone.

## Review outcome
This track now ships a strict source-only acute 2025 canary bundle, deterministic
canonical serialization, reviewable bundle diffs, a loader used by the acute
reference-bundle contract, docs, and tests. It deliberately does not claim
official parity validation until SAS and workbook fixture evidence closes the
remaining extraction gaps.
