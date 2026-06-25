# Specification: Repository Topology Authority

## Overview

Define the repository topology authority for MCHS. The canonical implementation
root is `microcosting_healthservices`; the outer `mchs` checkout is treated as a
transitional wrapper until its source and evidence slices are migrated, archived,
or retired. The policy must make nested Git repositories, unmanaged gitlinks,
package surfaces, generated artifacts, and release evidence boundaries explicit.

## Functional Requirements

- Declare the canonical repository root and the relationship between the outer
  wrapper and the implementation repo.
- Ban unmanaged nested `.git` directories and gitlinks unless a valid
  `.gitmodules` entry and governance rationale exist.
- Define which directories are source, generated, evidence, vendor, external
  archive, registry packaging, or local environment.
- Require every package surface to have an owner, manifest, support status,
  validation command, release target, and evidence boundary.
- Require topology decisions to preserve source and evidence before deletion.
- Require local repo completion and external registry/admin gates to remain
  separate blocker classes.

## Non-Functional Requirements

- Preserve existing calculator behavior and public package contracts.
- Prefer a monorepo model for current language bindings until extraction
  criteria are met.
- Keep topology validation non-interactive and suitable for CI.
- Avoid overclaiming scaffold or roadmap-only surfaces.

## Acceptance Criteria

- `conductor/repository-topology.md` exists and names
  `microcosting_healthservices` as canonical.
- The policy explicitly bans unmanaged gitlinks and nested repos.
- The policy references package surface ownership, generated artifact retention,
  outer wrapper migration, release boundaries, and future repo splits.
- Tests confirm the track files, registry entry, and topology policy language.

## Out of Scope

- Moving files out of the outer wrapper.
- Splitting packages into new repositories.
- Publishing or re-publishing package registry artifacts.
