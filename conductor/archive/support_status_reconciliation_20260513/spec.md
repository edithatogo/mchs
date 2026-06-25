# Specification: Support Status Reconciliation

## Overview

Reconcile support status vocabulary across generated canonical schemas,
governance contracts, docs, API, MCP, and release evidence.

## Requirements

- Use one canonical vocabulary: `unsupported`, `blocked`, `planned`,
  `deferred`, `canary`, `opt_in`, `preview`, `release_candidate`, `ga`,
  `no_new_development`, `historical`.
- Remove conflicting `active`, `deprecated`, and `retired` lifecycle terms or
  map them explicitly as legacy metadata.
- Apply statuses to all streams, years, jurisdictions, surfaces, runtimes, and
  language tracks.

## Acceptance Criteria

- No conflicting support status enum is treated as canonical.
- Generated contracts and governance support matrix agree.
- Docs display the narrowest truthful support status.
