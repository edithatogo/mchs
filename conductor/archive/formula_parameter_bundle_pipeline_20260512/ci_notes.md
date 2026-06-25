# CI and Build Notes: Formula and Parameter Bundle Pipeline

## Current stance
- Require the committed acute 2025 canary bundle to load through strict models.
- Keep bundle diffs deterministic and reviewable.
- Treat source-discovered gaps as expected until the 2026 manifest and
  add-year fixture close them.
- Avoid CI language that suggests validated bundle coverage for a stream/year
  unless parity evidence exists.

## Required checks
- Validate bundle schema shape and required fields.
- Check that source-discovered gaps remain explicit and serialized.
- Fail on missing provenance, unsupported source formats, or unreadable fixture
  artifacts.
- Fail on bundle-loaded calculator behavior that diverges from golden fixtures.
- Fail if a bundle is marked validated without matching parity evidence.

## Evidence expectations
- The 2026 manifest gap records should stay aligned with bundle extraction
  scope.
- The add-year source-scanner fixture should continue to reflect the discovery
  contract.
- The downstream canary track should only reference bundle-backed behavior
  after the parity records exist.
