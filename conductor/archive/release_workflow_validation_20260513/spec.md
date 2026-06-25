# Specification: Release Workflow Validation

## Overview

Validate Cline's CI/CD and release workflow changes before merge.

## Requirements

- Check GitHub Actions YAML syntax and job outputs.
- Verify Rust release workflow tag/version outputs.
- Verify coverage gate extraction and Codecov OIDC settings.
- Verify SBOM generation fallback produces valid JSON.
- Verify security workflows are not over-broad or unpinned without rationale.

## Acceptance Criteria

- Workflows lint or dry-run where possible.
- Known output bugs are fixed.
- Release evidence bundle requirements are wired to release workflows.
