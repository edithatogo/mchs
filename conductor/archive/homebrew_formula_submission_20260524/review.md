# Review: Homebrew Formula Submission

## Status

Reviewed on 2026-06-25. Archive eligible for the personal tap publication
claim.

## Scope Reviewed

- Personal tap `edithatogo/homebrew-mchs` contains `Formula/nwau-py.rb`.
- Track evidence records strict audit, source install, and `brew test` passing.
- Homebrew/core remains an optional upstream review gate and is not claimed.

## Validation

- `curl -fsSL https://raw.githubusercontent.com/edithatogo/homebrew-mchs/main/Formula/nwau-py.rb`
- `uv run pytest tests/test_homebrew_formula_submission_track.py`
- `python conductor/scripts/stub_detector.py --root . --json`
