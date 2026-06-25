# Plan: Python Tooling and CI Modernization

## Phase 1: uv, Lockfile, and Python Matrix [checkpoint: c37fc9c]

- [x] Task: Write tests or checks for dependency resolution [3cf8d6a]
    - [x] Verify runtime, dev, docs, test, coverage, typing, property, mutation, and profiling groups resolve from `uv.lock`
    - [x] Verify Python 3.10-3.14 markers are represented
- [x] Task: Configure uv and CI matrix [99dba73]
    - [x] Add dependency groups and committed lockfile workflow
    - [x] Add Python 3.10, 3.11, 3.12, 3.13, and 3.14 GitHub Actions jobs
    - [x] Enforce locked installs in CI
- [x] Task: Conductor - User Manual Verification 'uv, Lockfile, and Python Matrix' (Protocol in workflow.md)

## Phase 2: Fast Quality Gates [checkpoint: c37fc9c]

- [x] Task: Write CI checks for quality tools [435716a]
    - [x] Verify `ruff format --check`, `ruff check`, `ty check`, `pytest`, and coverage commands run locally in the intended CI order
    - [x] Verify Codecov upload is configured
- [x] Task: Add quality tooling [b4893ee]
    - [x] Configure Codecov
    - [x] Configure ty
    - [x] Document `mypy` as transitional only while `ty` becomes the forward path
- [x] Task: Conductor - User Manual Verification 'Fast Quality Gates' (Protocol in workflow.md)

## Phase 3: Advanced Validation Jobs [checkpoint: c37fc9c]

- [x] Task: Add focused tests for Hypothesis strategies and mutmut configuration [1f9c8f8]
    - [x] Cover calculator invariants and boundary conditions
    - [x] Define mutation target modules
- [x] Task: Add scheduled or manual jobs for Hypothesis, mutmut, and Scalene [1f9c8f8]
    - [x] Keep normal PR feedback fast
    - [x] Store profiling output outside source files
- [x] Task: Conductor - User Manual Verification 'Advanced Validation Jobs' (Protocol in workflow.md)

## Phase 4: Maintenance Automation and Prose Quality [checkpoint: c37fc9c]

- [x] Task: Validate Renovate and Vale configuration [4a51bdf]
    - [x] Ensure calculator-impacting dependencies are not automerged unsafely
    - [x] Ensure Vale flags unsupported validation claims
- [x] Task: Add Renovate and Vale [4a51bdf]
    - [x] Configure Renovate package rules
    - [x] Configure Vale terminology and validation language rules
- [x] Task: Conductor - User Manual Verification 'Maintenance Automation and Prose Quality' (Protocol in workflow.md)
