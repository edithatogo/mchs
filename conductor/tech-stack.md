# Tech Stack

## 2026-11-08 shared valuation direction

The proposed [Dapane framework](../docs/roadmaps/dapane-framework.md) uses an
independent Rust core, Python first, then thin R/Julia bindings and optional
Arrow/Parquet/process/Power Platform adapters. This is a design decision for a
future shared package; it changes no current manifest, runtime pin or released
API. MCHS retains its domain equations and source-qualified tariff responsibilities.
The [execution track](tracks/shared_microcosting_valuation_20261108/index.md)
requires exact numeric transport, two domain consumers and installed-artifact
evidence before promotion.

## Current Repository State — manifest review 2026-11-08

The following records checked packaging and workflow declarations. It does not
establish that the declared versions install together, that CI has passed, or
that every calculator or binding is qualified.

- [Python metadata](../pyproject.toml) declares `nwau_py` version `0.2.2`,
  Python `>=3.15.1,<3.16` and a `setuptools>=77` build backend.
  [The interpreter file](../.python-version) and
  [PR workflow](../.github/workflows/pr-ci.yml) select Python `3.15.1`.
- Declared runtime dependencies are `click`, `lightgbm`, `msgpack>=1.2.1`,
  `numpy`, `pyarrow`, `pydantic`, `polars`, `narwhals>=2.28.0`, `pyreadstat`,
  `pyxlsb` and `pyyaml>=6.0.3`. `pyarrow` is a required root dependency;
  `pandas` is absent from this runtime list. Remaining legacy pandas use,
  including extraction tooling, needs its own compatibility evidence.
- Dependency groups separate `dev`, `test`, `coverage`, `security`, `typing`,
  `property`, `mutation`, `profiling`, `docs` and `privacy`. Current gates use
  Ruff, pytest, ty and the declared security tools. Existing mypy configuration
  is transitional rather than the active type-checking contract.
- Python entry points are `funding-calculator`, `mchs-mcp` and `mchs-mcp-http`.
- The [Rust workspace](../rust/Cargo.toml) contains `nwau-core`, `nwau-c-abi`
  and `nwau-py`, using edition 2021. It patches `pyo3-polars` to a vendored
  directory; that patch must be included in dependency/provenance reviews.
- [nwau-core](../rust/crates/nwau-core/Cargo.toml) declares Arrow/Parquet
  `60.1`, `rust_decimal` `1.43.0`, Rayon `1.12.0` and optional wgpu `30.0.1`.
  Its default features enable both Arrow/Parquet and hardware acceleration.
  Dapane's proposed minimal core must explicitly qualify a smaller dependency
  boundary; it must not inherit these defaults without a decision.
- [nwau-py](../rust/crates/nwau-py/Cargo.toml) declares PyO3 `0.29.0`,
  pyo3-polars `0.28.0` and Polars `0.55.2`. Its default `abi3-py310` feature
  is an extension ABI setting, not evidence that the root Python package
  supports Python 3.10. The [C ABI crate](../rust/crates/nwau-c-abi/Cargo.toml)
  has `publish = false`.
- Rust package descriptions still use acute/canary wording. Existing track
  completion markers and available source are not substitutes for installed
  artifact and calculator-specific parity evidence. This review does not
  promote any stream, wrapper or registry release.
- Configured Rust checks are `cargo fmt`, `cargo clippy` and `cargo test`;
  current workflow declarations also include audit and platform wheel jobs.

## Target Platform

MCHS currently declares the Python range recorded above. The earlier Python
3.10–3.14 target is superseded as a description of current packaging. A future
shared-framework compatibility matrix must be selected from installable provider
dependencies and independently exercised artifacts; no broader matrix is
qualified by this roadmap.

The intended end state is a proper polyglot library with a shared Rust core and
thin language adapters. Python remains the reference user-facing package during
the transition, but the long-term architecture should expose the same validated
calculator contracts through Python, Rust, R, Julia, C#/.NET, Go,
TypeScript/WASM, Java/JVM, C ABI, SQL/DuckDB, SAS interoperability, CLI/file
interop, web, Power Platform, and institutional integration surfaces without
duplicating formula logic.

Each advertised Python version must have installation, native-extension and
shared-fixture evidence in CI and coverage reporting. A configured matrix is
not evidence of a successful run. R may use extendr directly against the Rust
core; Julia's C ABI qualification does not block that R route.

## Package and Environment Management

Use `uv` for dependency management, lockfile generation, local development workflows, and CI installation.

Use `pyproject.toml` plus a committed `uv.lock` as the source of truth for environment resolution. Keep `requirements.txt` and `requirements-dev.txt` only as transitional compatibility artifacts or generated views during the migration to `uv`.

