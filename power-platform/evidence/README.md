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
  present. Placeholder-looking values and mismatched app/play URL pairs are
  also blocked.
- `pac-observation-capture-20260521.json`: current machine-checkable PAC
  blocker capture. It remains blocked until `appId`, `playUrl`, and
  `connectionId` are observed.
- `power-platform/deployment/pac-operator-runbook.md`: operator runbook for PAC re-auth,
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
- `scripts/preflight_power_platform_service_boundary_endpoint_operator_package.py`:
  offline gate that validates the operator input and probe JSON artifacts and
  stays blocked on placeholder hosts or example-only probe text.
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
  path that first validates the sanitized operator-inputs env file for
  placeholder values, then checks required repository secrets, prints exact
  `gh secret set` commands with placeholders, and only dispatches the workflow
  after the inputs and secrets exist.
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
- `live-tenant-browser-sweep-20260524.json`: authenticated Playwright browser
  sweep of the NSW Health Department default environment. It records that the
  selected tenant session returned zero editable classic canvas apps, visible
  connected generic connections but no MCHS service-boundary connection, and no
  usable MCHS flow/custom connector inventory. This is blocker evidence only;
  it does not claim runtime readiness.

## Evidence import mapping

The tables below map each capture script argument or input file to the exact
checked-in value used by this repository. Do not replace blocked or secret
values with guesses. Secret bodies are intentionally omitted.

### GitHub live gate

| Script or file | Exact value |
| --- | --- |
| `scripts/bootstrap-power-platform-github-live-gate.sh` | Dispatches `.github/workflows/power-platform-official-actions.yml` as `Power Platform Official Actions` with `run_live_checks=true`. |
| `docs/runbooks/github-live-gate.env` | `LIVE_GATE_WORKFLOW=publish.yml`, `LIVE_GATE_TAG=v0.0.0`, `NSW_OPERATOR_NAME=NSW operator name`, `NSW_OPERATOR_EMAIL=operator@example.nsw.gov.au`, `NSW_APPROVER_NAME=NSW approver name`, `NSW_APPROVER_EMAIL=approver@example.nsw.gov.au`, `NSW_RELEASE_REASON=Manual live-gate dispatch for GitHub release or registry publication`, `NSW_RELEASE_NOTES=Document the evidence bundle, dispatch time, and approval reference here`, `GITHUB_TOKEN=provided_by_github_actions`, `GH_TOKEN=provided_by_github_actions`. |
| Repository secrets | `POWER_PLATFORM_ENVIRONMENT_URL`, `POWER_PLATFORM_APPLICATION_ID`, `POWER_PLATFORM_CLIENT_SECRET`, `POWER_PLATFORM_TENANT_ID`. The secret bodies are not documented here. |
| Real non-secret environment value | `POWER_PLATFORM_ENVIRONMENT_URL=https://orgefc9aa3e.crm6.dynamics.com/`. |
| Real tenant value | `POWER_PLATFORM_TENANT_ID=a687a7bf-02db-43df-bcbb-e7a8bda611a2`. |

### PAC app and connection capture

| Script or file | Exact value |
| --- | --- |
| `scripts/capture_power_platform_pac_observations.py` | Capture `appId`, `playUrl`, and `connectionId` from the live tenant. |
| `power-platform/evidence/canvas-app-publication-20260520.json` | Published app values: `appId=ff64f58a-73de-42ee-b92d-f65503619c49`, `playUrl=https://apps.powerapps.com/play/e/611bca65-0b2a-eaa1-9e74-23bbba8eeec4/a/ff64f58a-73de-42ee-b92d-f65503619c49?tenantId=a687a7bf-02db-43df-bcbb-e7a8bda611a2`. Optimized publication values: `optimizedPublication.appId=669d0089-8abe-4e94-ab50-aa69513a6cc4`, `optimizedPublication.playUrl=https://apps.powerapps.com/play/e/611bca65-0b2a-eaa1-9e74-23bbba8eeec4/a/669d0089-8abe-4e94-ab50-aa69513a6cc4?tenantId=a687a7bf-02db-43df-bcbb-e7a8bda611a2`. |
| `power-platform/evidence/connection-reference-evidence-template.json` | `logicalName=mchs_service_boundary`, `connector=mchs-service-boundary`, `connectorId=0f3d6edc-9653-f111-bec6-00224893a0e1`, `baseUrlEnvironmentVariable=mchs_api_base_url`, `apiKeySecretName=mchs_service_boundary_api_key`, `valueStatus=missing`, `pacObservedConnections.customConnectorConnectionId=null`. |
| Current PAC state | `connectionId` is still blocked pending a real observed connection. |

