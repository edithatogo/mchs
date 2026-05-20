# Power Platform Monitoring, DLP, and Support Capture Runbook

Use this package to collect the exact monitoring, DLP, connector policy, and
support inputs required by
`scripts/update_power_platform_monitoring_dlp_evidence.py`.

## Safety boundary

- Do not claim real admin evidence exists unless you have an actual export or
  tenant-admin capture in hand.
- Do not replace the placeholder values in
  `monitoring-dlp-capture-sample.json` with guesses.
- Keep patient data out of the capture. The required fields are operational and
  diagnostic only.

## Package contents

- `monitoring-dlp-capture-sample.json`: placeholder-only capture input with the
  exact required fields expected by the updater.
- `monitoring-dlp-evidence-template.json`: blocked evidence template that the
  updater fills from a supplied capture object.
- `dlp-monitoring-policy-evidence-20260521.json`: checked-in blocked evidence
  record.
- `scripts/update_power_platform_monitoring_dlp_evidence.py`: fail-closed
  updater that preserves the blocked state until every required field is
  populated.

## Exact required capture fields

| JSON path | Capture expectation |
| --- | --- |
| `monitoring.owner` | Monitoring owner or group name |
| `monitoring.failureMetrics.connectorFailures` | Placeholder or actual connector-failure metric evidence |
| `monitoring.failureMetrics.flowRunFailures` | Placeholder or actual flow-run-failure metric evidence |
| `monitoring.failureMetrics.serviceBoundaryHealth` | Placeholder or actual service-boundary-health metric evidence |
| `monitoring.failureMetrics.appHealthMetrics` | Placeholder or actual app-health metric evidence |
| `monitoring.failureMetrics.correlationIdsWithoutPatientData` | Placeholder or actual sanitized-correlation evidence |
| `dlp.policyId` | Tenant DLP policy identifier |
| `dlp.policyName` | Tenant DLP policy name |
| `dlp.policyClassification` | Classification used by the tenant policy |
| `dlp.policyCaptureState` | Capture state for the supplied DLP record |
| `connectorPolicy.policyId` | Policy identifier for the connector allow/deny check |
| `connectorPolicy.policyName` | Policy name for the connector allow/deny check |
| `connectorPolicy.connectorAllowState` | Connector policy state |
| `support.owner` | Operational support owner |
| `support.escalationOwner` | Escalation owner |
| `support.escalationPath` | Escalation path |
| `support.escalationContact` | Escalation contact |

## Placeholder capture workflow

1. Open `monitoring-dlp-capture-sample.json`.
2. Replace each placeholder only with a real value from the tenant admin
   source.
3. Save the edited file outside the repository if you are working with real
   administrative evidence.
4. Run the updater with the capture file:

```bash
python3 scripts/update_power_platform_monitoring_dlp_evidence.py \
  --input /tmp/mchs-monitoring-dlp-capture.json \
  --output /tmp/mchs-monitoring-dlp-evidence.json
```

5. Inspect the updater summary.
   - If the capture still contains placeholders, the summary remains blocked
     and `complete` stays `false`.
   - If every required field is populated, the summary reports `complete:
     true`, but the checked-in evidence still must not claim production
     readiness.

## What to capture from the admin environment

- The monitoring owner and each required failure metric.
- The tenant DLP policy identifiers and classification.
- The connector policy identifiers and allow state for
  `mchs-service-boundary`.
- The support owner and escalation contacts that responders should use.

## What not to capture

- Real patient payloads.
- Secrets.
- Any statement that the tenant policy or monitoring posture has been approved
  unless you have the source export that proves it.

