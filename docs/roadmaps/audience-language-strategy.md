# Audience and Language Strategy

The project should not try to support every language equally. The language
roadmap should be governed by two primary audiences and one rule: no adapter may
own formula logic.

## Primary audiences

### Researchers

Researchers need reproducibility, transparent evidence, and familiar analysis
workflows.

Priority surfaces:

- Python.
- R.
- CLI/file.
- Arrow/Parquet.
- Quarto/Jupyter documentation.
- Julia where existing binding work can be retained.

Conditional surfaces:

- SAS interoperability for parity and legacy institutional datasets.
- Stata interoperability for health-economics and econometric workflows.

### Enterprise engineers

Enterprise engineers need stable contracts, deployment boundaries, and release
evidence.

Priority surfaces:

- Rust crate.
- HTTP API.
- Python binding.
- TypeScript/WASM for browser or edge deployment.
- C#/.NET for Power Platform and Microsoft enterprise integration.
- MCP and OpenAI tool adapters for agentic workflows.

Conditional surfaces:

- TypeScript/WASM for GitHub Pages demos and optional web delivery.
- Power Platform where service boundaries are approved.

## Deprioritized, Decommissioned, and Removed from Roadmap

These language surfaces are deprioritized, decommissioned, and removed from the active roadmap to keep focus strictly on the Rust core:

- Scala/Spark (Formally decommissioned and removed from the active roadmap; no new development).
- Swift (Formally decommissioned and removed from the active roadmap; no new development).
- MATLAB (Historical submission evidence retained only; deprioritized).
- Go (Module proxy evidence retained; deprioritized).
- Standalone C language support / C/C++ (vcpkg/Conan decommissioned; no new development).
- SQL/DuckDB (Deprioritized by default).
- Additional language bindings without a named audience, sponsor, and test owner.

## Active Language Focus (Rust-Core First)

The active roadmap is strictly focused on three core environments:

1. **Rust (`nwau-core`):** Canonical calculation engine, 128-bit decimal arithmetic, high-performance CLI, and single source of truth.
2. **Python (`nwau_py` / Polars):** Thin PyO3 wrapper for health economics, data science, and pipeline execution.
3. **R (`nwauR`):** C-ABI / thin wrapper for academic biostatistics and clinical researchers.

## Promotion criteria

A language or surface can move forward only when it has:

- A clearly named audience.
- A maintainer or owner.
- A thin-binding design.
- Contract tests against canonical schemas.
- Parity fixtures.
- Documentation and examples.
- Packaging and release evidence.

## Recommended strategy

The immediate implementation strategy should be:

1. Rust Core GA.
2. Canonical domain schemas.
3. CLI/file contracts.
4. HTTP API contract.
5. MCP contract.
6. OpenAI tool adapter.
7. HWAU terminology and state/local pricing registry.
8. Parallel national, state, local, and discounted valuation outputs.
9. Conditional languages only after evidence and demand.
