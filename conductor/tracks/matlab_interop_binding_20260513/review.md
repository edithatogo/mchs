# MATLAB Interop Binding Track Review

## Findings

1. Resolved - The track records file-import and CLI-invocation as the initial
   primary paths, MAT-exchange as a native MATLAB fallback, and C ABI MEX as
   a deferred path until the Rust cdylib toolchain and mex configuration gates
   are stable.
2. Resolved - The track includes live contract examples, a binding strategy
   document, and tests that validate metadata, diagnostics, provenance, and
   no formula duplication.
3. Resolved - Toolbox publication is explicitly gated and remains future-only;
   the adapter is not a published MATLAB toolbox claim.
4. Resolved - The MATLAB surface now includes concrete file/CLI boundary
   helpers: `validateInput`, `importResultTable`, and `invokeCli`. They only
   inspect or move data across external boundaries and retain diagnostics and
   provenance for validation.

## Changed files

- `microcosting_healthservices/bindings/matlab/mchs/validateInput.m`
- `microcosting_healthservices/bindings/matlab/mchs/importResultTable.m`
- `microcosting_healthservices/bindings/matlab/mchs/invokeCli.m`
- `microcosting_healthservices/contracts/matlab-interop-binding/matlab-interop-binding.contract.json`
- `microcosting_healthservices/contracts/matlab-interop-binding/matlab-interop-binding.schema.json`
- `microcosting_healthservices/conductor/tracks/matlab_interop_binding_20260513/review.md`

## Validation

- Focused pytest validation: `python -m pytest tests/test_matlab_interop_binding_track.py`.
- Static MATLAB surface validation checks that the adapter uses `readtable`,
  `parquetread`, and `system()` while avoiding calculator rule implementation.

## Risks

- The MATLAB interop adapter is synthetic and transport-only; it only invokes a
  caller-provided external CLI and imports caller-provided result files.
- C ABI MEX posture remains a documented gate until a Rust cdylib build and
  MATLAB mex configuration are validated.
- Toolbox publication remains held at the parity and release evidence gate.
