# PAC Operator Package Runbook

Purpose: provide a conservative operator path for PAC re-auth, app publication
evidence, and custom connector connection binding.

This runbook is intentionally blocked-state only. It packages evidence and
captures blockers, but it does not claim that a live app or connector binding
exists.

## Package contents

- `power-platform/evidence/pac-operator-package-20260521.json`
- `power-platform/evidence/pac-observation-capture-20260521.json`
- `power-platform/evidence/canvas-app-publication-20260520.json`
- `power-platform/evidence/connection-reference-evidence-template.json`

## Current state

- PAC re-auth is not yet re-captured in a fresh operator session.
- App publication evidence exists, but this package does not claim a new live
  publication event.
- Custom connector connection binding remains blocked until a real
  `connectionId` is observed.
- The current PAC blocker evidence is machine-checkable and remains blocked
  until `appId`, `playUrl`, and `connectionId` are all present.

## Runbook

### 1. Re-authenticate PAC

- Use `pac auth create` in the intended tenant/environment context.
- Confirm the authenticated context matches the tenant and environment recorded
  in the PAC evidence files.
- Do not treat successful login as proof of app publication or connector
  binding.

### 2. Keep app publication evidence explicit

- Use `power-platform/evidence/canvas-app-publication-20260520.json` as the
  publication evidence record.
- Verify the app ID and play URL in that record remain the published values.
- Do not restate production readiness from publication evidence alone.

### 3. Capture custom connector connection binding

- Observe the custom connector connection ID from PAC.
- Keep `power-platform/evidence/connection-reference-evidence-template.json`
  blocked until the connection ID and environment binding are known.
- Record the observed connection ID in the PAC blocker capture before any claim
  change.

### 4. Refresh the blocker capture

- Run `scripts/capture_power_platform_pac_observations.py`.
- If any of `appId`, `playUrl`, or `connectionId` is missing, the capture stays
  blocked.
- Only update `power-platform/evidence/pac-operator-package-20260521.json`
  after the capture is complete.

## Hard stops

Stop immediately and keep the surface blocked if any of these are true:

- `appId` is missing.
- `playUrl` is missing.
- `connectionId` is missing.
- A live connection or app claim would need to be inferred instead of observed.
- Production readiness would need to be asserted from this package alone.

## Machine-checkable blocker rule

```json
{
  "status": "blocked_pending_required_pac_observations",
  "requiredEvidence": ["appId", "playUrl", "connectionId"],
  "claimBoundary": {
    "appPublished": false,
    "connectionConfigured": false,
    "productionReadinessClaimed": false
  }
}
```

## No-claim rule

Do not claim app publication, connector connection binding, or production
readiness from this runbook alone.
