# Implementation Plan: Pure Polars Migration

## Phase 1: Calculator & Loader Refactoring [checkpoint: 478932a]
- [x] Task: Refactor `nwau_py/data/loader.py` and `bundles.py` to return native `pl.DataFrame` e1acf45
- [x] Task: Refactor `nwau_py/calculators/acute.py` and `funding_formula.py` to use Polars native join and expression operations. fd0fe85
- [x] Task: Refactor `ed.py`, `mh.py`, `outpatients.py`, and `subacute.py` to eliminate Pandas DataFrame operations. d32cee7
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Calculator Refactoring' (Protocol in workflow.md) 478932a

## Phase 2: Grouper, Fixtures, and CLI Modernization [checkpoint: 56f372f]
- [x] Task: Refactor `groupers/hac.py` and `groupers/ahr.py` to pure Polars. cc21867
- [x] Task: Update `cli/main.py` and `fixtures.py` to read and output Polars tables. a70b8c7
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Grouper & CLI Modernization' (Protocol in workflow.md) 56f372f

## Phase 3: Dependency Pruning & Strict Parity Gates [checkpoint: fd4df72]
- [x] Task: Remove `pandas` from `pyproject.toml` dependencies and run `uv lock`. 3815363
- [x] Task: Run full 820+ test suite and assert `sys.modules` contains no `pandas` import. 935867f
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3: Dependency Pruning & Parity' (Protocol in workflow.md) fd4df72
