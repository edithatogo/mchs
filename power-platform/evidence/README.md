# Power Platform Evidence

Evidence files in this directory distinguish source readiness from external
deployment state. Do not mark NSW deployment, managed promotion, or production
readiness complete unless a target-environment import and smoke result is
recorded here.

## Current Evidence Split

- `nsw-managed-import-20260520.json`: real managed solution import evidence for
  NSW `dylan`.
- `nsw-operational-readiness-bundle-template.json`: operational bundle with the
  managed import recorded and runtime blockers preserved.
- `runtime-smoke-evidence-template.json`: app, flow, and service-boundary smoke
  evidence shape.
- `service-boundary-endpoint-template.json`: blocked endpoint configuration and
  probe contract for a real HTTPS service boundary once provided.
- `flow-smoke-evidence-template.json`: structured real Power Automate flow smoke
  traceability and blocked checklist while live run evidence is absent.
- `connection-reference-evidence-template.json`: connection reference and
  environment-variable deployment value evidence shape, including the blocked
  service-boundary endpoint handoff.
- `monitoring-dlp-evidence-template.json`: monitoring, DLP, support, and
  escalation evidence shape.
- `official-github-live-gate-evidence-template.json`: official GitHub Actions live-gate
  evidence shape for environment-bound validation.
- `github-live-gate-20260521.json`: current blocked live-gate record with the
  repository secrets, workflow run URL, who-am-i, solution checker, and
  artifact-hash placeholders preserved.
- `power-platform/repository/standalone-subrepo-remote-or-waiver-closure-template.json`:
  standalone subrepo split decision and waiver closure checklist.
- `platform-test-status.json`: live platform-test status, including the fact
  that the Power App has not yet been viewed, smoke-tested, or visually
  optimized in the tenant.

`scripts/validate_power_platform_operational_evidence.py` enforces that managed
import evidence can be claimed while runtime production readiness remains
blocked until live smoke and tenant policy evidence exists.

`scripts/validate_power_platform_service_boundary_endpoint.py` validates a
supplied HTTPS endpoint configuration or probes a provided real endpoint
without inventing one in source control.

`scripts/validate_power_platform_github_live_gate.py` enforces that the official
GitHub live-gate evidence keeps the required secrets, workflow run URL,
`who-am-i`, solution checker, and managed artifact hash fields explicit while
the gate remains blocked.

`scripts/validate_power_platform_platform_tests.py` enforces that platform tests
and visual optimization are not overclaimed before real app/flow evidence
exists.
