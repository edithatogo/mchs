# Stata Interoperability Binding Contract

This directory defines the Stata interop binding contract for the MCHS
(MicroCosting Health Services) project.

## Purpose

Provide a synthetic contract that describes how Stata workflows interact
with the shared calculator core through file-based exchange (CSV, Parquet,
DTA) and CLI invocation, with a thin `mchs.ado` adapter for the local
file/CLI boundary — **without** duplicating any calculator formula logic in
Stata code.

## Scope

- **Transport modes**: File import, CLI invocation, DTA exchange
- **Stata adapter**: `bindings/stata/mchs.ado` imports CSV output, invokes
  the shared-core CLI, and validates required provenance columns
- **Request struct**: `StataInteropRequest` — mirrors the public calculator
  contract fields plus transport metadata
- **Response struct**: `StataInteropResponse` — captures success,
  diagnostics, provenance, and transport-specific outputs
- **Examples**: Pass and fail JSON files for validation
- **Rules**: All examples are synthetic; no formula logic is included

## Out of scope

- Stata `.do` or `.ado` file generation with formula logic
- Stata formula port or calculator reimplementation
- SSC package publication
- Real IHACPA pricing data or patient-level extracts

## Files

| File | Description |
|------|-------------|
| `stata-interop-binding.contract.json` | Full Stata interop binding contract |
| `stata-interop-binding.schema.json` | JSON Schema (draft/2020-12) for the contract |
| `examples/` | Pass and fail example JSON files |

## Transport modes

| Mode | Priority | Notes |
|------|----------|-------|
| `file-import` | primary | Stata `import delimited` reads CSV/Parquet from shared core |
| `cli-invocation` | primary | Stata `shell`/`winexec` invokes shared-core CLI |
| `dta-exchange` | fallback | Stata `save`/`use` for native `.dta` workflow |
| `service` | fallback | Online request/response when file/CLI paths are unavailable |

## Privacy

All committed examples are **synthetic**. No real IHACPA data, patient
records, or licensed pricing material is included. See `privacy` block in
the contract JSON for details.
