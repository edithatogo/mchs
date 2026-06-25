# Binding Strategy: Swift Binding

## Decision

Use a staged integration strategy for Swift consumers, initially targeting
file/Arrow exchange and CLI invocation, with C ABI as a future native
integration path. The package now provides a concrete transport adapter:
Swift consumers validate local CSV/Parquet file boundaries and can invoke the
shared core CLI through `Foundation.Process` on macOS. No Swift formula port is
created.

This follows the polyglot Rust core roadmap and reuses the C ABI and CLI/file
interop contracts established by the shared core.

## Rationale

- Native Swift FFI via C ABI (Rust `#[no_mangle]` extern "C" functions) is
  viable but requires a C bridge header and module map for Swift Package
  Manager integration.
- File/Arrow exchange has no language dependency and works immediately from
  Swift Foundation's `Parquet`, `CSV`, or `JSONDecoder`.
- CLI invocation via `Process` gives a zero-build-consumer path for Swift
  scripts and CLI tools on macOS.
- Apple-platform constraints (sandboxing, app store review, privacy
  manifests) are easier to satisfy with file-based or service boundaries than
  with embedded C ABI libraries.
- Swift Package Manager build tooling is committed for the transport adapter,
  but publication remains gated by audience, owner, and platform evidence.

## Contract shape

### Integration modes

| Mode          | Consumer              | Transport       | Notes                               |
|---------------|-----------------------|-----------------|-------------------------------------|
| File exchange | Swift `ParquetReader` | Parquet / CSV   | Primary mode; no framework deps     |
| CLI process   | Swift `Process`       | CLI stdout/json | Zero-build; invokes shared-core CLI |
| C ABI         | Swift `CFunction`     | C library .dylib| Future path; requires module map    |
| Service API   | Swift `URLSession`    | HTTP / REST     | Network boundary; async integration |

### Parquet/CSV schema contract

Swift reads the same Parquet and CSV schemas produced by the CLI/file interop
track:

- `contract_version` — pinned calculator contract version
- `calculator_id` — public calculator identifier
- `pricing_year` — target IHACPA pricing year
- `input_schema` — structured input columns matching the calculator contract
- `output_schema` — computed output columns with diagnostic flags
- `provenance` — shared-core version, source archive hash, generation timestamp
- `fixture_gate` — declared synthetic-only or local-only gate

### CLI invocation pattern

```swift
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
```

## Supported calculators

All calculators exposed through the CLI/file interop track are accessible from
Swift. No Swift-specific calculator packaging is required.

## Limitations

- Swift does not execute calculator logic. All computation happens in the
  shared core.
- C ABI integration requires a Rust `cdylib` build and a Swift module map.
  This path remains a future native support gate, not a current Swift support
  claim.
- iOS and visionOS sandboxing restricts CLI `Process` invocation. On those
  platforms, file exchange or service API is preferred.
- No Swift-specific formula UDFs, property wrappers, or result builders are
  maintained in this repository.

## Versioning

- Swift integration pins to the CLI/file interop contract version for
  Parquet/CSV schemas.
- C ABI integration would pin to the C ABI contract version.
- No separate Swift interop version is needed.

## Diagnostics and provenance

- File outputs include full provenance metadata consumed by Swift decoder
  types.
- CLI invocation captures diagnostic output (stderr) and exit codes for error
  handling.
- Provenance metadata supports traceability from Swift clients back to shared
  core execution.

## Privacy and synthetic examples

- All committed Swift example manifests and test files are synthetic.
- Real IHACPA pricing data or patient-level extracts are never committed as
  Swift examples.
- The `fixture_gate` field distinguishes synthetic examples from local-only
  real data.

## When to use Swift vs. other bindings

Use Swift when:
- the consumer is an Apple-platform app (macOS, iOS, iPadOS, visionOS)
- the workflow requires native Swift concurrency (`async/await`) or
  SwiftUI presentation
- the team standardises on Swift for institutional tooling

Prefer CLI/file interop or service API when:
- the consumer is not Apple-platform-native
- the integration needs zero client-side dependencies
- the deployment target does not support Swift runtime

## Readiness bar

- This track is transport-adapter ready for file-boundary validation and
  macOS CLI invocation.
- Integration workflows are documented and validated with a Swift smoke
  executable and shared track tests.
- Do not claim Swift Package Index or app-platform readiness until a named
  audience, accountable owner, and Apple-platform CI evidence are recorded.
