# Implementation Plan: Rust-Core First Multi-Stream Engine

## Phase 1: Emergency Department & Mental Health Kernels
- [x] Task: Port Emergency Department AECC and UDG lookup and valuation into `nwau-core/src/ed.rs`.
- [x] Task: Port Admitted Mental Health AMHCC models into `nwau-core/src/mental_health.rs`.
- [x] Task: Add metamorphic and unit tests verifying parity against SAS golden fixtures.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: ED & Mental Health' (Protocol in workflow.md)

## Phase 2: Outpatient & Subacute Kernels
- [x] Task: Port Non-Admitted Outpatients Tier 2 Clinic models into `nwau-core/src/outpatients.rs`.
- [x] Task: Port Subacute AN-SNAP v5.0 branch valuation into `nwau-core/src/subacute.rs`.
- [x] Task: Add metamorphic and unit tests verifying parity against SAS golden fixtures.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Outpatient & Subacute' (Protocol in workflow.md)

## Phase 3: Universal Accumulator & Drift Audit
- [x] Task: Run 100k episode streaming simulations across all 5 streams in Rust.
- [x] Task: Verify 0.00000000 accumulator drift and profile throughput (>50k eps/sec).
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Drift & Throughput' (Protocol in workflow.md)

## Phase: Review Fixes
- [x] Task: Apply review suggestions 95de8ec
