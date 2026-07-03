# Calculator Modules

This page outlines the Python implementations of the IHACPA NWAU calculators. Each module loosely mirrors a SAS program from the official calculator package.
The repository documents the 2026-27 NEP26 calculator set as available and
listed, but this page does not claim parity validation against extracted IHACPA
outputs unless tests explicitly establish it.
The shared classification preflight validator is available in
`nwau_py.classification_validation`, but this page does not claim it is wired
into every calculator or CLI entry point yet.
The runtime support status for CLI, MCP, and docs is generated from
`contracts/support/calculator-capability-matrix.json`, which is the single
source of truth for current support claims.
For the broader feature-to-tool summary, see the
[IHACPA Tool Coverage Matrix](../../conductor/ihacpa-tool-coverage-matrix.md).

## Supported pricing years

| Year | NWAU price | Acute classification | Non-admitted classification | Notes |
| --- | ---: | --- | --- | --- |
| NEP26 (2026-27) | $7,418/NWAU(26) | AR-DRG v12.0 | Tier 2 v10.0 | Transition from AR-DRG v11.0 (acute) and Tier 2 v7 (non-admitted). AECC v1.1, AMHCC v1, AN-SNAP v5, UDG v1.3 unchanged. Not yet validated; parity is only claimed when tests prove it. |

| Module | SAS source | Notes |
|-------|-----------|-------|
|`acute`|`NWAU25_CALCULATOR_ACUTE.sas`|Calculates NWAU25 for acute admitted episodes. Implements ICU hour logic, length of stay categories and private patient adjustments using pandas operations. 2026-27 documentation coverage notes AR-DRG v12.0 for admitted acute and Tier 2 v10.0 for non-admitted. An opt-in Rust-backed acute 2025 adapter is also available via `calculate_acute_rust_2025()`.|
|`ed`|`NWAU25_CALCULATOR_ED.sas`|Handles Emergency Department/Service activity. Supports UDG and AECC classifications with remoteness and indigenous adjustments.|
|`mh`|`NWAU25_CALCULATOR_MH.sas`|Implements the mental health consumer model. Applies private patient services and accommodation adjustments.|
|`subacute`|`NWAU25_CALCULATOR_SUBACUTE.sas`|Calculates NWAU25 for subacute admitted activity based on SNAP.|
|`outpatients`|`NWAU25_CALCULATOR_OUTPATIENTS.sas`|For non‑admitted clinic activity. Applies remoteness and indigenous adjustments.|
|`adjust`|`Calculate Adjusted NWAU.sas`|Combines base NWAU with Hospital Acquired Complication (HAC) and Avoidable Hospital Readmission (AHR) adjustments.|

The SAS programs are stored under `archive/sas/NEP25_SAS_NWAU_calculator/calculators`. The Python functions focus on the core weighting formulae and use pandas for data manipulation. See the source code of each module for details of the translation.

Community mental health still needs an official-source fixture pack before the
`mh` surface can be validated against extracted IHACPA outputs. The current gap
record and pricing-year caveats are documented in
[`conductor/tracks/community_mental_health_calculator_20260512/fixture_gaps.md`](../../conductor/tracks/community_mental_health_calculator_20260512/fixture_gaps.md).

For the 2026-27 NEP26 release, the calculators are listed as available
documentation references, but validation parity is intentionally not claimed in
this page unless tests establish it.

For the current feature-to-tool incorporation summary, see the generated
capability matrix at `contracts/support/calculator-capability-matrix.json`.

For cross-language parity work, the package also ships manifest-driven fixture packs under
`tests/fixtures/golden/`, with the acute pilot pack at `tests/fixtures/golden/acute_2025/`. The
shared loader helpers live in `nwau_py.fixtures` and let Python tests consume the same manifest and
payload layout used by future runners.

## Usage examples

Below are minimal examples for each calculator. Dataframes should provide the columns referenced in the IHACPA documentation.

### Acute
```python
from nwau_py.calculators import AcuteParams, calculate_acute
result = calculate_acute(acute_df, AcuteParams())
```

### Emergency department
```python
from nwau_py.calculators import EDParams, calculate_ed
result = calculate_ed(ed_df, EDParams())
```

### Mental health
```python
from nwau_py.calculators import MHParams, calculate_mh
result = calculate_mh(mh_df, MHParams())
```

### Subacute
```python
from nwau_py.calculators import SubacuteParams, calculate_subacute
result = calculate_subacute(sa_df, SubacuteParams())
```

### Outpatients
```python
from nwau_py.calculators import OutpatientParams, calculate_outpatients
result = calculate_outpatients(op_df, OutpatientParams())
```

### Adjustment
```python
from nwau_py.calculators import calculate_adjusted_nwau
result = calculate_adjusted_nwau(weight_df)
```

## Command line interface

The calculators can also be executed from the command line using
``python -m nwau_py.cli.main``. Each calculator is available as a
subcommand:

```bash
python -m nwau_py.cli.main acute input.csv --output out.csv --year 2025
```

Use ``ed`` or ``non-admitted`` for emergency and outpatient activity.
Options such as ``--params`` select the weights directory while
``--icu/--no-icu`` and ``--covid/--no-covid`` toggle specific adjustments.

## Debugging and cleanup

Each parameter dataclass includes two optional flags:

* `debug_mode` – when ``True`` intermediate columns (those beginning with
  underscores) are retained in the returned dataframe. The default ``False``
  mimics the SAS calculators by dropping these helper fields.
* `clear_data` – when ``True`` any cached reference tables under ``.cache`` are
  removed after calculation completes.

Example usage:

```python
params = AcuteParams(debug_mode=True)
df = calculate_acute(data, params)
```
