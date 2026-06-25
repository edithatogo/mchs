# CI and Build Notes: Pricing-Year Diff Tooling

Keep CI conservative and review-driven. The diff tool is a comparison surface,
not an optimistic support claim.

## Current stance

- Use `funding-calculator diff-year <from-year> <to-year>` as the named diff
  command for this track.
- Validate manifest compatibility, comparison stability, and output shape on
  every diff-related change.
- Treat missing manifests or non-deterministic ordering as hard failures.
- Keep release-note wording aligned with recorded diff outputs.

## Suggested CI checks

- Verify markdown and JSON fixtures stay in sync.
- Fail when the command omits changed-key summaries for large tables.
- Fail when comparison output includes unstable ordering or raw dumps that
  exceed the agreed summary budget.
- Confirm the completion notes continue to reference the concrete evidence
  surfaces from this track.

## Review expectations

- Review any change in wording around supported years or status transitions.
- Confirm the command name stays on
  `funding-calculator diff-year <from-year> <to-year>`.
- Keep source-data changes and implementation changes clearly separated in
  docs and fixtures.
