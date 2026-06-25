# CI and Build Notes: TypeScript / WASM Track

This track has a private TypeScript WASM export adapter today. Keep CI conservative until the generated WASM artifact, generated TypeScript contract, and fixture set exist together in the repo.

## Current stance

- Do not add a WASM CI gate to `.github/workflows` yet unless the implementation lands a deterministic package layout and repeatable command sequence.
- Prefer reusable repo-wide checks over track-specific workflow logic until the binding is real and testable.

## Future CI gate commands

Use these as the likely minimum gate once the binding package is implemented:

```bash
cd rust && cargo test
cd rust && cargo fmt --all --check
cd rust && cargo clippy --all-targets --all-features -- -D warnings
cd docs-site && npm ci
cd docs-site && npm run build
```

If a dedicated WASM package or workspace member is added, gate it with the deterministic build command that matches the package manager and target shape, for example:

```bash
cd rust/crates/<wasm-crate> && wasm-pack build --target web --release
cd docs-site && npm run build
```

If browser-level WASM tests are added later, prefer a single stable headless browser command over ad hoc local scripts.

## Fixture parity expectations

- WASM and TypeScript outputs must match the shared Rust-core golden fixtures for every calculator that is exposed in the browser contract.
- Fixture parity should be checked against the same canonical inputs and expected outputs used by the Rust core.
- If any cross-language rounding, formatting, or serialization difference is intentional, document the exception and keep the fixture update scoped to the affected calculator only.
- Do not allow generated wrappers to drift from the Rust contract without an explicit fixture refresh and review note.

## Sensitive-data restrictions

- Browser demos and WASM fixtures must use synthetic or anonymized inputs only.
- Do not place PHI, patient-level data, secrets, API keys, tokens, or private datasets in the repo, the WASM bundle, or CI logs.
- Do not add upload, telemetry, or persistence steps that would export real user data during build or test jobs.
- Any fixture committed for parity checks must be deterministic, minimal, and safe to publish.

## Approval bar for workflow changes

- Only add a workflow gate when the command is reproducible on clean CI runners.
- The gate should fail loudly on fixture mismatch, contract drift, or bundle-size regressions that affect the browser demo contract.
