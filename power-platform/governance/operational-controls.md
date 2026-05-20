# Power Platform Operational Controls

## Monitoring

- Monitor connector call failures.
- Monitor flow run failures.
- Monitor service boundary `/healthz`.
- Record correlation IDs for support without storing patient-level data.
- Capture Power Apps health metrics for app launch and synthetic submission.
- Capture Power Automate run IDs for validation, calculation, deployment smoke,
  and evidence export flows.
- Store sanitized payload hashes only; do not store patient-level payloads.
- Correlation IDs must be retained with flow/component name, flow ID, and run ID.

## Privacy and DLP

- Source-controlled examples are synthetic only.
- DLP policy must permit the custom connector and target environment before
  import.
- Secrets are stored only in Power Platform connection references or approved
  deployment secret stores.
- Evidence must include the DLP policy name or ID before runtime readiness is
  claimed.

## Support

Escalation requires solution version, environment, connector operation,
correlation ID, and sanitized diagnostic payload.

## Evidence Contracts

- Connection reference evidence:
  `power-platform/evidence/connection-reference-evidence-template.json`.
- Runtime smoke evidence:
  `power-platform/evidence/runtime-smoke-evidence-template.json`.
- Monitoring and DLP evidence:
  `power-platform/evidence/monitoring-dlp-evidence-template.json`.
- Real flow smoke evidence:
  `power-platform/evidence/flow-smoke-evidence-template.json`.
- Official GitHub Actions live-gate evidence:
  `power-platform/evidence/official-github-live-gate-evidence-template.json`.
- Standalone subrepo closure evidence:
  `power-platform/repository/standalone-subrepo-remote-or-waiver-closure-template.json`.
