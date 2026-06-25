# Review: HWAU Terminology Migration

## Verdict

Reviewed; keep live as `complete-with-gaps`.

## Findings

1. The terminology rule is documented: HWAU is the generic abstraction and NWAU remains Australian source terminology.
2. The track is not archive-ready because tests currently prove roadmap wording, not runtime/schema alias behavior.
3. Archive should wait until HWAU/NWAU compatibility is tested across canonical contracts and public adapters that expose weighted activity fields.

## Validation

- `uv run pytest tests/test_pricing_hwau_strategy_tracks.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Add runtime or schema-level alias tests for HWAU and NWAU compatibility.
- Verify public contract examples and adapters use HWAU generically without breaking Australian NWAU examples.
