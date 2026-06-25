# Strategy: Reference Data Manifest Schema

## Decision
Use a versioned YAML manifest per pricing year with one canonical path:
`reference-data/{pricing_year}/manifest.yaml`.

The manifest is the strict contract for discovered source artifacts, pricing-
year constants, parameter bundles, coding-set versions, validation state, and
known gaps. It is not a narrative note file and it must not rely on implicit
missingness.

## Schema shape
- `schema_version`: required. Governs the manifest contract family and must be
  checked before any other field is trusted.
- `pricing_year`: required. Identifies the year the manifest governs.
- `canonical_path`: required. Must point to the canonical manifest location for
  the declared pricing year.
- `validation`: required. Holds the manifest validation status and the latest
  check metadata.
- `sources`: required. Lists all source artifacts used by the manifest.
- `parameters`: required. Holds the year-scoped constants, weights, adjustment
  parameters, and coding-set references.
- `gaps`: required. Lists explicit gaps and unresolved scope items, even when
  the list is empty.

### Source artifact records
Each source artifact record should carry stable identity and provenance fields:
- `source_id`
- `kind`
- `title`
- `url` or `local_path`
- `publication_date`
- `retrieved_date`
- `sha256` when a digest is available
- `license`
- `provenance_notes`
- `scope`

If a source is known but not yet retrievable, the missing locator must be
represented as a gap record rather than implied by omission.

### Parameter sections
The `parameters` object is divided into typed sub-objects:
- `constants` for NEP/NEC and other year constants
- `weights` for stream price weights and similar coefficients
- `adjustments` for explicit adjustment parameters
- `coding_sets` for versioned coding-set references

Each value must be tied back to a source record or a derivation note. Derived
values are acceptable only when the derivation itself is documented in the
manifest.

## Validation-status taxonomy
The validation status is a small, ordered taxonomy. Loaders must treat the
status as declarative, not aspirational.

- `source-discovered`: the source exists and has been identified, but the
  manifest may still be incomplete.
- `source-referenced`: the source has a stable locator and the manifest can
  point to it unambiguously.
- `schema-complete`: the manifest satisfies the structural requirements for the
  declared schema version.
- `gap-explicit`: every known omission is represented in `gaps[]`; there are no
  silent holes in the manifest shape.
- `validated`: the manifest claims have been checked against the accepted source
  set and no unresolved gaps remain for in-scope claims.

Status transitions must be monotonic in intent. A manifest may stay at an
earlier status if a later check fails, but it should not jump past an
unverified stage.

## Explicit gap semantics
Gaps are first-class records. They are the only acceptable way to represent a
known absence.

Each gap record should include:
- `gap_id`
- `kind`
- `scope`
- `reason`
- `expected_resolution`
- `introduced_at`
- `status`

Suggested gap kinds:
- `source_missing`
- `publication_pending`
- `checksum_unavailable`
- `value_unpublished`
- `license_unclear`
- `scope_unknown`
- `validation_blocked`

Rules:
- A missing item is not a gap unless it is recorded in `gaps[]`.
- `null`, empty strings, and placeholder tokens such as `TBD` are not a
  substitute for a gap record.
- Known gaps may coexist with a valid manifest only when the schema version and
  declared validation status permit them.
- A manifest that claims `validated` must not retain unresolved gaps for any
  in-scope field.

## Schema versioning
The manifest schema version is independent from the pricing year.

- Major schema changes are breaking and require a new schema family.
- Additive, backward-compatible changes may extend the schema with optional
  fields only.
- Loaders must reject unknown major schema versions rather than guessing.
- Schema migrations should preserve canonical paths and keep older manifests
  readable until they are deliberately retired.

The first contract family should be treated as frozen once checked in. Future
changes must preserve strict validation and deterministic diagnostics.

## Canonical paths
Use canonical, repository-relative paths for all manifest references.

- Manifest: `reference-data/{pricing_year}/manifest.yaml`
- Source artifacts: `reference-data/{pricing_year}/sources/<publisher>/<file>`
- Derived artifacts: `reference-data/{pricing_year}/derived/<name>`

Any alternate filename or import location is an alias only. It must not replace
the canonical manifest path in docs, fixtures, or validation output.

## Readiness bar
Keep claims conservative.

- Do not describe the schema as production-ready until invalid manifests fail
  with actionable diagnostics.
- Do not claim full coverage until example manifests exist for at least one
  current and one historical pricing year.
- Do not treat unresolved gaps as silent omissions.
- Do not relax schema checks to make partially populated manifests pass.
