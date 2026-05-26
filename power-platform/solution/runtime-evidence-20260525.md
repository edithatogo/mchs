# Power Platform Runtime Evidence - 2026-05-25

This note records CLI-observed runtime state for the MCHS Power Platform
orchestration surface. It is evidence of the deployed environment state, not a
claim that the runtime path is production-ready.

## Environment

- Active PAC profile: `nsw-dylan`
- User: `<authenticated_user>`
- Environment ID: `611bca65-0b2a-eaa1-9e74-23bbba8eeec4`
- Dataverse URL: `https://orgefc9aa3e.crm6.dynamics.com/`
- Organization ID: `8b153003-d5ea-f011-89f5-0022489424c0`
- Solution observed: `mchs_alm_orchestration`
- Solution version observed: `0.2.2.0`
- Solution managed state observed: managed

## Custom connector

PAC lists the custom connector:

- Connector ID: `0f3d6edc-9653-f111-bec6-00224893a0e1`
- Name: `new_mchs-20service-20boundary`
- Display name: `MCHS Service Boundary`
- Type: `CustomConnector`

`pac connector download` succeeded for the connector and produced
`apiDefinition.json` plus `apiProperties.json`.

The downloaded connector definition still points to the placeholder endpoint:

- Scheme: `https`
- Host: `example.invalid`
- Base path: `/`
- Authentication shape: API key in `x-api-key`
- Operations: `/healthz`, `/v1/calculate`, `/v1/calculators`,
  `/v1/evidence`, `/v1/schemas/{schema_name}`, `/v1/validate`

The downloaded `apiProperties.json` does not include populated connection
parameters, capabilities, brand metadata, or policy template instances.

## Connections and connection references

`pac connection list` shows generic Dataverse, OneDrive, Excel, Office 365,
SharePoint, Planner, Teams, and Office 365 Users connections for the signed-in
user. It does not show a live custom connector connection for
`MCHS Service Boundary` / `new_mchs-20service-20boundary`.

This means the repository must not claim that the deployed app has an executable
custom-connector runtime path until a real connector connection and connection
reference value are observed.

## DLP and tenant governance

`pac admin dlp-policy list` is readable and shows tenant-level DLP policy
inventory. The broad NSW Health initial policy is visible:

- Policy name: `09683835-e24c-419e-9f61-f73f083eb04b`
- Display name: `1 - NSW Health Initial Policy`
- Environment type: `ExceptEnvironments`
- Default classification: `Blocked`
- Last modified: `2026-05-21T03:53:24.7402202Z`
- Connector groups observed through `show`: `Confidential` 50,
  `General` 15, `Blocked` 1643

The exact policy-to-environment exemption and connector group placement for the
MCHS custom connector still need environment-specific confirmation before DLP
compatibility is claimed.

Tenant settings are readable through `pac admin list-tenant-settings`. Notable
settings observed include:

- Non-admin environment creation disabled.
- Developer environment creation by non-admin users disabled.
- Sharing with everyone disabled for Power Apps.
- Flow run resubmission disabled for Power Automate.
- Canvas App Insights enabled.

## Export and runtime blockers

`pac solution export --name mchs_alm_orchestration` fails because the deployed
solution is managed:

```text
Error: An error occurred while exporting a solution. Managed solutions cannot be exported.
```

The app-player/browser runtime smoke remains blocked in this automation session:

- The in-app browser backend reported unavailable.
- Chrome is installed and running.
- The Codex Chrome Extension is installed and enabled in the selected Chrome
  profile.
- The native host manifest is present and valid.
- The Chrome automation bridge still reported unavailable.

## Current claim boundary

The current Power Platform claim is limited to:

- authenticated PAC access to the target environment,
- managed solution presence,
- custom connector row presence,
- downloadable connector definition,
- tenant DLP inventory visibility,
- generic connection inventory visibility.

The current Power Platform claim does not include:

- live `mchs-service-boundary` custom connector connection,
- production or test endpoint configured in the connector,
- populated connection reference values,
- Power Automate flow IDs or run history,
- app-player runtime execution,
- DLP placement confirmation for the MCHS connector,
- monitoring or App Insights export.

## Recheck - 2026-05-26

Authenticated PAC was rechecked against environment
`611bca65-0b2a-eaa1-9e74-23bbba8eeec4`. The target environment is active and
`pac connector list` still shows custom connector
`0f3d6edc-9653-f111-bec6-00224893a0e1` / `new_mchs-20service-20boundary` /
`MCHS Service Boundary`.

This dated file is retained as the cumulative PAC runtime-evidence log for the
current blocker thread; later rechecks are appended here to keep the connector
observation history in one place.

`pac connection list` still does not show a connection for
`/providers/Microsoft.PowerApps/apis/new_mchs-20service-20boundary`; only
generic Microsoft, Dataverse, Office, SharePoint, Planner, and Teams
connections were visible.

`pac connector download` succeeded for the MCHS connector. The downloaded
`apiDefinition.json` still has `host: example.invalid`, `basePath: /`, and
`schemes: [https]`. The downloaded `apiProperties.json` did not expose populated
connection parameters.

Fresh evidence is recorded in
`power-platform/evidence/tenant-cli-observation-20260526.json`. The blocker is
unchanged: the connector shape exists, but runtime closure still requires a real
reachable HTTPS service-boundary URL, API key/custom connector connection, and
connection-reference binding before app, flow, DLP, or monitoring readiness can
be claimed.
