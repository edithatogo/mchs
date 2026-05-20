# NSW Deployment Readiness Template

Scope: Power Platform managed-solution readiness planning for NSW-aligned deployments.

This is a planning template and **does not claim an active NSW production deployment**.

## Decision context

- Surface: Power Platform managed solution + connector/orchestration layer.
- Deployment target: NSW target tenant environments (e.g., test, UAT, production).
- Readiness model: `blocked` until tenant credentials and tenant-specific deployment
  evidence are available.

## Required evidence bundle sections

1. `tenant_profile`

- Tenant name and region.
- Tenant ID (or a controlled alias reference).
- Owner contact and approval record.
- Data classification review result for the tenant boundary.

2. `solution_artifacts`

- Unpacked solution source-of-truth version.
- Managed solution artifact checksum.
- Solution Checker result and log location.
- Plugin/custom connector/export package list.
- Governance role assignments used for import.

3. `connector_hardening`

- API endpoint hostname and health-check URL.
- TLS and cert trust chain evidence.
- Timeout/retry policy and backoff settings.
- Error correlation IDs and trace IDs enabled.

4. `deployment_runbook`

- Environment bootstrap checklist (order: dev -> test -> UAT -> production).
- Manual approval or change-control record per promotion.
- Rollback command and fallback artifact references.

5. `evidence_of_observability`

- Import result logs for each managed import.
- Smoke test transcript (`/health`, `/status`, or equivalent) for each environment.
- Audit trail record for configuration changes.

## Blocker register (operationally enforced)

Keep these as hard blockers until explicitly removed by evidence updates:

- `tenant_client_secret_missing`: client secret / secret reference is missing.
- `tenant_service_principal_missing`: service principal app registration not provisioned.
- `tenant_environment_id_unknown`: target environment ID not confirmed.
- `tenant_connectivity_unverified`: connectivity from deployment runner to tenant endpoint
  not validated.

## NSW-specific caution

- NSW pricing, jurisdiction, and policy fields must remain in controlled, local-only
  configuration.
- Do not route NSW-sensitive artifacts through public, unauthenticated surfaces.
- If any blocker remains unresolved, the state remains `blocked` and is not suitable
  for production promotion.

## Readiness decision template

```text
State: blocked
Why: Missing required tenant credentials and environment evidence.
Next action: complete all evidence sections and clear blocker register once credentials
are provisioned and verified.
``` 

## No-claim rule

Do not claim NSW deployment or production readiness from this template alone.
Claims require target-environment credentials, managed solution import evidence,
solution checker output, app smoke evidence, and flow smoke evidence.

## Precision evidence checklists

- Real flow smoke checklist: complete `power-platform/evidence/flow-smoke-evidence-template.json`
  with per-flow IDs, run IDs, and synthetic pass evidence for the tenant environment.
- DLP/monitoring/connector policy checklist: complete
  `power-platform/evidence/monitoring-dlp-evidence-template.json` with policy identifiers,
  connector allow-state, and monitored failure evidence.
- Official GitHub live-gate checklist: run
  `.github/workflows/power-platform-official-actions.yml` with `run_live_checks=true`
  and store workflow evidence in
  `power-platform/evidence/official-github-live-gate-evidence-template.json`.
- Standalone subrepo closure checklist: provision standalone remote governance
  in `power-platform/repository/subrepo-manifest.json` or explicitly close the waiver
  in `power-platform/repository/standalone-subrepo-remote-or-waiver-closure-template.json`.
