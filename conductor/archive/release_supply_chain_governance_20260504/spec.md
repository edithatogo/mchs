# Specification: Release and Supply-Chain Governance

## Goal

Make releases reproducible, auditable, and resistant to accidental calculator behavior drift.

## Requirements

- This track is sequenced after the Python Tooling and CI Modernization track and should consume its lockfile, CI, and validation outputs.
- Release artifacts should include package version, calculator data bundle version, validation status, source checksums, and the lockfile revision used to build them.
- Validation claims should be backed by manifest or registry records with calculator, year, parity type, fixture set, tolerance, and reviewer fields.
- Dependency updates should be reviewable and should not silently change calculator outputs.
- Release workflows should support SBOM generation, signed artifacts, pinned tool versions, and locked installs.
- CI should verify source artifact checksums before extraction or validation.

## Acceptance Criteria

- Release policy distinguishes code releases, data bundle releases, and validation-status changes.
- Supply-chain controls are documented and represented in CI or release plans.
- Renovate rules are aligned with calculator validation requirements and calculator-impacting dependency changes are gated.
