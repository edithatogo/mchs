# Specification: Go Binding

## Overview
Provide a Go integration path for services, command-line tools, and data-pipeline systems. The current Go surface is a concrete service adapter and binding-file adapter over the shared contract; Go should consume the shared Rust core through C ABI, service, or CLI/file contracts and must not reimplement formulas.

## Functional Requirements
- Evaluate cgo C ABI, gRPC/service, and CLI/Arrow-file interop.
- Define Go request/response structs aligned to the public contract.
- Reuse shared golden fixtures.
- Document module publication only after parity gates are stable.

## Acceptance Criteria
- Go service and binding-file adapters identify the initial supported integration strategy.
- Go examples validate against shared fixtures.
- No formula logic is implemented in Go.

## Strategy Notes

- Initial path: CLI / Arrow-file interop.
- Fallback path: gRPC / service.
- Implemented adapter surface: service execution plus binding request/response
  file loading and saving.
- Deferred path: cgo C ABI, only after ABI stability and cross-compilation
  requirements are documented and met.
- The Go surface may define request and response structs aligned to the public
  contract, but it may not duplicate any formula logic from the shared Rust
  core.
