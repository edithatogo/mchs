# Swift Binding Track Review

## Findings

1. Resolved - The track records file-exchange and CLI invocation as the initial
   path, service as fallback, and C ABI as a deferred future path until a Rust
   cdylib and Swift module map are available.
2. Resolved - The track includes a live contract schema, synthetic examples,
   a Swift transport adapter, and tests that validate metadata, diagnostics,
   provenance, file-boundary checks, CLI invocation, and no formula duplication.
3. Resolved - Swift Package Manager publication is explicitly gated and remains
   future-only; the package is a local transport adapter and not a publication
   claim.

## Changed files

- `microcosting_healthservices/conductor/archive/swift_binding_20260513/review.md`
- `microcosting_healthservices/bindings/swift/Package.swift`
- `microcosting_healthservices/bindings/swift/Sources/MCHSBind/adapter.swift`
- `microcosting_healthservices/bindings/swift/Sources/MCHSBindSmoke/main.swift`
- `microcosting_healthservices/bindings/swift/README.md`
- `microcosting_healthservices/contracts/swift-binding/swift-binding.contract.json`
- `microcosting_healthservices/contracts/swift-binding/swift-binding.schema.json`
- `microcosting_healthservices/tests/fixtures/swift_binding/contract_bundle.json`
- `microcosting_healthservices/tests/test_swift_binding_track.py`

## Validation

- `swift build`
- `swift run MCHSBindSmoke`
- `python -m pytest tests/test_swift_binding_track.py`

## Risks

- The Swift package is synthetic and transport-only; default CLI invocation
  targets the shared Python CLI command shape, while smoke validation uses a
  local process fixture rather than running calculator data.
- C ABI cross-compilation posture remains a documented gate until a Rust cdylib
  is built for arm64 and x86_64 Apple targets.
- iOS and visionOS sandboxing restricts CLI `Process` invocation; on those
  platforms, file exchange or service API is preferred.
- Swift Package Manager publication remains held at the parity and platform
  evidence gate.
