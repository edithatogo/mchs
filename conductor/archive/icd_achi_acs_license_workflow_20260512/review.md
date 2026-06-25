# Review: ICD-10-AM/ACHI/ACS Licensed Product Workflow

## Findings

1. Resolved: `nwau_py.licensed_product_workflow` now implements metadata-only
   manifests, local-only path validation, commit-safe exclusion checks, and
   environment-variable-backed local path resolution.

2. Resolved: Missing licensed-asset diagnostics identify safe missing
   categories and local path hints without reading or exposing restricted
   contents.

3. Resolved: The track metadata and plan now reflect implemented
   local-only-workflow scope, with publication status kept `not-ready`.

## Blockers

- None for metadata-only local licensed-product workflow scope.

## Caveats

- The repository still does not ship licensed ICD-10-AM, ACHI, ACS, AR-DRG
  tables, manuals, code rows, or grouper binaries.
- Users remain responsible for lawful access to any licensed products.

## Validation commands

Not run for this review. The project workflow defines these commands:

- `uv sync --locked --group dev --group test --group coverage --group typing --group property --group mutation --group profiling --group docs`
- `uv run ruff format --check .`
- `uv run ruff check .`
- `uv run ty check`
- `uv run pytest`
- `uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml --cov-fail-under=80`
- `cd rust && cargo fmt --all --check`
- `cd rust && cargo clippy --all-targets --all-features -- -D warnings`
- `cd rust && cargo test`
- `uv run vale conductor README.md docs`
