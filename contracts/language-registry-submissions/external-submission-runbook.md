# External Submission Runbook

As of 2026-06-12, all language/distribution registry tracks have discovery and local preparation evidence. PyPI, npm, NuGet, the Homebrew personal tap, Julia General, Stata SSC, and the Go module are externally published and verified. The remaining items require direct authenticated publish, public listing evidence, legal/publisher agreement completion, upstream maintainer review, or registry policy changes.

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

- Extension: `edithatogo.mchs-tools`
- Required credentials: `OVSX_PAT` is configured for Open VSX publication; `VSCE_PAT` is still required before Visual Studio Marketplace can be synchronized to `0.1.1`.
- Credential status: Open VSX Access Tokens became available after the Eclipse publisher agreement was accepted; `OVSX_PAT` was created and stored as a GitHub secret on 2026-06-13. The first authenticated publish failed until namespace `edithatogo` was created, then workflow run `https://github.com/edithatogo/mchs/actions/runs/27455601114` published `edithatogo.mchs-tools v0.1.0`. Workflow run `https://github.com/edithatogo/mchs/actions/runs/27457810800` later published `edithatogo.mchs-tools v0.1.1` to Open VSX. Visual Studio Marketplace is publicly listed for `edithatogo.mchs-tools@0.1.0`; `0.1.1` is not claimed there until `VSCE_PAT` is configured and the Marketplace publish succeeds.
- Prepared artifact: `microcosting_healthservices/integrations/vscode/mchs-tools.vsix` when packaged with the workflow command `npx --yes --package @vscode/vsce vsce package --no-dependencies --out mchs-tools.vsix`; plain `vsce package` defaults to the versioned filename `mchs-tools-0.1.0.vsix`.
- Latest artifact evidence: merged workflow dry-run `https://github.com/edithatogo/mchs/actions/runs/27455041574` packaged the VSIX successfully on 2026-06-13; publish workflow `https://github.com/edithatogo/mchs/actions/runs/27455601114` packaged and published the same extension to Open VSX.
- Latest public probe on 2026-06-14: Open VSX API `https://open-vsx.org/api/edithatogo/mchs-tools` returns `edithatogo.mchs-tools` version `0.1.1`; Visual Studio Marketplace extension query for `edithatogo.mchs-tools` returns publisher `edithatogo`, extension `mchs-tools`, display name `MCHS Tools`, and version `0.1.0`.
- Open VSX command: `cd microcosting_healthservices/integrations/vscode && npx --yes --package @vscode/vsce vsce package --no-dependencies --out mchs-tools.vsix && npx --yes --package ovsx ovsx publish mchs-tools.vsix --pat "$OVSX_PAT"`
- Marketplace command for future updates: `cd microcosting_healthservices/integrations/vscode && npx --yes --package @vscode/vsce vsce package --no-dependencies --out mchs-tools.vsix && npx --yes --package @vscode/vsce vsce publish --packagePath mchs-tools.vsix --pat "$VSCE_PAT"`
- Remaining step: configure `VSCE_PAT` or manually upload the `0.1.1` VSIX in the Visual Studio Marketplace publisher portal, then re-run the live monitor and verify both Open VSX and Marketplace expose `0.1.1`.

## Maintainer-review or PR-gated submissions

### CRAN

