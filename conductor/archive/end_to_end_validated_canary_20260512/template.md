# End-to-End Canary Template

Use this template when promoting another stream/year from source discovery to
validated lifecycle evidence.

## Required Scope

- Stream:
- Pricing year:
- Official source page:
- Source artifact paths:
- Licensing or local-only constraints:

## Required Evidence

- Source manifest with URLs, retrieval dates, hashes, and source authority.
- Formula and parameter bundle with `parity_claim` set to `false` until parity
  evidence is attached.
- Synthetic or official fixture pack with tolerance and rounding policy.
- Python baseline validation.
- Optional Rust or other engine validation against the same fixture pack.
- CLI/file validation and Arrow/Parquet bundle validation where the surface is
  claimed.
- Starlight page documenting the scope, caveats, and validation status.

## Promotion Rules

Do not claim full official parity until all of these are present:

- official SAS output parity for the selected stream/year;
- official Excel workbook output parity or a documented workbook-output
  comparison run;
- fixture parity with provenance and tolerance;
- cross-engine parity for every public surface being claimed;
- explicit licensed-classification and grouper boundary notes.

If any official parity evidence is missing, mark the track
`complete-with-gaps`, keep runtime support claims scoped to the local fixture
evidence, and record the blocking gap in `metadata.json` and the docs page.
