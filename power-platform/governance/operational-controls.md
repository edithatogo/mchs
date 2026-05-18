# Power Platform Operational Controls

## Monitoring

- Monitor connector call failures.
- Monitor flow run failures.
- Monitor service boundary `/healthz`.
- Record correlation IDs for support without storing patient-level data.

## Privacy and DLP

- Source-controlled examples are synthetic only.
- DLP policy must permit the custom connector and target environment before
  import.
- Secrets are stored only in Power Platform connection references or approved
  deployment secret stores.

## Support

Escalation requires solution version, environment, connector operation,
correlation ID, and sanitized diagnostic payload.
