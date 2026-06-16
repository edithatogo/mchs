# External Submission Runbook

As of 2026-06-16, all language/distribution registry tracks have discovery and local preparation evidence. PyPI, npm, crates.io, NuGet, the Homebrew personal tap, the Go module, Swift Package Index, Maven Central, MATLAB File Exchange, Open VSX, Visual Studio Marketplace, and Stata SSC are externally published and verified. The official MCP Registry publication is verified outside this language-registry contract. The remaining items require CRAN/conda-forge/ConanCenter reviewer action.

Email guardrail: do not send, reply, forward, or transmit corrected archives from any mailbox unless the user explicitly approves the exact outbound action first. Local draft text and package preparation can proceed, but outbound email remains user-approval gated.

Live-monitor note: scheduled or manual `.github/workflows/language-registry-live.yml` runs upload the Markdown/JSON live reports and append the Markdown report, including the generated timestamp, promotion group counts, submission detail, public detail, promotion state, and next action, to the GitHub Actions job summary. The workflow exposes `GITHUB_TOKEN` only to the report-generation step so GitHub PR and feedstock probes avoid anonymous rate limits. For GitHub PR submissions, submission detail includes live mergeability fields when the API provides them.

CRAN public-proof note: the live monitor checks the CRAN package page, CRANDB, and `https://cran.r-project.org/src/contrib/PACKAGES`; CRAN publication is not treated as verified until one of those public surfaces exposes target version `0.1.0`.

conda-forge public-proof note: the live monitor checks both the Anaconda `conda-forge/nwau-py` package API and `https://github.com/conda-forge/nwau-py-feedstock`; feedstock creation alone is not treated as publication until the target package version is visible through Anaconda.

vcpkg / ConanCenter public-proof note: the live monitor checks the ConanCenter raw recipe and `conandata.yml` before the vcpkg raw port. ConanCenter publication evidence can satisfy the active Conan side of the gate, but the combined registry remains partial while vcpkg is upstream-policy deferred.

Stata SSC public-proof note: the live monitor checks the Boston College SSC/RePEc `mchs.pkg`, `mchs.ado`, and `mchs.sthlp` paths; installability is treated as verified when the package manifest and ado/help files expose the `mchs` command identity. SSC `.pkg` metadata does not expose semantic versions, so version `0.1.0` remains local archive evidence.

## Already published and verified

- PyPI: `nwau-py==0.2.2`
- npm: `@edithatogo/mchs-wasm-binding@0.1.0`
- crates.io: `nwau-core@0.1.0`
- NuGet: `Mchs.Bindings.DotNet@0.1.0`
- Homebrew personal tap: `https://github.com/edithatogo/homebrew-mchs`
- Go module proxy/pkg.go.dev: `github.com/edithatogo/mchs/bindings/go@v0.1.0`
- Swift Package Index: `MCHSBind@0.1.0`
- Maven Central: `io.github.edithatogo:mchs-jvm-bindings:0.1.0`
- Visual Studio Marketplace: `edithatogo.mchs-tools@0.1.1`
- Open VSX: `edithatogo.mchs-tools@0.1.0` remains available; latest is `0.1.1`
- Stata SSC: `mchs` installable from Boston College SSC/RePEc public files

## Credential-gated direct publishes

### crates.io

- Package: `nwau-core@0.1.0`
- Publication status: published and verified at `https://crates.io/crates/nwau-core/0.1.0`.
- Public evidence: crates.io version API reports `created_at=2026-05-25T13:59:23.536614Z`, checksum `c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547`, and `yanked=false`.
- Credential/workflow status: `.github/workflows/publish-registry-packages.yml` has a manual `workflow_dispatch` `cratesio` path. Dispatch run `https://github.com/edithatogo/mchs/actions/runs/26404356667` reported the version already existed on crates.io.
- Dependency note: `nwau-core` is now available before `nwau-c-abi` packaging/submission.
- Safety note: credential cleanup is complete: the browser-created crates.io token was revoked and the stale GitHub Actions secret was deleted.

### NuGet

