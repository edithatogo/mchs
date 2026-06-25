# Review: Pricing-Year Validation Gates

Scope audited against:
- [`conductor/archive/pricing_year_validation_gates_20260512/spec.md`](./spec.md)
- [`conductor/archive/pricing_year_validation_gates_20260512/plan.md`](./plan.md)
- [`conductor/workflow.md`](../../workflow.md)
- [`nwau_py/reference_manifest.py`](../../../nwau_py/reference_manifest.py)
- [`nwau_py/cli/main.py`](../../../nwau_py/cli/main.py)
- [`docs-site/src/content/docs/governance/reference-data-manifests.mdx`](../../../docs-site/src/content/docs/governance/reference-data-manifests.mdx)
- [`nwau_py/docs/calculators.md`](../../../nwau_py/docs/calculators.md)
- [`nwau_py/README.md`](../../../nwau_py/README.md)

## Findings

1. High: The required `nwau validate-year <year>` gate does not exist in the current CLI surface.
   - Evidence: `nwau_py/cli/main.py:144-299` defines `interop`, `sources scan`, `sources add-year`, `acute`, `ed`, and `non-admitted`, but no `validate-year` command.
   - Evidence: the track spec explicitly requires `nwau validate-year <year>` and CI checks for missing evidence at `conductor/archive/pricing_year_validation_gates_20260512/spec.md:7-10`, with the plan repeating that implementation target at `plan.md:9-13`.
   - Impact: the track cannot enforce manifest completeness or fixture evidence from the intended command line entrypoint, so the acceptance criteria are not reachable from the current CLI contract.

2. High: The validation-status vocabulary is inconsistent across the new track, the existing manifest schema, and the docs that describe the lifecycle.
   - Evidence: the track spec proposes statuses such as `discovered`, `archived`, `extracted`, `implemented`, `fixture-tested`, `validated`, and `deprecated` at `spec.md:7-10`.
   - Evidence: the actual manifest loader and validation model currently recognize `source-discovered`, `source-only`, `schema-complete`, `gap-explicit`, `partially-validated`, `validated`, and `deprecated` at `nwau_py/reference_manifest.py:27-36` and `nwau_py/reference_manifest.py:206-220`.
   - Evidence: the public docs page uses yet another lifecycle set, including `drafted`, `schema-checked`, and `gap-recorded`, at `docs-site/src/content/docs/governance/reference-data-manifests.mdx:20-28`.
   - Impact: without a single canonical taxonomy or an explicit mapping table, the planned gates will drift between docs, schema, and CI, which makes transition checks brittle and support-claim enforcement ambiguous.

3. Medium: The existing docs still present support and validation as static prose/table content instead of something derived from recorded validation status.
   - Evidence: `nwau_py/docs/calculators.md:11-15` publishes a hard-coded supported-pricing-years table, while `nwau_py/docs/calculators.md:33-35` only says parity is not claimed unless tests establish it.
   - Evidence: `nwau_py/README.md:58-64` describes validation as manifest-driven, but there is no command or manifest binding in the current CLI surface that lets docs/API metadata consume that status directly.
   - Evidence: `docs-site/src/content/docs/governance/reference-data-manifests.mdx:110-118` says the manifest should point back to the public calculator coverage matrix, yet `nwau_py/reference_manifest.py` has no support-link field or enforcement that connects the manifest record to a coverage claim.
   - Impact: the planned rule “prevent docs/API metadata from claiming support beyond recorded validation status” has no concrete integration point yet, so the docs can still diverge from the gate state even if the loader remains strict.

## Recommended validation commands

- `uv run pytest tests/test_reference_data_manifest_schema.py tests/test_fixture_manifest.py`
- `uv run python -m nwau_py.cli.main --help`
- After the gate exists, `uv run python -m nwau_py.cli.main validate-year 2025`
- After the gate exists, `uv run python -m nwau_py.cli.main validate-year 2026`

## Blockers

- Resolved in integration: the CLI now exposes
  `funding-calculator validate-year <year>` with text and JSON output.
- Resolved in integration: the implementation and docs now use the canonical
  reference-manifest statuses: `source-discovered`, `source-only`,
  `schema-complete`, `gap-explicit`, `partially-validated`, `validated`, and
  `deprecated`.
- Remaining caveat: public support matrices are still mostly prose-driven. The
  gate prevents local evidence overclaims, but a later track should generate
  public support tables directly from manifests.
