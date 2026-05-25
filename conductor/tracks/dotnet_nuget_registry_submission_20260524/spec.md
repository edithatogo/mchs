# .NET NuGet Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `.NET/C#`
- Registry: `NuGet`
- Package candidate: `Mchs.Bindings.DotNet`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/bindings/dotnet/DotNetBinding.csproj`
- Current status: `prepared_pending_nuget_api_key_and_push`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally. `DotNetBinding.csproj` is now packable and `dotnet pack --configuration Release` created `Mchs.Bindings.DotNet.0.1.0.nupkg`. The remaining blocker is external credentials: `NUGET_API_KEY` is not configured locally.

## Preparation Evidence

- Public registry discovery: `https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/index.json` returned `BlobNotFound`.
- Local package command: `dotnet pack --configuration Release`
- Package artifact: `microcosting_healthservices/bindings/dotnet/bin/Release/Mchs.Bindings.DotNet.0.1.0.nupkg`
- Verification result: restore, build, and package creation completed successfully.
- Remaining external blocker: NuGet API key/login required.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
