# Language Registry External Gates

Language registry work is locally prepared where possible. Publication is intentionally not claimed without external registry evidence.

| Registry | Package | Local state | External gate |
| --- | --- | --- | --- |
| crates.io | `nwau-core` | published and verified at `https://crates.io/crates/nwau-core/0.1.0`; checksum `c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547` | complete; browser-created crates token revoked and stale GitHub secret deleted |
| NuGet | `Mchs.Bindings.DotNet` | NuGet flat-container exposes `0.1.0` after workflow push in run `26404217645` | complete |
| CRAN | `nwauR` | `R CMD build` and `R CMD check` passed | CRAN maintainer submission and review |
| Julia General | `NationalWeightedActivityUnitWrapper` | reviewer-requested replacement PR #156254 is open; registry consistency and treecheck pass; superseded PRs marked with `[noblock]` comments because close permission was denied | AutoMerge stopwatch, General PR #156254 merge, and public registry propagation |
| Go proxy/pkg.go.dev | Go binding module | Go module proxy and pkg.go.dev expose `v0.1.0` | complete |
| Swift Package Index | `MCHSBind` | `swift build` passed; PackageList issue closed; repo metadata/release fixed | public SPI listing/version evidence still pending |
| Maven Central | `io.github.edithatogo:mchs` | JVM module builds locally; Maven publishing metadata and Central Portal repository wiring present; exact local checks are `gradle -p bindings/jvm tasks --all` and `gradle -p bindings/jvm publishAllPublicationsToCentralPortalRepository --dry-run` | namespace verification, signing credentials, publish credentials, Central Portal release |
| conda-forge | `nwau-py` | branch updated on PR `https://github.com/conda-forge/staged-recipes/pull/33452`; latest head `e6c8b9d632953263517de6a146783f3697fc450d` has linter, check-skip, aggregate staged-recipes, linux, osx, and win checks passing | maintainer review, merge, and feedstock publication |
| Homebrew | `nwau-py` | personal tap published; audit, source install, and `brew test` pass with Click resource plus lazy CLI patch | optional Homebrew/core PR/review |
| Open VSX / Visual Studio Marketplace | `mchs-tools` | extension source scaffold committed; manifest is publisher-ready; generated `.vsix` intentionally not committed | Eclipse Open VSX Publisher Agreement, Visual Studio Marketplace publisher/PAT access, package, then publish |
| MATLAB File Exchange | `mchs-matlab-interop` | upload bundle exists | MathWorks account upload and review |
| SSC / Stata package distribution | `mchs-stata-interop` | ado/help/pkg bundle exists | SSC maintainer submission and review |
| vcpkg / ConanCenter | `nwau-c-abi` | dedicated source archive exists; Conan static/shared builds and native `test_package` pass; vcpkg overlay install passes locally with CMake config target and linkage-aware artifacts; upstream vcpkg and ConanCenter PRs are open | ConanCenter CLA plus maintainer job approval/review after job request comment; vcpkg Rust/Cargo toolchain policy plus Microsoft CLA before publication can be claimed |

Run `python scripts/language_registry_external_gate_report.py` from `microcosting_healthservices/` for the current gate list.

Use `python scripts/language_registry_external_gate_report.py --live` to query recorded submission URLs, such as the conda-forge staged-recipes PR, and deterministic public package probes without claiming publication.

Use `python scripts/language_registry_external_gate_report.py --promotion` to group tracks into completion candidates, publication follow-up items, partial publications, submitted-review items, and external blocks from the checked-in contract without network access.

Use `python scripts/language_registry_external_gate_report.py --promotion --live` to refresh those groups with live submission and public-registry probes. Live completion candidates require target-version evidence from the public registry response; a package-level `200` without the expected version remains `public_listing_version_unverified`.

Add `--output <path>` to any mode to persist the report as a release or CI artifact.

The PR CI workflow writes non-live JSON artifacts only, so pull requests remain deterministic. The scheduled/manual `.github/workflows/language-registry-live.yml` monitor runs the live report commands and uploads `language-registry-live` artifacts for registry drift review.

The Go row is intentionally split: the Go proxy submission URL verifies the tagged module, while the public package probe checks `https://pkg.go.dev/github.com/edithatogo/mchs/bindings/go`. Once pkg.go.dev exposes the target version, the Go track can be completed.

The Maven Central row is intentionally fail-closed: a real publish attempt must
provide `-PcentralPortalUsername` and `-PcentralPortalPassword`, and missing
credentials stop the publish path instead of falling back to anonymous access.
