# TypeScript/WASM npm Registry Submission

## Overview

Track discovery, local preparation, submission, and publication evidence for the npm registry without overclaiming publication.

## Registry

- Ecosystem: `TypeScript/WASM`
- Registry: `npm`
- Package candidate: `@edithatogo/mchs-wasm-binding`
- Version candidate: `0.1.0`
- Local surface: `wasm-binding/package.json`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for existing package/version evidence.
- Record absence, submission, or publication evidence in the language registry contract.
- Prepare registry-specific metadata or artifacts only from committed package surfaces.
- Submit only through an authenticated, authorized publisher account or upstream review workflow.
- Keep external legal, credential, maintainer-review, and propagation blockers explicit.

## Current Blocker

None; publication is verified.

## Evidence

- Submission URL: https://www.npmjs.com/package/@edithatogo/mchs-wasm-binding/v/0.1.0
- Contract source: `contracts/language-registry-submissions/language-registry-submissions.contract.json`
- External gate roadmap: `docs/roadmaps/language-registry-external-gates.md`

## Acceptance Criteria

- Track context exists for the contract's `typescript_npm_registry_submission_20260524` reference.
- Current status and blocker language match the checked-in language registry contract.
- Publication is claimed only when public registry evidence verifies the target version.

## Out of Scope

- Accepting CLAs, publisher agreements, or legal terms on behalf of a contributor.
- Inventing credentials, namespace ownership, API keys, or registry maintainer approval.
- Claiming publication from local artifacts alone.