### Public HTTPS endpoint capture

| Script or file | Exact value |
| --- | --- |
| `docs/runbooks/service-boundary-public-endpoint-operator-package.md` | Uses `REAL_BASE_URL` only after a live HTTPS endpoint exists. |
| `power-platform/evidence/service-boundary-endpoint-template.json` | `logicalConnectionReference=mchs_service_boundary`, `baseUrlEnvironmentVariable=mchs_api_base_url`, `healthzPath=/healthz`, `serverCardPath=/.well-known/mcp/server-card.json`, `expectedScheme=https`, `httpsBaseUrl=null`, `apiKeySecretConfigured=false`, `publiclyReachableFromPowerPlatform=false`, `tlsTrusted=false`. |
| `power-platform/deployment/nsw/readiness.md` | Target environment details: `Environment ID=611bca65-0b2a-eaa1-9e74-23bbba8eeec4`, `Environment URL=https://orgefc9aa3e.crm6.dynamics.com/`, `PAC profile=nsw-dylan`. |
| Current endpoint state | No real public HTTPS service-boundary base URL is recorded yet. |

### Flow-smoke capture

| Flow | Exact value |
| --- | --- |
| `mchs-validate-input` | `flowFile=power-platform/flows/validate-input/flow.json`, `operation=ValidateInput`, `connectionReference=mchs_service_boundary`, `connectionReferenceId=0f3d6edc-9653-f111-bec6-00224893a0e1`, `flowId=null`, `runId=null`, `runStatus=null`, `runUrl=null`. |
| `mchs-calculate-request` | `flowFile=power-platform/flows/calculate-request/flow.json`, `operation=Calculate`, `connectionReference=mchs_service_boundary`, `connectionReferenceId=0f3d6edc-9653-f111-bec6-00224893a0e1`, `flowId=null`, `runId=null`, `runStatus=null`, `runUrl=null`. |
| `mchs-evidence-export` | `flowFile=power-platform/flows/evidence-export/flow.json`, `operation=GetEvidence`, `connectionReference=mchs_service_boundary`, `connectionReferenceId=0f3d6edc-9653-f111-bec6-00224893a0e1`, `flowId=null`, `runId=null`, `runStatus=null`, `runUrl=null`. |
| `mchs-deployment-smoke` | `flowFile=power-platform/flows/deployment-smoke/flow.json`, `operation=Health`, `connectionReference=mchs_service_boundary`, `connectionReferenceId=0f3d6edc-9653-f111-bec6-00224893a0e1`, `flowId=null`, `runId=null`, `runStatus=null`, `runUrl=null`. |
| `power-platform/evidence/flow-smoke-capture-sample.json` | `status=template_placeholder_only`, `captureType=power_automate_flow_smoke_capture`, `realNswRunEvidence=null`. |
| Current flow-smoke state | The capture is still blocked until each run has a real `flowId`, `runId`, `runStatus`, and `runUrl`. |

### DLP and monitoring capture

| Script or file | Exact value |
| --- | --- |
| `scripts/update_power_platform_monitoring_dlp_evidence.py` | Consumes the monitoring, DLP, connector policy, and support capture input. |
| `power-platform/evidence/monitoring-dlp-capture-sample.json` | `monitoring.owner=TBD`, all monitoring failure metrics are required, `dlp.policyId=TBD`, `dlp.policyName=TBD`, `dlp.policyClassification=TBD`, `dlp.policyCaptureState=blocked_pending_policy_capture`, `connectorPolicy.connectorName=mchs-service-boundary`, `connectorPolicy.connectorId=0f3d6edc-9653-f111-bec6-00224893a0e1`, `connectorPolicy.policyId=TBD`, `connectorPolicy.policyName=TBD`, `connectorPolicy.connectorAllowState=blocked_pending_policy_capture`, `support.owner=TBD`, `support.escalationOwner=TBD`, `support.escalationPath=TBD`, `support.escalationContact=TBD`. |
| `power-platform/evidence/dlp-monitoring-policy-evidence-20260521.json` | `tenantName=NSW Health Department`, `status=blocked_pending_nsw_admin_policy_capture`, `claimBoundary.dlpCompatible=false`, `claimBoundary.monitoringOperational=false`, `claimBoundary.productionReadinessClaimed=false`. |
| Current DLP state | No real DLP policy or monitoring export is recorded yet. |

