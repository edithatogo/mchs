# Swift Package Index Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Swift`
- Registry: `Swift Package Index`
- Package candidate: `MCHSBind`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/bindings/swift/Package.swift`
- Current status: `deprecated_cancelled_publication_retained`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved and published as historical evidence, then deprecated and cancelled on 2026-07-03. `swift build` completes for `MCHSBind`, a clean public package repository exists at `https://github.com/edithatogo/mchs-swift.git`, tag `v0.1.0` exists, `swift package dump-package` succeeds, and the Swift Package Index PackageList issue was closed as completed on 2026-05-24. On 2026-06-12, a Swift Package Index maintainer confirmed the original issue had been closed prematurely and added the package with merged PackageList PR `https://github.com/SwiftPackageIndex/PackageList/pull/13999`. Public repository metadata was improved with an MIT license, Swift package topics, and a GitHub release for `v0.1.0`. A public Swift Package Index page probe exposes `MCHSBind`, `edithatogo/mchs-swift`, stable `v0.1.0`, the SPM manifest snippet, and the GitHub release link. No further SPI publication, compatibility, or monitoring work is planned unless re-chartered.

## Preparation Evidence

- Public index discovery: live probes on 2026-06-12 confirmed PackageList PR `https://github.com/SwiftPackageIndex/PackageList/pull/13999` merged at `2026-06-12T12:02:16Z`, raw PackageList main contains `https://github.com/edithatogo/mchs-swift.git`, and the GitHub release API returns `tag_name=v0.1.0`, `draft=false`, and `prerelease=false`; `https://swiftpackageindex.com/edithatogo/mchs-swift` returned HTTP 200 with page evidence for `MCHSBind`, `edithatogo/mchs-swift`, stable `v0.1.0`, the SPM manifest snippet using `from: "0.1.0"`, and the GitHub release link.
- Build command: `swift build`
- Build result: `Build complete.`
- Test note: `swift test` exits with `no tests found` because the package has no `Tests` target.
- Fixed publication metadata: added MIT license, Swift package topics, and GitHub release `https://github.com/edithatogo/mchs-swift/releases/tag/v0.1.0`.
- Remaining external blocker: none.

## Submission Evidence

- Package repository: `https://github.com/edithatogo/mchs-swift.git`
- Tag: `v0.1.0`
- GitHub release: `https://github.com/edithatogo/mchs-swift/releases/tag/v0.1.0`
- Latest release probe: GitHub release API returned `tag_name=v0.1.0`, `name=MCHSBind v0.1.0`, `draft=false`, `prerelease=false`, and `published_at=2026-05-25T13:03:45Z`.
- Maintainer correction: `https://github.com/SwiftPackageIndex/PackageList/issues/13717#issuecomment-4691089818` says the package was added with PR `https://github.com/SwiftPackageIndex/PackageList/pull/13999`.
- PackageList PR: `https://github.com/SwiftPackageIndex/PackageList/pull/13999`, merged at `2026-06-12T12:02:16Z` with merge commit `ffdaf6cf883878adcb7f31691f6120e3d7f64c48`; validation checks succeeded and maintainer review was approved.
- Raw PackageList probe: `https://raw.githubusercontent.com/SwiftPackageIndex/PackageList/main/packages.json` contains `https://github.com/edithatogo/mchs-swift.git`.
- Latest public SPI probe: `https://swiftpackageindex.com/edithatogo/mchs-swift` returned HTTP 200 on 2026-06-12 with title `MCHSBind - Swift Package Index`, canonical `edithatogo/mchs-swift` links, stable `v0.1.0`, an SPM manifest snippet using `from: "0.1.0"`, and a release link to `https://github.com/edithatogo/mchs-swift/releases/tag/v0.1.0`.
- Metadata commit: `02b12bd6667fae762cdf26833514dbbce5c05476`
- PackageList issue: `https://github.com/SwiftPackageIndex/PackageList/issues/13717`, closed as completed on 2026-05-24.
- `swift package dump-package`: returned package name `MCHSBind` and tools version `5.9.0`

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists.
- Publication is verified by the public Swift Package Index page exposing the package and version, but the surface is now deprecated and cancelled.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
