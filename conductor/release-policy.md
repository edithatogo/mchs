# Release Policy

## Purpose

Release artifacts must be reproducible, auditable, and resistant to accidental
calculator behavior drift.

Conformance is bounded: every release claim is scoped to an explicit support
boundary (calculator, year, runtime, parity surface, and validation mode). A
release does not imply exhaustive proof across unsampled runtimes, implementations,
or external business outcomes.

## Release Types

- **Code release**: package code and helper logic.
- **Data bundle release**: bundled reference data, manifests, and checksums.
- **Validation-status release**: a change in parity, fixture, or validation
  status without a code change.

## Required Metadata

Every release should identify:

- Boundaries and explicit gaps for unvalidated runtimes, integrations, and
  business outcomes.
- Scope declaration (`calculator`, `year`, `runtime`, `parity surface`,
  `fixture cohort`, and supported deployment mode).
- Package version.
- Calculator data bundle version.
- Validation status.
- Source checksum set.
- Lockfile revision used for the build.
- Evidence-backed parity records for the release claim within the declared scope.
- For Rust artifacts, crate version, workspace lockfile revision, and binding package version.
- For browser artifacts, the build hash or package version for the generated
  fixture/demo bundle.

## Supply-Chain Controls

- Release workflows should run from a locked environment.
- Source artifact checksums must be verified before extraction or validation.
- SBOM generation should be available for published artifacts.
- Signed artifacts should be used where the distribution channel supports them.
- Rust releases should evaluate `cargo audit`, `cargo deny`, SBOM generation,
  signing, and attestations before the release claim expands.
- Renovate updates that touch calculator-impacting dependencies require review
  against the validation surface.
- GitHub Actions must pass before any push, merge, or release claim is made for
  the affected branch or tag.

## Calculator Migration Policy

Calculator migration should remain calculator-by-calculator rather than
wide-bang.

- Rust promotion requires golden fixture parity and explicit validation status.
- Python remains the default runtime path until a calculator-specific
  promotion record exists.
- Promotion records should name the calculator, pricing year, parity type,
  fixture set, tolerance, reviewer, declared scope, and any known gaps.
- Canary runs, parity evidence, performance measurements, rollback guidance,
  and release-note requirements should be recorded before any Rust-backed path
  becomes default.

## Reviewer Rule

Do not merge a release that broadens a validation claim without a matching
manifest, fixture, or registry record that names the calculator, year, parity
type, fixture set, tolerance, reviewer, and declared scope. Any intentionally
untested runtime path or business outcome must be listed as an explicit gap.
