---
title: Power Platform deployment readiness
author: MCHS Maintainers
---

## Power Platform Deployment Readiness

This page documents the Power Platform managed-solution readiness path for NSW-style
governance without overclaiming production status.

## Current claim posture

- Template-only readiness documentation.
- Real NSW tenant deployment is **not claimed** yet.
- Evidence bundles are required before any public readiness claim.

## What is required before claimable status

1. Tenant deployment readiness template completed.
2. Managed promotion runbook evidence recorded for each environment.
3. Tenant credentials present and verified (service principal, secret reference,
   environment IDs).
4. Import and smoke evidence present for all managed promotions.
5. Rollback evidence captured and runnable.

## Blockers that force `blocked`

- Missing tenant service principal.
- Missing tenant client secret or secret reference.
- Missing target environment ID.
- Missing tenant connectivity verification.
- Missing solution checker/import logs.

## Operational evidence bundle

The evidence bundle template is at:
`power-platform/evidence/nsw-operational-readiness-bundle-template.json`.

It is intentionally strict: unresolved credentials keep readiness as `blocked` until
resolved.

## Governance intent

- Keep orchestration thin and logic out of low-code expressions.
- Require managed solutions for downstream environments.
- Capture explicit approvals, logs, and rollback evidence for each promotion step.
