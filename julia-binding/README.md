# NationalWeightedActivityUnitWrapper

`NationalWeightedActivityUnitWrapper` is a minimal Julia wrapper around the
authoritative Python `nwau_py` CLI. It does not reimplement any funding
formulas in Julia. Instead, it moves CSV files across a stable process boundary
and lets the existing Python calculator perform the work.

This keeps the Julia surface conservative and low risk while preserving a
single source of truth for calculator logic.

## What this package provides

- `CliFileAdapter` for local CLI/file execution against the shared core
- `ServiceAdapter` for opaque JSON service handoff experiments
- `calculate(...)` for generic CLI/file execution
- `calculate_acute(...)`, `calculate_ed(...)`, and `calculate_non_admitted(...)`
  convenience helpers
- `interop_contract(...)` to persist the shared CLI/file contract emitted by the
  Python CLI
- `execute_service_request(...)` to POST a JSON request file and write the raw
  JSON response without interpreting calculator payloads

## Contract

The wrapper shells out to:

```text
python -m nwau_py.cli.main <subcommand> <input_csv> --output <output_csv>
```

Optional arguments are forwarded when supplied:

- `--year`
- `--params`

The Julia code only coordinates file paths and process execution. Validation,
classification checks, and all formula logic remain in Python.

The CLI/file adapter captures stdout, stderr, exit code, input path, output
path, and the exact command vector in a `CalculationResult`. Non-zero exits
raise by default so callers do not accidentally treat a failed shared-core run
as a completed calculation; pass `check = false` when a caller needs to inspect
failure diagnostics directly.

## Requirements

- Julia 1.10 or newer
- Python 3 with the `nwau_py` package available on the selected interpreter
- The archived calculator data under `archive/sas/<YEAR>/`

The wrapper defaults to `python3` and `nwau_py.cli.main`, but both can be
overridden through environment variables:

```julia
ENV["NWAU_PYTHON"] = "/path/to/python"
ENV["NWAU_MODULE"] = "nwau_py.cli.main"
```

## Example

```julia
using NationalWeightedActivityUnitWrapper

output_csv = calculate_acute(
    "tests/fixtures/golden/acute_2025/input.csv";
    year = 2025,
    params_dir = "archive/sas/2025",
)

println(output_csv.output_csv)
```

The returned value is a `CalculationResult`; `result.output_csv` is the path to
the Python-produced output CSV. If you want the data as a Julia table, load it
separately with your preferred CSV package.

To write the shared CLI/file contract for audit or packaging checks:

```julia
interop_contract(output_json = "build/cli-file-interop.contract.json")
```

For service-backed experiments, Julia keeps the request and response opaque:

```julia
adapter = ServiceAdapter("https://example.invalid/mchs/bindings")
result = execute_service_request(
    adapter;
    request_json = "request.json",
    response_json = "response.json",
)
```

Arrow is the target interchange format for larger cross-language batches after
the shared CLI/file contract supports it. The current executable prototype is
CSV-only because that is the active shared CLI contract.

## Boundary

This package is intentionally wrapper-only.

- Formula logic stays in Python
- Input validation stays in Python
- Julia only handles file handoff and process invocation
- Service requests remain opaque JSON transport envelopes in Julia

## Rename note

The local Julia payload previously used the short package/module name
`NWAUJulia`. That name is retained only in historical track evidence. The active
package and module name is `NationalWeightedActivityUnitWrapper`.
