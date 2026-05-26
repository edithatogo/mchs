# External Submission Runbook

As of 2026-05-26, all language/distribution registry tracks have discovery and local preparation evidence. PyPI, npm, NuGet, the Homebrew personal tap, and the Go module are externally published and verified. The remaining items require publish automation, direct authenticated publish, public listing evidence, legal/publisher agreement completion, or upstream maintainer review.

## Already published and verified

- PyPI: `nwau-py==0.2.2`
- npm: `@edithatogo/mchs-wasm-binding@0.1.0`
- NuGet: `Mchs.Bindings.DotNet@0.1.0`
- Homebrew personal tap: `https://github.com/edithatogo/homebrew-mchs`
- Go module proxy/pkg.go.dev: `github.com/edithatogo/mchs/bindings/go@v0.1.0`

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

- Extension: `edithatogo.mchs-tools@0.1.0`
- Required credentials: Open VSX token and Visual Studio Marketplace publisher token.
- Credential status: Open VSX GitHub login succeeded, but token creation is blocked until the Eclipse Foundation Open VSX Publisher Agreement is signed via an Eclipse account. The Visual Studio Marketplace publisher page for `edithatogo` returned 404 in the current Microsoft session, so publisher/PAT access remains unresolved.
- Prepared artifact: `microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix`
- Open VSX command: `npx --yes ovsx publish microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$OVSX_PAT"`
- Marketplace command: `npx --yes @vscode/vsce publish --packagePath microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$VSCE_PAT"`

## Maintainer-review or PR-gated submissions

### CRAN

- Package: `nwauR@0.1.0`
- Prepared artifact: `microcosting_healthservices/nwauR_0.1.0.tar.gz`
- Local check: `R CMD check --no-manual nwauR_0.1.0.tar.gz` returned `Status: OK`.
- Submit through CRAN maintainer upload/review workflow.

### Julia General

- Package: `NationalWeightedActivityUnitWrapper@0.1.0`
- Local check: `julia --project=. -e 'using Pkg; Pkg.instantiate(); Pkg.test()'` passed.
- Dedicated package repo: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl`
- Tag: `v0.1.0`
- Commit: `56ddec5ae29513e80717d4625f82c024a211c949`
- UUID: `58dad789-f56a-4ab3-a66f-c15139bf9cbe`
- Registrator trigger issue: `https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1`
- General registry PR: `https://github.com/JuliaRegistries/General/pull/156254`
- Superseded feedback PRs: `https://github.com/JuliaRegistries/General/pull/156236`, `https://github.com/JuliaRegistries/General/pull/156235`, `https://github.com/JuliaRegistries/General/pull/156200`
- Feedback addressed: reviewers agreed `NwauCore` was misleading and recommended a wrapper name; the active replacement uses `NationalWeightedActivityUnitWrapper`, README purpose/usage documentation, MIT license, and matching repo name.
- Current state: open; registry consistency, treecheck, AutoMerge, and AutoMerge-stopwatch checks passed.
- Remaining step: wait for General PR `#156254` merge and public registry propagation. The superseded PRs `#156236`, `#156235`, and `#156200` are now closed after `[noblock]` superseded comments were posted. Reviewer clarification was answered at `https://github.com/JuliaRegistries/General/pull/156254#issuecomment-4540952348`, confirming that "National" refers to Australia's National Weighted Activity Unit.

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
- PackageList issue: `https://github.com/SwiftPackageIndex/PackageList/issues/13717`, closed as completed on 2026-05-24.
- Fixed publication metadata: added MIT license, Swift package topics, and GitHub release `v0.1.0`.
- Remaining step: verify public SPI listing/version evidence at `https://swiftpackageindex.com/edithatogo/mchs-swift`.

### Maven Central

- Artifact: `io.github.edithatogo:mchs:0.1.0`
- Local scaffold: `bindings/jvm` contains a minimal JVM module with Gradle `maven-publish`, `signing`, and Central Portal repository wiring for `io.github.edithatogo:mchs:0.1.0`. `gradle -p bindings/jvm build --console=plain` passed in the clean clone.
- Required steps: Central Portal namespace verification, signing key setup, GitHub secrets `CENTRAL_PORTAL_USERNAME`, `CENTRAL_PORTAL_PASSWORD`, `MAVEN_SIGNING_KEY`, and `MAVEN_SIGNING_PASSWORD`, manual workflow `Publish Maven Central package` dry-run, authenticated publish/release, and public Maven Central verification.

### conda-forge

