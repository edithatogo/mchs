# Language Registry Submissions Contract

This contract tracks language/package registry publication work independently from implementation readiness. A binding contract or scaffold does not imply registry publication. Each registry must pass four gates before it can be marked complete:

1. Discover whether publication already exists.
2. Prepare publishable package metadata and artifacts.
3. Submit using the registry-specific workflow and authenticated account.
4. Capture immutable evidence such as URL, version, checksum, PR, review status, or registry API response.

Current claim boundary as of 2026-06-12:

- Tracks created: yes.
- Discovery completed: yes, using public registry/API/page evidence where available.
- Local preparation completed: yes, with explicit runtime/tooling limitations recorded per registry.
- Submissions completed: crates.io and NuGet direct uploads are accepted and publicly verified; conda-forge, Swift Package Index, vcpkg, ConanCenter, and other review-gated submissions have recorded PR/issue evidence where available.
- Publications verified: PyPI `nwau-py`, crates.io `nwau-core`, NuGet `Mchs.Bindings.DotNet`, npm `@edithatogo/mchs-wasm-binding`, Homebrew personal tap, Julia General `NationalWeightedActivityUnitWrapper`, Stata SSC `mchs`, Go module proxy/pkg.go.dev, and the official MCP/Smithery MCP registry submissions tracked outside this language-registry contract.
- Credential and automation setup updated: `.github/workflows/publish-registry-packages.yml` provides manual `workflow_dispatch` paths for crates.io and NuGet. NuGet publication is verified; crates.io publication is verified and the crates.io token/GitHub secret cleanup is complete. The only remaining GitHub repo secret observed for registry publishing is `NUGET_API_KEY`.

MATLAB and Stata interop bundles now also have stable GitHub release assets at `https://github.com/edithatogo/mchs/releases/tag/language-interop-v0.1.0`. Stata SSC publication is verified from the public SSC/RePEc archive; the MATLAB bundle remains available for MathWorks File Exchange upload/linking.

Remaining blockers are publisher agreement/PAT setup for Open VSX, Central Portal namespace/signing for Maven Central, conda-forge maintainer review/merge and Anaconda propagation, ConanCenter job scheduling/maintainer review, vcpkg Rust-library support policy, Swift Package Index public listing probe visibility, CRAN submission/review, MATLAB File Exchange upload/review, or unavailable local proprietary runtimes for MATLAB runtime validation.
