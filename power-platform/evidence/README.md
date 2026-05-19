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
- `connection-reference-evidence-template.json`: connection reference and
  environment-variable deployment value evidence shape.
- `monitoring-dlp-evidence-template.json`: monitoring, DLP, support, and
  escalation evidence shape.
- `platform-test-status.json`: live platform-test status, including the fact
  that the Power App has not yet been viewed, smoke-tested, or visually
  optimized in the tenant.

`scripts/validate_power_platform_operational_evidence.py` enforces that managed
import evidence can be claimed while runtime production readiness remains
blocked until live smoke and tenant policy evidence exists.

`scripts/validate_power_platform_platform_tests.py` enforces that platform tests
and visual optimization are not overclaimed before real app/flow evidence
exists.
