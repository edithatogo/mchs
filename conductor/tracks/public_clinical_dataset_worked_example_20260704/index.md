# Track public_clinical_dataset_worked_example_20260704 Context

- This track adds a real-public-dataset worked example only after an explicit
  dataset discovery, access, licensing, and suitability assessment.
- The default target is MIMIC-IV Clinical Database Demo v2.2, but the workflow
  must fail closed around Australian AR-DRG provenance and use a synthetic
  Australian classification overlay only for runnable documentation.
- Raw MIMIC files and other public patient-level dataset extracts remain
  local-only and must not be committed.
- Implementation must commit after every task with `Commit notes:`, attach git
  notes, push branch and notes after each task and phase, run `conductor-review`
  after each phase, and review GitHub Actions after the track is pushed.
- Requirements/design authority: `conductor/requirements.md` now defines
  `MUST-013`, `SHOULD-006`, `COULD-004`, and `WONT-005`; `conductor/design.md`
  now defines the Public Dataset Worked Example design.
- The worked example should demonstrate useful existing advanced features:
  provenance reporting, data-quality summaries, support-status output, and
  CLI/file interoperability where available. New feature needs discovered during
  implementation should become GitHub issues rather than unbounded scope.
- Follow-up GitHub issues created from scope review:
  [#346](https://github.com/edithatogo/mchs/issues/346) MIMIC-IV-ED example,
  [#347](https://github.com/edithatogo/mchs/issues/347) FHIR/MEDS examples,
  [#348](https://github.com/edithatogo/mchs/issues/348) dataset suitability
  registry, and [#349](https://github.com/edithatogo/mchs/issues/349)
  downloader/cache guard, and
  [#350](https://github.com/edithatogo/mchs/issues/350) reusable
  provenance/data-quality report contract.

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
