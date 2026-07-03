# VS Code/Open VSX Extension Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `VS Code extension`
- Registry: `Open VSX / Visual Studio Marketplace`
- Package candidate: `mchs-tools`
- Version candidate: `0.1.1`
- Local surface: `microcosting_healthservices/integrations/vscode/package.json`
- Current status: `deprecated_cancelled_publication_retained`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved for the canonical `0.1.0` submission and latest `0.1.1` synchronization as historical evidence, then deprecated and cancelled on 2026-07-03. A concrete VS Code helper extension project exists and packages into `mchs-tools-0.1.1.vsix` using `vsce`. The helper exposes commands to inspect the checked-in VS Code/Open VSX registry gate, open the registry contract, open the external-gates roadmap, and copy the gated Open VSX publish command. Visual Studio Marketplace is published and public as `edithatogo.mchs-tools@0.1.1`; Open VSX also exposes `edithatogo.mchs-tools@0.1.0` and latest `0.1.1`. No further extension publishing or synchronization work is planned unless re-chartered.

Follow-up synchronization is resolved: on 2026-06-16, the signed-in Marketplace publisher page showed `MCHS Tools` version `0.1.1` as public under `edithatogo`, and the public Gallery API returned `edithatogo.mchs-tools` version `0.1.1`. The prepared local sync artifact remains at `integrations/vscode/mchs-tools-0.1.1.vsix` with SHA-256 `bfbeca13497f21489c532e58af3b1e10df9fe60ae5eab4c721e632baee9b5dd6`; the public Marketplace VSIX SHA-256 returned by the Gallery API is `1d20feaa22e66978d5259dfb7b83467ed803a776d3fcb101792f2f164a2807ad`.

## Preparation Evidence

- Public registry discovery: `https://open-vsx.org/api/edithatogo/mchs-tools` returned HTTP 404 `Extension not found` with `Accept: application/json` on 2026-05-26 before publication. The Visual Studio Marketplace item page returned HTTP 404, and the Gallery `extensionquery` API returned 0 extensions for `edithatogo.mchs-tools`. The earlier Open VSX HTTP 406 was caused by sending a GitHub vendor `Accept` header to Open VSX; the live probe now uses registry-neutral JSON headers for Open VSX.
- Marketplace publication evidence: Visual Studio Marketplace Gallery `extensionquery` returns public extension `edithatogo.mchs-tools`, publisher ID `bd039266-4396-4e4c-8bb8-13364a4aab70`, extension ID `8cf2c772-2ead-4a18-8dde-c5069790380a`, version `0.1.1`, and public VSIX SHA-256 `1d20feaa22e66978d5259dfb7b83467ed803a776d3fcb101792f2f164a2807ad`.
- Open VSX publication evidence: `https://open-vsx.org/api/edithatogo/mchs-tools` returns namespace `edithatogo`, name `mchs-tools`, latest version `0.1.1`, and allVersions including `0.1.1`, `0.1.0`, and `latest`.
- Package command: `npx --yes @vscode/vsce package --no-dependencies`
- Artifact: `microcosting_healthservices/integrations/vscode/mchs-tools-0.1.0.vsix`
- Package result: packaged 6 files, 4.33 KB.
- Marketplace sync artifact: `microcosting_healthservices/integrations/vscode/mchs-tools-0.1.1.vsix`
- Marketplace sync artifact SHA-256: `bfbeca13497f21489c532e58af3b1e10df9fe60ae5eab4c721e632baee9b5dd6`
- Marketplace sync package result: packaged 6 files, 4.42 KB; no publish command was run.
- Local fix: added local `LICENSE`, package `files` allowlist, and a concrete registry-gate helper command surface.
- Latest Open VSX browser evidence: on 2026-06-13, Open VSX user settings were logged in as `edithatogo`, Access Tokens could be generated, a fresh token named `mchs-tools publish 2026-06-13` was generated, `ovsx publish` returned that `edithatogo.mchs-tools 0.1.0` is already published, and the fresh token was deleted afterwards. A pre-existing Open VSX token row was left untouched.
- Remaining external blocker: none for historical evidence. The surface is now deprecated and cancelled, so no future Open VSX or Marketplace publishing work is planned unless re-chartered.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
