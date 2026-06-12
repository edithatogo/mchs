# Plan: JVM Maven Central Registry Submission

## Phase 1: Discovery

- [x] Record package candidate, version, registry, and local surface.
- [x] Store discovery/submission state in the language registry contract.

## Phase 2: Preparation

- [x] Capture repo-side package readiness or prepared artifact evidence where available.
- [x] Keep placeholder, credential-gated, or review-gated publication claims fail-closed.
    - [x] 2026-06-12 GitHub Actions dry-run `Publish Maven Central package` succeeded at `https://github.com/edithatogo/mchs/actions/runs/27407884659` after the workflow runtime JDK was moved to 17 for Gradle 9.

## Phase 3: Submission or Publication

- [ ] Verify target-version publication in the public registry.
- [ ] Record upstream submission URL or external gate.
- [x] Record remaining blocker explicitly.

## Phase 4: Closure

- [ ] Mark publication complete only after public target-version evidence exists.
- [x] Maintain this Conductor track so contract references resolve to a real track directory.
