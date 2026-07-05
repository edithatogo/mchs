# Review: Parallel Valuation Outputs

## Verdict

Reviewed; archive-ready as `complete-with-gaps`.

## Findings

1. The repository now exposes a runtime PriceRegistry API for national, state, local, and discounted rows.
2. The parallel NSW/national valuation helper and archive-track tests prove the executable valuation contract at the library boundary.
3. Surface-level valuation adapters remain a follow-on gap, but they do not block archive readiness for the library contract.

## Validation

- `uv run pytest tests/test_parallel_valuation_outputs_archive_track.py tests/test_price_registry.py tests/test_nsw_funding_model.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Surface-level valuation adapters are not yet first-class output surfaces in the CLI/file, HTTP API, MCP, or OpenAI adapters.
- Official sourced state/local coverage remains incomplete beyond the public-safe fixtures committed here.
