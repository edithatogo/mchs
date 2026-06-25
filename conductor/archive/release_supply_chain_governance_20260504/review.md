# Review: Release and Supply-Chain Governance

## Verdict

Archive-ready for local governance and control-plane scope.

## Findings

- No blocking findings remain for release policy, supply-chain controls, and local metadata validation.
- The archived scope must not be read as evidence that signed artifacts, SBOM attestations, or every registry publication gate has completed externally.

## Evidence Reviewed

- `conductor/release-policy.md` defines release types, required metadata, scoped validation claims, Rust migration policy, and reviewer rules.
- `conductor/supply-chain-controls.md` records checksum, provenance, locked install, SBOM, signing, Renovate, and GitHub Actions expectations.
- `.github/scripts/validate_release_metadata.py` validates tag version, project version, conda recipe version, and MCP registry metadata consistency.
- `.github/workflows/release.yml`, `.github/workflows/publish.yml`, and release workflow validation tests wire metadata and evidence checks into release paths.
- `tests/test_release_governance.py` validates the release policy and supply-chain control documents.

## Validation

- `uv run pytest tests/test_release_governance.py tests/test_release_workflow_validation_track.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Notes

The release metadata validator is present and workflow-wired, but tag-style validation is a release-gate check. In the current development checkout, the dynamic source version and conda recipe version are intentionally not treated as release-tag evidence. External registry publication, signed release artifacts, SBOM/provenance attestations, and CI-side audit evidence remain owned by release workflow and registry tracks.
