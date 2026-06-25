# Julia Binding CI Notes

The Julia binding track deliberately avoids adding a required GitHub Actions
Julia matrix in this phase.

## Current posture

- The committed package scaffold is wrapper-only and validates command
  construction locally.
- The executable boundary is `python -m nwau_py.cli.main` with CSV input and
  output.
- Repository Python tests enforce the documented strategy, package scaffold,
  no-formula-duplication rule, and conservative publication posture.

## Deferred CI gate

Add a guarded Julia CI job only after the shared CLI/file contract has
fixture-backed parity that can run deterministically in CI. The future job
should:

- Install Julia with a pinned supported version.
- Install the Python package through the same `uv` environment used by the
  Python CI.
- Run `julia --project=julia-binding -e 'using Pkg; Pkg.test()'`.
- Execute at least one synthetic shared golden fixture through the wrapper.
- Upload any generated parity reports as CI artifacts.

Until that fixture parity exists, a Julia Actions job would mostly validate
packaging mechanics and could overstate release readiness.
