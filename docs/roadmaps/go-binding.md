# Go Binding Roadmap

Roadmap snapshot: 2026-05-13.

This document compares the candidate integration strategies for the Go binding
workstream and records the initial path, fallback, and guardrails. Local
service and binding-file adapters now exist as evidence for the path, but this
document does not claim a public Go module release or a production-ready
binding.

## Scope

- Provide a Go integration path for services, command-line tools, and
  data-pipeline systems.
- Keep the shared Rust core as the only source of formula logic.
- Use the Go surface for transport, packaging, diagnostics, and host
  integration only.

## Comparison

| Strategy | Strengths | Costs | Best fit |
| --- | --- | --- | --- |
| C ABI / cgo | Lowest call overhead for in-process consumers; useful when Go must embed the core directly. | Highest maintenance burden: native toolchains, memory ownership rules, ABI stability, and cross-compilation friction. It is the most brittle choice while the contract is still moving. | Deferred option for latency-sensitive embedding only after the ABI and packaging rules are stable. |
| gRPC / service | Clear versioning, easier operational isolation, and a single place to host diagnostics and fixtures. It keeps the formula engine centralized and avoids native linking. | Adds process and network hops, service availability requirements, and an operational surface to run and secure. | Secondary path for callers that need online interaction or a stable long-running endpoint. |
| CLI / Arrow-file interop | Lowest maintenance for the initial Go rollout: no native linking, no daemon dependency, straightforward cross-compilation, and a file contract that is easy to inspect and fixture-test. | Slower than in-process calls and less ergonomic for interactive request/response flows. | Initial path for batch workflows, reproducible validation, and environments that prefer portable artifacts. |

## Decision

Start with **CLI / Arrow-file interop** as the initial Go strategy. The current
local Go adapter evidence covers service and binding-file boundaries over the
shared contract; public module release remains gated on registry and parity
evidence.

Use **gRPC / service** as the fallback when a caller needs online request/
response behavior, multi-step orchestration, or a persistent endpoint.

Defer **C ABI / cgo** until the ABI, memory-ownership model, and packaging
rules are stable enough to justify native embedding.

## Why CLI / Arrow-file interop comes first

- It keeps the calculator formulas in one place.
- It avoids native toolchain requirements in the first Go delivery.
- It supports batch and offline usage without introducing a service runtime.
- It is the most predictable path for shared golden-fixture validation.
- It keeps the initial maintenance burden low while the contract is still
  evolving.

## Cross-compilation constraints

- The default Go delivery should remain buildable with pure Go tooling.
- `CGO_ENABLED=0` should be the normal baseline for the initial rollout.
- Any cgo-backed experiment must document the required C compiler, sysroot,
  and target `GOOS`/`GOARCH` pairing explicitly.
- Cross-compiling cgo artifacts must not be assumed to work without a target
  C toolchain and matching native dependencies.
- Static linking should not be treated as the default packaging assumption for
  any native path.
- CLI and Arrow-file workflows should remain usable across supported platforms
  without requiring native bindings.

## No formula-logic duplication

- The Rust core remains the single source of formula logic.
- Go structs may mirror request and response shapes, but they may not
  reimplement calculator rules, adjustment logic, or fallback heuristics.
- The service layer may validate, route, authenticate, and translate payloads,
  but it may not become a second calculator.
- File interchange may serialize canonical inputs and outputs, but it may not
  introduce a parallel calculation path.

## Sequencing guidance

1. Stabilize the CLI / Arrow-file contract and fixture-backed examples first.
2. Add gRPC / service support for callers that need an always-on endpoint.
3. Promote cgo only after ABI stability, memory ownership, and build
   portability are proven.

## Validation rule

- Every Go example must validate against shared golden fixtures.
- A Go binding that duplicates formula constants, thresholds, or adjustment
  rules is out of scope.
- Release claims for Go packaging should wait until registry gates are clear,
  the chosen contract is stable, and parity evidence exists for the shared
  fixtures.
