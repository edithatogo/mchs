# Native Power Platform Pipelines Integration

## Purpose

Use native Power Platform Pipelines as the environment-aware deployment layer
once NSW provides a configured pipeline host. GitHub Actions remains the
source-level validation gate; Power Platform Pipelines handles solution
promotion, environment variables, connection references, and delegated approvals.

## Current State

- Status: scaffolded and blocked pending NSW pipeline host details.
- Stable fallback: `scripts/power-platform-alm.sh` pack, checker, and managed
  import commands.
- Target environment: NSW `dylan`.
- Production-readiness claim: not allowed until pipeline run evidence exists.

## Required NSW Inputs

- Pipeline host environment ID.
- Development environment ID.
- Target environment ID.
- Pipeline ID or name.
- Deployment stage names.
- Delegated deployment approvers.
- Connection reference owners.
- Environment-variable values.

## Required Gates

- Source validation passes in GitHub Actions.
- Managed solution pack succeeds.
- Solution checker has zero critical/high findings.
- Pipeline prevalidation confirms dependencies.
- Connection references are mapped before import.
- Environment variables are supplied before import.
- Import and publish evidence is attached to the deployment bundle.

## Rollback

Rollback must use a previously imported managed solution version or a supported
Power Platform solution upgrade rollback procedure. Manual edits in target
environments are not accepted as rollback evidence.
