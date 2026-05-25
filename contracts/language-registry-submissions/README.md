# Language Registry Submissions Contract

This contract tracks language/package registry publication work independently from implementation readiness. A binding contract or scaffold does not imply registry publication. Each registry must pass four gates before it can be marked complete:

1. Discover whether publication already exists.
2. Prepare publishable package metadata and artifacts.
3. Submit using the registry-specific workflow and authenticated account.
4. Capture immutable evidence such as URL, version, checksum, PR, review status, or registry API response.

Current claim boundary as of 2026-05-25:

- Tracks created: yes.
- Discovery completed: yes, using public registry/API/page evidence where available.
- Local preparation completed: yes, with explicit runtime/tooling limitations recorded per registry.
- Submissions completed: NuGet upload was accepted by the registry API and public NuGet flat-container verification now exposes `Mchs.Bindings.DotNet@0.1.0`.
- Publications verified: no, except PyPI `nwau-py`, crates.io `nwau-core`, NuGet `Mchs.Bindings.DotNet`, npm `@edithatogo/mchs-wasm-binding`, Homebrew personal tap, Go module proxy/pkg.go.dev, and the official MCP/Smithery MCP registry submissions tracked outside this language-registry contract.
- Credential and automation setup updated: GitHub repository secrets `CARGO_REGISTRY_TOKEN` and `NUGET_API_KEY` exist, and `.github/workflows/publish-registry-packages.yml` provides manual `workflow_dispatch` paths for crates.io and NuGet. Publication is still not claimed until those paths are dispatched and public registry evidence is captured.

Remaining blockers are token rotation/manual dispatch for crates.io, publisher agreement/account setup for Open VSX and Visual Studio Marketplace, Central Portal namespace/signing for Maven Central, upstream maintainer review workflows, public semantic tags/indexing, or unavailable local proprietary runtimes such as MATLAB/Stata.