### Subrepo closure capture

| Script or file | Exact value |
| --- | --- |
| `scripts/write_power_platform_subrepo_closure.py` | Writes the blocked default record, the standalone remote record, or the explicit waiver record. |
| `power-platform/repository/subrepo-closure-20260521.json` | `status=blocked_pending_remote_or_explicit_waiver`, `claimBoundary.standaloneRemoteProvisioned=false`, `claimBoundary.explicitWaiverRecorded=false`, `claimBoundary.subrepoClosureComplete=false`, `standaloneRemote.provisioned=false`, `standaloneRemote.remoteUrl=null`, `standaloneRemote.defaultBranch=null`, `standaloneRemote.syncProcedure=null`, `standaloneRemote.importOwner=null`, `explicitWaiver=null`. |
| `power-platform/evidence/standalone-subrepo-remote-input-template.json` | `asOf=2026-05-21`, `remoteUrl=https://github.com/example/power-platform-subrepo.git`, `defaultBranch=main`, `syncProcedure=git pull --ff-only; git push --follow-tags`, `importOwner=NSW import owner`. |
| `power-platform/evidence/explicit-waiver-input-template.json` | `asOf=2026-05-21`, `approvedBy=NSW platform governance`, `approvalRecord=GOV-2026-05-21-001`, `reason=Standalone remote is deferred pending repository split approval.`, `reviewDate=2026-05-21`, `riskAcceptance=Accepted by product owner for the governed boundary.` |
| Current closure state | The repository is still blocked pending either a real standalone remote or a real explicit waiver record. |

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

`scripts/preflight_power_platform_readiness.py` runs the blocked endpoint,
GitHub, PAC, flow-smoke, DLP, and subrepo checks together and prints one JSON
summary. It is a reporting wrapper only and does not mutate the checked-in
evidence files. Each check is expected to carry both a short `help` hint and a
concrete `nextAction` so blocked output stays actionable.

Aggregate preflight check handoffs:

| Check | help | nextAction |
| --- | --- | --- |
| `endpoint` | Run the endpoint validator on a real public HTTPS base URL. | Provide a real public HTTPS base URL, publish the `healthz` and server-card routes, then rerun `scripts/validate_power_platform_service_boundary_endpoint.py` with `--probe`. |
| `github` | Verify repository secrets and the live GitHub Actions gate. | Configure the required repository secrets, dispatch the workflow run, and rerun the GitHub live-gate bootstrap path. |
| `pac` | Capture real PAC app, play URL, and connection observations. | Run PAC auth and recapture real `appId`, `playUrl`, and `connectionId` values before changing any claim state. |
| `flow_smoke` | Capture real flow run evidence for every logical flow. | Provide real `flowId`, `runId`, `runStatus`, and HTTPS `runUrl` values for every flow logical name, then rerun the flow-smoke updater. |
| `dlp` | Capture the monitoring, DLP, connector policy, and support fields. | Supply real monitoring and DLP evidence fields, then rerun the monitoring/DLP updater preflight. |
| `subrepo` | Choose the governed subrepo closure path. | Supply either a standalone remote or an explicit waiver record, then rerun the subrepo closure writer. |

`scripts/render_power_platform_readiness_checklist.py` turns that aggregate
JSON into a concise Markdown operator checklist with one section per blocked
check. The output is task-oriented only; it does not claim readiness or change
the underlying evidence.

## Remaining blocker identifiers

The current `remaining-blockers-20260521.json` evidence file uses the following
machine-readable blocker IDs, and each one is represented in this evidence
surface or the adjacent runbooks:

- `service_boundary_production_endpoint_and_connection_reference_values`
- `real_power_automate_flow_component_smoke_evidence`
- `production_service_boundary_execution_evidence`
- `power_app_operation_pages_are_source_ux_complete_but_not_live_runtime_proven`
