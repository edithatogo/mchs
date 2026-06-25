# Specification: TypeScript and WebAssembly Binding

## Overview
Provide a TypeScript/WASM integration for browser-based documentation demos, GitHub Pages workflows, and optional Node use. WASM must consume the shared Rust core and must be scoped carefully around data privacy and bundle size.

## Functional Requirements
- Define WASM-safe calculator boundaries and supported streams.
- Generate typed TypeScript wrappers and validation errors.
- Add browser demo examples using synthetic data only.
- Add CI build checks for WASM artifacts without publishing sensitive data.

## Acceptance Criteria
- TypeScript API definitions are generated or hand-maintained from the public contract.
- Browser examples run only on synthetic data.
- WASM outputs match shared golden fixtures for validated calculators.
