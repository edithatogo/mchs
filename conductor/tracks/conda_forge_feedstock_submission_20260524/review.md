# Review: conda-forge Feedstock Submission

## Review Result

Not archive eligible.

The local recipe and staged-recipes submission are prepared and submitted, but
the track remains live because conda-forge maintainer review, merge, feedstock
creation, and Anaconda package publication are still external gates. Public
conda-forge publication is not claimed.

## Evidence Reviewed

- `packaging/conda-forge/meta.yaml`
- `contracts/language-registry-submissions/language-registry-submissions.contract.json`
- `contracts/language-registry-submissions/external-submission-runbook.md`
- `docs/roadmaps/language-registry-external-gates.md`
- `conductor/tracks/conda_forge_feedstock_submission_20260524/review_checklist.md`
- `tests/test_conda_forge_feedstock_submission_track.py`

## Live Probe

Checked on 2026-06-25:

- `gh pr view 33452 --repo conda-forge/staged-recipes` reports PR state
  `OPEN`, `isDraft=false`, `mergedAt=null`, head
  `bffc5bf1a85389dc695adfd96c87bf2413f4db25`, no review decision, and
  successful staged-recipes/linter/check-skip/linux/osx/win check rollup.
- `https://api.anaconda.org/package/conda-forge/nwau-py` returns HTTP 404.
- `https://api.github.com/repos/conda-forge/nwau-py-feedstock` returns HTTP 404.

## Remaining Gates

- conda-forge staged-recipes maintainer review and merge.
- feedstock repository creation.
- Anaconda package API exposing `nwau-py==0.2.2`.

## Validation

- `uv run pytest tests/test_conda_forge_feedstock_submission_track.py`
- `python conductor/scripts/stub_detector.py --root . --json`
