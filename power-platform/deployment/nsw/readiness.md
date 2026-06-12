# NSW Power Platform Deployment Readiness

## Status

Authenticated to NSW tenant and target `dylan` environment; deployment remains blocked pending managed solution pack/import, solution checker output, connection-reference configuration, and app/flow smoke evidence.

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


## Authenticated Target Evidence

- Azure CLI user: `<redacted-nsw-operator-email>`
- Tenant: `NSW Health Department` (`a687a7bf-02db-43df-bcbb-e7a8bda611a2`)
- PAC profile: `nsw-dylan`
- Environment: `Dylan Mordaunt (Illawarra Shoalhaven LHD)'s Environment`
- Environment ID: `611bca65-0b2a-eaa1-9e74-23bbba8eeec4`
- Environment URL: `https://orgefc9aa3e.crm6.dynamics.com/`
- Unique name: `unq8b153003d5eaf01189f5002248942`

## Tooling Note

The default `pac` wrapper at `/Users/doughnut/.local/pac-cli/pac` crashes in
MSAL broker initialization on this machine. Use the stable PAC shim first in
`PATH` for deployment work:

```bash
PATH="/tmp/mchs-tools:$PATH" ./scripts/bootstrap-power-platform-alm.sh --check-auth
```

Authentication and command-surface checks pass with that shim.


## Managed Import Evidence - 2026-05-20

- Managed solution import: complete.
- Solution unique name: `mchs_alm_orchestration`.
- Version: `0.2.2.0`.
- Managed: `True`.
- Solution Checker correlation ID: `a797a828-b297-420d-8372-686ce60de571`.
- Solution Checker findings: critical `0`, high `0`, medium `0`, low `0`, informational `0`.
- Managed artifact SHA-256: `50bbe04a5b27907409c231f620d65b95867fbcb65912e9282d3b09c168528efa`.
- Import verification: `pac solution list` shows `mchs_alm_orchestration` version `0.2.2.0` as managed in `dylan`.

## Remaining Runtime Smoke Boundary

Do not claim app or flow runtime readiness yet. The imported package establishes
the managed ALM solution shell and evidence chain. Runtime app/flow smoke remains
pending until real app/flow components are imported, connection references are
configured, and the production service boundary endpoint is reachable.

## Current Audit - 2026-06-12

- Local `pac auth list` still shows active profile `nsw-dylan` for the target
  NSW `dylan` environment at `https://orgefc9aa3e.crm6.dynamics.com/`.
- GitHub repository secret audit currently shows only `NUGET_API_KEY`; the
  official Power Platform live-gate secrets `POWER_PLATFORM_ENVIRONMENT_URL`,
  `POWER_PLATFORM_APPLICATION_ID`, `POWER_PLATFORM_CLIENT_SECRET`, and
  `POWER_PLATFORM_TENANT_ID` are not configured.
- Runtime smoke remains blocked until the custom connector connection, service
  boundary endpoint, app/flow smoke runs, DLP policy mapping, monitoring export,
  and live-gate secrets are captured.
