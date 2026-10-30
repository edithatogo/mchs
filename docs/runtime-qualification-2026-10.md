# Runtime and dependency qualification — 31 October 2026

Parent #396, implementation #397. Python 3.15.1 is the active runtime.
Run `uv sync --locked --python 3.15.1 --all-groups`, then verify `.venv/bin/python --version`.
The lock refresh selects latest resolved Python packages; npm manifests/locks
select current Astro/Starlight and TypeScript/Vitest releases. This does not
claim all Rust, JVM, R, Julia or Power Platform surfaces have been upgraded.

Local qualification: Python package installation; Ruff format/check and strict ty;
800 tests passed with five genuine optional-capability skips, plus the repaired
Rust CLI parity node passed on failure-only rerun. Native maturin extension built
and installed on Python 3.15.1; its cp310 abi3 wheel tag is an ABI floor, not an
active Python 3.10 runner. WASM TypeScript typecheck and four tests passed.
Astro built 137 pages. Python audit and docs npm audit found no vulnerabilities.

Strict typing repairs distinguish None from empty values without changing
adjustment truthiness. Historical funding formulas are unchanged. The Rust pilot
contract is input columns plus NWAU25, whereas Python also exposes diagnostics;
all contracted columns are compared at existing tolerances. Diagnostic-schema
parity is not asserted. Existing pandas paths remain legacy package APIs; no
pandas adoption in downstream research is implied.

Remaining evidence: remote CI and cross-platform wheel checks must pass before
merge; local success alone is insufficient. Historical SAS decoding deprecation
warnings remain visible. No registry submission, credentials or study records are
included. Unrelated dirty local work is preserved outside this isolated clone.

Pinned third-party Conductor code is excluded from project Ruff formatting;
its upstream bytes are preserved rather than rewritten. Project-owned code
retains the same lint/format rules. The integrated registry-readiness track is
explicitly incomplete in the status matrix. NEP25 correction is documented in
nep25-correction.md; broader #201 consolidation remains open.
