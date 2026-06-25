# CI and Build Notes: Coding-Set Version Registry

Keep CI conservative. This track defines a shared contract for classification
versions and licensing boundaries, so the required checks should fail closed
whenever source provenance or license handling is unclear.

## Current stance

- Do not require registry implementation in CI until the schema and seed
  records exist.
- Keep any version matrix or registry data deterministic and reviewable.
- Treat licensed classification products as local-only references unless the
  license explicitly allows redistribution.
- Avoid CI language that suggests broad support for a coding set unless the
  registry entry and consuming validator both exist.

## Future required checks

- Validate registry schema shape and required fields.
- Check that the current classification matrix remains aligned with the seeded
  registry records.
- Fail on unknown versions, missing pricing-year applicability, or missing
  stream applicability.
- Fail on missing license metadata for restricted classification families.
- Fail if local-only or licensed artifacts are copied into redistributable
  locations.

## Evidence expectations

- The registry should stay consistent with
  `conductor/tracks/classification_input_validation_20260512/classification_matrix.md`.
- Validation notes should preserve the distinction between public metadata and
  restricted products.
- If a year is supported only by a local licensed artifact, the CI record
  should name that limitation rather than implying redistribution.
