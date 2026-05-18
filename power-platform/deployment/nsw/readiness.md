# NSW Power Platform Deployment Readiness

## Status

Blocked pending target-environment credentials and identifiers.

## Required Inputs

- NSW tenant ID or approved tenant alias.
- Power Platform environment URL and environment ID.
- Account or service principal with solution import permissions.
- DLP policy confirmation for the custom connector.
- Service boundary base URL and authentication configuration.

## Deployment Command

```bash
./scripts/power-platform-alm.sh validate
./scripts/power-platform-alm.sh pack-managed
./scripts/power-platform-alm.sh checker
./scripts/power-platform-alm.sh import-managed
```

## Claim Boundary

Do not claim NSW deployment until this file is replaced or supplemented with
actual `pac auth list`, solution import, publish, connector connection, app
open, flow smoke, and environment-specific evidence.
