# Review: R CRAN Registry Submission

## Verdict

Reviewed and still live. This track is not archive-ready because CRAN publication is not visible publicly and the remaining gate is external CRAN incoming/pretest, reviewer response, and package-page publication.

## Evidence Reviewed

- `R CMD build`, `R CMD check --no-manual`, package-local CRAN-style check, and live CRAN incoming metadata check are recorded as passing or expected-note-only.
- The CRAN submission was uploaded on 2026-06-12 and the maintainer confirmation link was clicked by the user.
- Live public probes on 2026-07-05 showed:
  - `https://cran.r-project.org/package=nwauR` resolves to the package page and returns HTTP 404.
  - `https://cran.r-project.org/web/packages/nwauR/index.html` returns HTTP 404.
  - `https://cran.r-project.org/src/contrib/PACKAGES` returns HTTP 200 but does not contain `Package: nwauR`.
  - `https://crandb.r-pkg.org/nwauR` returned HTTP 404 and is not positive publication evidence.
- The durable probe artifact is `live_probe_20260705.json`.

## Fixes Applied

- Added explicit support scope and a gap-register entry for the remaining external CRAN gate.
- Refreshed the public-publication probe wording without claiming publication.
- Added `live_probe_20260705.json` and linked it from metadata and the shared language-registry submissions contract.
- Kept the track in `conductor/tracks/` with `[~]` status.
- Updated the focused CRAN test so generated upload artifacts are not required to be committed; the checksum is validated when the local tarball is present.

## Validation

- `uv run pytest tests/test_r_cran_registry_submission_track.py -q`
- `python scripts/validate_language_registry_submission_tracks.py`
- `python conductor/scripts/stub_detector.py --root . --json`
