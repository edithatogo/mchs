# Language Registry External Gates

Language registry work is locally prepared where possible. Publication is intentionally not claimed without external registry evidence.

| Registry | Package | Local state | External gate |
| --- | --- | --- | --- |
| crates.io | `nwau-core` | published and verified at `https://crates.io/crates/nwau-core/0.1.0`; checksum `c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547` | complete; browser-created crates token revoked and stale GitHub secret deleted |
| NuGet | `Mchs.Bindings.DotNet` | NuGet flat-container exposes `0.1.0` after workflow push in run `26404217645` | complete |
| CRAN | `nwauR` | 2026-06-12T13:40:27Z temp-directory `R CMD build` and `R CMD check --as-cran` completed with `Status: 1 NOTE`; `.Rbuildignore` excludes `cran-comments.md`; current Homebrew `tidy-html5` lets HTML manual validation pass; generated tarball SHA-256 `13e4f96f1e75908cd6b255d9eb4daa610afd546d19b4d65f750eeedff26d09ad`; public CRAN probes still returned 404 | Replace placeholder maintainer email, then CRAN maintainer submission/review |
| Julia General | `NationalWeightedActivityUnitWrapper` | General PR #156254 merged on 2026-05-28; raw General registry files verify `v0.1.0`, UUID `58dad789-f56a-4ab3-a66f-c15139bf9cbe`, and git-tree-sha1 `bb22d4bd44689549064bd441092fd540b5d852cf` | complete; JuliaHub may lag but raw General registry evidence is authoritative |
| Go proxy/pkg.go.dev | Go binding module | Go module proxy and pkg.go.dev expose `v0.1.0` | complete |
| Swift Package Index | `MCHSBind` | `swift build` passed; PackageList issue closed; repo metadata/release fixed; 2026-06-12T12:22:49Z raw PackageList probe now contains `https://github.com/edithatogo/mchs-swift.git`; SPI page probes still return Cloudflare HTTP 403 and API probe returned HTTP 000 from this environment | public SPI listing/version evidence still pending |
| Maven Central | `io.github.edithatogo:mchs` | JVM module builds locally; Maven publishing metadata and Central Portal repository wiring present; GitHub Actions dry-run `https://github.com/edithatogo/mchs/actions/runs/27407884659` passes after setting workflow JDK 17 for Gradle 9; 2026-06-12T12:12:06Z audit found no local CENTRAL/MAVEN/GPG/SIGNING credential env vars and only `NUGET_API_KEY` configured in GitHub secrets | namespace verification, signing credentials, required Maven Central GitHub secrets, Central Portal release |
| conda-forge | `nwau-py` | 2026-06-12T11:56:04Z live check: 2026-06-12T12:38:52Z live check: PR `https://github.com/conda-forge/staged-recipes/pull/33452` is open and mergeable at head `bffc5bf1a85389dc695adfd96c87bf2413f4db25`; conda-forge-linter, GitHub linter, Azure staged-recipes, linux_64, osx_64, win_64, build status, fast-finish, and check-skip checks are green | maintainer review, merge, feedstock publication, and public Anaconda propagation |
| Homebrew | `nwau-py` | personal tap published and verified; `brew info edithatogo/mchs/nwau-py --json=v2` verified stable `0.2.2`, tap head `fa12ed26c1d6a289b40bf59c9bacbb9a5e42f823`, and linked keg `0.2.2` | complete for personal tap; optional Homebrew/core PR/review only if core distribution is required |
| Open VSX / Visual Studio Marketplace | `mchs-tools` | Visual Studio Marketplace publisher page shows `MCHS Tools` version `0.1.0` as Public under publisher `edithatogo`; public Marketplace extension query for `edithatogo.mchs-tools` returns publisher `edithatogo`, extension `mchs-tools`, display name `MCHS Tools`, and version `0.1.0`; Open VSX Access Tokens became available after the Eclipse publisher agreement was accepted; namespace `edithatogo` was created; publish workflow `https://github.com/edithatogo/mchs/actions/runs/27455601114` published `edithatogo.mchs-tools v0.1.0`; Open VSX extension page `https://open-vsx.org/extension/edithatogo/mchs-tools` returned HTTP 200 immediately after publish, while the API endpoint still returned 404 during propagation | complete for `0.1.0`; monitor Open VSX API propagation only |
| MATLAB File Exchange | `mchs-matlab-interop` | upload bundle exists with SHA-256 `7e4b0e628fa72b7f21f133e89d321d64291a8e4c087e34c207c7040610765f3c`; 2026-06-12T12:18:08Z public File Exchange search returned HTTP 200 but no exact listing match; neither `matlab` nor `octave` is available on PATH | MathWorks account upload and review |
| SSC / Stata package distribution | `mchs` (`mchs-stata-interop` bundle) | public SSC/RePEc archive files `mchs.pkg`, `mchs.ado`, and `mchs.sthlp` returned HTTP 200 on 2026-06-12; `mchs.pkg` records Distribution-Date `20260526` | complete; Stata runtime validation remains unclaimed because Stata is unavailable locally |
| vcpkg / ConanCenter | `nwau-c-abi` | dedicated source archive exists; Conan static/shared local MCHS mirror builds pass; 2026-06-12T12:38:52Z live check shows ConanCenter PR #30262 is open and mergeable at head `c635b0f9d2f1619d9149e4fa964185658c063f5d` with CLA signed and Job scheduler `ACTION_REQUIRED`; vcpkg overlay install passes locally but upstream vcpkg PR #51965 is closed by Rust-library support policy | ConanCenter job scheduler/maintainer review; vcpkg Rust-library support policy before publication can be claimed |

Run `python scripts/language_registry_external_gate_report.py` from `microcosting_healthservices/` for the current gate list.

Use `python scripts/language_registry_external_gate_report.py --live` to query recorded submission URLs, such as the conda-forge staged-recipes PR, and deterministic public package probes without claiming publication.

Use `python scripts/language_registry_external_gate_report.py --promotion` to group tracks into completion candidates, publication follow-up items, partial publications, submitted-review items, and external blocks from the checked-in contract without network access.

Use `python scripts/language_registry_external_gate_report.py --promotion --live` to refresh those groups with live submission and public-registry probes. Live completion candidates require target-version evidence from the public registry response; a package-level `200` without the expected version remains `public_listing_version_unverified`.

Add `--output <path>` to any mode to persist the report as a release or CI artifact.

The PR CI workflow writes non-live JSON artifacts only, so pull requests remain
deterministic. The scheduled/manual
`.github/workflows/language-registry-live.yml` monitor runs
`python scripts/language_registry_external_gate_report.py --promotion --live`
and uploads `language-registry-live` artifacts for registry drift review.

The Go row is intentionally split: the Go proxy submission URL verifies the tagged module, while the public package probe checks `https://pkg.go.dev/github.com/edithatogo/mchs/bindings/go`. Once pkg.go.dev exposes the target version, the Go track can be completed.

The Maven Central row is intentionally fail-closed: a real publish attempt must
provide `-PcentralPortalUsername` and `-PcentralPortalPassword`, and missing
credentials stop the publish path instead of falling back to anonymous access.

## Operator unblocker checklist

The account, maintainer-review, and live-environment inputs needed to move the
remaining blocked registries are listed in
`docs/roadmaps/registry-unblocker-inputs-20260612.md`.

## Latest live monitor artifact

The first passive monitor run after adding `.github/workflows/language-registry-live.yml`
completed successfully at `https://github.com/edithatogo/mchs/actions/runs/27420156173`
and uploaded the `language-registry-live` artifact. See
`docs/roadmaps/language-registry-live-monitor-20260612.md`.
