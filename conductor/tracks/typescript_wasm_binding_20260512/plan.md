# Plan: TypeScript and WebAssembly Binding

## Phase 1: Browser Contract and Safety
- [x] Task: Define the conservative browser docs demo contract and WASM-safe scope.
    - [x] Identify calculators suitable for client-side execution only when they are fixture-backed and deterministic.
    - [x] Lock docs demos to synthetic data only and keep privacy rules explicit.
    - [x] Set initial bundle boundaries and defer anything that expands the browser surface materially.
    - [x] Require TypeScript definitions to be generated from, or hand-maintained against, the public contract.
    - [x] Require browser-demo examples and fixtures to be synthetic-data-only.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Browser Contract and Safety' (Protocol in workflow.md)

## Phase 2: WASM Build and TypeScript API
- [x] Task: Add a minimal WASM build prototype with a hand-maintained public TypeScript facade.
    - [x] Keep generated helpers limited to low-level bindings or export metadata.
    - [x] Validate included calculators against shared golden fixtures before widening scope.
    - [x] Add the browser docs demo and thin Node workflow as prototype surfaces only.
    - [x] Add a wrapper-only TypeScript WASM export adapter that rejects modules whose exports do not match the contract.
    - [x] Add CI notes for future WASM artifact checks without publishing sensitive data.
    - [x] Add repository tests for the adapter, synthetic-only policy, no formula duplication, and conservative publication state.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: WASM Build and TypeScript API' (Protocol in workflow.md)
