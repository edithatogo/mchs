---
title: C#/.NET binding
slug: 2026/governance/csharp-dotnet-binding
---

The C#/.NET surface is a downstream adapter, not a calculator engine. It
exists to consume the shared public calculator contract and present the
results in a .NET-friendly shape.

## .NET strategy

* Keep the .NET layer thin and contract driven.
* Use the shared calculator contract for request and response shapes.
* Do not duplicate formula logic, validation rules, or pricing-year
  semantics inside C#.
* Treat the .NET surface as a packaging and integration concern, not a source
  of calculator authority.

## Power Platform adjacency

Power Platform sits next to the .NET surface as an orchestration channel, not
inside the calculator boundary.

* Power Platform should call a secured service boundary or custom connector.
* Any .NET component used alongside Power Platform must still respect the same
  contract boundary.
* Do not let Power Platform or .NET become a second implementation of the
  calculator rules.

## Contract boundary

The contract boundary is the stable interface between the calculator core and
downstream runtimes.

* C#/.NET consumes the public contract rather than owning it.
* Shared request and response schemas stay runtime neutral.
* Boundary failures should surface as structured contract errors, not as
  language-specific exceptions in public docs.

See the canonical contract in
[Public calculator contract](./public-calculator-contract/).

## NuGet packaging posture

NuGet publication evidence now exists for `Mchs.Bindings.DotNet 0.1.0`, but
the .NET surface remains a preview, thin-boundary adapter.

* Treat the NuGet package as registry publication evidence, not a GA support
  claim.
* Keep the documented posture focused on the contract and service boundary.
* Do not duplicate formula logic, validation rules, or pricing-year semantics
  inside .NET package code.

## Related pages

* [Downstream packaging plans](./downstream-packaging-plans/)
* [Web and Power Platform delivery](./web-and-power-platform-delivery/)
* [Polyglot Rust core roadmap](./polyglot-rust-core-roadmap/)
