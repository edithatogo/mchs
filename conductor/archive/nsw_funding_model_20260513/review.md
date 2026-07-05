# Review: NSW Funding Model

## Verdict

Reviewed; archive-ready as `complete-with-gaps`.

## Findings

No unresolved local implementation blockers remain.

The NSW registry now exposes public-source fixtures for 2025 and 2026, plus
fail-closed missing-year handling and parallel valuation output. Remaining gaps
are limited to broader historical coverage and any restricted service-agreement
artefacts that should not be redistributed.

## Validation

- `uv run pytest tests/test_nsw_funding_model.py tests/test_nsw_funding_model_archive_track.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Residual External Gates

- Official review for additional historical NSW years.
- Licence review for restricted NSW service-agreement artefacts.
- District/network-specific adjustment validation beyond the public fixture notes.
