# Review: Historical IHACPA Coverage Audit

## Status

Reviewed on 2026-06-25. Archive eligible as a completed governance track with
explicit provenance gaps.

## Scope Reviewed

- Historical IHACPA coverage from 2012-13 through 2026-27 is separated across
  NEP determinations, national pricing model technical specifications, NWAU
  calculators, price weights, NHCDC evidence, and validation status.
- `scripts/validate_historical_ihacpa_inventory.py` protects the foundational
  2012-13 hashes and the 2013-14 through 2026-27 calculator archive span.
- Track metadata now records explicit support scope and gap register entries.

## Findings

- 2012-13 calculator support remains an explicit gap.
- NHCDC evidence is costing-study provenance only and is not calculator parity
  evidence.
- The current IHACPA NWAU calculator URL is used in the specification.

## Validation

- `uv run python scripts/validate_historical_ihacpa_inventory.py`
- `uv run pytest tests/test_historical_ihacpa_coverage_track.py tests/test_ihacpa_2026_27_track.py`
- `python conductor/scripts/stub_detector.py --root . --json`
