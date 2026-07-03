# wasm-binding

This directory is a TypeScript WASM export adapter for Rust/WASM calculator
modules. It preserves a thin loading, validation, and delegation boundary.

It is intentionally not a calculator implementation. The wrapper only:

- loads a `wasm-pack`-style module
- validates the exported surface
- provides a safe boundary for downstream callers

Formula logic stays outside this package. Generated Rust/WASM output should be
wired into the adapter here rather than duplicating calculator rules in
TypeScript.

Browser demos that use this package must use synthetic data only. Do not place
PHI, patient-level records, secrets, tokens, or private study data in fixtures,
bundles, screenshots, logs, or example payloads.

## Current Status

- No funding formulas are implemented here
- The package validates and delegates to `wasm-pack` output
- Published to npm as `@edithatogo/mchs-wasm-binding@0.1.0`
- Publication does not imply formula ownership; TypeScript remains a boundary
  layer over Rust/WASM exports

## Suggested shape

The adapter expects a module factory so callers can plug in WASM output
without changing the wrapper contract:

```ts
import { createWasmCalculatorAdapter } from './src/index.js';

const binding = await createWasmCalculatorAdapter(() => import('../pkg'));
await binding.ready;

const output = await binding.calculate({ fixture: 'synthetic-only' });
```

The calculator adapter validates that the WASM module exposes a callable
`calculate` export, runs optional `wasm-pack` default initialization, calls an
optional exported `init`, and then delegates calculation to Rust/WASM. It does
not implement or re-state formula rules in TypeScript.
