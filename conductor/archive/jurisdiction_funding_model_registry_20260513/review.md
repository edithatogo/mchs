# Review: Jurisdiction Funding Model Registry

## Verdict

Reviewed; keep live as `complete-with-gaps`.

## Findings

1. The registry design names every state and territory, but implemented rows or blocked-source rows are not present for all jurisdictions.
2. Current implementation evidence is limited to roadmap text and synthetic constants, with no full NSW, VIC, QLD, WA, SA, TAS, ACT, and NT status test matrix.
3. The track should remain live until source status and provenance rows are explicit.

## Validation

- `uv run pytest tests/test_pricing_hwau_strategy_tracks.py tests/test_price_registry.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Add registry or blocked-source rows for all states and territories.
- Add tests covering source status, provenance, and blocked/local-only handling for NSW, VIC, QLD, WA, SA, TAS, ACT, and NT.
