# Review: IHACPA Source Scanner

## Verdict

Complete with discovery-only boundaries. The scanner contract is implemented as an offline, review-first source discovery scaffold under `funding-calculator sources ...`.

## Scope Reviewed

- `metadata.json`, `spec.md`, `plan.md`, `index.md`
- `strategy.md`, `ci_notes.md`
- Source scanner parser, dry-run, gap-record, unchanged-source, and CLI tests

## Residual Gaps

- Publication status remains not-ready.
- Scanner output is draft review material only; it does not download live sources, commit artifacts, or establish calculator parity.
- Any future live scan should stay separate from required CI.

## Validation

- `uv run pytest tests/test_ihacpa_source_scanner.py`
- `uv run funding-calculator sources scan --html-file tests/fixtures/source_scanner/nwau_scanner_listing.html --source-page-url https://www.ihacpa.gov.au/ --year 2027 --json`