- Package: `Mchs.Bindings.DotNet@0.1.0`
- Required credential: `NUGET_API_KEY`.
- Credential/workflow status: `NUGET_API_KEY` exists as a GitHub repository secret, and `.github/workflows/publish-registry-packages.yml` has a manual `workflow_dispatch` `nuget` path that packs and pushes the package.
- Prepared artifact: `microcosting_healthservices/bindings/dotnet/bin/Release/Mchs.Bindings.DotNet.0.1.0.nupkg`
- Prepared command: `dotnet nuget push microcosting_healthservices/bindings/dotnet/bin/Release/Mchs.Bindings.DotNet.0.1.0.nupkg --api-key "$NUGET_API_KEY" --source https://api.nuget.org/v3/index.json`
- Workflow dispatch: run the `Publish registry packages` workflow with `registry=nuget`.
- Submission evidence: GitHub Actions run `https://github.com/edithatogo/mchs/actions/runs/26404217645` completed successfully and NuGet returned `Created` / `Your package was pushed`.
- Publication evidence: `https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/index.json` returned HTTP 200 with version `0.1.0`.
- Package blob: `https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/0.1.0/mchs.bindings.dotnet.0.1.0.nupkg` returned HTTP 200.
- Registration API: `https://api.nuget.org/v3/registration5-semver1/mchs.bindings.dotnet/index.json` returned HTTP 200 with `listed: true`.
- Note: the NuGet HTML package page returned 404 from this environment during verification, so API and package blob evidence are authoritative.

### Open VSX / Visual Studio Marketplace

- Extension: `edithatogo.mchs-tools@0.1.1`
- Public probe: `https://open-vsx.org/api/edithatogo/mchs-tools` returns namespace `edithatogo`, name `mchs-tools`, latest version `0.1.1`, and allVersions including `0.1.1`, `0.1.0`, and `latest`; Visual Studio Marketplace Gallery `extensionquery` returns public `edithatogo.mchs-tools` version `0.1.1` with VSIX SHA-256 `1d20feaa22e66978d5259dfb7b83467ed803a776d3fcb101792f2f164a2807ad`.
- Credential status: Open VSX Access Tokens became available for `edithatogo` after Eclipse Publisher Agreement recognition. A fresh token named `mchs-tools publish 2026-06-13` was generated for the publish check, `npx --yes ovsx publish integrations/vscode/mchs-tools-0.1.0.vsix --pat [REDACTED]` returned that `edithatogo.mchs-tools 0.1.0` is already published, and the fresh token was deleted afterwards. A pre-existing Open VSX token row was left untouched. Visual Studio Marketplace publisher `edithatogo` is visible in the publishing portal with Owner role under the signed-in Microsoft account; Marketplace web upload accepted `mchs-tools-0.1.0.vsix` and published version `0.1.0`. On 2026-06-16, the signed-in Marketplace publisher page showed `MCHS Tools` version `0.1.1` as Public under `edithatogo`.
- Track-specific checklist: `conductor/tracks/vscode_openvsx_registry_submission_20260524/access_checklist.md`.
- Prepared artifact: `microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix`
- Prepared sync artifact: `microcosting_healthservices/integrations/vscode/mchs-tools-0.1.1.vsix` with local SHA-256 `bfbeca13497f21489c532e58af3b1e10df9fe60ae5eab4c721e632baee9b5dd6`.
- Open VSX publish check: `npx --yes ovsx publish integrations/vscode/mchs-tools-0.1.0.vsix --pat [REDACTED]` returned that version `0.1.0` is already published.
- Remaining step: none for the verified `0.1.1` publication; preserve publisher ID `bd039266-4396-4e4c-8bb8-13364a4aab70`, extension ID `8cf2c772-2ead-4a18-8dde-c5069790380a`, Open VSX API evidence, Marketplace Gallery API evidence, and token-cleanup evidence.

## Maintainer-review or PR-gated submissions

### CRAN