- Package: `nwau-py==0.2.2`
- Prepared recipe: `microcosting_healthservices/packaging/conda-forge/meta.yaml`
- Submitted PR: `https://github.com/conda-forge/staged-recipes/pull/33452`
- Feedback addressed: pushed commit `e6ff7985c94b78471457e446e8fe3abfbe61fa41` to add recipe maintainers, tests, build number, `license_file`, `setuptools`, noarch Python pins, runtime dependencies, and entry points.
- Branch update: GitHub accepted another update-branch request on 2026-05-26. Latest poll: PR head `8e479175a4e9feffcd4e5313ef149abb485f1343`; conda-forge linter/check jobs are rerunning after the update.
- Remaining step: checks returning green, conda-forge staged-recipes maintainer review, merge, feedstock publication, and public Anaconda propagation.

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
- Local status: repo-ready for source/artifact preparation. The MATLAB source tree, contract surface, examples, and `bindings/matlab/mchs-matlab-interop-0.1.0.zip` bundle are present; MATLAB/Octave runtime validation is not claimed in this environment.
- Required step: use a MathWorks account to upload the prepared bundle and complete File Exchange review.

### Stata SSC

- Package: `mchs@0.1.0` (`mchs-stata-interop` bundle)
- Submission status: Gmail sent message id `19e5ffd483ef5841` on thread `19e5ff9a74554b3a` to `baum@bc.edu` with `bindings/stata/mchs-stata-interop-0.1.0-ssc.zip` attached; Stata runtime validation is not claimed in this environment.
- Remaining step: wait for SSC maintainer review and public archive publication evidence.

### vcpkg / ConanCenter

- Package: `nwau-c-abi@0.1.0`
- Draft vcpkg port: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
- Draft vcpkg portfile: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/portfile.cmake`
- Draft vcpkg version metadata: `microcosting_healthservices/packaging/vcpkg/versions/n-/nwau-c-abi.json`
- Draft Conan recipe: `microcosting_healthservices/packaging/conan/conanfile.py`
- Dedicated source archive: `https://github.com/edithatogo/mchs/releases/download/nwau-c-abi-v0.1.0/nwau-c-abi-0.1.0-source-r2.tar.gz`
- Dependency gate: `nwau-core` is published to crates.io, and `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-c-abi/Cargo.toml` now resolves it from the registry and verifies `nwau-c-abi`.
- Local validation: Conan `conan create packaging/conan --build=missing` and `conan create packaging/conan -o 'nwau-c-abi/*:shared=True' --build=missing` passed against the dedicated archive; vcpkg overlay install passed for `nwau-c-abi:arm64-osx@0.1.0` with release/debug libraries, usage text, and copyright installed.
- vcpkg upstream PR: `https://github.com/microsoft/vcpkg/pull/51965`.
- ConanCenter upstream PR: `https://github.com/conan-io/conan-center-index/pull/30262`.
- ConanCenter fork updates: commit `d8cbc1de` fixes ConanCenter review risks for Cargo Release/Debug profile mapping, static/shared package separation, and portable `test_package` execution; commit `0e7d9052` changes the C smoke test pointer comparison from `0` to `NULL`; commit `d3a07060` switches the test package runner to `self.cpp.build.bindir` for multi-config and Windows portability; commit `657c7a31` adds explicit `_cargo_profile()` and `_library_patterns()` helpers so Cargo profile and shared/static artifact selection are direct recipe-side fixes.
- ConanCenter validation after mirroring `657c7a31`: local MCHS mirror validations `conan create packaging/conan --build=missing` and `conan create packaging/conan -o 'nwau-c-abi/*:shared=True' --build=missing` both passed.
- ConanCenter PR state: submitted at head `657c7a31` and waiting on maintainer job-scheduler approval plus CLA Assistant legal acceptance before upstream CI/publication can be claimed. Maintainer job request posted at `https://github.com/conan-io/conan-center-index/pull/30262#issuecomment-4535445528`; portable runner follow-up posted at `https://github.com/conan-io/conan-center-index/pull/30262#issuecomment-4535716273`; explicit profile/library-pattern follow-up posted at `https://github.com/conan-io/conan-center-index/pull/30262#issuecomment-4535839977`; CLAassistant reports the CLA as pending/not signed and requires authorized contributor legal acceptance.
- vcpkg fork update: commit `58ff86fe` adds Rust target-triple mapping, honors `VCPKG_LIBRARY_LINKAGE`, installs a `nwau-c-abi::nwau-c-abi` CMake config target, excludes Android, and regenerates vcpkg version metadata.
- vcpkg maintainer guidance request: `https://github.com/microsoft/vcpkg/pull/51965#issuecomment-4535415243`.
- vcpkg PR state: submitted, but CI fails where `cargo` is unavailable on macOS, Linux, and Windows triplets; Android lanes succeeded and are not the blocker. Local investigation found no first-class vcpkg Rust/Cargo acquisition helper or Rust toolchain port.
- Required submission steps: wait for upstream ConanCenter review/merge; resolve vcpkg Cargo/toolchain policy and Microsoft CLA legal acceptance before vcpkg publication can be claimed.
