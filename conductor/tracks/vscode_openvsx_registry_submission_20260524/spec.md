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

Resolved. A VS Code extension project exists and packages into `mchs-tools` VSIX artifacts using `vsce`. Open VSX and Visual Studio Marketplace both expose `edithatogo.mchs-tools@0.1.1`; no active VS Code Marketplace/Open VSX publication blocker remains.

## Preparation Evidence

- Public registry discovery: `https://open-vsx.org/api/edithatogo/mchs-tools` returned `Extension not found`.
- Package command: `npx --yes @vscode/vsce package --no-dependencies`
- Artifact: `microcosting_healthservices/integrations/vscode/mchs-tools.vsix` through the explicit workflow `--out` path; manual Marketplace update used `/tmp/mchs-tools-0.1.1.vsix`.
- Package result: packaged successfully in workflow run `https://github.com/edithatogo/mchs/actions/runs/27457810800` before Open VSX `0.1.1` publication.
- Local fix: added local `LICENSE` and package `files` allowlist.
- Publication evidence: Open VSX API verifies `0.1.1`, and the Visual Studio Marketplace Gallery API verifies public `0.1.1` with VSIX SHA-256 `1d20feaa22e66978d5259dfb7b83467ed803a776d3fcb101792f2f164a2807ad`.
- Remaining external blocker: none for Open VSX / Visual Studio Marketplace `0.1.1` publication.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
