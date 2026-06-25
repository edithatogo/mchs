# Review: Parallel Valuation Outputs

## Verdict

Reviewed; keep live as `complete-with-gaps`.

## Findings

1. The output contract intent is documented, including HWAU-only, national, state, local, and discounted valuations.
2. The track is not archive-ready because there is no executable valuation schema or surface behavior test matrix for the claimed output classes.
3. Pricing application remains correctly separated from formula execution, but source/provenance-backed valuation behavior is still pending.

## Validation

- `uv run pytest tests/test_pricing_hwau_strategy_tracks.py tests/test_price_registry.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Add valuation output schema fields for price source, rule, year, jurisdiction, and checksum.
- Add tests for national, state, local, discounted, missing schedule, and unsupported jurisdiction behavior.
- Prove CLI/file, HTTP API, MCP, and OpenAI adapter surfaces preserve the valuation contract.
