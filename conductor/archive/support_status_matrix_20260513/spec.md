# Specification: Support Status Matrix

## Overview

Define machine-readable support statuses so docs, packages, APIs, MCP tools,
and releases cannot overclaim support.

## Requirements

- Define canonical statuses: `unsupported`, `blocked`, `planned`, `deferred`,
  `canary`, `opt_in`, `preview`, `release_candidate`, `ga`,
  `no_new_development`, and `historical`.
- Apply statuses to streams, years, jurisdictions, surfaces, runtimes, and
  languages.
- Require fail-closed behavior for missing evidence.
- Make public docs display the narrowest truthful status.

## Acceptance Criteria

- Support status matrix roadmap exists.
- Canonical contract foundation depends on the status vocabulary.
- Deferred and historical surfaces use explicit statuses.
- Tests validate that unsupported claims do not appear as GA.
