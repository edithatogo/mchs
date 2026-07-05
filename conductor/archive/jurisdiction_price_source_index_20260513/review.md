# Review: Jurisdiction Price Source Index

## Verdict

Reviewed; archive-ready as `complete-with-gaps`.

## Findings

No unresolved local implementation blockers remain.

The source-index API now provides public-safe metadata or explicit blocked rows
for NSW, VIC, QLD, WA, SA, TAS, ACT, and NT. The remaining gaps are external
source/licence/unit-mapping gates for extracting official numeric price values.

## Validation

- `uv run pytest tests/test_coordination_and_evidence_tracks.py -q`
- `uv run pytest tests/test_jurisdiction_price_sources.py tests/test_jurisdiction_price_source_index_archive_track.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Residual External Gates

- Official source review and extraction of jurisdiction-specific price values.
- Licence review for restricted or unclear state and local schedules.
- Validated unit mappings for QWAU, WIES, WAU, and local activity terms.
