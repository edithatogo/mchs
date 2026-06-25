# CI and Build Notes: CLI and File Interoperability Binding

This track is still conservative by design. Keep CI focused on deterministic
CLI/file contracts, fixture parity, and documentation quality before adding any
hard workflow gate.

## Current stance

- Do not add a required workflow gate until the CLI command shape, file schema,
  and golden fixtures are stable on clean runners.
- Prefer repo-wide checks and explicit track notes over bespoke workflow logic
  while the binding remains in planning or early implementation.
- Keep the contract versioned and fail closed on unknown schema or unsupported
  file variants.

## Future CI gate commands

Use these as the minimum future gate once the implementation is present and
repeatable:

```bash
uv run funding-calculator --help
uv run funding-calculator interop contract
uv run pytest tests/test_cli.py tests/test_cli_file_interop_binding_track.py -q
```

The current executable CLI surface is the Python Click entrypoint
`nwau_py.cli.main:cli`, exposed as `funding-calculator`. Do not gate a future
workflow on `./target/debug/<cli-binary>` unless a Rust CLI binary has actually
replaced or supplemented that entrypoint.

Add Arrow/Parquet smoke tests only when the command surface supports those
formats:

```bash
uv run funding-calculator acute fixtures/sample.csv --output /tmp/output.csv
uv run funding-calculator <future-command> validate --input fixtures/sample.parquet
uv run funding-calculator <future-command> run --input fixtures/sample.arrow --output /tmp/output.parquet
```

If a dedicated wrapper or packaging step is introduced, gate that exact
reproducible command as well.

## Round-trip fixture checks

- Validate Arrow/Parquet round trips against shared golden fixtures for every
  exposed calculator or file-transform path.
- Include a CSV compatibility path only where it is explicitly intended and
  loss characteristics are documented.
- Refresh fixtures only when the contract change is intentional and scoped to a
  reviewable set of inputs and outputs.
- Keep canonical inputs minimal, deterministic, and representative of the
  supported edge cases.

## Schema validation expectations

- Validate file inputs and outputs against the published schema or schema-like
  contract before comparing results.
- Fail CI on missing required fields, incompatible types, unexpected enum
  values, or drift in versioned metadata.
- Treat provenance, calculator version, and contract version as part of the
  contract, not optional extras.

## Docs example checks

- Keep shell, notebook, and pipeline examples in sync with the CLI contract and
  file paths used in the tests.
- Prefer doctest-style or example-extraction checks where practical so docs do
  not drift from the supported commands.
- Use examples that are small enough to run in CI and stable enough to compare
  across platforms.

## Sensitive-data and privacy guardrails

- Use synthetic or anonymized fixture data only.
- Do not commit PHI, patient-level records, secrets, tokens, or private source
  data into fixtures, docs, logs, or artifacts.
- Avoid CI steps that upload raw input files unless they are already known to be
  synthetic and safe to retain.
- Keep logs terse and redact any identifiers that could be sensitive.

## Artifact retention

- Retain CLI logs, schema diffs, and fixture mismatch artifacts long enough to
  debug a failed run, but avoid indefinite storage.
- Keep retained artifacts scoped to the smallest useful set: command output,
  comparison report, and the mismatched fixture pair.
- Do not retain full raw datasets when a summarized diff or minimal failing
  sample is sufficient.

## Approval bar for workflow changes

- Only add `.github/workflows` enforcement when the same command sequence runs
  cleanly on CI runners without manual setup.
- The gate should fail loudly on schema drift, fixture mismatch, unsupported
  file formats, or docs-example breakage.
- Keep any workflow addition low-risk and narrowly scoped to this track until
  the binding is demonstrably stable.