- Package: `nwauR@0.1.0`
- Prepared artifact: `microcosting_healthservices/nwauR_0.1.0.tar.gz`
- Local check: `R CMD check --no-manual nwauR_0.1.0.tar.gz` returned `Status: OK`.
- Package-local CRAN-style check: `_R_CHECK_CRAN_INCOMING_REMOTE_=false R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz` returned `Status: OK`.
- Live CRAN remote incoming metadata check: `R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz` returned `Status: 1 NOTE`; the only reported NOTE is the expected CRAN incoming `New submission` note.
- Submission state: submitted through the CRAN web upload workflow on 2026-06-12 using the maintainer email in `r-binding/DESCRIPTION`; CRAN confirmation email was received in Outlook on 2026-06-12 02:17 Australia/Sydney, and the user clicked the confirmation link. The CRAN confirmation result page displayed `The package has been uploaded successfully to CRAN submission team.`
- Track-specific checklist: `conductor/tracks/r_cran_registry_submission_20260524/submission_checklist.md`.
- Next-action checklist:
  1. Wait for CRAN incoming/pretest or reviewer email and record the incoming/pretest URL or message identifier in the CRAN track evidence.
  2. Respond to any CRAN maintainer email with a patched tarball or explanation, then replace the checksum in the track evidence if the tarball changes.
  3. Verify `https://cran.r-project.org/package=nwauR` and record version `0.1.0` before changing the gate to complete.
- Latest public probe: on 2026-06-16, `https://cran.r-project.org/web/packages/nwauR/index.html` returned HTTP 404; CRANDB returned HTTP 404; `src/contrib/PACKAGES` did not contain `Package: nwauR`. Latest mail-probe evidence remains the 2026-06-13 connected Gmail search with no CRAN/nwauR response; Microsoft 365/Outlook connector previously returned `No accounts found. Please login first.`

### Julia General

- Replacement package candidate: `NationalWeightedActivityUnitWrapper@0.1.0`
- Active package repo: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`
- Active Registrator trigger issue: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1`
- Active General registry PR: `https://github.com/JuliaRegistries/General/pull/156254`
- Active tag: `v0.1.0`
- Active commit: `56ddec5ae29513e80717d4625f82c024a211c949`
- Active PR head: `bb63b2a81ec2ded2c5675f09fb6cd63128f10a07`
- Package UUID: `58dad789-f56a-4ab3-a66f-c15139bf9cbe`
- Submission status: published_verified; checks successful; merged at `2026-05-28T15:34:44Z`.
- Publication status: published_verified; the merged General PR is the authoritative publication evidence.
- Local check: existing Julia binding `Pkg.test()` evidence passed before the replacement registration rename.
- Superseded package: `NwauCore@0.1.0`
- Superseded dedicated package repo: `https://github.com/edithatogo/NwauCore.jl`
- Superseded tag: `v0.1.0`
- Superseded Registrator trigger issue: `https://github.com/edithatogo/NwauCore.jl/issues/1`
- Superseded General registry PR: `https://github.com/JuliaRegistries/General/pull/156236`
- Superseded feedback PRs: `https://github.com/JuliaRegistries/General/pull/156200`, `https://github.com/JuliaRegistries/General/pull/156235`
- Superseded feedback addressed: package renamed to `NwauCore`, repository moved to `NwauCore.jl`, and MIT license added to the package top-level folder.
- Current state: the `NwauCore` PR has registry consistency and treecheck history but is not expected to merge after reviewer feedback that the `Core` name is misleading.
- Remaining step: no remaining publication step for this registry track. Preserve the merged PR evidence and keep the superseded `NwauCore` PR archived as historical context.

### Go module proxy / pkg.go.dev

- Module: `github.com/edithatogo/mchs/bindings/go`
- Local check: `go test ./...` passed.
- Completed step: public repository files were updated and tag `bindings/go/v0.1.0` was created.
- Verified proxy URL: `https://proxy.golang.org/github.com/edithatogo/mchs/bindings/go/@v/v0.1.0.info`
- Verified pkg.go.dev URL: `https://pkg.go.dev/github.com/edithatogo/mchs/bindings/go`
- Remaining step: none. Version `0.1.0` was verified by the live registry probe.

### Swift Package Index

