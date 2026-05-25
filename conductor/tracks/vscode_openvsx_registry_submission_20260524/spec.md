# VS Code/Open VSX Extension Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `VS Code extension`
- Registry: `Open VSX / Visual Studio Marketplace`
- Package candidate: `mchs-tools`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/integrations/vscode/package.json`
- Current status: `prepared_pending_publisher_tokens_and_vsix_publish`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved locally. A VS Code extension project exists and packages into `mchs-tools-0.1.0.vsix` using `vsce`. The remaining blocker is external: Open VSX and Visual Studio Marketplace require publisher accounts/tokens for authenticated publishing.

## Preparation Evidence

- Public registry discovery: `https://open-vsx.org/api/edithatogo/mchs-tools` returned `Extension not found`.
- Package command: `npx --yes @vscode/vsce package --no-dependencies`
- Artifact: `microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix`
- Package result: packaged 6 files, 2.56 KB.
- Local fix: added local `LICENSE` and package `files` allowlist.
- Remaining external blocker: publisher tokens for Open VSX and Visual Studio Marketplace.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
