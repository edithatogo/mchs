# Implementation Plan: Pure Polars Migration

## Phase 1: Calculator & Loader Refactoring
- [ ] Task: Refactor `nwau_py/data/loader.py` and `bundles.py` to return native `pl.DataFrame`.
- [ ] Task: Refactor `nwau_py/calculators/acute.py` and `funding_formula.py` to use Polars native join and expression operations.
- [ ] Task: Refactor `ed.py`, `mh.py`, `outpatients.py`, and `subacute.py` to eliminate Pandas DataFrame operations.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Calculator Refactoring' (Protocol in workflow.md)

## Phase 2: Grouper, Fixtures, and CLI Modernization
- [ ] Task: Refactor `groupers/hac.py` and `groupers/ahr.py` to pure Polars.
- [ ] Task: Update `cli/main.py` and `fixtures.py` to read and output Polars tables.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Grouper & CLI Modernization' (Protocol in workflow.md)

## Phase 3: Dependency Pruning & Strict Parity Gates
- [ ] Task: Remove `pandas` from `pyproject.toml` dependencies and run `uv lock`.
- [ ] Task: Run full 820+ test suite and assert `sys.modules` contains no `pandas` import.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Dependency Pruning & Parity' (Protocol in workflow.md)
