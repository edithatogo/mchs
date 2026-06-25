# Review: NSW Funding Model

## Verdict

Reviewed; keep live as `complete-with-gaps`.

## Findings

1. The track is not archive-ready because NSW-specific evidence remains roadmap-level.
2. Current price values in `nwau_py.price_registry` are synthetic and do not prove sourced NSW State Price support.
3. Acceptance still requires at least one public-safe NSW source fixture, missing-year blocked handling, and tests for parallel application.

## Validation

- `uv run pytest tests/test_pricing_hwau_strategy_tracks.py tests/test_price_registry.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Add official or public-safe NSW source fixtures.
- Add behavior tests for sourced NSW rows, missing years, blocked/unknown statuses, and parallel valuation output.
