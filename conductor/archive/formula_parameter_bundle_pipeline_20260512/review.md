# Review: Formula and Parameter Bundle Pipeline

Scope audited against:
- [`conductor/archive/formula_parameter_bundle_pipeline_20260512/spec.md`](./spec.md)
- [`conductor/archive/formula_parameter_bundle_pipeline_20260512/plan.md`](./plan.md)
- [`conductor/workflow.md`](../../workflow.md)
- [`nwau_py/bundles.py`](../../../nwau_py/bundles.py)
- [`nwau_py/fixtures.py`](../../../nwau_py/fixtures.py)
- [`nwau_py/reference_data.py`](../../../nwau_py/reference_data.py)
- [`nwau_py/calculators/acute.py`](../../../nwau_py/calculators/acute.py)
- [`nwau_py/source_scanner.py`](../../../nwau_py/source_scanner.py)
- [`nwau_py/pricing_year_validation.py`](../../../nwau_py/pricing_year_validation.py)
- [`nwau_py/pricing_year_diff.py`](../../../nwau_py/pricing_year_diff.py)
- [`tests/test_bundles.py`](../../../tests/test_bundles.py)
- [`tests/test_reference_data.py`](../../../tests/test_reference_data.py)
- [`tests/test_acute.py`](../../../tests/test_acute.py)
- [`tests/test_ihacpa_source_scanner.py`](../../../tests/test_ihacpa_source_scanner.py)
- [`tests/test_pricing_year_validation_gates.py`](../../../tests/test_pricing_year_validation_gates.py)
- [`tests/test_pricing_year_diff_tooling.py`](../../../tests/test_pricing_year_diff_tooling.py)

## Findings

1. Resolved: The acute 2025 canary now loads bundle weights through
   `load_acute_2025_canary_reference_bundle()` and feeds the existing
   `AcuteReferenceBundle` contract.

2. Resolved: Bundle-specific canonical serialization, hashing, and
   `bundle_diff()` now compare formula and parameter bundle payloads directly.
   The pricing-year diff command remains manifest-oriented by design.

3. Accepted caveat: Pricing-year validation evidence remains year-oriented.
   Calculator and stream-scoped validation is a follow-on gate for multi-stream
   parity evidence, not a blocker for this source-only canary.

## Blockers

- None for the source-only canary scope.

## Remaining caveats

- Official SAS and Excel extraction is not complete.
- The committed bundle is `source-only` and must not be presented as parity
  validated.
- Future stream/year bundles must preserve source evidence until fixture parity
  closes their extraction gaps.

## Recommended validation commands

- `uv run pytest tests/test_bundles.py tests/test_reference_data.py tests/test_acute.py tests/test_ihacpa_source_scanner.py tests/test_pricing_year_validation_gates.py tests/test_pricing_year_diff_tooling.py`
- `uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml --cov-fail-under=80`
- `uv run ruff check .`
- `uv run ty check`
- `uv run python -m nwau_py.cli.main validate-year 2025`
- `uv run python -m nwau_py.cli.main diff-year 2025 2026 --json`