- Package: `MCHSBind@0.1.0`
- Local check: `swift build` passed.
- Dedicated package repo: `https://github.com/edithatogo/mchs-swift.git`
- Tag: `v0.1.0`
- GitHub release: `https://github.com/edithatogo/mchs-swift/releases/tag/v0.1.0`
- PackageList issue: `https://github.com/SwiftPackageIndex/PackageList/issues/13717`, closed as completed on 2026-05-24; maintainer comment on 2026-06-12 says the original closure was premature and the package was added with PR `https://github.com/SwiftPackageIndex/PackageList/pull/13999`.
- PackageList PR: `https://github.com/SwiftPackageIndex/PackageList/pull/13999`, merged on 2026-06-12 at `2026-06-12T12:02:16Z` with merge commit `ffdaf6cf883878adcb7f31691f6120e3d7f64c48`.
- Raw PackageList evidence: `https://raw.githubusercontent.com/SwiftPackageIndex/PackageList/main/packages.json` contains `https://github.com/edithatogo/mchs-swift.git`.
- Fixed publication metadata: added MIT license, Swift package topics, and GitHub release `v0.1.0`.
- Publication evidence: on 2026-06-12, `https://swiftpackageindex.com/edithatogo/mchs-swift` returned HTTP 200 and exposed `MCHSBind`, canonical `edithatogo/mchs-swift` links, stable `v0.1.0`, the SPM manifest snippet using `from: "0.1.0"`, and the GitHub release link.
- Remaining step: none for Swift Package Index publication. Preserve the PackageList merge, raw PackageList, release, and public SPI page evidence.
- Track-specific checklist: `conductor/tracks/swift_package_index_submission_20260524/public_probe_checklist.md` is retained as completed publication evidence.

### Maven Central

- Artifact: `io.github.edithatogo:mchs-jvm-bindings:0.1.0`
- Local check: `gradle -p bindings/jvm validateCentralPortalReadiness build` passed.
- Generated local artifacts: binary jar, sources jar, javadoc jar, Maven POM, and Gradle module metadata.
- Namespace verification: on 2026-06-12, Sonatype Central Portal shows `io.github.edithatogo` as Verified after public GitHub repository verification with key `f7fztfn9vz`.
- Signing check: local GPG key `9DF6B142F065199E` / `BB03C82343A653EE44BD5CDA9DF6B142F065199E` exists for `Dylan Mordaunt <d.a.mordaunt@gmail.com>`; upload to supported keyservers returned success and Central validation passed after propagation.
- Publication evidence: Publisher API deployment `5fb01ae9-2609-4284-9427-5830e08bcbb5` validated and was published with HTTP 204. `https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml` returns HTTP 200 and exposes latest/release/version `0.1.0`.
- Artifact evidence: public JAR URL `https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/0.1.0/mchs-jvm-bindings-0.1.0.jar` returns HTTP 200 with SHA-256 `2f499b78d06317fd9bf2e343542b74043f163f127cd32db4651098f6ac6af49e`; public POM URL returns HTTP 200 with SHA-256 `367e6a08a9d57ebd6d97d9fa14f1fe65fbfdf7fce882369ab8264996995c36c6`.
- Next-action checklist:
  1. None for Maven Central publication. Preserve the public metadata/JAR evidence and revoked-token notes.
- Track-specific checklist: `conductor/tracks/jvm_maven_central_registry_submission_20260524/submission_checklist.md`.

### conda-forge

