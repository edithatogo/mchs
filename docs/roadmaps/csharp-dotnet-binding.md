# C#/.NET Binding Roadmap

Roadmap snapshot: 2026-05-13.

This document compares the candidate integration strategies for the C#/.NET
binding workstream and records the initial path, fallback, and guardrails. It
does not introduce formula logic. Local .NET adapter code can exercise the
service and file boundaries, but this document does not claim a NuGet release
or a production-ready binding. Later registry evidence verifies
`Mchs.Bindings.DotNet 0.1.0` on NuGet; that publication does not change this
roadmap's preview support boundary.

## Scope

- Provide a C#/.NET integration path for institutional services,
  health-service applications, and Power Platform-adjacent workloads.
- Keep the shared Rust core as the only source of formula logic.
- Use the .NET surface for transport, packaging, diagnostics, and host
  integration only.

## Comparison

| Strategy | Strengths | Costs | Best fit |
| --- | --- | --- | --- |
| C ABI / PInvoke | Lowest call overhead for in-process consumers; good fit for desktop or service hosts that can load native libraries directly. | Requires stable native packaging, strict ABI compatibility, and careful memory-ownership rules. It is the most brittle option when the contract is still moving. | Latency-sensitive .NET hosts that need direct in-process calls after the ABI is stable. |
| Service boundary | Easiest way to keep the formula engine single-sourced; clean versioning and diagnostics; aligns well with cloud, enterprise, and Power Platform integration. | Adds process and network hops; needs service availability, auth, and operational support. | Initial .NET rollout when the contract is still stabilizing and Power Platform adjacency matters. |
| CLI / Arrow-file interop | Strong for batch, auditability, reproducibility, and offline handoff. The file contract is easy to inspect and fixture-test. | Slower than in-process calls and less ergonomic for interactive .NET consumers. | Fallback path for batch workflows, offline use, and environments that cannot depend on a live service. |

## Decision

Start with the **service boundary** as the initial C#/.NET strategy. The
current local .NET adapter evidence is a pre-release integration boundary, not
a public package or production support claim.

Use **CLI / Arrow-file interop** as the fallback when a caller needs batch
execution, offline handoff, or a more inspectable contract than a live service
can provide.

Defer **C ABI / PInvoke** until the native ABI, packaging, and compatibility
rules are stable enough to justify an in-process surface.

## Why the service boundary comes first

- It keeps the calculator formulas in one place.
- It avoids forcing native DLL distribution before the contract is stable.
- It lines up with enterprise deployment patterns where .NET apps, services,
  and Power Platform solutions already communicate through approved endpoints.
- It allows the team to reuse the same diagnostics, provenance, and fixture
  contract across consumers.

## Power Platform adjacency

- Power Platform is an orchestration surface, not a place to host calculator
  formulas.
- A service boundary is the natural adjacency point because managed solutions,
  connectors, and flows can call a versioned endpoint without embedding the
  business logic.
- If a Power Platform scenario needs batch or governed file exchange, the same
  contract can fall back to the CLI / Arrow-file path.
- Any Power Platform-facing component must remain thin and route work to the
  shared contract rather than duplicate calculator rules in expressions,
  flows, or app code.

## No formula-logic duplication

- The Rust core remains the single source of formula logic.
- C# models may mirror request and response shapes, but they may not
  reimplement calculator rules, adjustment logic, or fallback heuristics.
- The service layer may validate, route, authenticate, and translate payloads,
  but it may not become a second calculator.
- File interchange may serialize canonical inputs and outputs, but it may not
  introduce a parallel calculation path.

## Sequencing guidance

1. Stabilize the service contract and shared diagnostics first.
2. Wire .NET clients to the service boundary and keep them thin.
3. Use CLI / Arrow-file interop for batch or offline scenarios that need a
   safer handoff than in-process code.
4. Promote C ABI / PInvoke only after the ABI and packaging rules are stable
   and there is a clear latency or embedding need.

## Validation rule

- Every .NET example must validate against shared golden fixtures.
- A .NET binding that duplicates formula constants, thresholds, or adjustment
  rules is out of scope.
- NuGet publication evidence may be cited for package availability, but support
  claims still wait until the chosen boundary is stable and parity evidence
  exists for the shared contract.
