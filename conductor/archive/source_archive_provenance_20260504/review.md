# Review: Source Archive and Provenance Registry

## Verdict

Archive-ready.

## Findings

- No blocking correctness or scope findings remain. The track is a provenance and acquisition-policy baseline, not a claim that every IHACPA artifact has been extracted, implemented, or validated.
- The remaining 2021-22 and 2022-23 Box-hosted SAS items are correctly retained as explicit acquisition gaps rather than being treated as completed binary downloads.

## Evidence Reviewed

- `conductor/source-archive.md` documents manifest fields, raw-binary retention rules, lifecycle axes, restore workflow, and Box-hosted gap handling.
- `scripts/archive_ihacpa_sources.py` provides the list/download acquisition workflow and writes tracked provenance outputs.
- `nwau_py/provenance.py` defines the manifest helper types, tracked manifest paths, lifecycle statuses, checksum fields, and acquisition status normalization.
- `tests/test_source_archive_manifest.py` validates manifest serialization, SHA-256 and byte-count fields, run context, source page snapshots, tracked output paths, and lifecycle axes.
- `tests/test_ihacpa_source_scanner.py` validates fixture-based IHACPA page parsing, dry-run behavior, explicit gap records, unchanged-source detection, and CLI source-scan outputs.

## Validation

- `uv run pytest tests/test_source_archive_manifest.py tests/test_ihacpa_source_scanner.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Notes

The archived scope preserves the source archive contract and acquisition workflow. Downstream tracks remain responsible for extraction completeness, calculator implementation parity, and final validation evidence.
