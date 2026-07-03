# Rust Core Continuation

Roadmap snapshot: 2026-05-24.

This document records the current Rust support state for the Rust Core
Continuation track. Python remains the validated public baseline until Rust
parity evidence exists stream by stream.

## Completion Status

Rust Core Continuation is complete as a documentation and support-status
baseline, not as a broad Rust runtime promotion. The completed state is:

- Acute 2025 is the only Rust-backed calculator canary.
- Python remains the default validated runtime for public calculator use.
- Subacute has an internal Rust synthetic canary boundary only; it remains
  blocked for Python/public support until source-backed parity fixtures and a
  bridge entrypoint exist.
- Every other non-acute Rust calculator stream remains blocked or not-ready
  until stream-specific parity tests and evidence exist.
- No stream is promoted to Rust `opt_in`, `release_candidate`, or `ga` by this
  continuation pass.

## Current Rust State

| Area | Evidence | State |
| --- | --- | --- |
| Rust workspace | `rust/crates/nwau-core`, `rust/crates/nwau-py`, and `rust/crates/nwau-c-abi` exist | `preview` implementation workspace |
| Acute 2025 kernel | `nwau-core/src/acute.rs`, `Acute2025Kernel`, and acute 2025 Rust tests exist | `canary` for a bounded synthetic/reference-fixture slice |
| Python Rust bridge | `nwau_py/rust_bridge.py` loads optional `nwau_py._rust` and falls back by absence | `opt_in` bridge, not default Python runtime |
| C ABI | `nwau-c-abi` exposes acute 2025 FFI shape and status codes | `preview` ABI surface |
| CLI/file Rust path | Rust modules for CLI/file IO exist, but public README usage still names Python CLI | `planned` or `preview` depending on local command coverage |
| Subacute Rust kernel | `SubAcuteKernel` has a bounded synthetic canary and explicit unsupported diagnostics for non-canary activity | internal `canary`; blocked for Python/public support claims |
| Other calculator streams | No Rust kernel parity evidence found in the current docs reviewed for this track | `planned` or `blocked` until fixtures and tests exist |

## Promotion Matrix

| Stream or surface | Current runtime support | Rust state | Next action |
| --- | --- | --- | --- |
| Acute 2025 | Python validated public path; Rust acute canary exists | `canary` | Add parity tests against committed Python and source-derived fixtures, then decide whether to promote to `opt_in`. |
| ED | Python public path | `planned` | Select representative fixture rows and write failing parity tests before Rust implementation. |
| Admitted mental health | Python public path | `planned` | Confirm source fixture availability and map required reference tables. |
| Community mental health | Not GA in support docs | `blocked` | Keep blocked until source, expected outputs, and support scope are explicit. |
| Subacute | Python public path | internal Rust synthetic `canary`; Python/public support blocked | Add a source-backed fixture, Python bridge entrypoint, and parity tests before any user-facing Rust opt-in support. |
| Outpatient | Python public path | `planned` | Inventory formula and reference-data dependencies before kernel work. |
| Adjustment, HAC, AHR | Python public path or supporting logic | `planned` | Decide whether these are standalone kernels or post-processing stages in canonical schemas. |
| State/local pricing | Registry and pricing tracks in progress | `planned` | Keep outside Rust GA until source registry and valuation contracts are stable. |
| Classification-adjacent groupers | Licensed and source-boundary constraints apply | `blocked` where external assets are unavailable | Use local-only placeholders and do not reimplement restricted groupers. |
| Python binding | Optional Rust extension bridge | `opt_in` only for canary work | Preserve Python fallback and emit diagnostics when Rust is unavailable. |
| CLI/file and C ABI | Required Rust GA surfaces | `planned`/`preview` | Prove both consume shared Rust contracts for promoted streams. |

## Validation Commands

Run these commands before changing any support claim in this document:

```bash
uv run pytest tests/test_rust_parity -q
uv run pytest tests/test_rust_core_continuation_track.py tests/test_rust_core_ga_roadmap.py -q
(cd rust && cargo test -p nwau-core --test acute_2025_contract --test phase2_promotion_gate)
```

Optional discovery checks for blocked streams:

```bash
rg -n "SubAcuteKernel|subacute|sub-acute" rust tests docs
rg -n "community mental health|admitted mental|outpatient|HAC|AHR" conductor docs tests rust
```

## Promotion Vocabulary

- `canary`: Rust code exists for a bounded stream/year slice and limited
  fixtures. It is not default behavior.
- `opt_in`: Users can explicitly choose the Rust path and receive fallback or
  diagnostics when unsupported.
- `release_candidate`: Stream parity, docs, CI, packaging, provenance, and
  rollback evidence are complete enough for final validation.
- `ga`: Rust is the supported default for the declared stream/year/surface.
- `blocked`: Required source, fixture, license, implementation, or release
  evidence is missing.
- `contract-only`: Internal backlog label for shape without support evidence.
  Public docs must map it to `blocked`, `planned`, or `deferred`.

## Remaining Limits

- Acute canary evidence is limited to the committed acute 2025 fixture and does
  not prove all acute years, SAS/Excel parity, or public default readiness.
- Subacute has Python calculator coverage, but the Rust kernel is not
  promotable because the current Rust path is an internal synthetic canary with
  no source-backed parity evidence.
- ED, mental health, outpatient, HAC, AHR, state/local pricing, and
  classification-adjacent surfaces need source scope, fixture provenance, and
  red-phase parity tests before Rust implementation or support promotion.
- CLI/file, C ABI, and language adapters remain preview or planned surfaces
  until they are proven against shared Rust contracts for a promoted stream.

## Completion Risks

- Acute 2025 canary tests may cover a narrow fixture slice but still be read as
  full acute parity.
- Optional Python bridge loading can hide missing Rust builds unless diagnostics
  are explicit.
- C ABI shape can be mistaken for stable ABI support before compatibility tests
  and semver policy exist.
- Internal canary kernels such as subacute can satisfy a bounded Rust test
  boundary while still being blocked for Python/public support.
- Future language adapters can duplicate formula logic if they are promoted
  before the Rust contracts are stable.

## Next Actions

1. Expand acute 2025 fixture provenance before any release-candidate claim.
2. Add source-backed subacute fixtures before exposing the Rust subacute canary
   through Python or CLI/file surfaces.
3. Write failing parity tests before expanding implementation.
4. Update support status only after the tests pass and evidence is recorded.
5. Keep Python as the default runtime until a stream reaches GA.
6. Require CLI/file and C ABI consumers to call shared Rust kernels for any
   promoted Rust stream.
7. Keep deferred adapters boundary-only until Rust release-candidate evidence
   exists.
