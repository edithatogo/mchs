# External Submission Runbook

As of 2026-06-12, all language/distribution registry tracks have discovery and local preparation evidence. PyPI, npm, crates.io, NuGet, the Homebrew personal tap, and the Go module are externally published and verified. The official MCP Registry publication is verified outside this language-registry contract. The remaining items require public listing evidence, token/account linking, upstream maintainer review, or registry-specific validation and PR workflows.

## Already published and verified

- PyPI: `nwau-py==0.2.2`
- npm: `@edithatogo/mchs-wasm-binding@0.1.0`
- crates.io: `nwau-core@0.1.0`
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
- Public probe: `https://open-vsx.org/api/edithatogo/mchs-tools` returned HTTP 404 `Extension not found` with `Accept: application/json` on 2026-05-26. The Visual Studio Marketplace item page returned HTTP 404, and the Gallery `extensionquery` API returned 0 extensions for `edithatogo.mchs-tools`. A 406 Open VSX response means the probe used an incompatible `Accept` header, not that the extension is listed.
- Required credentials: Open VSX token and Visual Studio Marketplace publisher token.
- Credential status: The user reports the Eclipse Foundation Open VSX Publisher Agreement is completed. Eclipse account `edithatogo` is now connected with GitHub account `edithatogo`, and Open VSX GitHub login succeeds. Open VSX Access Tokens still reports that no Eclipse Foundation Open VSX Publisher Agreement is signed and the Profile page redirects to Eclipse Foundation password login for the `openvsx_publisher_agreement` scope. Visual Studio Marketplace publisher `edithatogo` is visible in the publishing portal with Owner role under the signed-in Microsoft account; Marketplace PAT creation and authenticated VSIX publish remain unresolved.
- Track-specific checklist: `conductor/tracks/vscode_openvsx_registry_submission_20260524/access_checklist.md`.
- Prepared artifact: `microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix`
- Open VSX command: `npx --yes ovsx publish microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$OVSX_PAT"`
- Marketplace command: `npx --yes @vscode/vsce publish --packagePath microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$VSCE_PAT"`
- Next-action checklist:
  1. Complete the Eclipse Foundation password login/agreement-recognition flow for account `edithatogo`.
  2. Create an Open VSX access token and expose it only as `OVSX_PAT` for the publish session.
  3. Run `npx --yes ovsx publish microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$OVSX_PAT"`.
  4. Verify `https://open-vsx.org/api/edithatogo/mchs-tools` returns version `0.1.0`.
  5. Create a Marketplace PAT with extension publish rights for the existing Visual Studio Marketplace publisher `edithatogo` and expose it only as `VSCE_PAT`.
  6. Run `npx --yes @vscode/vsce publish --packagePath microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix --pat "$VSCE_PAT"`.
  7. Verify the Visual Studio Marketplace Gallery `extensionquery` API returns `edithatogo.mchs-tools` version `0.1.0`.

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
- PackageList issue: `https://github.com/SwiftPackageIndex/PackageList/issues/13717`, closed as completed on 2026-05-24.
- Fixed publication metadata: added MIT license, Swift package topics, and GitHub release `v0.1.0`.
- Remaining step: verify public SPI listing/version evidence at `https://swiftpackageindex.com/edithatogo/mchs-swift`.
- Latest public probe: on 2026-06-12, the PackageList issue remained closed completed and the GitHub release `v0.1.0` remained published, but the SPI page returned HTTP 403 with a Cloudflare `Just a moment...` challenge and no visible `MCHSBind` or `0.1.0` evidence.
- Track-specific checklist: `conductor/tracks/swift_package_index_submission_20260524/public_probe_checklist.md`.

### Maven Central

- Artifact: `io.github.edithatogo:mchs-jvm-bindings:0.1.0`
- Local check: `gradle -p bindings/jvm validateCentralPortalReadiness build` passed.
- Generated local artifacts: binary jar, sources jar, javadoc jar, Maven POM, and Gradle module metadata.
- Namespace verification: on 2026-06-12, Sonatype Central Portal shows `io.github.edithatogo` as Verified after public GitHub repository verification with key `f7fztfn9vz`.
- Signing check: local GPG key `9DF6B142F065199E` / `BB03C82343A653EE44BD5CDA9DF6B142F065199E` exists for `Dylan Mordaunt <d.a.mordaunt@gmail.com>`; upload to `hkps://keyserver.ubuntu.com` and `hkps://pgp.mit.edu` returned success, and a clean temporary keyring can receive the key from `hkps://keyserver.ubuntu.com`. Central validation still cannot discover the key by fingerprint.
- Latest local refresh: on 2026-06-12, Maven Central metadata still returned HTTP 404, `gradle -p bindings/jvm validateCentralPortalReadiness build -PmavenCentralNamespaceVerified=true` passed, and the readiness report records `namespaceVerified=true`, `publisherCredentialsPresent=false`, `signingCredentialsPresent=false`, and `publicationUpload=not-attempted`.
- Upload attempts: on 2026-06-12, Publisher API uploads succeeded in `USER_MANAGED` mode for deployments `89d0d2a9-91c6-4994-9f8e-fdd34bb501d0`, `fccefc51-9ccb-4466-8f85-8a47bc16cf3c`, and `7ced6d47-59ee-40fb-9c9b-09b1aa9f8491`; each failed validation because Central could not discover public key `BB03C82343A653EE44BD5CDA9DF6B142F065199E`. The temporary Central user token was revoked after the attempts.
- Next-action checklist:
  1. Wait for Central to discover public key `BB03C82343A653EE44BD5CDA9DF6B142F065199E` from a supported keyserver, or publish the public key through another supported path.
  2. Create a fresh short-lived Central user token.
  3. Re-upload `build/mchs-jvm-bindings-0.1.0-central-bundle.zip` through Central Portal or the Publisher API.
  4. Release the deployment after validation succeeds.
  5. Verify `https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml` contains version `0.1.0` before changing the gate to complete.
