# Stata file/CLI boundary adapter

This directory contains a synthetic, non-published Stata interop adapter for
health-economics workflows. The adapter handles file import, CLI invocation,
and boundary validation in Stata while delegating all calculations to the
shared core.

## Scope

- CSV file import into Stata via `mchs import`
- CLI invocation via `mchs run`, using Stata `shell`
- File-boundary column validation via `mchs validate`
- Health-economics workflow notes

## Out of scope

- Formula parsing or evaluation in Stata
- Stata `.do` or `.ado` files with calculator formula logic
- Stata formula port or reimplementation
- SSC package or ADO publication

## Layout

- `mchs.ado` — thin Stata command adapter for file and CLI boundaries
- `mchs.sthlp` — Stata help for the adapter
- `README.md` — this file
- `examples/` — Stata `.do` examples showing CLI invocation and file import
- `stata-interop-notes.md` — Health-economics workflow notes

## Usage

Refer to the binding strategy document at
`conductor/tracks/stata_interop_binding_20260513/binding_strategy.md`
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
