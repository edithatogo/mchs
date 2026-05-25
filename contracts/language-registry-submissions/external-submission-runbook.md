# External Submission Runbook

As of 2026-05-25, all language/distribution registry tracks have discovery and local preparation evidence. PyPI, npm, NuGet, the Homebrew personal tap, and the Go module are externally published and verified. The remaining items require publish automation, direct authenticated publish, public listing evidence, legal/publisher agreement completion, or upstream maintainer review.

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

- Package: `NwauCore@0.1.0`
- Local check: `Pkg.test()` passed.
- Dedicated package repo: `https://github.com/edithatogo/NwauCore.jl`
- Tag: `v0.1.0`
- Registrator trigger issue: `https://github.com/edithatogo/NwauCore.jl/issues/1`
- General registry PR: `https://github.com/JuliaRegistries/General/pull/156236`
- Superseded feedback PRs: `https://github.com/JuliaRegistries/General/pull/156200`, `https://github.com/JuliaRegistries/General/pull/156235`
- Feedback addressed: package renamed to `NwauCore`, repository moved to `NwauCore.jl`, and MIT license added to the package top-level folder.
- Current state: open; registry consistency and treecheck checks passed. README purpose/usage documentation was added to the package repo in commit `f42f440`, and the review feedback was answered on the General PR with a `[noblock]` comment.
- Remaining step: wait for General automerge/review and merge. If reviewers require the registration payload itself to include the README update, create a new tag/version or re-registration flow.

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
- Local scaffold: `bindings/jvm` now contains a minimal JVM module with Gradle `maven-publish` and `signing` metadata for `io.github.edithatogo:mchs:0.1.0`.
- Required steps: Central Portal namespace verification, signing key setup, publishing credentials, Gradle publish validation, staged release.

### conda-forge

- Package: `nwau-py==0.2.2`
- Prepared recipe: `microcosting_healthservices/packaging/conda-forge/meta.yaml`
- Submitted PR: `https://github.com/conda-forge/staged-recipes/pull/33452`
- Feedback addressed: pushed commit `e6ff7985c94b78471457e446e8fe3abfbe61fa41` to add recipe maintainers, tests, build number, `license_file`, `setuptools`, noarch Python pins, runtime dependencies, and entry points.
- Branch update: GitHub accepted an update-branch request on 2026-05-26; the linter is passing and platform builds are rerunning on head `e65bf3d5eeee2d1ea3cf4b8cbde4f9e3e32bfac1`.
- Remaining step: wait for rerun platform builds, conda-forge staged-recipes review, merge, and feedstock publication.

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
- Required step: MathWorks account upload and File Exchange review.

### Stata SSC

- Package: `mchs-stata-interop@0.1.0`
- Prepared artifact: `microcosting_healthservices/bindings/stata/mchs-stata-interop-0.1.0.zip`
- Required step: SSC maintainer submission/review.

### vcpkg / ConanCenter

- Package: `nwau-c-abi@0.1.0`
- Draft vcpkg port: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
- Draft vcpkg portfile: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/portfile.cmake`
- Draft Conan recipe: `microcosting_healthservices/packaging/conan/conanfile.py`
- Dependency gate: `nwau-core` is published to crates.io, and `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-c-abi/Cargo.toml` now resolves it from the registry and verifies `nwau-c-abi`.
- Required submission steps: complete vcpkg `portfile.cmake`/version files and ConanCenter recipe packaging, then submit upstream PR/review workflows.
- Current blocker: no vcpkg/Conan PR opened because the local vcpkg port is manifest-only and upstream registry PR/review workflows still need to be prepared.
