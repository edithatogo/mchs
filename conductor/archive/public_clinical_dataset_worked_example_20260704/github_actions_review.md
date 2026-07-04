# GitHub Actions Review: Public Clinical Dataset Worked Example

Review date: 2026-07-04 UTC / 2026-07-05 Australia/Sydney.

Branch: `codex/registry-gate-publication-evidence-20260617`

Reviewed commit: `070aa9b626196d648318bbd18ffbf1376b44d7b8`

## Runs

| Workflow | Run | Status | Jobs | Interpretation |
| --- | --- | --- | ---: | --- |
| Docs Site | [28713315483](https://github.com/edithatogo/mchs/actions/runs/28713315483) | failure | 0 | Failed before job scheduling. |
| Release Rust | [28713315735](https://github.com/edithatogo/mchs/actions/runs/28713315735) | failure | 0 | Failed before job scheduling. |

`gh run view` returned empty `jobs` arrays for both runs, and
`gh run view --log-failed` returned `log not found`. That means the failures
occurred before any job log was produced.

## Existing Issue

The failure mode matches [#354](https://github.com/edithatogo/mchs/issues/354),
`bug: reconcile branch workflow files with current GitHub Actions hardening`.
That issue records the branch workflow-file mismatch and the same zero-job
failure pattern.

## Track Impact

Local track validation is complete for the public clinical dataset worked
example:

- `python conductor/scripts/stub_detector.py --root . --json`
- `uv run pytest tests/test_public_clinical_dataset_worked_example_track.py -q`
- `uv run ruff check nwau_py/public_clinical_datasets.py examples/mimic_demo/run_worked_example.py tests/test_public_clinical_dataset_worked_example_track.py`
- `uv run ty check nwau_py/public_clinical_datasets.py examples/mimic_demo/run_worked_example.py tests/test_public_clinical_dataset_worked_example_track.py`

The pushed GitHub Actions gate remains externally blocked by the branch
workflow-file issue in #354, not by a job-level failure in this track.
