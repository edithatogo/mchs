# Review: Release Workflow Validation

## Verdict

Archive-ready. The track validates checked-in release, Rust CI, coverage, and security workflow wiring; GitHub-hosted execution remains an ordinary CI runtime gate, not a reason to keep the local validation track open.

## Evidence Reviewed

- `.github/workflows/release.yml` and `.github/workflows/publish.yml` run `.github/scripts/validate_release_metadata.py`.
- `.github/workflows/release-rust.yml` generates and validates `release-evidence-bundle.json`.
- `.github/workflows/rust-ci.yml`, `.github/workflows/coverage.yml`, and `.github/workflows/security.yml` are retained as completion evidence.
- `tests/test_release_workflow_validation_track.py` validates the workflow hooks and track evidence.

## Fixes Applied

- Added explicit support scope and an empty gap register.
- Replaced generic test evidence with concrete test files.
- Added a focused workflow validation track test.

## Validation

- `uv run pytest tests/test_release_workflow_validation_track.py tests/test_strict_quality_gates_contract.py tests/test_tooling_configuration.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`