The project should maintain clear dependency groups for:

- Runtime dependencies.
- Development tooling.
- Testing and validation.
- Documentation tooling.
- Performance and profiling tools.

Use Renovate for automated dependency update proposals, including Python tooling, GitHub Actions, documentation tooling, and any package manager files managed by `uv`.

Changes to the declared Python range, Rust dependencies or compatibility matrix
require their own lockfile, packaging and consumer qualification. This roadmap
does not change those declarations or advance any provider pin.

## DataFrame and Compute Stack

The target DataFrame engine should be Polars rather than pandas.

Arrow should be the canonical interchange and storage format for tabular reference data, extracted calculator tables, intermediate reusable datasets, and cross-library compatibility. DataFrame boundaries should prefer Arrow-compatible schemas so data can move between Polars, Python libraries, and future compute backends without lossy conversion.

For MCHS batch execution, Arrow-compatible input and output remain the intended
interchange boundary. The proposed Dapane core uses typed quantities and exact
decimal/rational semantics independently of a table engine; optional Arrow and
Polars adapters must preserve those semantics without silent float coercion.

JAX/XLA should be considered for calculation paths where vectorized numerical behavior, compilation, batching, or accelerator portability provides a measurable benefit. JAX should not obscure calculator traceability; calculation behavior must remain explainable against IHACPA source logic.

Existing pandas code should be treated as legacy implementation detail until replaced or wrapped behind stable abstractions.

## Validation and Modeling

Use Pydantic where structured validation is needed for calculator parameters, configuration, input schemas, output schemas, pricing-year metadata, and extracted reference data manifests.

Validation should be explicit at module boundaries:

- Calculator parameters should have strict schemas.
- Pricing year selection should validate against available and supported data.
- Input data requirements should be declared, checked, and documented.
- Output columns and types should be predictable and testable.
- Reference data provenance should be represented in structured metadata.

## Calculator Architecture

The project should enforce strict abstraction between:

- Calculator orchestration.
- Calculator formulas and deterministic logic.
- Parameter models.
- Input/output schemas.
- Reference data loading.
- Source provenance and validation metadata.
- Classification and coding-set registries.
- Mapping-table and formula-bundle extraction.
- External classifier and grouper integration.
- CLI and user-facing workflow code.
- Rust-core kernel logic and language adapters.

Calculator functions should avoid hidden global state. Calculation behavior should be deterministic for a given input dataset, pricing year, parameter model, and reference data bundle.

The architecture should support comparisons against SAS, Excel, compiled/Python
reference files and extracted Arrow-backed datasets. A historical Python output
is a regression comparator, not automatically an independent scientific oracle.
Rust promotion remains calculator-specific and requires recorded source and
fixture evidence.

Future calculator support should follow a ports-and-adapters model:

- Formula kernels consume validated parameter bundles and typed input batches.
- Reference data bundles describe the pricing-year facts used by the kernels.
- Coding-set registries describe which classification versions are compatible
  with each pricing year and stream.
- Mapping and grouping adapters derive classifications only through declared
  table, command, service, or local licensed-tool interfaces.
- Language bindings call the shared Rust core or CLI/file contract and must not
  duplicate formula logic.
- Apps and notebooks orchestrate data preparation, validation, and result
  presentation only.

Abstraction boundaries are part of the validation surface. A new stream,
pricing year, classifier, language binding, or app surface is not complete until
tests demonstrate that the correct contract is used and incompatible versions
or duplicated formula paths are rejected.

Rust-core promotion should be staged:

- Retain qualified Python/reference implementations as comparison baselines until
  a Rust stream matches the applicable independent fixtures. Record any repairs
  to earlier implementations separately from mechanical migration.
- Promote one calculator stream at a time from Python parity baseline to Rust
  canary, Rust opt-in, then Rust default only after evidence is recorded.
- Keep Arrow-compatible batch schemas as the cross-language boundary.
- Keep all language bindings thin and generated or contract-tested wherever
  practical.
- Treat C ABI, WASM, R, Julia, C#/.NET, Go, Java/JVM, SQL/DuckDB, SAS interop,
  CLI/file, web, and Power Platform surfaces as consumers of the shared
  contract, not as peer formula implementations.

## Testing and Quality

Use `pytest` as the base test runner.

Use Codecov for coverage reporting. The current PR workflow declares Python
3.15.1; extend coverage only alongside a separately qualified compatibility
matrix. No successful CI or coverage result is asserted by this document review.

Use Hypothesis for property-based tests around calculator invariants, input validation, boundary conditions, and source-parity assumptions where exhaustive examples are impractical.

