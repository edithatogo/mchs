# CI and Build Notes: IHACPA Source Scanner

Keep CI non-network and review-first. The scanner is a discovery tool, not a
validation claim generator.

## Current stance

- Do not require live IHACPA access in CI.
- Use checked-in fixtures or synthetic HTML for parser coverage.
- Treat scan output as draft material until a human reviews the source
  categories and gap records.
- Avoid any documentation or test language that implies parity, completeness,
  or release readiness from discovery alone.

## Required CI coverage

- Parser behavior against saved source fixtures.
- Unchanged-source detection when the same source set is scanned twice.
- Gap-record creation for missing, inaccessible, or restricted artifacts.
- No accidental network calls in the required test path.

## Review expectations

- Review the scan diff before committing manifest updates.
- Confirm that licensed or non-redistributable material is represented by
  policy notes or gap records, not copied files.
- Verify that the manifest uses conservative wording for discovery-only
  outcomes.

## Future gate shape

The required gate should remain deterministic and offline. If a future workflow
adds a live scan job, keep it separate from required CI and label it as
informational only.
