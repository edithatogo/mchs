# Review: Pricing-Year Diff Tooling

Status: integration review complete

## Resolved Findings

1. High: The diff command needed a real CLI surface.
   - Resolution: `funding-calculator diff-year <from-year> <to-year>` now emits markdown by default and JSON with `--json`.
   - Evidence: `nwau_py/cli/main.py` defines the `diff-year` command and `tests/test_pricing_year_diff_tooling.py` exercises JSON and markdown output.

2. High: The committed diff examples needed to match the current reference manifests.
   - Resolution: contract examples and docs now target the manifest-backed `2025` and `2026` years.
   - Evidence: `contracts/pricing-year-diff/examples/diff-year.json` and `contracts/pricing-year-diff/examples/diff-year.markdown.md` are keyed to `2025 -> 2026`.

3. Medium: Track registry metadata needed concrete evidence files.
   - Resolution: `strategy.md` and `ci_notes.md` are present and linked by the track metadata.

4. Medium: Release documentation needed to consume diff output.
   - Resolution: Starlight governance docs describe year-diff release-note consumption.

## Closure Notes

- Resolved in integration: `funding-calculator diff-year <from-year> <to-year>`
  now emits markdown by default and JSON with `--json`.
- Resolved in integration: contract examples and docs now target the
  manifest-backed `2025` and `2026` years.
- Resolved in integration: track `strategy.md` and `ci_notes.md` are present.
- Resolved in integration: Starlight governance docs describe year-diff release
  note consumption.

## Recommended validation commands

- `uv run pytest tests/test_pricing_year_diff_tooling.py`
- `uv run pytest tests/test_pricing_year_validation_gates.py`
- `uv run python -m nwau_py.cli.main diff-year 2025 2026 --json`
- `uv run python -m nwau_py.cli.main diff-year 2025 2026 --help`
- `uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml --cov-fail-under=80`
- `uv run ruff check .`
- `uv run ty check`