- Track-specific checklist: `conductor/tracks/jvm_maven_central_registry_submission_20260524/submission_checklist.md`.

### conda-forge

- Package: `nwau-py==0.2.2`
- Prepared recipe: `microcosting_healthservices/packaging/conda-forge/meta.yaml`
- Submitted PR: `https://github.com/conda-forge/staged-recipes/pull/33452`
- Feedback addressed: pushed commit `e6c8b9d632953263517de6a146783f3697fc450d` to add recipe maintainers, tests, build number, `license_file`, `setuptools`, noarch Python pins, runtime dependencies, and entry points.
- Branch update: GitHub accepted an update-branch request on 2026-05-26; linter, check-skip, linux_64, osx_64, win_64, and aggregate checks are passing on the current head.
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
- Next-action checklist:
  1. Sign in to MathWorks File Exchange with the publishing account.
  2. Create a new File Exchange submission named `mchs-matlab-interop`.
  3. Upload `microcosting_healthservices/bindings/matlab/mchs-matlab-interop-0.1.0.zip`.
  4. Copy the description, license, tags, and version from `bindings/matlab/file-exchange-submission.json`.
  5. Submit for File Exchange review and record the submission URL or review email in the MATLAB track evidence.
  6. Verify the public File Exchange page exposes version `0.1.0` before changing the gate to complete.
- Track-specific checklist: `conductor/tracks/matlab_file_exchange_submission_20260524/submission_checklist.md`.

### Stata SSC

- Package: `mchs-stata-interop@0.1.0`
- Prepared artifact: `microcosting_healthservices/bindings/stata/mchs-stata-interop-0.1.0.zip`
- Contents: ado/help/pkg files, README, MIT license, notes, and example `.do` workflows.
- Next-action checklist:
  1. Email the SSC package submission contact with package name `mchs-stata-interop`, version `0.1.0`, maintainer contact, and a short description.
  2. Attach or link `microcosting_healthservices/bindings/stata/mchs-stata-interop-0.1.0.zip`.
  3. Include `bindings/stata/pkg-mchs.pkg` as the package index file and list the included ado/help/example files.
  4. Record the sent email date, recipient, and message identifier in the Stata SSC track evidence.
  5. Apply any maintainer-requested package changes, rebuild the zip, and update the checksum evidence if the archive changes.
  6. Verify the package is installable from SSC before changing the gate to complete.
- Track-specific checklist: `conductor/tracks/stata_ssc_submission_20260524/submission_checklist.md`.

### vcpkg / ConanCenter

- Package: `nwau-c-abi@0.1.0`
- Prepared vcpkg port: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
- Prepared vcpkg portfile: `microcosting_healthservices/packaging/vcpkg/ports/nwau-c-abi/portfile.cmake`
- Prepared Conan recipe: `microcosting_healthservices/packaging/conan/conanfile.py`
- Dependency gate: `nwau-core` is published to crates.io, and `cargo package --allow-dirty --locked --manifest-path rust/crates/nwau-c-abi/Cargo.toml` now resolves it from the registry and verifies `nwau-c-abi`.
- Conan validation: `conan create packaging/conan --build=missing` builds and packages `nwau-c-abi/0.1.0` locally on macOS armv8.
- vcpkg validation: bootstrapped vcpkg under `/tmp/mchs-vcpkg-validation` and ran `/tmp/mchs-vcpkg-validation/vcpkg install nwau-c-abi --overlay-ports=/Volumes/PortableSSD/GitHub/mchs/microcosting_healthservices/packaging/vcpkg/ports --triplet arm64-osx --clean-after-build --binarysource=clear`; install completed successfully with release/debug static libraries, header, copyright, and SPDX metadata.
- vcpkg submission: PR `https://github.com/microsoft/vcpkg/pull/51965` was closed unmerged on 2026-05-26. The actionable port-quality feedback was addressed in fork commit `58ff86fe`, but maintainers closed the PR because vcpkg does not currently support building Rust libraries.
- ConanCenter submission: PR `https://github.com/conan-io/conan-center-index/pull/30262` is open. Portability fixes were pushed in commit `c635b0f9d2f1619d9149e4fa964185658c063f5d`; remaining external gates are CLA/recheck, job scheduler, maintainer review, and merge.
- Track-specific checklist: `conductor/tracks/c_cpp_vcpkg_conan_submission_20260524/upstream_pr_checklist.md`.
- Next-action checklist:
  1. Treat vcpkg as upstream-policy deferred unless vcpkg adds Rust-library port support or the package is redesigned to avoid requiring vcpkg to build Rust code.
  2. Complete the ConanCenter CLA/recheck gate for PR `https://github.com/conan-io/conan-center-index/pull/30262`.
  3. Wait for ConanCenter job scheduler and maintainer review, then apply requested fixes if any.
  4. Verify the merged ConanCenter package page before changing the Conan side of the gate to complete.
  5. Keep vcpkg publication unclaimed until an accepted upstream path exists.
