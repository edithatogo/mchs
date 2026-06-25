# CI and Build Notes: Reference Data Manifests

Reference data manifests are documentation-heavy but still need strict
validation. Keep CI conservative until the schema, loader, and example
manifests are stable enough to be treated as a source contract.

## Current stance

- Validate required fields, schema version pins, and status values on every
  manifest change.
- Treat missing upstream artifacts as explicit gap records, not as omitted
  fields.
- Keep source provenance complete enough to reconstruct where each value came
  from and how it was normalized.
- Do not promote calculator support claims from the manifest alone; those
  claims should stay aligned with the public support matrix.

## Suggested CI checks

- Load the pinned `reference-data/2026/manifest.yaml` and
  `reference-data/2025/manifest.yaml` examples so CI does not depend on
  time-relative "current year" wording.
- Fail on malformed URLs, missing hashes, missing retrieval dates, or missing
  provenance notes for source artifacts.
- Fail if a required gap record is absent for a known missing source.
- Verify that schema evolution remains backward readable for any supported
  historical manifest version.
- Check that the docs page and support-matrix links stay in sync with the
  manifest schema.

## Release posture

- Update the docs page and this note in the same change whenever the manifest
  schema changes.
- Keep status terminology stable across docs, fixtures, and CI output.
- If a manifest field must become required later, add it as optional first and
  only tighten the validator once the backfill is complete.

## Failure expectations

- Missing provenance should fail closed.
- A discovered source with no gap record should fail closed if the source is
  known to be absent.
- Schema drift should fail closed until the migration path is documented.
