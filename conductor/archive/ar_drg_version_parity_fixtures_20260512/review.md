# Review: AR-DRG Version Parity Fixtures

## Findings

1. Resolved: `nwau_py.ar_drg_version_parity_fixtures` now provides a
   metadata-only parity fixture registry for synthetic and local licensed
   references.

2. Resolved: Tests validate synthetic fixture metadata, local licensed
   references, missing local fixture diagnostics, and cross-version rejection.

3. Resolved: A dedicated contract bundle now documents the no-proprietary
   payload boundary and synthetic/local-only fixture examples.

## Blockers

- None for metadata-only parity fixture scope.

## Remaining caveats

- This track does not commit grouped episode outputs from licensed groupers.
- Local licensed parity fixture payloads remain user-supplied and ignored.
- Full patient-level or official parity remains dependent on local licensed
  assets and is not claimed by the public repository.

## Validation commands

Use the project defaults from `conductor/workflow.md` once implementation is
present:

```bash
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest
uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml --cov-fail-under=80
cd rust && cargo fmt --all --check
cd rust && cargo clippy --all-targets --all-features -- -D warnings
cd rust && cargo test
uv run vale conductor README.md docs
```

For this review pass, no validation commands were run because the review was
limited to the track documentation and existing code surface.
