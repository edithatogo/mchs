# Strategy: CLI and File Interoperability Binding

## Decision
Use a versioned CLI plus file-interchange contract as the conservative
integration path for non-native consumers. Keep the boundary language-neutral
and prefer Arrow/Parquet as the target interchange format, with CSV supported
only for compatibility where the loss characteristics are explicit.

This is the safest path because it:
- keeps the calculation core single-sourced
- works across R, Julia, Power Platform, notebooks, and batch systems
- avoids forcing a native binding before the contract is stable
- preserves reproducibility through files, provenance, and fixture diffs

## Contract shape

### CLI contract
- Every externally supported command must have an explicit versioned contract
  and documented input/output flags.
- The CLI must reject unknown contract versions rather than guessing.
- Batch commands should expose a validation mode and a compute mode so callers
  can fail fast before committing to a full run.
- Diagnostics should be machine-readable and stable enough for regression
  testing.

### File contract
- Arrow IPC or Parquet is the target interchange for the long term.
- CSV remains a compatibility format only when the schema is flat enough and
  the caller accepts its limitations.
- The contract must document required fields, nullability, types, encoding,
  ordering assumptions, and versioned metadata fields.
- File-based round trips must be fixture-driven and deterministic.

### Versioning policy
- Version the CLI/file contract independently from release packaging.
- Major version changes indicate breaking schema, command, or semantics
  changes.
- Minor versions may add optional fields, diagnostics, or compatible
  commands.
- Patch versions are reserved for non-contractual fixes.
- Callers must be able to discover the runtime contract version before
  attempting a run.

## Diagnostics and provenance
- Emit provenance with the output artifact or alongside it in a dedicated
  machine-readable record.
- Include at minimum the contract version, calculator version, command name,
  timestamp, source input reference, schema identifier or hash, and summary
  counts.
- Validation warnings should be explicit and separable from successful compute
  output.
- Failure output should explain which field, file, or rule failed without
  leaking unrelated internal state.

## Privacy and synthetic examples
- Use synthetic or anonymized examples only.
- Do not place PHI, patient-level extracts, secrets, or private source data in
  fixtures, docs, logs, or sample output.
- Keep examples small, deterministic, and representative of edge cases that
  matter for schema compatibility.
- When a realistic example is needed, derive it from synthetic data generation
  rules rather than copied operational records.

## When to use file interop instead of native bindings
Choose file interop when the priority is:
- cross-language reuse without adding a runtime dependency
- auditability and reproducible batch execution
- clear artifact retention for review or handoff
- integration with data pipelines, schedulers, or notebook workflows
- a stable, externally inspectable contract before an in-process API exists

Prefer native bindings only when all of the following are true:
- the consumer needs low-latency in-process calls
- the host runtime is already a supported dependency
- the binding can share a stable schema and error model with the CLI contract
- the team is ready to own release, packaging, and compatibility work for that
  host language

For this track, file interop remains the preferred default until the shared
contract proves stable across golden fixtures and representative consumers.

## Readiness bar
- This track is conservative and roadmap-first.
- Do not claim production readiness until the CLI contract, file schema,
  diagnostics, provenance, and CSV compatibility rules are all fixture-backed.
- Arrow/Parquet should be the target for serious batch use; CSV is a bridge,
  not the endpoint.
- A stronger native binding story can follow later, but only after the file
  contract is stable enough to anchor it.
