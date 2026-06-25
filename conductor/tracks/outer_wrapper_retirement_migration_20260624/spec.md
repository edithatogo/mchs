# Specification: Outer Wrapper Retirement Migration

## Overview

Inventory and retire the transitional outer `mchs` wrapper after preserving
source, evidence, governance, Power Platform, script, and test slices that are
not already represented in the canonical repo. The existing outer gitlink for
`microcosting_healthservices` has no `.gitmodules` mapping, so it must not
remain as an ambiguous superproject.

## Functional Requirements

- Inventory every outer-wrapper path and classify it as duplicate, generated,
  source, evidence, local-only, migration candidate, or delete candidate.
- Preserve source and evidence slices before deleting or ignoring wrapper files.
- Migrate unique Power Platform governance and evidence artifacts into canonical
  repo paths or record why they remain external.
- Decide whether the outer wrapper is retired, converted into a valid
  superproject, or retained as a separate non-authoritative evidence repo.
- Require a migration manifest before any source or evidence removal.
- Record residual blockers when outer files require user or registry action.

## Non-Functional Requirements

- Do not delete raw archives, release evidence, screenshots, or registry proof
  without a manifest entry.
- Do not modify active package source while retiring wrapper-only artifacts.
- Preserve branch and PR history by using minimal, reviewable commits.

## Acceptance Criteria

- `conductor/outer-wrapper-retirement.md` records classification rules,
  migration sequencing, and rollback guidance.
- The topology validator can detect an invalid outer gitlink when an outer root
  is explicitly checked.
- Source and evidence preservation is required before cleanup.
- Wrapper retirement does not imply that package registry gates are complete.

## Out of Scope

- Directly deleting outer repo files in this track creation slice.
- Changing package runtime behavior.
- Creating new external repositories.
