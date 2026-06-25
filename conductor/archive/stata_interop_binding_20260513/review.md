# Stata Interoperability Track Review

## Findings

1. Resolved - The track records file-import and CLI-invocation as the
   primary paths, DTA-exchange and service as fallback, and explicitly
   excludes Stata formula ports.
2. Resolved - The track includes live contract examples, a bounded Stata
   file/CLI adapter, and tests that validate metadata, diagnostics,
   provenance, command surface, and no formula duplication.
3. Resolved - The adapter exposes `mchs import`, `mchs run`, and
   `mchs validate` while publication and owner-backed promotion remain
   deferred; no Stata package publication or formula logic is claimed.

## Changed files

- `microcosting_healthservices/conductor/archive/stata_interop_binding_20260513/review.md`
- `microcosting_healthservices/bindings/stata/mchs.ado`
- `microcosting_healthservices/bindings/stata/README.md`
- `microcosting_healthservices/bindings/stata/mchs.sthlp`
- `microcosting_healthservices/bindings/stata/examples/file_import_workflow.do`
- `microcosting_healthservices/bindings/stata/examples/nwau_cli_invocation.do`
- `microcosting_healthservices/bindings/stata/stata-interop-notes.md`
- `microcosting_healthservices/contracts/stata-interop-binding/README.md`
- `microcosting_healthservices/contracts/stata-interop-binding/stata-interop-binding.contract.json`
- `microcosting_healthservices/conductor/archive/stata_interop_binding_20260513/binding_strategy.md`
- `microcosting_healthservices/conductor/archive/stata_interop_binding_20260513/metadata.json`
- `microcosting_healthservices/conductor/archive/stata_interop_binding_20260513/plan.md`
- `microcosting_healthservices/tests/test_stata_interop_binding_track.py`

## Validation

- Design review was conducted against the binding strategy specification
  and the Stata interop contract. All transport modes, request/response
  structs, diagnostics, provenance, and fixture gates are documented.
- Focused static validation checks the bounded adapter command surface and
  confirms Stata remains a transport-only boundary.

## Risks

- The Stata adapter is transport-only and shells out to the installed
  shared-core CLI; runtime success depends on `funding-calculator` or an
  explicitly configured CLI command being available.
- CLI invocation from Stata on Windows requires PATH configuration and
  may need full binary paths for `winexec`.
- The `parquet` Stata package is community-maintained and
  version-dependent; CSV is the recommended portable format.
- The maintained Stata `.ado` adapter must remain free of calculator formula
  logic; no Mata implementation or SSC package publication is maintained in
  this repository.
