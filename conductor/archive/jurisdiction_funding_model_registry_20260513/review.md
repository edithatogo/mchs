# Review: Jurisdiction Funding Model Registry

## Verdict

Reviewed; archive-ready as `complete-with-gaps`.

## Findings

No unresolved local implementation blockers remain.

The runtime registry now exposes explicit rows for every state and territory,
with priced rows for NSW, VIC, and QLD and explicit public or blocked rows for
WA, SA, TAS, ACT, and NT. Remaining gaps are limited to broader official source
coverage and later-year extraction.

## Validation

- `uv run pytest tests/test_jurisdiction_funding_model_registry.py tests/test_jurisdiction_funding_model_registry_archive_track.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Residual External Gates

- Official state and territory funding-model extraction for additional years.
- Licence review for restricted funding schedules.
- Validation of jurisdiction-specific adjustment caveats beyond the committed rows.
