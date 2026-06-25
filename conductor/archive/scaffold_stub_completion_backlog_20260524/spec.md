# Specification: Scaffold and Stub Completion Backlog

## Overview

This track converts the repository's scaffold, stub, placeholder, and
complete-with-gaps inventory into executable remediation work. The purpose is
not to hide unfinished surfaces; it is to either bring them to real validated
completion or mark them with truthful non-completion states until implementation
and validation evidence exists.

The immediate trigger is the current no-stub detector result, which reports
completed tracks without matching implementation evidence. The broader scope is
the visible set of scaffold-heavy surfaces in bindings, contracts,
Power Platform, WebAssembly, registry submissions, documentation claims, and
Conductor metadata.

## Functional Requirements

- Run the repository stub detector and preserve the initial finding set as
  remediation evidence.
- Inventory every surface that is `scaffold-only`, `roadmap-only`,
  `complete-with-gaps`, `not-ready`, `future-only`, private, or otherwise
  described as placeholder, synthetic, prototype, mock-only, or not implemented.
- Split inventory items into one of three states:
  - promote to implementation now,
  - retain as explicit non-final scaffold with a pending implementation track,
  - remove or quarantine because it is misleading or no longer wanted.
- Fix state mismatches where a track is marked complete but detector evidence
  cannot find matching implementation files.
- Record at least one validation command for every remediation item that is
  retained, promoted, or downgraded.
- Require concrete completion evidence before any remediation item can move to
  complete: implementation files, tests, docs, support status, and validation
  command output.
- Keep publication and registry claims conservative. A package, registry,
  adapter, or integration surface is not published or ready unless immutable
  publication evidence exists.
- Update user-facing docs, support matrices, Conductor metadata, and track
  registry entries so they agree.

## Non-Functional Requirements

- Preserve active Python calculator behavior while cleaning scaffold status.
- Do not delete potentially useful scaffold material without recording the
  decision and impact.
- Use the existing support-state vocabulary instead of inventing new labels.
- Keep remediation tasks small enough for independent implementation tracks or
  subagents with disjoint write sets.

## Acceptance Criteria

- The stub detector either reports zero unresolved findings or every finding is
  tied to an incomplete remediation track and no longer marked as complete.
- All completed tracks have implementation, validation, documentation, and
  review evidence that is more than roadmap or scaffold content.
- All non-final surfaces are marked consistently as roadmap-only,
  scaffold-only, complete-with-gaps, not-ready, future-only, private, blocked,
  or another approved support state.
- The README package registry table, documentation support pages, Conductor
  metadata, and tests agree on what is real product versus scaffold.
- Follow-on implementation tracks exist for every scaffold surface that the
  project still intends to finish.

## Out of Scope

- Implementing every deferred language binding in this track.
- Publishing registry packages without completed implementation and release
  evidence.
- Reverting unrelated user work or deleting source archive material.
