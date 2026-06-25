# Specification: Release Boundary Control Plane

## Overview

Create a control plane that ties each package surface to its version source,
release workflow, registry evidence, support status, and external gate class.
This prevents README, docs, support matrices, and release notes from claiming
publication or readiness before immutable evidence exists.

## Functional Requirements

- Define release-boundary fields in the package surface registry.
- Map every surface to a version source and release target.
- Distinguish local-ready, submitted, blocked, published, and published-verified
  states without blending them.
- Require immutable registry links or API evidence for publication claims.
- Require explicit external blocker names for registry/admin/reviewer gates.
- Require docs and README claims to match release evidence boundaries.

## Non-Functional Requirements

- Do not require live network checks in the topology validator.
- Keep live registry proof in dedicated registry-gate scripts.
- Preserve conservative support status vocabulary.

## Acceptance Criteria

- `conductor/release-boundary-control-plane.md` documents the rules.
- `package-surfaces.json` includes release boundary fields for every surface.
- Tests verify registry state terms and blocker separation.

## Out of Scope

- Live registry polling.
- Uploading packages.
- Changing release workflow semantics beyond topology validation.
