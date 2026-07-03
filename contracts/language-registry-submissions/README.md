# Language Registry Submissions Contract

This contract tracks language/package registry publication work independently from implementation readiness. A binding contract or scaffold does not imply registry publication. Each registry must pass four gates before it can be marked complete:

1. Discover whether publication already exists.
2. Prepare publishable package metadata and artifacts.
3. Submit using the registry-specific workflow and authenticated account.
4. Capture immutable evidence such as URL, version, checksum, PR, review status, or registry API response.

Current claim boundary as of 2026-07-03:

- Tracks created: yes.
- Discovery completed: yes, using public registry/API/page evidence where available.
- Local preparation completed: yes, with explicit runtime/tooling limitations recorded per registry.
- Submissions completed: CRAN upload was confirmed by the user-clicked CRAN confirmation link, conda-forge staged-recipes PR `33452` is open with checks passing, SSC submission/maintainer-identity email has been sent and Boston College SSC/RePEc public files now expose the `mchs` package, Maven Central Publisher API deployment `5fb01ae9-2609-4284-9427-5830e08bcbb5` has published, and MATLAB File Exchange exposes `MCHS MATLAB Interop@0.1.0`. Swift Package Index, Visual Studio Marketplace/Open VSX, and vcpkg/ConanCenter are deprecated and cancelled; their existing evidence is historical only.
- Publications verified: PyPI `nwau-py`, crates.io `nwau-core`, NuGet `Mchs.Bindings.DotNet`, npm `@edithatogo/mchs-wasm-binding`, Homebrew personal tap, Go module proxy/pkg.go.dev, Maven Central `io.github.edithatogo:mchs-jvm-bindings@0.1.0`, MATLAB File Exchange `MCHS MATLAB Interop@0.1.0`, Stata SSC `mchs`, and the official MCP registry submission tracked outside this language-registry contract. Historical evidence is retained for cancelled Swift Package Index `MCHSBind@0.1.0`, Open VSX `edithatogo.mchs-tools@0.1.1`, and Visual Studio Marketplace `edithatogo.mchs-tools@0.1.1`.
- Credential and automation setup updated: GitHub repository secret `NUGET_API_KEY` exists, `.github/workflows/publish-registry-packages.yml` provides manual `workflow_dispatch` paths for crates.io and NuGet, and the browser-created crates.io publish token was revoked after verification with `CARGO_REGISTRY_TOKEN` deleted from GitHub Actions secrets.

Remaining active blockers are CRAN pretest/reviewer response plus public package publication and conda-forge staged-recipes review/merge. Swift Package Index, VS Code/Open VSX, and C/C++ vcpkg/Conan are deprecated and cancelled, not active blockers.
