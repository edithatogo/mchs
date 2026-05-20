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
- `canvas-app-publication-20260520.json`: publication blocker record that keeps
  app ID and play URL evidence machine-checkable without claiming production
  readiness.
- `pac-operator-package-20260521.json`: blocked operator package manifest for
  PAC re-auth, app publication evidence, and custom connector connection
  binding. It points at the current PAC blocker capture and does not claim a
  live app or connection.
- `scripts/capture_power_platform_pac_observations.py`: capture helper for
  current PAC observations. It writes `pac-observation-capture-<as-of>.json`
  and stays blocked until `appId`, `playUrl`, and `connectionId` are all
  present.
- `pac-observation-capture-20260521.json`: current machine-checkable PAC
  blocker capture. It remains blocked until `appId`, `playUrl`, and
  `connectionId` are observed.
- `deployment/pac-operator-runbook.md`: operator runbook for PAC re-auth,
  app publication evidence, and custom connector connection binding.
- `service-boundary-endpoint-template.json`: blocked endpoint configuration and
  probe contract for a real HTTPS service boundary once provided, including a
  machine-checkable handoff with the required base URL input and probe paths.
- `examples/service-boundary-endpoint-operator-input.example.json`: operator
  input sample showing the fields to populate before creating a live probe
  config.
- `examples/service-boundary-probe-result.example.json`: sample probe payload
  shape for the updater when you want a dry-run package without claiming a live
  endpoint.
- `docs/runbooks/service-boundary-public-endpoint-operator-package.md`: the
  operator package/runbook with exact command sequence for building a real
  public HTTPS service-boundary endpoint and collecting probe evidence.
- `scripts/update_power_platform_service_boundary_endpoint_evidence.py`:
  evidence renderer that accepts a real HTTPS base URL plus a probe-result JSON
  file and emits an updated record while keeping `productionReadinessClaimed`
  false.
- `flow-smoke-evidence-template.json`: structured real Power Automate flow smoke
  traceability and blocked checklist while live run evidence is absent. Use
  `scripts/update_power_platform_flow_smoke_evidence.py` with a capture JSON
  containing `flowRuns` or `realNswRunEvidence` entries to materialize a real
  evidence file only when every flow includes `flowId`, `runId`, `runStatus`,
  and `runUrl`. The script writes to
  `power-platform/evidence/power-automate-flow-smoke-20260521.json` by
  default.
- `flow-smoke-capture-runbook.md`: operator-facing capture runbook for
  collecting Power Automate flow run metadata, checking the required fields,
  and converting a completed capture into evidence without claiming a live
  run from placeholders.
- `flow-smoke-capture-sample.json`: placeholder capture package that shows the
  expected `flowRuns` shape with null fields and reminder text. It is not a
  live capture and will stay blocked until operators replace every placeholder
  with real run metadata.
- `connection-reference-evidence-template.json`: connection reference and
  environment-variable deployment value evidence shape, including the blocked
  service-boundary endpoint handoff, the connector connection ID placeholder,
  the environment binding, and the PAC observation requirements.
- `monitoring-dlp-evidence-template.json`: monitoring, DLP, support, and
  escalation evidence shape. Use
  `scripts/update_power_platform_monitoring_dlp_evidence.py` to merge supplied
  policy and monitoring fields into the blocked evidence record without
  claiming readiness early.
- `monitoring-dlp-operator-runbook.md`: operator runbook for collecting the
  monitoring, DLP, connector policy, and support capture inputs from a real
  admin environment.
- `monitoring-dlp-capture-sample.json`: placeholder-only capture input with the
  exact required fields expected by the monitoring/DLP updater. It is a sample
  shape, not evidence that any admin export has already been obtained.
- `official-github-live-gate-evidence-template.json`: official GitHub Actions live-gate
  evidence shape for environment-bound validation.
- `scripts/bootstrap-power-platform-github-live-gate.sh`: non-destructive bootstrap
  path that checks required repository secrets, prints exact `gh secret set`
  commands with placeholders, and only dispatches the workflow after the
  secrets exist.
- `scripts/bootstrap-power-platform-github-live-gate.md`: companion runbook for
  the live-gate bootstrap path.
- `github-live-gate-20260521.json`: current blocked live-gate record with
  structured secret, workflow dispatch, run URL, who-am-i, solution checker, and
  artifact-hash placeholders preserved.
- `power-platform/repository/standalone-subrepo-remote-or-waiver-closure-template.json`:
  standalone subrepo split decision and waiver closure checklist.
- `standalone-subrepo-remote-input-template.json`: sample input values for the
  standalone remote closure path.
- `explicit-waiver-input-template.json`: sample input values for the explicit
  waiver closure path.
- `scripts/bootstrap-power-platform-subrepo-closure.md`: operator runbook for
  the subrepo closure writer and the two closure paths.
- `platform-test-status.json`: live platform-test status, including the fact
  that the Power App has not yet been viewed, smoke-tested, or visually
  optimized in the tenant.

`scripts/validate_power_platform_operational_evidence.py` enforces that managed
import evidence can be claimed while runtime production readiness remains
blocked until live smoke and tenant policy evidence exists. The monitoring/DLP
updater keeps the evidence record blocked until every required field is
present, then writes the completed capture without lifting the claim boundary.

`scripts/validate_power_platform_service_boundary_endpoint.py` validates a
supplied HTTPS endpoint configuration or probes a provided real endpoint
without inventing one in source control.

When a real URL exists, use the validator to capture probe output and the
renderer to create a derived evidence record. The example files in
`power-platform/evidence/examples/` show the required JSON shapes, but they do
not claim that a live endpoint exists:

```bash
REAL_BASE_URL='https://your-real-public-host.example'

jq --arg url "$REAL_BASE_URL" \
  '.serviceBoundary.httpsBaseUrl = $url | .serviceBoundary.apiKeySecretConfigured = true' \
  power-platform/evidence/service-boundary-endpoint-template.json \
  > /tmp/mchs-service-boundary-config.json

python3 scripts/validate_power_platform_service_boundary_endpoint.py \
  --config /tmp/mchs-service-boundary-config.json \
  --probe > /tmp/mchs-service-boundary-probe.json

python3 scripts/update_power_platform_service_boundary_endpoint_evidence.py \
  --https-base-url "$REAL_BASE_URL" \
  --probe-result /tmp/mchs-service-boundary-probe.json \
  --output /tmp/mchs-service-boundary-evidence.json

python3 scripts/update_power_platform_service_boundary_endpoint_evidence.py \
  --https-base-url 'https://service-boundary.example' \
  --probe-result power-platform/evidence/examples/service-boundary-probe-result.example.json \
  --output /tmp/mchs-service-boundary-evidence-preview.json
```

The checked-in template stays blocked; only the generated artifact reflects the
supplied URL and probe result.

`scripts/validate_power_platform_github_live_gate.py` enforces that the official
GitHub live-gate evidence keeps the required secrets, workflow run URL,
`who-am-i`, solution checker, and managed artifact hash fields explicit while
the gate remains blocked.

`scripts/bootstrap-power-platform-github-live-gate.sh` is the operator-facing
path for secret verification and gated dispatch before any live evidence is
claimed.

`scripts/validate_power_platform_platform_tests.py` enforces that platform tests
and visual optimization are not overclaimed before real app/flow evidence
exists.
