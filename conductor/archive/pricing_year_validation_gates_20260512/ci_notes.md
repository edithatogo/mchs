# CI and Build Notes: Pricing-Year Validation Gates

Keep CI conservative and status-driven. The gate is a validation control, not
an optimistic support claim.

## Current stance

- Use `funding-calculator validate-year <year>` as the only named validation
  command for this track.
- Validate manifest completeness, evidence references, and allowed status
  transitions on every gate-related change.
- Treat missing source, extraction, or fixture evidence as a hard failure.
- Keep support-matrix and docs wording aligned with recorded validation
  status.

## Suggested CI checks

- Verify the manifest schema and validation vocabulary load without drift.
- Fail when a pricing year is marked supported or validated without the
  required evidence references.
- Fail on unsupported or non-monotonic status transitions.
- Confirm the completion notes continue to reference the concrete evidence
  surfaces from this track.

## Review expectations

- Review any support-claim diffs before merging gate changes.
- Confirm that the validation command name stays on
  `funding-calculator validate-year <year>`.
- Keep the distinction between discovery, extraction, and validation explicit
  in commit diffs and documentation.
