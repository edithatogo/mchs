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

- Azure CLI user: `Dylan.Mordaunt@health.nsw.gov.au`
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