Use mutmut for mutation testing of core calculation logic, especially arithmetic, branching, adjustment, and validation paths.

Use Scalene for profiling performance and memory behavior during calculator execution, extraction workflows, and DataFrame conversion paths.

Use `ty` instead of `mypy` for Python type checking. Treat `mypy` as transitional only until the migration is complete.

Codecov is the coverage reporting gate for CI. Local coverage runs should
produce the same XML artifact that the workflow uploads so the report remains
stable across the active Python matrix.

Use Ruff for linting and formatting unless a future decision explicitly replaces it.

Use Rustfmt and Clippy for Rust code formatting and linting, and keep Rust
tests in the CI gate once the workspace is part of the active track.

## Logging and Observability

Use Python logging consistently across CLI, data loading, extraction, validation, and calculator orchestration code.

Logging should support maintainers without changing calculation outputs. It should make data source selection, pricing-year resolution, validation warnings, cache use, and comparison workflows easier to diagnose.

Avoid print-based diagnostics in library code.

## Version Management

The project should use explicit version management for the package, calculator data bundles, validation status, and supported pricing years.

Versioning should make clear distinctions between:

- Package release version.
- IHACPA pricing year.
- Reference data version.
- Extracted dataset version.
- Calculator validation status.

Release notes should identify calculator behavior changes, source-data changes, validation changes, and compatibility changes.

## Documentation Stack

Documentation should use a state-of-the-art documentation approach that supports API reference material, conceptual guides, validation guides, source provenance, and contributor workflows.

The documentation system should support:

- Generated API reference from typed Python code.
- Narrative guides for calculator parity and pricing-year validation.
- Source mapping from IHACPA SAS, Excel, compiled/Python, and support files to Python modules.
- Versioned documentation for supported releases or pricing years where practical.
- Executable examples or checked snippets where useful.
- Clear contributor guides for adding or validating a pricing year.

Use Vale for prose linting so documentation remains precise, conservative, and consistent with project terminology.

## Starlight Documentation Site

The public documentation site should be implemented with Astro and Starlight.

Current manifest declarations and roadmap assumptions:

- [docs-site/package.json](../docs-site/package.json) currently declares
  `@astrojs/starlight` `0.42.8`, `astro` `7.4.4`,
  `starlight-links-validator` `0.27.0` and `starlight-versions` `0.10.1`.
  These are inspected pins, not a claim of latest upstream versions or a
  successfully built combination. Advance them through reviewed dependency
  updates with site-build and link evidence.
- Use Starlight on GitHub Pages with a static build output.
- Treat versioned documentation as a first-class requirement for calculator release and pricing-year docs.
- Expose versioned docs through the `/versions/` index and keep the version switcher available in the public docs header.
- Keep the default Pagefind search unless a stronger search service becomes necessary.
- Include `starlight-links-validator` in CI to catch broken links early.
- Use `starlight-versions` for release-year navigation and versioned reference paths.
- Keep the Starlight extension set minimal: use `starlight-links-validator` and `starlight-versions`; evaluate `starlight-openapi` and `starlight-typedoc` only when those surfaces are real.
- Evaluate `starlight-openapi` if generated API documentation becomes part of the public docs surface.
- Publish the public calculator contract in the docs site so OpenAPI or typed client generation has a clear canonical anchor when that surface is needed.
- Avoid adding plugins that do not support docs quality, versioning, navigation, or generated reference content.

## Dependency and Maintenance Automation

Use Renovate to keep dependencies and GitHub Actions current through reviewable pull requests.

Renovate should be configured to avoid unsafe automatic upgrades for tools or libraries that may affect calculator outputs without validation.

## Migration Guidance

Treat the transitional tools and files as compatibility scaffolding, not as the long-term contract:

- `requirements.txt` and `requirements-dev.txt` are compatibility views during the `uv` migration.
- `mypy` remains a comparator until the `ty` migration is complete.
- Remaining pandas-based paths are legacy compatibility surfaces; pandas is not
  declared in the current root runtime dependency list. Qualify or repair those
  paths explicitly rather than describing them as the universal current engine.
- Rust-core migration should be calculator-by-calculator and fixture-gated. Adapter code in Python, C#, web, Power Platform, R, Julia, Go, and TypeScript must not duplicate formula logic.

Changes to legacy pandas paths, Polars/Arrow adapters, Pydantic validation or
experimental JAX/XLA paths must proceed in bounded phases with independent
reference cases and regression checks. No implementation or dependency migration
is completed by these documentation changes.

Each migration phase should preserve or improve calculator fidelity against IHACPA reference sources and should be documented in this file as either transitional or intended-state tooling.