- Package: `nwauR@0.1.0`
- Prepared artifact: `microcosting_healthservices/nwauR_0.1.0.tar.gz`
- Local check: `R CMD check --no-manual nwauR_0.1.0.tar.gz` returned `Status: OK`.
- Latest public probe on 2026-06-12: CRANDB, `https://cran.r-project.org/package=nwauR`, and `https://cran.r-project.org/src/contrib/Archive/nwauR/` all returned HTTP 404, so no public CRAN publication is claimed.
- Submitted through CRAN maintainer upload workflow on 2026-06-13 as package id 344701; maintainer confirmation email was sent to Dylan Mordaunt <d.a.mordaunt@gmail.com> and must be confirmed before CRAN review proceeds.

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
- Publication status: General PR `#156254` merged on 2026-05-28T15:34:44Z. Public General registry raw files verify `NationalWeightedActivityUnitWrapper v0.1.0`, UUID `58dad789-f56a-4ab3-a66f-c15139bf9cbe`, and git-tree-sha1 `bb22d4bd44689549064bd441092fd540b5d852cf`. JuliaHub still returns 404, so General registry raw files are the publication source of truth.

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
- Latest probe on 2026-06-12: PackageList issue returned HTTP 200 and closed/completed; GitHub release `v0.1.0` returned HTTP 200 and was published on 2026-05-25; raw PackageList `packages.json` returned HTTP 200 but had zero matches for `edithatogo`, `mchs-swift`, or `MCHSBind`; SPI public probes still failed with API HTTP 401, badge/page Cloudflare HTTP 403, and `packages.swift.org` DNS resolution failure from this environment.
- Follow-up: posted `https://github.com/SwiftPackageIndex/PackageList/issues/13717#issuecomment-4690679058` asking maintainers/bot to recheck why the completed submission is absent from the canonical package list.
- Remaining step: verify public SPI listing/version evidence at `https://swiftpackageindex.com/edithatogo/mchs-swift`.

### Maven Central

- Artifact: `io.github.edithatogo:mchs:0.1.0`
- Local scaffold: `bindings/jvm` contains a minimal JVM module with Gradle `maven-publish`, `signing`, and Central Portal repository wiring for `io.github.edithatogo:mchs:0.1.0`. `gradle -p bindings/jvm build --console=plain` passed in the clean clone.
- Dry-run evidence: GitHub Actions run `https://github.com/edithatogo/mchs/actions/runs/27407884659` succeeded with `dry_run=true` on 2026-06-12 after commit `cde0439` moved the workflow runtime JDK to 17 for Gradle 9. The binding module remains Java 11-targeted via Gradle configuration.
- Adjacent artifact probe: `https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml` returned public metadata for `io.github.edithatogo:mchs-jvm-bindings:0.1.0` on 2026-06-14. This does not close the checked-in `io.github.edithatogo:mchs:0.1.0` target unless the contract target is intentionally changed.
- Required steps: Central Portal namespace verification, signing key setup, GitHub secrets `CENTRAL_PORTAL_DEPLOY_URL`, `CENTRAL_PORTAL_USERNAME`, `CENTRAL_PORTAL_PASSWORD`, `MAVEN_SIGNING_KEY`, and `MAVEN_SIGNING_PASSWORD`, authenticated publish/release, and public Maven Central verification. A 2026-06-13 `gh secret list` audit found `NUGET_API_KEY` and `OVSX_PAT` configured, but no Maven Central secrets, so `CENTRAL_PORTAL_DEPLOY_URL`, `CENTRAL_PORTAL_USERNAME`, `CENTRAL_PORTAL_PASSWORD`, `MAVEN_SIGNING_KEY`, and `MAVEN_SIGNING_PASSWORD` are still absent. A fresh dry-run, `Publish Maven Central package` run 27456830098, succeeded from `master` with `dry_run=true`.

### conda-forge

- Package: `nwau-py==0.2.2`
- Prepared recipe: `microcosting_healthservices/packaging/conda-forge/meta.yaml`
- Submitted PR: `https://github.com/conda-forge/staged-recipes/pull/33452`
- Feedback addressed: pushed commit `e6ff7985c94b78471457e446e8fe3abfbe61fa41` to add recipe maintainers, tests, build number, `license_file`, `setuptools`, noarch Python pins, runtime dependencies, and entry points.
- Branch/update status: latest live poll on 2026-06-12 shows PR head `bffc5bf1a85389dc695adfd96c87bf2413f4db25`; conda-forge-linter, GitHub linter, Azure staged-recipes, linux_64, osx_64, win_64, build status, fast-finish, and check-skip checks are all green.
- Remaining step: conda-forge staged-recipes maintainer review, merge, feedstock publication, and public Anaconda propagation. Anaconda API still returns 404 for `conda-forge/nwau-py`, so publication is not claimed.

