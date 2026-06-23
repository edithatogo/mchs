# Rust Core Promotion Matrix

This matrix is the Phase 1 baseline for continuing Rust core promotion after
the Rust Core GA roadmap. It is intentionally conservative: Python remains the
validated public baseline unless a stream has Rust parity evidence, delivery
surface tests, support-status evidence, and release evidence for the declared
scope.

## State Vocabulary

| State | Meaning |
| --- | --- |
| `blocked` | Desired support is blocked by source, licence, parity, implementation, or release evidence. |
| `contract-only` | A contract or registry shape exists, but no validated Rust calculator behavior is claimed. |
| `canary` | Experimental Rust behavior exists for limited synthetic or internal fixtures only. |
| `opt-in` | Users may explicitly enable Rust behavior for the declared scope; it is not default. |
| `release-candidate` | Promotion evidence is nearly complete and pending final validation. |
| `GA` | Rust is the default public path for the declared stream and scope. |
| `not-ready` | The stream needs scope, source, or contract work before implementation should begin. |

No stream is marked `GA` in this Phase 1 baseline. The matrix is complete for
Rust Core Continuation support-status purposes: it records acute as canary and
keeps every unproven Rust stream blocked, not-ready, or internal contract-only.

## Stream Matrix

| Stream or surface | Current state | Support claim | Evidence | Owner | Next action | Validation command |
| --- | --- | --- | --- | --- | --- | --- |
| Acute admitted | `canary` | Rust canary only for acute 2025; Python remains default. | `rust/crates/nwau-core/src/acute.rs`, `rust/crates/nwau-core/tests/acute_2025_contract.rs`, `tests/test_rust_parity/test_python_parity.py`, and the opt-in Python bridge show limited acute 2025 Rust parity over synthetic fixtures. SAS/Excel execution remains recorded as not run where licensed tooling is required. | Rust core lane | Keep acute 2025 as the first promotion candidate; expand fixture provenance and source-derived parity before any release-candidate claim. | `(cd rust && cargo test -p nwau-core acute_2025)`; `uv run pytest tests/test_rust_parity/test_python_parity.py tests/test_rust_parity/test_sas_parity.py` |
| Emergency department | `blocked` | No Rust support claim. | ED classification and transition tracks exist, but there is no Rust ED kernel or release evidence in `nwau-core`. | Emergency/classification lane | Define ED input/output contract and fixture bundle before writing Rust parity tests. | `uv run pytest tests/test_emergency_classification_parity_fixtures_track.py tests/test_emergency_grouper_integration_track.py tests/test_emergency_udg_aecc_transition_registry_track.py` |
| Admitted mental health | `not-ready` | No Rust support claim. | No Rust kernel, fixture pack, or stream-specific support-status entry was identified for admitted mental health in the current Rust core. | Mental health stream owner, unassigned | Inventory source material and decide whether this is a distinct admitted stream or an acute-classified slice before implementation. | `rg -n "admitted mental|mental health" conductor docs tests rust` |
| Community mental health | `blocked` | No Rust support claim. | Historical community mental health work is archived; no active Rust stream module or parity fixture is present. | Mental health stream owner, unassigned | Reopen source and fixture discovery before adding Rust contracts. | `rg -n "community mental health" conductor docs tests rust` |
| Subacute | internal `canary` / public `blocked` | Synthetic Rust canary only; no Python or public Rust support claim. | `SubAcuteKernel` has a bounded `SUBACUTE-CANARY` path in `rust/crates/nwau-core/src/kernels.rs` and unsupported diagnostics for all non-canary activity. There is no source-backed fixture or Python Rust entrypoint. | Rust core lane | Add source-backed fixtures and parity tests before exposing subacute through Python, CLI/file, or release evidence. | `(cd rust && cargo test -p nwau-core --test phase2_promotion_gate)`; `uv run pytest tests/test_rust_parity/test_phase2_promotion_gate.py` |
| Outpatient | `not-ready` | No Rust support claim. | No Rust outpatient kernel, source fixture, or support-status entry was identified. | Outpatient stream owner, unassigned | Define Tier 2/outpatient scope, source fixtures, and classification inputs before Rust implementation. | `rg -n "outpatient|Tier 2|tier 2" conductor docs tests rust` |
| Adjustment factors | `contract-only` | Acute canary input support only; no standalone Rust support claim. | Acute 2025 accepts adjustment factors in Rust, but broader adjustment registries and cross-stream validation are not promoted. | Rust core and pricing lane | Separate shared adjustment bundle validation from acute-only scalar inputs and add provenance checks. | `(cd rust && cargo test -p nwau-core adjustment)`; `uv run pytest tests/test_formula_parameter_bundle_pipeline.py tests/test_pricing_year_validation_gates.py` |
| Hospital-acquired complications (HAC) | `not-ready` | No Rust support claim. | No Rust HAC module, HAC classification contract, or parity fixture was identified. | Classification-adjacent lane | Inventory HAC source rules and decide whether the first Rust work is validation, classification input, or calculator adjustment behavior. | `rg -n "HAC|hospital-acquired|hospital acquired" conductor docs tests rust` |
| Avoidable hospital readmissions (AHR) | `not-ready` | No Rust support claim. | No Rust AHR module, AHR classification contract, or parity fixture was identified. | Classification-adjacent lane | Inventory AHR source rules and fixture requirements before implementation. | `rg -n "AHR|avoidable hospital readmission|avoidable readmission" conductor docs tests rust` |
| State and local pricing | `blocked` | No Rust support claim. | Jurisdiction price source and state/local registry tracks exist, but Rust core support is not promoted and support status remains evidence-gated. | Pricing and jurisdiction lane | Complete source index validation and choose one jurisdiction/year slice for Rust contract tests. | `uv run pytest tests/test_pricing_hwau_strategy_tracks.py tests/test_governance_contracts.py` |
| Classification-adjacent surfaces | `blocked` | No Rust formula or grouper support claim. | AR-DRG, emergency, coding-set, and classification input validation tracks define contracts and fixtures, but proprietary groupers and restricted coding assets remain out of scope for Rust formula claims. | Classification lane | Keep classification as versioned validation and registry input to Rust; do not claim grouper implementation without licensed artefacts and parity evidence. | `uv run pytest tests/test_classification_validation.py tests/test_ar_drg_version_parity_fixtures_track.py tests/test_coding_set_version_registry.py` |

## Promotion Order

1. Acute admitted 2025 remains the only current Rust canary candidate.
2. Adjustment factors should be hardened as shared inputs only after acute
   fixture provenance and parity are stable.
3. Subacute canary should stay internal until source-backed failing tests,
   fixture provenance, and Python/CLI exposure decisions exist.
4. ED and classification-adjacent surfaces should advance as validation and
   registry inputs before any proprietary grouping claim.
5. State/local pricing should remain blocked until jurisdiction source indexes
   and validation gates identify a bounded year/jurisdiction slice.
6. Mental health, outpatient, HAC, and AHR should not enter Rust implementation
   until their source scope and fixtures are explicit.

## Phase 1 Validation Notes

- This baseline does not promote any stream to `release-candidate` or `GA`.
- The acute canary claim is limited to the currently visible Rust kernel,
  Python bridge, and synthetic parity fixtures.
- Subacute has only a synthetic internal Rust canary and remains blocked for
  public Rust support unless and until source-backed fixtures, parity tests,
  Python/CLI exposure, and release evidence exist.
- Missing source evidence stays `blocked` or `not-ready`; it is not inferred
  from adjacent contracts.
- Deferred language adapters must remain thin consumers of Rust, CLI/file, C
  ABI, or service contracts and must not duplicate formulas.
