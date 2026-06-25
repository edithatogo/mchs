# Review: Stata SSC Submission

## Verdict

Archive-ready. The track, registry contract, runbook, and live SSC/RePEc files consistently record public installability for the `mchs` Stata package.

## Evidence Reviewed

- `contracts/language-registry-submissions/language-registry-submissions.contract.json` records `stata_ssc` as `published_verified`.
- Live SSC/RePEc probes returned `mchs.pkg`, `mchs.ado`, and `mchs.sthlp` from `http://fmwww.bc.edu/repec/bocode/m/`.
- The public package manifest lists Dylan Mordaunt support contact information, `mchs.ado`, `mchs.sthlp`, and example files.
- `bindings/stata/mchs-stata-interop-0.1.0.zip` matches the checksum recorded in the contract.

## Fixes Applied

- Added explicit support scope and an empty gap register.
- Updated README and runbook status text so they no longer claim Stata SSC is only prepared.
- Preserved the outbound-email guardrail: no SSC follow-up email or corrected archive is required or authorized by this archive step.
- Made registry archive tests resolve either live tracks or archived tracks.

## Validation

- `uv run pytest tests/test_matlab_stata_registry_archives.py tests/test_registry_submission_checklists.py -q`
- `python scripts/validate_language_registry_submission_tracks.py`
- `python conductor/scripts/stub_detector.py --root . --json`