- Package: `nwau-py==0.2.2`
- Prepared recipe: `microcosting_healthservices/packaging/conda-forge/meta.yaml`
- Submitted PR: `https://github.com/conda-forge/staged-recipes/pull/33452`
- Feedback addressed: pushed commit `e6ff7985c94b78471457e446e8fe3abfbe61fa41` to add recipe maintainers, tests, build number, `license_file`, `setuptools`, noarch Python pins, runtime dependencies, and entry points; the PR was later refreshed to head `bffc5bf1a85389dc695adfd96c87bf2413f4db25`.
- Branch update: GitHub accepted an update-branch request on 2026-05-26; authenticated live evidence on 2026-06-16 observed current head `bffc5bf1a85389dc695adfd96c87bf2413f4db25` with linter, conda-forge-linter, staged-recipes, build fast finish, linux_64, osx_64, win_64, build status, and check skip passing.
- Latest live PR probe: 2026-06-16 authenticated live monitor shows PR `33452` still open, `merged=False`, `draft=False`, `mergeable=True`, and `mergeable_state=clean`; GitHub CLI GraphQL mergeability currently reports `UNKNOWN`. Current linter/Azure staged-recipes checks remain successful, no review decision is present, and no actionable comments appear after the 2026-06-11 author follow-up. Anaconda API still returns HTTP 404 for `conda-forge/nwau-py`, and the `conda-forge/nwau-py-feedstock` repository still returns HTTP 404.
- Remaining step: wait for conda-forge staged-recipes maintainer review, merge, and feedstock publication.
- Track-specific checklist: `conductor/tracks/conda_forge_feedstock_submission_20260524/review_checklist.md`.

### Homebrew

- Formula: `nwau-py`
- Prepared formula: `microcosting_healthservices/packaging/homebrew/nwau-py.rb`
- Published personal tap: `https://github.com/edithatogo/homebrew-mchs`
- Formula URL: `https://raw.githubusercontent.com/edithatogo/homebrew-mchs/main/Formula/nwau-py.rb`
- Audit: `brew audit --strict --online edithatogo/mchs/nwau-py` passed.
- Install/test: `brew install --build-from-source edithatogo/mchs/nwau-py` and `brew test edithatogo/mchs/nwau-py` pass.
- Local fix prepared: root `funding-calculator --help` no longer eagerly imports pandas, numpy, pydantic, or pyreadstat; the tap carries an equivalent temporary patch plus a Click PyPI resource.
- Remaining step: optional Homebrew/core PR/review if core distribution is required.

### MATLAB File Exchange

- Package: `mchs-matlab-interop@0.1.0`
- Prepared artifact: `microcosting_healthservices/bindings/matlab/mchs-matlab-interop-0.1.0.zip`
- Contents: README, MIT license, File Exchange metadata, workflow notes, adapter functions, and examples.
- Published URL: `https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop`.
- Public evidence: Chrome observed the published File Exchange page on 2026-06-13 with title `MCHS MATLAB Interop - File Exchange - MATLAB Central`, version `0.1.0`, add-on id `184067`, add-on UUID `91133d3e-f475-413c-85bc-544188a60074`, the banner `Your submission has been published in File Exchange.`, tags `cli`, `csv`, `health economics`, `matlab`, `microcosting`, and `parquet`, and the recorded requirements text.
- Submission note: the MathWorks live editor required population through its rich-text editor state before validation; the final public page shows the intended description and requirements. The original uploaded archive SHA-256 was `1156f506cda8ab797b5d07adebc35ecccb36bd9758cffaf011029c71c9d2515a`. After publication, the local ZIP was corrected so its README/metadata no longer say no File Exchange upload occurred; corrected local SHA-256 is `d78cc11a9ab23080b38604e21c5d21ba9c8801ae0cf6219888f1797834cf2336`.
- Replacement follow-up: Chrome opened new-version draft `https://www.mathworks.com/contribute/submissions/aaea44a8-4710-4e2c-a17d-a97aede040de/edit` with update notes and version `0.1.1`, but the browser automation backend could not complete a trusted replacement ZIP upload. No corrected replacement publication is claimed.
- Remaining step: none for File Exchange publication; keep the local note that MATLAB/Octave runtime execution is not claimed in this repository evidence.
- Track-specific checklist: `conductor/tracks/matlab_file_exchange_submission_20260524/submission_checklist.md`.

### Stata SSC

