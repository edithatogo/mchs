# TypeScript/WASM npm Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `TypeScript/WASM`
- Registry: `npm`
- Package candidate: `@edithatogo/mchs-wasm-binding`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/wasm-binding/package.json`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Blocker

Resolved. The original `@mchs/wasm-binding` candidate could not be published because the `@mchs` scope was not owned/available to the authenticated npm account. The package was renamed to the owned `@edithatogo` scope and published as `@edithatogo/mchs-wasm-binding@0.1.0`.

## Publication Evidence

- npm package URL: `https://www.npmjs.com/package/@edithatogo/mchs-wasm-binding/v/0.1.0`
- Registry tarball: `https://registry.npmjs.org/@edithatogo/mchs-wasm-binding/-/mchs-wasm-binding-0.1.0.tgz`
- Integrity: `sha512-0GarRubfN7lucDSKVM4wMpIZCqKb1qn2oYQzx55SlCJs5O5kub5qDYUpGic+zCDB5Kl0l9oOxZwDwJims6bXug==`
- Published at: `2026-05-24T09:08:12.407Z`
- Verified with: `npm view @edithatogo/mchs-wasm-binding@0.1.0 name version dist.tarball dist.integrity time --json --registry=https://registry.npmjs.org`

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
