# Power Platform Deployment Readiness (Roadmap Addendum)

## Purpose

Provide a controlled gateway for Power Platform managed-solution promotion with
explicit evidence and blocker tracking.

## Current position

- Power Platform remains an orchestration surface through service boundary.
- This section is roadmapping evidence, not a claim of production NSW tenancy
  deployment.

## Planned operational artifacts

- `power-platform/deployment/nsw-deployment-readiness-template.md`
- `power-platform/deployment/nsw-managed-solution-promotion-runbook.md`
- `power-platform/evidence/nsw-operational-readiness-bundle-template.json`
- `power-platform/governance/nsw-power-platform-governance.md`

## Gate model

1. Documentation gate: template and runbook completed.
2. Credential gate: tenant principal, secret reference, and environment IDs present.
3. Validation gate: managed import and smoke checks pass in dev → test → UAT.
4. Evidence gate: blocker list empty and rollback evidence recorded.

Any missing tenant credential keeps the surface in `blocked` and prevents release
readiness claims.

## CI wiring

- `.github/workflows/power-platform-alm.yml` runs an `aggregate-readiness-preflight`
  job as a local-only validation step.
- The job checks repository health, operational evidence, platform test status,
  and the GitHub live-gate evidence contract with local files only.
- The local validators are `validate_power_platform_repo_health.py`,
  `validate_power_platform_operational_evidence.py`,
  `validate_power_platform_platform_tests.py`, and
  `validate_power_platform_github_live_gate.py`.
- The job does not read repository secrets or dispatch live workflows.

## Governance contract

- No formula logic in Power Platform apps, flows, or formulas.
- Managed solution is the boundary artifact for promotion.
- NSW deployment evidence is explicit and non-hypothetical.
