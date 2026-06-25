# .NET NuGet Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `.NET/C#`
- Registry: `NuGet`
- Package candidate: `Mchs.Bindings.DotNet`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/bindings/dotnet/DotNetBinding.csproj`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Published and verified. `DotNetBinding.csproj` is packable, the GitHub Actions publish workflow pushed `Mchs.Bindings.DotNet.0.1.0.nupkg` in run `26404217645`, NuGet accepted the upload, and the public flat-container endpoint now returns HTTP 200 with version `0.1.0`.

## Preparation Evidence

- Public registry discovery: `https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/index.json` returned `BlobNotFound`.
- Local package command: `dotnet pack --configuration Release`
- Package artifact: `microcosting_healthservices/bindings/dotnet/bin/Release/Mchs.Bindings.DotNet.0.1.0.nupkg`
- Verification result: restore, build, and package creation completed successfully.
- Submission evidence: `https://github.com/edithatogo/mchs/actions/runs/26404217645` completed successfully and NuGet returned `Created` / `Your package was pushed`.
- Publication evidence: `https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/index.json` returned HTTP 200 with `0.1.0`.
- Publication URL: `https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/index.json`
- Package blob URL: `https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/0.1.0/mchs.bindings.dotnet.0.1.0.nupkg`
- Registration API URL: `https://api.nuget.org/v3/registration5-semver1/mchs.bindings.dotnet/index.json`

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists.
- Publication is claimed only because public NuGet flat-container evidence includes version `0.1.0`.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
