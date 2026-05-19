# MCHS Service Boundary Custom Connector Artifacts

This directory contains the source connector definitions consumed by Power Platform
for orchestration of calculator workflows.

- `apiDefinition.swagger.json`: OpenAPI 3.0 contract for the connector surface.
- `apiDefinition.swagger2.json`: Swagger 2.0 deployment artifact for
  `pac connector create`, because the current Power Platform custom connector
  import path rejects OpenAPI 3 definitions.
- `apiProperties.json`: Connector metadata and connection-parameter declarations.

Deployment policy:

- The connector must call only the secured service boundary at runtime-provided base
  URL.
- API key should be populated from an environment variable in the target Power
  Platform environment.
- App, flow, and table artifacts must not contain calculator formulas.

Suggested environment variables:

- `mchs_service_boundary_url` -> service base URL
- `mchs_service_boundary_api_key` -> deployment-managed key
