# Review: Jurisdiction Price Source Index

## Verdict

Reviewed; keep live as `complete-with-gaps`.

## Findings

1. The source-index schema and field vocabulary are described, but actual source rows are not implemented.
2. Acceptance requires public-safe or blocked rows for NSW, VIC, QLD, WA, SA, TAS, ACT, and NT; current evidence is strategy text and track artifacts.
3. The focused tests prove visibility of the roadmap and coordination evidence, not source-index completeness.

## Validation

- `uv run pytest tests/test_coordination_and_evidence_tracks.py -q`
- `python conductor/scripts/stub_detector.py --root . --json`

## Archive Blockers

- Add machine-readable source rows or blocked-source rows for each jurisdiction.
- Add tests that verify row status, provenance, source title, source URL/path, and local-only handling.
