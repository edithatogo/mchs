# Specification: Release Evidence Bundle

## Overview

Define the evidence bundle required for release-candidate and GA claims.

## Requirements

- Include release identifier, commit, tag, packages, supported scope, source
  manifests, schema versions, fixture results, parity reports, coverage, SBOM,
  security scan summary, provenance, limitations, and rollback instructions.
- Prevent GA status when required evidence is missing.
- Attach evidence to release artefacts.

## Acceptance Criteria

- Evidence bundle format exists.
- Support status matrix depends on release evidence.
- Release automation can validate required fields before GA.
