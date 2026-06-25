# Stata file/CLI boundary adapter

This directory contains the Stata interop adapter published on the Boston
College SSC/RePEc archive as the `mchs` package. The adapter handles file
import, CLI invocation, and boundary validation in Stata while delegating all
calculations to the shared core. Public SSC installability is verified through
the package manifest, ado file, and help file; no Stata runtime validation is
claimed in this local repository because Stata is not installed here.

## Scope

- CSV file import into Stata via `mchs import`
- CLI invocation via `mchs run`, using Stata `shell`
- File-boundary column validation via `mchs validate`
- Health-economics workflow notes

## Out of scope

- Formula parsing or evaluation in Stata
- Stata `.do` or `.ado` files with calculator formula logic
- Stata formula port or reimplementation
- Stata runtime execution in this local validation environment

## Layout

- `mchs.ado` — thin Stata command adapter for file and CLI boundaries
- `mchs.sthlp` — Stata help for the adapter
- `pkg-mchs.pkg` — SSC-style package manifest
- `LICENSE` — MIT license included in the prepared archive
- `README.md` — this file
- `examples/` — Stata `.do` examples showing CLI invocation and file import
- `stata-interop-notes.md` — Health-economics workflow notes
- `mchs-stata-interop-0.1.0.zip` — SSC review/evidence bundle

## SSC readiness

The archive includes the ado/help/pkg files, README, license, and example `.do`
workflows. Validate it from the repository root with:

```sh
unzip -l bindings/stata/mchs-stata-interop-0.1.0.zip
shasum -a 256 bindings/stata/mchs-stata-interop-0.1.0.zip
```

Public SSC installability is verified through:

- `http://fmwww.bc.edu/repec/bocode/m/mchs.pkg`
- `http://fmwww.bc.edu/repec/bocode/m/mchs.ado`
- `http://fmwww.bc.edu/repec/bocode/m/mchs.sthlp`

Stata is not installed in this local environment, so ado runtime execution is
not claimed here.

## Usage

Refer to the binding strategy document at
`conductor/archive/stata_interop_binding_20260513/binding_strategy.md`
for detailed interop patterns.

The adapter lets Stata users:

1. Import pre-computed CSV outputs:
   `mchs import using "results.csv", clear`
2. Invoke the shared-core CLI:
   `mchs run using "input.csv", calculator(acute) year(2025) output("results.csv") replace import clear`
3. Validate required provenance columns:
   `mchs validate`
4. Save results as `.dta` for native Stata analysis:
   `save "results.dta", replace`

By default, `mchs run` invokes the installed `funding-calculator` console
script. Use `cli("python -m nwau_py.cli.main")` or a full executable path when
running from a source checkout or controlled environment.

## Author

Dylan Mordaunt <dylan.mordaunt@vuw.ac.nz>

Repository: <https://github.com/edithatogo/mchs>
