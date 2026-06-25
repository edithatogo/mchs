# Swift bindings adapter

This directory contains a synthetic, non-published Swift package used as a
transport binding surface for Apple-platform and native client consumers.

Scope:

- Typed request/response structs mirroring the public calculator contract
- File-boundary validation for inspectable Parquet/CSV exchange
- CLI invocation through `Foundation.Process` on macOS

Out of scope:

- Formula parsing
- Formula evaluation
- Calculator logic of any kind
- Published Swift Package Manager module
- C ABI integration (documented as future path)
- Repo-wide build or release wiring
- Swift Package Index publication

## Layout

- `Sources/MCHSBind/`: request/response types, file-boundary validation, and CLI adapter
- `Sources/MCHSBindSmoke/`: local smoke executable for build and adapter validation

## Integration Strategy

| Mode          | Consumer              | Transport       | Priority |
|---------------|-----------------------|-----------------|----------|
| File exchange | Swift `ParquetReader` | Parquet / CSV   | Primary  |
| CLI process   | Swift `Process`       | CLI stdout/json | Primary  |
| Service API   | Swift `URLSession`    | HTTP / REST     | Fallback |
| C ABI         | Swift `CFunction`     | C library .dylib| Future   |

## Usage

```swift
import MCHSBind

let request = SwiftBindingRequest(
    calculatorId: "acute",
    pricingYear: "2025",
    inputSchemaVersion: "1.0",
    outputSchemaVersion: "1.0",
    mode: "cli",
    inputPath: "./input.csv",
    outputPath: "./output.csv",
    metadata: ["params_path": "./tests/data/2025"],
    fixtureGate: "synthetic_only_examples"
)

let adapter = CLIProcessBindingAdapter(executablePath: "/usr/bin/python3")
let response = try await adapter.execute(request: request)
print(response.status)
```

The default CLI adapter builds this shared command shape:

```text
python -m nwau_py.cli.main <calculator> <input.csv> --output <output.csv> --year <year>
```

The package validates file boundaries and invokes the shared CLI. It does not
compute formula results or mutate formula expressions.
