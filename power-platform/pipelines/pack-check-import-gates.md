# Pack / Check / Import Gate Contract

The ALM workflow keeps the solution lifecycle deterministic by requiring three locally
reproducible gates before environment promotion:

- **Pack gate**: `pac solution pack --help`, `pac solution unpack --help`
- **Check gate**: `pac solution checker run --help`
- **Import gate**: `pac solution import --help`

Current enforcement:

- The `power-platform-alm-lifecycle-gates.sh` script validates these gates in CI.
- The validator does not require credentials; it only executes help-path checks.
- Missing `pac` in CI is treated as a deterministic skip unless a caller passes
  an explicit requirement for live tooling checks.

These gates are expected to run after content changes are staged and before any
environment-scoped promotion steps.
