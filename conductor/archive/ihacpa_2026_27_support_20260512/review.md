# Review: IHACPA 2026-27 Support

## Status

Reviewed on 2026-06-25. Archive eligible as a completed governance track with
documented gaps.

## Scope Reviewed

- 2026-27 source inventory records official NEP, NEC, technical specification,
  price-weight, SAS archive, and Excel calculator evidence.
- Pricing constants expose NEP26 and NEC26 headline values with source metadata.
- Track metadata now records explicit support scope and gap register entries.

## Findings

- Calculator parity is not claimed.
- The SAS `.7Z` archive is not extracted.
- Excel `.xlsb` internals are not audited.
- HAC/AHR companion hashes are deferred.
- Stale `what-we-do` IHACPA paths and the price-weight checksum contradiction
  were corrected.

## Validation

- `uv run python scripts/validate_historical_ihacpa_inventory.py`
- `uv run pytest tests/test_historical_ihacpa_coverage_track.py tests/test_ihacpa_2026_27_track.py`
- `python conductor/scripts/stub_detector.py --root . --json`
