# Go Module Registry Submission

## Overview

Work this registry one by one using a fail-closed process: discover existing publication, prepare the submission if absent, submit only when package readiness and credentials are present, and record durable publication evidence.

## Registry

- Ecosystem: `Go`
- Registry: `Go module proxy/pkg.go.dev`
- Package candidate: `github.com/edithatogo/mchs/bindings/go`
- Version candidate: `0.1.0`
- Local surface: `microcosting_healthservices/bindings/go/go.mod`
- Current status: `published_verified`

## Functional Requirements

- Query the public registry or authoritative submission system for an existing package/listing.
- Record discovered package URL, version, owner, checksum, PR, or absence evidence.
- If not published, prepare registry-specific package metadata and artifacts.
- Verify package readiness locally before any publish attempt.
- Submit only through an authenticated, authorized publisher account.
- Capture immutable evidence after submission.

## Current Status

Resolved locally and publicly indexed. `go.mod` and package imports now use the real GitHub module path, `go test ./...` passes, the Go module proxy lists `v0.1.0`, and pkg.go.dev now exposes `https://pkg.go.dev/github.com/edithatogo/mchs/bindings/go` with version `0.1.0` evidence from the live registry probe.

## Preparation Evidence

- Public proxy discovery: `https://proxy.golang.org/github.com/edithatogo/mchs/bindings/go/@v/list` returns `v0.1.0`.
- pkg.go.dev discovery: `https://pkg.go.dev/github.com/edithatogo/mchs/bindings/go` exposes version `0.1.0`.
- Test command: `go test ./...`
- Test result: all packages passed.
- Remaining external blocker: none.

## Submission Evidence

- Tag: `bindings/go/v0.1.0`
- Commit: `48a658adeb882033147b1fdd4c6b9c0eafcdf727`
- Proxy info URL: `https://proxy.golang.org/github.com/edithatogo/mchs/bindings/go/@v/v0.1.0.info`
- Proxy status: HTTP `200`
- `pkg.go.dev` status: indexed version `0.1.0` verified by live probe on 2026-05-24.

## Acceptance Criteria

- Discovery evidence exists and is linked from this track.
- Preparation evidence exists for package metadata, artifact integrity, and registry policy checks.
- Submission evidence exists, or the track remains blocked with a concrete reason.
- Publication is not claimed unless a public registry URL or accepted upstream PR/merge evidence exists.

## Out of Scope

- Inventing package credentials or registry ownership.
- Publishing prototype, private, placeholder, or non-packable surfaces.
- Claiming support for clinical/private data workflows from package publication.