### Homebrew

- Formula: `nwau-py`
- Prepared formula: `microcosting_healthservices/packaging/homebrew/nwau-py.rb`
- Published personal tap: `https://github.com/edithatogo/homebrew-mchs`
- Formula URL: `https://raw.githubusercontent.com/edithatogo/homebrew-mchs/main/Formula/nwau-py.rb`
- Audit: `brew audit --strict --online edithatogo/mchs/nwau-py` passed.
- Install/test: `brew install --build-from-source edithatogo/mchs/nwau-py` and `brew test edithatogo/mchs/nwau-py` pass.
- Local fix prepared: root `funding-calculator --help` no longer eagerly imports pandas, numpy, pydantic, or pyreadstat; the tap carries an equivalent temporary patch plus a Click PyPI resource.
- Publication status: personal tap is published and verified. A 2026-06-12 `brew info edithatogo/mchs/nwau-py --json=v2` probe verified stable version `0.2.2`, tap head `fa12ed26c1d6a289b40bf59c9bacbb9a5e42f823`, formula SHA-256 `6f987bc4a81f3ac78cbc893d6a502fc572a534905f9f1f89cfc05600ff4ddff3`, and linked keg `0.2.2`. Optional Homebrew/core PR/review remains available only if core distribution is required.

### MATLAB File Exchange

- Package: `mchs-matlab-interop@0.1.0`
- Local status: repo-ready for source/artifact preparation. The MATLAB source tree, contract surface, examples, and `bindings/matlab/mchs-matlab-interop-0.1.0.zip` bundle are present; MATLAB/Octave runtime validation is not claimed in this environment.
- Latest public probe on 2026-06-14: `https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop` returned HTTP 200 with title `MCHS MATLAB Interop - File Exchange - MATLAB Central`.
- Remaining note: MATLAB/Octave runtime validation is not claimed because neither runtime is installed locally.

### Stata SSC

- Package: `mchs@0.1.0` (`mchs-stata-interop` bundle)
- Publication status: published and verified. Public SSC/RePEc archive files `http://fmwww.bc.edu/repec/bocode/m/mchs.pkg`, `mchs.ado`, and `mchs.sthlp` returned HTTP 200 on 2026-06-12; `mchs.pkg` records Distribution-Date `20260526`. Stata runtime validation is not claimed in this environment.

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
- ConanCenter PR state: submitted and mergeable at head `c635b0f9d2f1619d9149e4fa964185658c063f5d`; CLA Assistant reports all committers have signed. The remaining visible gate is ConanCenter Job scheduler ACTION_REQUIRED / maintainer review before upstream CI/publication can be claimed. Maintainer job request posted at `https://github.com/conan-io/conan-center-index/pull/30262#issuecomment-4535445528`; portable runner follow-up posted at `https://github.com/conan-io/conan-center-index/pull/30262#issuecomment-4535716273`; explicit profile/library-pattern follow-up posted at `https://github.com/conan-io/conan-center-index/pull/30262#issuecomment-4535839977`; latest resolved-thread follow-up posted at `https://github.com/conan-io/conan-center-index/pull/30262#issuecomment-4688059783`.
- vcpkg fork update: commit `58ff86fe` adds Rust target-triple mapping, honors `VCPKG_LIBRARY_LINKAGE`, installs a `nwau-c-abi::nwau-c-abi` CMake config target, excludes Android, and regenerates vcpkg version metadata.
- vcpkg maintainer guidance request: `https://github.com/microsoft/vcpkg/pull/51965#issuecomment-4535415243`.
- vcpkg PR state: closed after maintainer guidance that vcpkg does not currently support building Rust libraries. Local investigation found no first-class vcpkg Rust/Cargo acquisition helper or Rust toolchain port.
- Required submission steps: wait for upstream ConanCenter job scheduling/review/merge; resolve vcpkg Rust-library support policy or change to a maintainer-accepted artifact strategy before vcpkg publication can be claimed.
