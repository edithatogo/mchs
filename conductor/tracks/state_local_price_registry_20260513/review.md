# Review: State and Local Price Registry

## Verdict

Reviewed; keep live as `complete-with-gaps`.

## Findings

1. The track is not archive-ready because the current evidence is roadmap and synthetic record serialization, not a complete sourced registry.
2. Runtime APIs such as `PriceRegistry`, `get_state_price`, `get_national_price`, and `list_available_jurisdictions` are not present in `nwau_py.price_registry`.
3. Official provenance-backed rows and behavior tests are still needed for national, state, local, discounted, missing, and blocked schedule handling.

## Validation

- `uv run pytest tests/test_pricing_hwau_strategy_tracks.py tests/test_coordination_and_evidence_tracks.py tests/test_price_registry.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Implement the runtime registry API or explicitly re-scope it out of this track.
- Add official or public-safe provenance rows and tests for the claimed schedule classes.
