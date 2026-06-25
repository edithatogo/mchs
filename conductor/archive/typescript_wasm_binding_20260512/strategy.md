# Strategy: TypeScript and WASM Binding Initial Path

## Decision
Start with **browser docs demos** as the first delivery path, using a narrow
WASM surface, synthetic data only, and a hand-maintained public TypeScript
facade. Keep **Node workflows** as a thin secondary path that reuses the same
exports and contract, but does not add a second implementation surface or any
data-collection behavior.

This is the conservative path because it:
- keeps the first visible demo small and easy to reason about,
- avoids exposing real study data in the browser,
- limits the initial bundle footprint,
- and lets the Node path stay aligned with the same contract instead of
  growing its own API shape.

## Comparison

### Browser docs demo first
- Lowest-risk way to prove the WASM contract in a controlled environment.
- Easy to enforce synthetic-data-only examples.
- Fits documentation and GitHub Pages style workflows without adding server
  dependencies.
- Best place to validate bundle size and loading behavior before widening scope.

### Node-first workflow
- Useful for local automation and developer checks.
- Broader file-system and runtime surface than a browser demo.
- Harder to keep visually and operationally constrained without accidentally
  expanding into a general-purpose runtime integration.
- Appropriate only as a thin wrapper around the same WASM artifact.

### Full browser + Node parity up front
- Highest maintenance cost.
- Encourages extra compatibility branches for bundling, module formats, and
  runtime assumptions.
- Too broad for an initial binding track that still needs fixture-backed parity
  evidence.

## WASM-safe calculator scope
Only include calculators that are safe to execute inside a browser or Node WASM
runtime without touching external systems.

Allowed in v1:
- deterministic calculations already present in the shared Rust core,
- pure validation and transformation logic over explicit inputs,
- calculator paths that can be verified against shared golden fixtures,
- small, bounded lookup tables that are embedded with the WASM artifact.

Deferred or excluded from v1:
- network access,
- filesystem access from browser code,
- auth/session handling,
- access to patient, worker, or study identifiers,
- time-based or locale-dependent branching that changes outputs implicitly,
- randomness,
- long-running batch orchestration,
- multi-threaded or SIMD-specific optimizations,
- any calculator that cannot be exercised against fixtures in isolation.

## Privacy rules
- Browser demos must use synthetic data only.
- No real patient, employee, provider, study, or billing records may appear in
  committed demo data, screenshots, or example payloads.
- No telemetry, remote logging, analytics, or background upload behavior is
  allowed in the demo path.
- Node workflows may read local files for developer use, but they must not
  transmit data externally or persist sensitive data in generated examples.
- Any debug output must be scrubbed of identifiers and user-level fields.

## Bundle-size boundaries
The initial browser bundle should stay intentionally small.

- Keep the demo shell, TypeScript facade, and WASM artifact narrow enough to
  load quickly in documentation contexts.
- If a candidate calculator pushes the browser artifact beyond the first-pass
  budget, leave it out of v1 instead of widening the bundle.
- Prefer prebuilt assets and simple imports over heavier bundler plugins or
  runtime shims.
- Do not add worker, streaming, or multi-module complexity until a measured
  size/performance need is demonstrated.

## TypeScript contract approach
Use a hybrid contract model:

- The public TypeScript facade is hand-maintained and checked in.
- Generated bindings may exist for low-level WASM glue or export metadata, but
  they are not the authoritative public API.
- The hand-maintained facade is the compatibility layer that browser demos and
  Node workflows import.
- Any generated helper output must stay reproducible from the shared Rust/WASM
  exports and cannot introduce new business rules.

This keeps the contract readable and reviewable while still allowing generated
code where it reduces mechanical drift.

## Deferrals
Defer the following until fixture-backed parity exists and the bundle budget is
still acceptable:

- publication-ready claims,
- npm publication,
- docs-site claims beyond prototype/demo status,
- Node package dual-format work unless it is needed for the thin wrapper,
- advanced performance work such as SIMD, threads, and worker sharding,
- non-synthetic examples,
- broader browser integrations beyond the docs demo surface,
- any calculator that needs extra runtime services or large embedded assets.

## Validation standard
The track must not be described as publication-ready until shared golden fixture
parity exists for the included calculators.

- Browser demos may be called prototype or demo-only before parity.
- Node workflows may be called internal or thin-wrapper only before parity.
- Claims about readiness must remain conservative until the shared fixtures and
  output comparisons prove the binding matches the core contract.
