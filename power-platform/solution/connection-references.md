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
