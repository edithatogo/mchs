# Rust Core Continuation Release Evidence

Date: 2026-05-24
Scope: Rust Core Continuation Phase 2-4 baseline parity and support evidence

## Summary

Rust Core Continuation remains a conservative parity gate. Production Rust was
changed only to replace ambiguous subacute fallback behavior with a bounded
synthetic canary and explicit unsupported diagnostics. Python remains the
default runtime and exposes no subacute Rust entrypoint.

The only Rust-backed calculator stream with executable baseline parity evidence
is the acute 2025 canary path:

- Rust kernel: `nwau-core` acute 2025
- Python opt-in entrypoint: `nwau_py.calculators.acute.calculate_acute_rust_2025`
- Golden fixture: `tests/fixtures/golden/acute_2025`
- Python parity tests: `tests/test_rust_parity/test_python_parity.py`
- Rust contract tests: `rust/crates/nwau-core/tests/acute_2025_contract.rs`

Support status after this continuation pass:

- Acute 2025: Rust canary only.
- Sub-acute: internal Rust synthetic canary only; blocked for Python/public
  Rust support until source-backed parity fixtures and a bridge entrypoint
  exist.
- Emergency and community mental health: blocked for Rust support.
- All other streams: no Rust promotion claim without stream-specific tests and
  release evidence.

## Phase 2 Gate Matrix

| Stream | Current Rust state | Evidence status | Next conservative gate |
| --- | --- | --- | --- |
| Acute 2025 | Canary | Passing synthetic Python/golden parity exists for the committed three-row fixture. | Broaden fixture coverage beyond the synthetic acute 2025 pack before default promotion. |
| Emergency | No Rust entrypoint | Blocked; Python calculator exists, but no Rust kernel or source-backed golden fixture is committed. | Add a trusted AECC or UDG fixture and write the failing parity test before Rust implementation. |
| Sub-acute | Internal synthetic Rust canary with unsupported diagnostics for all non-canary input | Blocked for Python/public support; canary output is not source-backed parity evidence. | Add a trusted source-backed fixture, red-phase parity test, and Python/CLI exposure decision before support promotion. |
| Community mental health | No Rust entrypoint | Blocked; Python calculator exists, but no Rust parity fixture is committed. | Add a trusted Python/source fixture before Rust promotion. |

## Remaining Limits

- The acute canary fixture is small and synthetic; it does not establish full
  acute SAS/Excel parity, all-year support, or default Rust runtime behavior.
- The optional Python Rust entrypoint is evidence for explicit acute 2025
  canary use only.
- Sub-acute cannot be promoted from internal canary to public opt-in support
  until a trusted fixture, failing parity test, Python/CLI entrypoint, and
  passing evidence are committed.
- CLI/file behavior, C ABI compatibility, packaging, and language bindings are
  not promoted by this evidence file.

## Intentionally Not Added As Failing Tests

The following would be valid red-phase tests, but they are intentionally
recorded here instead of committed as failing tests because this task was
limited to baseline evidence and no production Rust/Python implementation
changes:

- Emergency Rust parity against a trusted AECC or UDG fixture.
- Sub-acute Rust parity against a source-backed, non-synthetic fixture.
- Community mental health Rust parity against a trusted Python/source fixture.
- Rust default behavior in the Python binding for any stream other than the
  explicit acute 2025 canary entrypoint.

## Added Evidence Tests

- `tests/test_rust_parity/test_phase2_promotion_gate.py` records the Phase 2
  promotion matrix as executable Python evidence and asserts that only acute is
  claimed as a Rust canary stream.
- `rust/crates/nwau-core/tests/phase2_promotion_gate.rs` records the Rust
  registry gate, proves the synthetic subacute canary boundary, and asserts
  that non-canary subacute remains blocked from promotion.

## Commands Run

- `uv run pytest tests/test_rust_parity -q`
  - Result: passed, `19 passed in 0.36s`
- `uv run pytest tests/test_rust_core_continuation_track.py tests/test_rust_core_ga_roadmap.py -q`
  - Result: passed, `4 passed in 0.02s`
- `(cd rust && cargo test -p nwau-core --test acute_2025_contract --test phase2_promotion_gate)`
  - Result: passed after the subacute canary boundary landed.
- `(cd rust && DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/Caskroom/miniconda/base/lib cargo test)`
  - Result: passed. The fallback library path is required on this workstation so
    the `nwau-py` Rust test binary can locate `libpython3.13.dylib` without
    overriding Homebrew libraries used by Cargo.

Earlier validation exposed two test-harness
issues: tolerance was read as a mapping even though fixture precision is now a
dataclass, and randomized parity compared full frame shape even though the
Rust opt-in adapter intentionally returns a narrow result. Both were corrected
inside `tests/test_rust_parity/test_python_parity.py`; no production code was
changed.
