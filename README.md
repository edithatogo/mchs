# NWAU Calculator

[![PR CI](https://github.com/edithatogo/mchs/actions/workflows/pr-ci.yml/badge.svg?branch=master)](https://github.com/edithatogo/mchs/actions/workflows/pr-ci.yml)
[![Docs Site](https://github.com/edithatogo/mchs/actions/workflows/docs-site.yml/badge.svg?branch=master)](https://github.com/edithatogo/mchs/actions/workflows/docs-site.yml)
[![PyPI](https://img.shields.io/pypi/v/nwau-py.svg)](https://pypi.org/project/nwau-py/)
[![Python](https://img.shields.io/pypi/pyversions/nwau-py.svg)](https://pypi.org/project/nwau-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Contributing](CONTRIBUTING.md) | [Security](SECURITY.md) | [Code of Conduct](CODE_OF_CONDUCT.md) | [Citation](CITATION.cff)

This project provides Python translations of the IHACPA SAS funding
calculators. Modules cover acute, emergency department, mental health,
subacute and outpatient activity along with HAC and AHR adjustment
logic. The implementation is being brought into explicit parity with the
official SAS calculators, but validation is tracked per calculator and year
rather than claimed as complete across the whole repository. The current
implementation still uses pandas-based paths, while the longer-term data
stack is moving toward Arrow-backed interchange and Polars where parity work
allows it. A lightweight command line interface is available via the
`funding-calculator` script.

The public documentation site is built with Starlight from `docs-site/` and
serves as the canonical docs front door.
The GitHub Pages deployment path is wired through
[`.github/workflows/docs-site.yml`](.github/workflows/docs-site.yml).
Open the docs at <https://edithatogo.github.io/mchs/>.

## Releases

Releases are tag-driven and start from `v0.2.0`-style tags.
The repo uses release drafts for notes and a release workflow to build
distributions and publish GitHub Releases from tagged commits.
Tagged releases also trigger Python package publishing to PyPI through
trusted publishing. The current public Python release is `nwau-py 0.2.2`.
The Rust GA workflow also publishes Rust artifacts to GitHub Releases, and
`nwau-core 0.1.0` is published on crates.io; the other local Rust crates are
not public registry packages.
The conda-forge recipe is under staged-recipes review in
<https://github.com/conda-forge/staged-recipes/pull/33452>; users should treat
conda-forge as unpublished until that PR is merged and the package appears on
the public channel.
All release claims still depend on the CI and validation gates passing for the
tagged source.

## Package registry status

Registry status snapshot from checked-in registry evidence:

| Surface | Distribution evidence | Registry state |
| --- | --- | --- |
| Python package (`nwau-py`) | `pyproject.toml`, release workflow, and PyPI badge links | **Published** on PyPI at `nwau-py 0.2.2` |
| Conda package (`nwau-py`) | `packaging/conda-forge/meta.yaml` and staged-recipes PR `33452` | **Submitted, not published**; linter, check-skip, platform, and aggregate checks are passing; maintainer review, merge, and feedstock publication remain pending |
| MCP stdio server (`mchs-mcp`) | `nwau_py/mcp_server.py`, `contracts/mcp/registry/server.json`, `.github/workflows/publish-mcp-registry.yml` | **Published** to the official MCP Registry as `io.github.edithatogo/mchs` version `0.2.2` |
| Rust crate (`nwau-core`) | `rust/crates/nwau-core/Cargo.toml` and crates.io API evidence | **Published** on crates.io at `nwau-core 0.1.0`; checksum `c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547` |
| Other Rust crates (`nwau-c-abi`, `nwau-py`) | `rust/crates/*/Cargo.toml` | **Unpublished/Private**; `nwau-core` publication only closes their registry dependency gate |
| .NET package (`Mchs.Bindings.DotNet`) | `bindings/dotnet/DotNetBinding.csproj`, package artifact, and NuGet flat-container API | **Published** on NuGet at `Mchs.Bindings.DotNet 0.1.0` |
| Homebrew formula (`nwau-py`) | `packaging/homebrew/nwau-py.rb` and personal tap `edithatogo/homebrew-mchs` | **Published to personal tap** with audit, source install, and `brew test` passing; Homebrew/core remains optional/upstream-review-gated |
| Go module (`github.com/edithatogo/mchs/bindings/go`) | `bindings/go/go.mod`, Go module tag, proxy and pkg.go.dev evidence | **Published** at `v0.1.0` through the Go module proxy/pkg.go.dev |
| npm package (`@edithatogo/mchs-wasm-binding`) | `wasm-binding/package.json` and npm registry evidence | **Published** on npm at `0.1.0` |
| CRAN (`nwauR`) | R package build/check artifacts | **Prepared, not published**; CRAN maintainer submission/review remains external |
| Julia General (`NationalWeightedActivityUnitWrapper`) | `julia-binding/Project.toml` and merged General PR `156254` | **Published** in Julia General as `NationalWeightedActivityUnitWrapper 0.1.0`; merged registry PR is the authoritative publication evidence |
| Maven Central (`io.github.edithatogo:mchs-jvm-bindings`) | JVM/Gradle build evidence | **Published** on Maven Central at `io.github.edithatogo:mchs-jvm-bindings 0.1.0` |
| Open VSX / Visual Studio Marketplace (`mchs-tools`) | Historical `.vsix` artifact and public registry API evidence retained | **Deprecated and cancelled** as of 2026-07-03; no further extension publishing or synchronization is planned unless re-chartered |
| MATLAB File Exchange / Stata SSC | Prepared interop bundles and public registry evidence | **Published** as MATLAB File Exchange add-on `184067` and SSC package `mchs`; local MATLAB/Stata runtime execution is not claimed |
| vcpkg / ConanCenter (`nwau-c-abi`) | Historical portfile/recipe, local Conan create, vcpkg overlay validation, and upstream PR evidence retained | **Deprecated and cancelled** as of 2026-07-03; no public vcpkg or ConanCenter publication is claimed |
| Swift Package Index (`MCHSBind`) | Historical PackageList issue, merged PR, public page, and Swift package metadata retained | **Deprecated and cancelled** as of 2026-07-03; no further Swift Package Index work is planned unless re-chartered |
| R / Julia / Scala / Spark / Swift / Stata / MATLAB / Kotlin-Native / Power Platform adapters | Private adapter code, contracts, or track specs in this repo | **No support claim beyond the specific registry states above** |

Do not state registry submission success (including crates.io, npm, CRAN, NuGet,
etc.) unless a registry page exists and is linked in evidence.
For the current scaffold/product distinction, Rust promotion state, and
deferred-surface vocabulary, see
[Scaffold and Stub Completion Backlog](docs/roadmaps/scaffold-stub-completion-backlog.md),
[Rust Core Continuation](docs/roadmaps/rust-core-continuation.md), and
[Deferred Surface Status](docs/roadmaps/deferred-surface-status.md).

The repository also contains the Rust workspace used for calculator-core
migration. Python remains the current validated runtime path until Rust parity
is proven calculator by calculator.
Current Rust support is limited to an acute 2025 canary with documented parity
evidence plus an internal synthetic subacute canary boundary. Subacute remains
blocked for Python/public Rust support, and other Rust calculator streams
remain blocked or not-ready until stream-specific tests and evidence are
committed.
The intended architecture is a polyglot library: a shared Rust calculator core
with thin bindings or adapters for Python, Rust, R, Julia, C#/.NET, Go,
TypeScript/WASM, Java/JVM, C ABI, SQL/DuckDB, SAS interoperability, CLI/file
workflows, web demos, and Power Platform orchestration. Those surfaces must
consume shared contracts and validation fixtures rather than duplicating formula
logic.

## Calculator modules

Each module below mirrors a SAS program from the IHACPA package.

| Module | SAS source | Notes |
|-------|-----------|-------|
|`acute`|`NWAU25_CALCULATOR_ACUTE.sas`|Calculates NWAU25 for acute admitted episodes. Implements ICU hour logic, length of stay categories and private patient adjustments using the current tabular Python execution paths.|
|`ed`|`NWAU25_CALCULATOR_ED.sas`|Handles Emergency Department/Service activity. Supports UDG and AECC classifications with remoteness and indigenous adjustments.|
|`mh`|`NWAU25_CALCULATOR_MH.sas`|Implements the mental health consumer model. Applies private patient services and accommodation adjustments.|
|`subacute`|`NWAU25_CALCULATOR_SUBACUTE.sas`|Calculates NWAU25 for subacute admitted activity based on SNAP.|
|`outpatients`|`NWAU25_CALCULATOR_OUTPATIENTS.sas`|For non‑admitted clinic activity. Applies remoteness and indigenous adjustments.|
|`adjust`|`Calculate Adjusted NWAU.sas`|Combines base NWAU with Hospital Acquired Complication (HAC) and Avoidable Hospital Readmission (AHR) adjustments.|

Historical SAS calculators from IHACPA should be extracted to
`archive/sas/<YEAR>/`. Rename the downloaded directory so only the year
remains (for example `archive/sas/2025`). Each folder then contains the
original SAS programs and data tables for that pricing year.

## Calculators

The project includes Python versions of each funding calculator. The table
below lists the corresponding SAS programs and shows which pricing years have
validated weights and formulas.

| Calculator | SAS program | Python | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|-----------|------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------|------|
| Acute | `NWAU25_CALCULATOR_ACUTE.sas` | ✓ | | | | | | | | | | | ✓ | ✓ |
| ED | `NWAU25_CALCULATOR_ED.sas` | ✓ | | | | | | | | | | | ✓ | ✓ |
| MH | `NWAU25_CALCULATOR_MH.sas` | ✓ | | | | | | | | | | | ✓ | ✓ |
| Subacute | `NWAU25_CALCULATOR_SUBACUTE.sas` | ✓ | | | | | | | | | | | ✓ | ✓ |
| Outpatients | `NWAU25_CALCULATOR_OUTPATIENTS.sas` | ✓ | | | | | | | | | | | ✓ | ✓ |
| Adjustment | `Calculate Adjusted NWAU.sas` | ✓ | | | | | | | | | | | ✓ | ✓ |
| Readmission | `Avoidable Hospital Readmission Grouper 030.sas` | ✓ | | | | | | | | | | | ✓ | ✓ |

Weights and formulas are currently verified for 2024 and 2025. Earlier years
remain in progress until their outputs are validated against trusted reference
material.

## Installation

The preferred development workflow uses `uv`:

```bash
uv sync --locked --group dev --group test --group coverage --group typing --group property --group mutation --group profiling --group docs
```

Published releases are available from PyPI:

```bash
python -m pip install nwau-py
```

After the conda-forge staged-recipes submission is accepted and the package is publicly available, conda users can
install with:

```bash
conda install -c conda-forge nwau-py
```

Extract the official SAS calculators under `archive/sas/<YEAR>/` so the
Python modules can load the reference tables for each year.

### Dependencies

The calculators rely on several core Python packages:

- **NumPy** for numerical helpers
- **Pandas** for legacy tabular paths that remain under parity validation
- **Polars** and **PyArrow** for Arrow/Parquet interoperability and the newer bundle layer
- **LightGBM** for readmission risk scoring

The active development stack also uses:

- **uv** for environment and dependency management
- **Ruff** for linting and formatting
- **ty** for type checking
- **pytest** and **Codecov** for test execution and coverage reporting
- **Hypothesis** for property-based tests
- **mutmut** for mutation testing
- **Scalene** for profiling

Use `uv run` to execute tools inside the project environment:

```bash
uv run pytest
uv run ruff check .
uv run ty check
```

### Maintenance automation
Dependency updates are reviewed through Renovate, and documentation or
validation claims are checked with Vale before they are merged.

## Historical data

Place each year's SAS calculator under `archive/sas/<YEAR>/` and ensure the
folder name is just the year.  After extraction the directory should contain the
SAS programs and reference tables for that pricing year.

The Excel workbooks may also be archived under
`excel_calculator/archive/<year>` for historical comparison.  A helper script
(`excel_calculator/scripts/extract_all.py`) can recreate `weights.csv` and
`formula.json` from the workbooks but this is only required when reproducing the
original spreadsheets.


Directory layout
----------------
```
archive/
  sas/<YEAR>/        # SAS reference tables
excel_calculator/
  data/
    weights.csv      # default (current year)
    formula.json
    <YEAR>/weights.csv
    <YEAR>/formula.json
```
Dropping the SAS folder and matching `weights.csv`/`formula.json` files for a
new edition is all that's required to add support for that year.

The repository currently includes verified Excel-derived weights and formulas
for the 2025 edition. The 2024 formula mapping is retained for historical
comparison, but 2024 Excel weights are not committed until they can be
recreated from an archived workbook and validated.

### Data availability matrix

| Year | SAS archive | Verified weights | Validated Python |
|------|-------------|------------------|-----------------|
|2014|✅|❌|❌|
|2015|✅|❌|❌|
|2016|✅|❌ (sample only)|❌|
|2017|✅|❌|❌|
|2018|✅|✅ (sample)|❌|
|2019|✅|✅ (sample)|❌|
|2020|✅|❌|❌|
|2021|✅|❌|❌|
|2022|✅|❌|❌|
|2023|✅|❌|❌|
|2024|✅|❌|❌|
|2025|✅|✅|✅|

### Adding a new pricing year

1. Extract the SAS calculator for the new edition under
   `archive/sas/<YEAR>/`. Rename the folder so only the year remains.
2. Copy the Excel workbook to `excel_calculator/archive/<YEAR>` and run
   `python excel_calculator/scripts/extract_all.py`. This writes
   `weights.csv` and `formula.json` to `excel_calculator/data/<YEAR>/`.
3. If the remoteness classification year changes update
   `nwau_py/utils.RA_VERSION` accordingly.
4. Each calculator can then be invoked with ``--year <YEAR>`` or by
   passing ``year="<YEAR>"`` when calling the Python functions.

## SAS program mapping

The original SAS calculators are archived under
`archive/sas/<YEAR>/calculators`.  Each Python module in
`nwau_py` mirrors one of these programs.  The table below lists the main
equivalences.

| SAS program | Python module | Notes |
|-------------|---------------|-------|
|`NWAU##_CALCULATOR_ACUTE.sas`|`nwau_py/calculators/acute.py`|Matches SAS acute logic|
|`NWAU##_CALCULATOR_ED.sas`|`nwau_py/calculators/ed.py`|Equivalent ED calculations|
|`NWAU##_CALCULATOR_MH.sas`|`nwau_py/calculators/mh.py`|Mental health consumer model|
|`NWAU##_CALCULATOR_SUBACUTE.sas`|`nwau_py/calculators/subacute.py`|SNAP based calculator|
|`NWAU##_CALCULATOR_OUTPATIENTS.sas`|`nwau_py/calculators/outpatients.py`|Non-admitted activity|
|`Calculate Adjusted NWAU.sas`|`nwau_py/calculators/adjust.py`|Applies HAC and AHR adjustments|
|`Avoidable Hospital Readmission Grouper.sas`|`nwau_py/groupers/ahr.py`|Readmission grouper|
|`Hospital Acquired Complication Grouper.sas`|`nwau_py/groupers/hac.py`|HAC grouper|
|`Scorer_v3.py`|`nwau_py/scoring/scorer.py`|LightGBM readmission model|

## Usage
Weights and the pricing formula are stored in `excel_calculator/data`.
Each pricing year has its own subdirectory, e.g. `excel_calculator/data/2025`.
The top-level files remain as the default for 2025 so existing scripts
continue to work.
Funding calculators can be executed directly via ``python -m nwau_py.cli.main``.
For example, to process acute activity:

```bash
python -m nwau_py.cli.main acute patient_data.csv --output funding.csv
```

Replace `acute` with `ed` or `non-admitted` for other activity types. The
`--year` option selects which SAS release to use.

After installing the development environment you can run the tests, linting,
type checking, property tests, mutation testing, and profiling entry points
with `uv run`. Coverage reports are generated locally for Codecov upload in CI.

```bash
uv sync --locked --group dev --group test --group coverage --group typing --group property --group mutation --group profiling --group docs
uv run pytest
uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml --cov-fail-under=80
uv run ty check
uv run pytest -m hypothesis
uv run mutmut run
uv run scalene nwau_py/cli/main.py
```

See `nwau_py/docs/calculators.md` for an overview of each calculator module.
The `nwau_py` package exposes both a command line interface and functions for
use within Python.

## Validation Status

Validation claims in this repository are intentionally specific. Prefer
calculator- and year-scoped statements backed by fixture packs, parity tests,
or archived source artifacts. Avoid broad claims about project-wide or
all-years validation unless the supporting evidence is committed alongside the
claim.

## Remoteness classification

The calculators rely on the IHACPA remoteness area (RA) classification. The
edition used varies by pricing year. `nwau_py.utils.RA_VERSION` maps each year
to its RA edition and the helper function `ra_suffix(year)` returns the suffix
used in dataset column names.

```python
from nwau_py.utils import ra_suffix

assert ra_suffix("2025") == "ra2021"
```

### Handling missing demographics

When remoteness or Indigenous status is missing from the input data the
calculators can impute adjustment values using population distributions. Pass
a dictionary of proportions to the parameter dataclass:

```python
from nwau_py.calculators import AcuteParams, calculate_acute

rem_dist = {"RA1": 0.55, "RA2": 0.25, "RA3": 0.15, "RA4": 0.04, "RA5": 0.01}
ind_dist = {0: 0.8, 1: 0.2}
params = AcuteParams(
    remoteness_distribution=rem_dist,
    indigenous_distribution=ind_dist,
)
result = calculate_acute(df, params)
```

Missing adjustments are replaced by the weighted average of the relevant table
using the provided distribution.

### Command line

After installation the `funding-calculator` entry point is available. You can
select a specific pricing year with `--year`:

```bash
funding-calculator --year 2025 patient_data.csv > funding.csv
```

The `--year` option selects the data directory for that pricing year. The
example above uses the verified 2025 weights. `patient_data.csv` should contain
the columns referenced in `excel_calculator/data/formula.json` and the output
will include a `NWAU25` column.

To calculate funding using an older edition simply pass the relevant year.
For example, to run the 2025 calculator use:

```bash
funding-calculator --year 2025 patient_data.csv > funding.csv
```

This instructs the tool to load weights and the formula from
`excel_calculator/data/`.

The `nwau_py` package also exposes a lightweight command line interface via
`python -m nwau_py.cli.main`. The `--year` flag works with editions that have
committed validated source data. The subcommands `acute`, `ed` and
`non-admitted` mirror the SAS calculators:

```bash
python -m nwau_py.cli.main acute INPUT.csv --output out.csv --year 2025
```

Common options allow the weights directory to be overridden with `--params`
and enable or disable adjustments using `--icu/--no-icu` and
`--covid/--no-covid`.

### Python modules

The calculators can also be called directly from Python:

```python
from nwau_py.calculators import AcuteParams, calculate_acute

patient_df = ...  # tabular episode-level data frame
result = calculate_acute(patient_df, AcuteParams())
```

Pass ``year="2024"`` (for example) to use a different pricing edition.

Additional modules under `nwau_py.calculators` provide helpers for acute, emergency, mental health and other activity types. See `examples/run_acute.py` for a minimal demonstration.

#### Calculator examples

The individual calculators can be invoked directly when you need fine grained control. Each function expects a tabular input frame and returns the input with an additional `NWAU25` column.

```python
from nwau_py.calculators import AcuteParams, calculate_acute
result = calculate_acute(acute_df, AcuteParams())
```

```python
from nwau_py.calculators import EDParams, calculate_ed
result = calculate_ed(ed_df, EDParams())
```

```python
from nwau_py.calculators import MHParams, calculate_mh
result = calculate_mh(mh_df, MHParams())
```

```python
from nwau_py.calculators import SubacuteParams, calculate_subacute
result = calculate_subacute(sa_df, SubacuteParams())
```

```python
from nwau_py.calculators import OutpatientParams, calculate_outpatients
result = calculate_outpatients(op_df, OutpatientParams())
```

```python
from nwau_py.calculators import calculate_adjusted_nwau
result = calculate_adjusted_nwau(weight_df)
```
