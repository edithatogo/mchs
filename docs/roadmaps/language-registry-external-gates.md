# Language Registry External Gates

Language registry work is locally prepared where possible. Publication is intentionally not claimed without external registry evidence.

| Registry | Package | Local state | External gate |
| --- | --- | --- | --- |
| crates.io | `nwau-core` | published and verified at `https://crates.io/crates/nwau-core/0.1.0`; checksum `c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547` | complete; browser-created crates token revoked and stale GitHub secret deleted |
| NuGet | `Mchs.Bindings.DotNet` | NuGet flat-container exposes `0.1.0` after workflow push in run `26404217645` | complete |
| CRAN | `nwauR` | 2026-06-13 temp-directory `R CMD build` and `R CMD check --as-cran` completed with `Status: 1 NOTE`; `.Rbuildignore` excludes `cran-comments.md`; CRAN upload submitted as package id 344701 and maintainer confirmation email sent to `Dylan Mordaunt <dylan.mordaunt@vuw.ac.nz>`; 2026-07-03 public probes still return 404 for CRANDB, the CRAN package page, and the CRAN archive, so public CRAN publication is still unclaimed | CRAN maintainer email confirmation, review, acceptance, and public publication |
| Julia General | `NationalWeightedActivityUnitWrapper` | General PR #156254 merged on 2026-05-28; raw General registry files verify `v0.1.0`, UUID `58dad789-f56a-4ab3-a66f-c15139bf9cbe`, and git-tree-sha1 `bb22d4bd44689549064bd441092fd540b5d852cf` | complete; JuliaHub may lag but raw General registry evidence is authoritative |
| Go proxy/pkg.go.dev | Go binding module | Go module proxy and pkg.go.dev expose `v0.1.0` | complete |
| Swift Package Index | `MCHSBind` | `swift build` passed; PackageList issue closed; repo metadata/release fixed; 2026-06-12T12:22:49Z raw PackageList probe now contains `https://github.com/edithatogo/mchs-swift.git`; SPI page probes still return Cloudflare HTTP 403 and API probe returned HTTP 000 from this environment | historical / maintenance-only; public SPI listing/version evidence remains unclaimed |
| Maven Central | `io.github.edithatogo:mchs-jvm-bindings` | JVM module builds locally; Maven publishing metadata and Central Portal namespace/repository wiring are present; successful Publisher API deployment `5fb01ae9-2609-4284-9427-5830e08bcbb5` validated after public key propagation and was published; public Maven metadata exposes `0.1.0`; public JAR SHA-256 is `2f499b78d06317fd9bf2e343542b74043f163f127cd32db4651098f6ac6af49e` | complete |
| conda-forge | `nwau-py` | 2026-07-03 live probe: PR `https://github.com/conda-forge/staged-recipes/pull/33452` remains open and unmerged at head `bffc5bf1a85389dc695adfd96c87bf2413f4db25`; GitHub status API reports `conda-forge-linter` success; Anaconda API still returns 404 and no `nwau-py` entries appear in conda-forge noarch repodata | maintainer review, merge, feedstock publication, and public Anaconda propagation |
| Homebrew | `nwau-py` | personal tap published and verified; `brew info edithatogo/mchs/nwau-py --json=v2` verified stable `0.2.2`, tap head `fa12ed26c1d6a289b40bf59c9bacbb9a5e42f823`, and linked keg `0.2.2` | complete for personal tap; optional Homebrew/core PR/review only if core distribution is required |
| Open VSX / Visual Studio Marketplace | `mchs-tools` | Open VSX API `https://open-vsx.org/api/edithatogo/mchs-tools` returns `edithatogo.mchs-tools` version `0.1.1` after workflow `https://github.com/edithatogo/mchs/actions/runs/27457810800`; `/tmp/mchs-tools-0.1.1.vsix` was manually uploaded through the signed-in Visual Studio Marketplace publisher portal on 2026-06-16T00:24:00+10:00; the public Marketplace Gallery `extensionquery` API now returns public `edithatogo.mchs-tools` version `0.1.1`, last updated `2026-06-15T14:31:27.95Z`, with VSIX SHA-256 `1d20feaa22e66978d5259dfb7b83467ed803a776d3fcb101792f2f164a2807ad` | complete and retained as maintenance-only; no new extension work is planned unless a new evidence-backed need is opened |
| MATLAB File Exchange | `mchs-matlab-interop` | direct public page probe returned HTTP 200 for `https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop` with title `MCHS MATLAB Interop - File Exchange - MATLAB Central`; MATLAB/Octave runtime validation remains unclaimed because neither runtime is available locally | complete for public File Exchange listing; runtime validation remains unclaimed |
| SSC / Stata package distribution | `mchs` (`mchs-stata-interop` bundle) | public SSC/RePEc archive files `mchs.pkg`, `mchs.ado`, and `mchs.sthlp` returned HTTP 200 on 2026-06-12; `mchs.pkg` records Distribution-Date `20260526` | complete; Stata runtime validation remains unclaimed because Stata is unavailable locally |
| vcpkg / ConanCenter | `nwau-c-abi` | dedicated source archive exists; Conan static/shared local MCHS mirror builds pass; 2026-06-12T12:38:52Z live check shows ConanCenter PR #30262 is open and mergeable at head `c635b0f9d2f1619d9149e4fa964185658c063f5d` with CLA signed and Job scheduler `ACTION_REQUIRED`; vcpkg overlay install passes locally but upstream vcpkg PR #51965 is closed by Rust-library support policy | historical / maintenance-only; ConanCenter review and vcpkg Rust policy are retained as evidence, not active targets |

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

The Maven Central row remains fail-closed for future releases: a real publish
attempt must provide `-PcentralPortalUsername` and `-PcentralPortalPassword`,
and missing credentials stop the publish path instead of falling back to
anonymous access. Version `0.1.0` is verified for
`io.github.edithatogo:mchs-jvm-bindings`.

## Operator unblocker checklist

The account, maintainer-review, and live-environment inputs needed to move the
remaining blocked registries are listed in
`docs/roadmaps/registry-unblocker-inputs-20260612.md`.

## Latest live monitor artifact

The first passive monitor run after adding `.github/workflows/language-registry-live.yml`
completed successfully at `https://github.com/edithatogo/mchs/actions/runs/27420156173`
and uploaded the `language-registry-live` artifact. See
`docs/roadmaps/language-registry-live-monitor-20260612.md`.
