# Review: Julia General Registry Submission

## Status

Reviewed on 2026-06-25. Archive eligible as a published-verified registry
track.

## Scope Reviewed

- Julia General PR `156254` merged for
  `NationalWeightedActivityUnitWrapper v0.1.0`.
- Superseded `NwauCore` evidence remains historical and is not part of the
  current package publication claim.
- README registry status was corrected from submitted to published.

## Validation

- `curl -fsSL https://api.github.com/repos/JuliaRegistries/General/pulls/156254`
- `uv run pytest tests/test_julia_general_registry_submission_track.py`
- `python conductor/scripts/stub_detector.py --root . --json`
