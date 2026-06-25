# Review: Rust crates.io Registry Submission

## Status

Reviewed on 2026-06-25. Archive eligible as a published-verified registry
track.

## Scope Reviewed

- crates.io API exposes `nwau-core 0.1.0` with checksum
  `c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547`.
- Track metadata records publish workflow, duplicate-publish confirmation,
  public URL/API evidence, yanked state, and credential cleanup.
- Tests cover track metadata and contract registry evidence.

## Findings

- The crate version is public and not yanked.
- Credential cleanup is recorded.
- Rust GA across all calculator streams is not claimed by this registry track.

## Validation

- `python` crates.io API probe with explicit registry-probe user agent
- `uv run pytest tests/test_rust_crates_io_registry_submission_track.py`
- `python scripts/validate_language_registry_submission_tracks.py`
- `python conductor/scripts/stub_detector.py --root . --json`
