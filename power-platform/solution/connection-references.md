# Connection References

## Contract

Connection references must point to the secure service boundary used by the
Power Platform orchestration surface.

- `mchs_service_boundary`
- `mchs_solution_checker`

Canonical declaration:

- `power-platform/solution/connection-references.json`

## Rules

- Keep connection wiring declarative.
- Do not encode calculator behavior in the connection reference.
- Treat any authentication material as environment-managed configuration.
- Keep the blocker evidence explicit in
  `power-platform/evidence/connection-reference-evidence-template.json` so the
  environment binding, connector connection ID placeholder, and PAC discovery
  checks stay machine-readable while the connection remains unconfigured.
- As of the current runtime evidence, `pac connection list` does not show a
  live custom connector connection for `MCHS Service Boundary`; do not claim
  executable connector wiring until the connection and reference value are
  observed in the target environment.