- Package: `mchs-stata-interop@0.1.0`
- Prepared artifact: `microcosting_healthservices/bindings/stata/mchs-stata-interop-0.1.0.zip`
- Contents: ado/help/pkg files, README, MIT license, notes, and example `.do` workflows.
- Current archive SHA-256: `47e4f6a7c86d483ef71baa1daa8b9e20f61f12acab9973f94483923fb2e37f55`.
- Submission state: initial SSC submission and maintainer-identity clarification were sent via Gmail on 2026-06-12. Christopher Baum replied that the author contact information seemed to be missing from `mchs.sthlp`.
- Feedback fix: `mchs.sthlp` and the README now include the Author section with Dylan Mordaunt, `dylan.mordaunt@vuw.ac.nz`, and the repository URL; the SSC archive was rebuilt with the current checksum above.
- Corrected-reply draft: `conductor/tracks/stata_ssc_submission_20260524/corrected_archive_reply_draft.md`.
- Public evidence: on 2026-06-14, `http://fmwww.bc.edu/repec/bocode/m/mchs.pkg` was live and listed the MCHS module, Dylan Mordaunt support email, `mchs.ado`, `mchs.sthlp`, and example files; `http://fmwww.bc.edu/repec/bocode/m/mchs.ado` exposed `program define mchs`; `http://fmwww.bc.edu/repec/bocode/m/mchs.sthlp` exposed MCHS Stata help and `{cmd:mchs ...}` command help.
- Version boundary: SSC `.pkg` metadata does not expose semantic versions, so version `0.1.0` remains local archive evidence rather than public SSC metadata.
- Remaining step: none for SSC publication. The corrected-archive follow-up is obsolete because public installability evidence exists; do not send it without an explicit new user instruction.
- Track-specific checklist: `conductor/tracks/stata_ssc_submission_20260524/submission_checklist.md`.

### vcpkg / ConanCenter

- Package: `nwau-c-abi@0.1.0`
- Prepared vcpkg port: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
- Prepared vcpkg portfile: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/portfile.cmake`
- Prepared Conan recipe: `microcosting_healthservices/packaging/conan/conanfile.py`
- Dependency gate: `nwau-core` is published to crates.io, and `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-c-abi/Cargo.toml` now resolves it from the registry and verifies `nwau-c-abi`.
- Conan validation: `conan create packaging/conan --build=missing` builds and packages `nwau-c-abi/0.1.0` locally on macOS armv8.
- Latest ConanCenter probe: 2026-06-16 authenticated live monitor shows PR `30262` open, `merged=False`, `draft=False`, `mergeable=True`, and `mergeable_state=blocked`; `gh pr view` shows `reviewDecision=REVIEW_REQUIRED`, `license/cla` success, and `Job scheduler` `ACTION_REQUIRED`; no new actionable comments appear after the 2026-06-12 author follow-up.
- vcpkg validation: bootstrapped vcpkg under `/tmp/mchs-vcpkg-validation` and ran `/tmp/mchs-vcpkg-validation/vcpkg install nwau-c-abi --overlay-ports=/Volumes/PortableSSD/GitHub/mchs/microcosting_healthservices/packaging/vcpkg/ports --triplet arm64-osx --clean-after-build --binarysource=clear`; install completed successfully with release/debug static libraries, header, copyright, and SPDX metadata.
- vcpkg submission: PR `https://github.com/microsoft/vcpkg/pull/51965` was closed unmerged on 2026-05-26. The actionable port-quality feedback was addressed in fork commit `58ff86fe`, but maintainers closed the PR because vcpkg does not currently support building Rust libraries.
- ConanCenter submission: PR `https://github.com/conan-io/conan-center-index/pull/30262` is open. Portability fixes were pushed in commit `c635b0f9d2f1619d9149e4fa964185658c063f5d`; CLA/recheck is now resolved, and the remaining external gates are job scheduler, maintainer review, and merge.
- Track-specific checklist: `conductor/tracks/c_cpp_vcpkg_conan_submission_20260524/upstream_pr_checklist.md`.
- Next-action checklist:
  1. Treat vcpkg as upstream-policy deferred unless vcpkg adds Rust-library port support or the package is redesigned to avoid requiring vcpkg to build Rust code.
  2. Wait for ConanCenter job scheduler and maintainer review, then apply requested fixes if any.
  3. Verify the merged ConanCenter package page before changing the Conan side of the gate to complete.
  4. Keep vcpkg publication unclaimed until an accepted upstream path exists.
