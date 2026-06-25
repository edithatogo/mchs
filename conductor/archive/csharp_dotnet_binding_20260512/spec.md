# Specification: C#/.NET Binding

## Overview
Provide a C#/.NET integration path for institutional services, health-service applications, and Power Platform-adjacent workloads. The .NET surface must consume the shared Rust core through C ABI, service, or CLI/file contracts and must not duplicate formula logic.

## Functional Requirements
- Select a .NET integration path: C ABI/PInvoke, gRPC/service boundary, or CLI/Arrow-file interop.
- Define typed C# request/response models aligned with the public calculator contract.
- Reuse shared golden fixtures and provenance diagnostics.
- Document packaging as a NuGet package only after contract and parity gates are stable.

## Acceptance Criteria
- C# roadmap identifies the chosen initial integration strategy and fallback.
- C# examples validate against shared fixtures.
- No formula logic is implemented in C#.

## Strategy note

- Initial strategy: service boundary.
- Fallback: CLI / Arrow-file interop for batch, offline, or inspectable handoff
  scenarios.
- C ABI / PInvoke remains a later option for latency-sensitive or embedded
  .NET hosts once the ABI and packaging rules are stable.
- Power Platform-adjacent solutions must stay thin and route work through the
  shared contract rather than duplicating formula logic in flows, expressions,
  or app code.
