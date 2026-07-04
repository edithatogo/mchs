# Plan: Julia Binding

## Phase 1: Strategy Selection
- [x] Task: Compare C ABI, PythonCall, and Arrow/CLI integration for Julia.
    - [x] Select the initial binding path based on stability and maintenance cost.
    - [x] Document package and binary-distribution implications.
    - Selected path: CLI/file integration with CSV as the executable prototype and Arrow as the target interchange format, because it keeps calculator formulas single-sourced in the shared core.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Strategy Selection' (Protocol in workflow.md) [checkpoint: archived]

## Phase 2: Prototype and Validation
- [x] Task: Create a Julia prototype using the selected integration path.
    - [x] Add a wrapper-only Julia package scaffold that calls `python -m nwau_py.cli.main`.
    - [x] Add repository tests that enforce no Julia formula duplication and fixture-readiness claims.
    - [x] Add DataFrames.jl and Arrow-target documentation examples.
    - [x] Document CI posture without enabling brittle Julia Actions before fixture parity is executable in CI.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Prototype and Validation' (Protocol in workflow.md) [checkpoint: archived]

## Phase 3: Archive Repair
- [x] Task: Repair metadata.json to record a structured complete-with-gaps support scope, completion policy, archive evidence, and explicit Julia CI/publication gaps.
- [x] Task: Repair plan.md to preserve phase checkpoints and state that fixture parity, Julia CI, and publication readiness remain future gates.
- [x] Task: Tighten focused validation for wrapper-only Julia package metadata, archive metadata, no-formula-duplication guardrails, docs, and CI posture.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Archive Repair' (Protocol in workflow.md) [checkpoint: repaired]
