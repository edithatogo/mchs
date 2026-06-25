# Final Review: Costing-Study Tutorials and Examples

## Review Result

Archive eligible as `complete-with-gaps`.

The track satisfies the declared documentation and fixture scope: it provides
synthetic costing-study fixtures, versioned Starlight tutorials, package docs
mirrors, and caveats that distinguish pricing, funding, costing, and
benchmarking. The evidence is public-safe and does not embed real patient,
hospital, or jurisdiction-sensitive data.

## Evidence Reviewed

- `docs-site/src/content/docs/2026/tutorials/costing-study-nwau-nep.mdx`
- `docs-site/src/content/docs/2026/tutorials/costing-study-cost-vs-price.mdx`
- `docs-site/src/content/docs/2026/tutorials/costing-study-stream-benchmarking.mdx`
- `docs-site/src/content/docs/2026/tutorials/julia-dataframes-arrow-costing-study.mdx`
- `docs-site/src/content/docs/2026/tutorials/r-markdown-quarto-costing-study.mdx`
- `nwau_py/docs/tutorial_nwau_nep.md`
- `nwau_py/docs/tutorial_cost_vs_efficient_price.md`
- `nwau_py/docs/tutorial_stream_benchmarking.md`
- `tests/data/costing_study/README.md`
- `tests/data/costing_study/nwau_calculation_inputs.csv`
- `tests/data/costing_study/observed_costs.csv`
- `tests/data/costing_study/nhcdc_benchmarks.csv`
- `tests/test_costing_study_tutorials_track.py`

## Bounded Gaps

- The tutorials are synthetic training material, not official IHACPA costing
  outputs or policy/funding decision tools.
- The current validation checks documentation and fixture provenance rather
  than executing full notebook-style tutorials end to end.

## Validation

- `uv run pytest tests/test_costing_study_tutorials_track.py tests/test_starlight_site_scaffold.py tests/test_docs_site_migration.py`
- `python conductor/scripts/stub_detector.py --root . --json`
