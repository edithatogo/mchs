# Strategy: R Binding for MCHS

## Decision
Use a thin R wrapper over the shared CLI plus file interchange as the initial
delivery path. CSV is the executable prototype because the current CLI already
supports it; Arrow/Parquet is the target exchange format once the language-
neutral file contract is implemented.

This is the least duplicative option because:
- The costing formulas, validation rules, and diagnostics remain in one shared implementation.
- R only orchestrates input preparation, process execution, and result reading.
- The same core can later serve Python or other consumers without adding a second language binding.

## Comparison

### `extendr`
Best when the primary goal is a native R package with tight Rust integration.

Pros:
- Fast in-process calls.
- Good fit when the long-term target is a first-class R API.
- No Python dependency.

Cons:
- Adds Rust toolchain and compiled-package overhead.
- Increases CRAN release friction because compiled dependencies and cross-platform build support become part of the release surface.
- Tends to pull implementation details into the R package boundary sooner than necessary.

### `reticulate`
Best when the shared implementation already lives in Python or the team wants to reuse an existing Python service immediately.

Pros:
- Fastest path if there is already a maintained Python API.
- Easy for analysts who already work in mixed R/Python environments.

Cons:
- Introduces a Python runtime dependency into the R story.
- Packaging and environment management become harder for reproducible analyst workflows.
- It still leaves the boundary logic split across languages, even if the formulas remain elsewhere.

### CLI + file integration, with Arrow as the target
Best when the priority is single-sourced logic and portable batch workflows.

Pros:
- Keeps formulas and diagnostics in one executable core.
- Works well for large costing-study batches and Quarto/R Markdown pipelines.
- CSV exchange is available now through the existing CLI.
- Arrow/Parquet-style exchange remains the intended large-batch target.
- Easiest path to reuse from other languages or automation surfaces later.

Cons:
- Not as ergonomic as a pure in-process R API.
- Requires a discoverable CLI installation step or bundled runtime strategy.
- Adds file-based orchestration around the core execution path.

## Why this is the least duplicative initial path
Health economics and costing-study work usually needs repeatable batch runs,
auditable inputs, and exported outputs that can be checked in or handed to
reviewers. The CLI plus file-interchange path supports that workflow directly
without forcing the R package to become a second implementation of the
calculator.

That matters because the R surface should stay thin:
- read study inputs
- validate schema and required fields
- call the shared engine
- return results and diagnostics

All rule logic, especially formula logic, stays in the shared core so the R package cannot drift from other consumers.

## CRAN and internal-use constraints

### CRAN constraints
- CRAN expects a package that installs cleanly across platforms without fragile external runtime assumptions.
- Optional system dependencies are easier to manage than embedding a second language runtime, but any external CLI requirement must be clearly documented and handled defensively.
- A CRAN-facing package should therefore stay wrapper-only and avoid duplicating computational logic in R.

### Internal-use constraints
- Internal deployment can tolerate a stronger dependency on the CLI binary and on Arrow/Parquet tooling.
- That makes the CLI path practical for the first version, especially if analysts run the workflow inside controlled project environments.
- Internal distribution also gives room to tighten the contract before deciding whether an in-process binding is worth the added maintenance.

## Recommendation for MCHS
Start with CLI + CSV integration, and keep the API shaped so it can move to
Arrow/Parquet when the shared file-interchange contract is ready.

Follow-up paths:
- If CRAN packaging becomes the primary goal, keep the R package as a thin wrapper and isolate the CLI dependency behind graceful checks and clear install instructions. A future self-contained `extendr` package remains viable if release discipline and parity evidence are strong enough.
- If analyst demand for in-process calls becomes strong, revisit `extendr` later as a second-stage optimization, not the first implementation.
- Use `reticulate` only if the shared core already exposes a stable Python API that MCHS is committed to supporting.

## Formula single-sourcing rule
Formula logic must remain single-sourced in the shared core.

The R layer may own:
- argument shaping
- schema checks
- file IO
- user-facing summaries
- test harnesses and vignette examples

The R layer must not own:
- cost formulas
- adjustment logic
- validation rules tied to the economics engine
- business-rule fallbacks

This avoids drift between languages, preserves auditability for costing studies, and keeps future bindings aligned.
