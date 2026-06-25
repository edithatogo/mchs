# Binding Matrix

## Purpose

This matrix defines the recommended language bindings and delivery surfaces for
the Rust core. It is a roadmap artifact, not a promise that every surface is
already implemented.

Status vocabulary remains intentionally broad: `implemented`, `planned`,
`deferred`, `private`, `preview`, and `advisory` can all appear as surfaces move
through evidence gates.

## Sequencing Rule

- Rust/Python parity is the prerequisite for any non-Python adapter that would
  ship calculator logic.
- Language bindings are thin wrappers over the Rust core, not independent
  calculation engines.
- Stable ABI, Arrow exchange, WebAssembly, or a service boundary may be used as
  appropriate for the target surface.
- GitHub Pages remains synthetic/demo-only.
- Power Platform remains orchestration-only through a service or custom
  connector boundary.

## Language Binding Matrix

| Surface | Status | Recommended toolchain | Boundary shape | Primary risk | Sequencing |
| --- | --- | --- | --- | --- | --- |
| Python | implemented | PyO3 / maturin for the Rust bridge, with the current Python package as the first adapter | Arrow-compatible table exchange and native package import | Adapter drift from the Rust core if parity tests weaken | Keep as the validated production path until Rust parity is fixture-backed |
| Rust | implemented | Native Rust core crate and workspace consumers | Direct crate calls over Arrow-compatible structs/tables | Ordinary crate API stability and release discipline | Core source of truth for all later adapters |
| TypeScript | preview | wasm-bindgen or wasm-pack over a Rust/WASM build | WebAssembly package plus adapter for synthetic browser demos and Node smoke tests | Browser bundle size, serialization friction, and accidental real-data assumptions | Keep demo/fixture usage explicit and preserve shared contract tests |
| R | private | extendr or CLI/file wrapper, with FFI reviewed against the data contract before native promotion | Thin package wrapper over CLI/file or ABI contract | Packaging complexity and host-runtime compatibility | CRAN release remains maintainer-review gated; do not duplicate formula logic |
| Julia | private | jlrs or a Julia `ccall` wrapper depending on the packaging target | ABI wrapper, native package bridge, or CLI/file adapter | Tooling maturity and call-convention maintenance | General registry submission/review is tracked separately; keep adapter contract tests passing |
| C# | preview | Stable ABI wrapper or service boundary, not formula duplication | Managed package over local file/service boundary | Long-term maintenance of interop shims | NuGet publication exists; continue proving boundary-only behavior and compatibility |
| Go | private | C ABI or service boundary, plus file/service adapter where lower risk | Thin wrapper around the Rust core, CLI/file, or service contract | Cross-language memory management and build portability | Module publication exists; keep cross-compilation and contract fixtures stable |

## Delivery Surface Matrix

| Surface | Status | Recommended toolchain | Boundary shape | Primary risk | Sequencing |
| --- | --- | --- | --- | --- | --- |
| GitHub Pages | implemented | Static Astro/Starlight site with fixture-backed content | Synthetic demo shell only | User confusion if real data workflows appear in the browser | Keep demo-only forever; never own calculator math |
| Streamlit | planned | Python-hosted Streamlit app over the existing package | Local/demo analyst surface | Overexposing sensitive data or duplicating service logic | Ship only after Python adapter parity is stable |
| Power Platform | advisory | Custom Connector or secured service boundary | Workflow orchestration only | Formula duplication inside flows, Dataverse, or canvas apps | Consume contracts only; never compute calculator logic |

## Notes

- Implemented surfaces are the ones already available in the repository and
  validated by the current track state.
- Planned surfaces should be treated as sequencing targets, not commitments to
  ship in a single track.
- Deferred means the surface is intentionally not the next implementation step.
- Advisory means the surface is useful for orchestration or governance but
  should not own calculator computation.
