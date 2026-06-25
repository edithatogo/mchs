# .NET, C#, and Power Platform Readiness

## Current State

The repository has architecture documentation for C# and Power Platform, but
no executable implementation surface yet. Power Platform remains an
orchestration layer in the docs; calculation logic must live behind a secure
C# service boundary.

## .NET Minimum Bar

- SDK-style solution/project layout with executable `.sln` and/or `.csproj`
  artifacts.
- `global.json` or equivalent SDK pinning.
- Deterministic builds.
- A clear packaging or deployment strategy:
  - `dotnet pack` and NuGet artifacts for reusable libraries, or
  - `dotnet publish` artifacts for deployable services.
- Source Link and symbol packages where the artifact is distributable.
- Contract-parity tests against the shared fixtures before any readiness claim.

## Power Platform Minimum Bar

- Solution-based ALM with source-controlled solution files.
- Managed solutions for non-dev environments.
- A secure service boundary for calculation logic.
- Power Platform must remain orchestration-only; any connector or function
  boundary should call the C# service rather than implement calculator logic.

## Gate

Do not claim C# or Power Platform calculation parity until executable .NET
artifacts exist, they pass shared-fixture tests, and the service boundary is
validated as the calculator implementation surface.
