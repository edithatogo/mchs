# Power Platform Governance for NSW Readiness

This is the governance companion for Power Platform deployment planning around NSW
jurisdictions.

## Core governance posture

- Formula logic remains outside Power Platform app/flow layers.
- Managed solutions are the only promotion target for downstream environments.
- Credential-dependent actions require explicit approval evidence.
- Environment-specific values are injected at deploy time.

## Evidence principle

- Treat all NSW environment claims as operational evidence claims, not architectural
  promises.
- If tenant credentials are unavailable, all external claims remain `blocked`.
- Evidence bundles must include blockers before release posture changes.

## Explicit blockers policy

1. Tenant service principal missing
2. Tenant client secret / secret reference missing
3. Environment IDs missing
4. Health-check endpoint unverified
5. Solution checker or import logs unavailable

Any unresolved item in this list blocks managed promotion regardless of artifact
readiness.

## Release posture

- `blocked`: default posture until all blockers are cleared.
- `release_candidate`: blocked list is empty and smoke checks pass in dev/test.
- `ga`: blocked list is empty for all target environments and evidence is audited.

## Governance checks to perform before removing blockers

- Reconcile deployment runbook steps with evidence bundle IDs.
- Verify no hard-coded tenant secrets are in source control.
- Verify managed artifact checksums are immutable and reproducible.
- Verify rollback is executable and logged.

## Status statement

This governance document does not imply any real NSW deployment has occurred.

## Machine-readable blocker identifiers

Do not claim NSW deployment, managed promotion, or production readiness while any
of these blocker identifiers remain unresolved:

- `tenant_client_secret_missing`
- `tenant_service_principal_missing`
- `tenant_environment_id_unknown`
- `tenant_connectivity_unverified`
