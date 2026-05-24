---
title: Downstream packaging plans
---

Packaging for shell, notebook, R, Julia, SAS-adjacent, batch-system, C#,
Go, Power Platform, and the TypeScript/WASM browser demo stays thin and
contract driven. None of these surfaces should duplicate calculator formulas.

Rules:

- Shell scripts and notebook cells should call the shared CLI, write or read
  files at the boundary, and keep any local transformation limited to
  orchestration.
- Notebook examples should use synthetic fixture data and document the file
  names, working directory, and CLI command that produced each result.
- R should start with a thin wrapper over the shared CLI plus CSV file
  exchange, with Arrow/Parquet deferred until the shared file contract exists.
- R should evaluate `extendr` when native Rust integration is justified by
  fixture-backed parity and stable ownership boundaries.
- R Markdown and Quarto examples should use synthetic fixture data and read
  back shared outputs only.
- Keep the R surface wrapper-only; do not reimplement formulas, adjustment
  logic, or validation rules in R.
- Treat CRAN packaging as deferred until the install posture, dependency
  checks, and package skeleton are stable.
- Julia should start with a thin CLI/file wrapper, using CSV for the executable
  prototype and `DataFrames.jl` plus `Arrow.jl` around the target interchange
  workflow once the shared Arrow contract exists. Treat C ABI, `ccall`, and
  `jlrs` as later options only if native embedding becomes necessary.
- Julia should evaluate `jlrs` or a `ccall` wrapper only after fixture parity
  and the Rust core boundary are stable.
- SAS-adjacent workflows should stay file based and external-process driven.
  Use them for importing fixtures, calling the shared CLI, and exporting
  outputs, not for reimplementing calculator rules inside SAS code.
- C ABI consumers should use a stable C boundary or a secured service
  boundary. Any native integration must document ownership, allocator
  responsibilities, and error translation before it is embedded in an
  institution's runtime.
- C# should prefer a stable ABI or secured service boundary.
- Go should prefer a C ABI wrapper or secured service boundary.
- Power Platform should use a custom connector or service boundary only.
- Batch systems should treat the shared CLI as the execution unit and pass
  input and output files through scheduler-managed storage or object storage
  rather than embedding formula logic in job steps.
- The TypeScript/WASM browser demo should stay synthetic, browser-only, and
  wrapper-only. Use WASM as the runtime target, keep Node limited to build and
  developer tooling, and keep browser bundle size under a practical demo
  budget.
- Browser privacy limits apply: do not treat the client as a trusted data
  store, do not cache patient-level data, and keep any telemetry synthetic only.
- Keep all formula and validation logic in the shared engine; do not duplicate
  calculator rules in TypeScript just to make the browser demo easier.
- For any downstream surface that reads or writes files, prefer the current
  CSV contract for executable examples and the Arrow/Parquet target for the
  shared interchange roadmap. Use explicit schemas and column names so the
  files remain compatible across runtimes.
- Capture diagnostics and provenance alongside every batch run: record the CLI
  version, file hashes or source identifiers, input file name, output file
  name, and any validation warnings that were emitted.
- Keep privacy rules consistent across all wrappers: do not store patient-level
  data in browser caches, notebook outputs, or ad hoc local artifacts beyond
  the minimum needed to run the job.
- Release readiness depends on shared fixture parity, stable contract
  versioning, and repeatable cross-runtime validation evidence.
- Release readiness depends on shared fixture parity, stable contract
  versioning, and Arrow-boundary consistency across all downstream surfaces.
- For C ABI consumers, keep fixture parity with the shared engine, preserve
  Arrow as the boundary for tabular exchange where possible, and avoid formula
  duplication in the native wrapper.

See the CLI/file interop tutorial in
[tutorials/cli-file-interop](../tutorials/cli-file-interop.mdx).

See also the C ABI consumer guide in
[tutorials/c-abi-consumers](../tutorials/c-abi-consumers.mdx).

See the canonical source in
[Conductor downstream-packaging-plans.md](https://github.com/edithatogo/microcosting_healthservices/blob/master/conductor/downstream-packaging-plans.md).
