# Strategy: Pricing-Year Validation Gates

## Contract

The track defines the conservative validation gate under the installed CLI
entrypoint:

- `funding-calculator validate-year <year>`

The command verifies manifest completeness, required evidence references, and
fixture-backed validation status before a pricing year can be claimed as
supported or validated.

## Evidence surfaces

Completion is anchored to these repository surfaces:

- The pricing-year validation ladder in `conductor/roadmap-governance.md`
- The validation vocabulary in `conductor/validation-vocabulary.md`
- The manifest schema contract in
  `conductor/archive/reference_data_manifest_schema_20260512`
- The track-local plan, index, and CI notes in this directory

## Implementation posture

- Keep the gate deterministic and review-first.
- Fail closed on missing source, extraction, or fixture evidence.
- Use the canonical reference-manifest statuses: `source-discovered`,
  `source-only`, `schema-complete`, `gap-explicit`, `partially-validated`,
  `validated`, and `deprecated`.
- Do not claim support from manifest presence alone.

## Review outcome

The track was standardized to the `funding-calculator` entrypoint and the
completion record now names explicit evidence surfaces instead of relying on a
generic docs/workflows/tests placeholder.
