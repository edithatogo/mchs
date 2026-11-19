# Synthetic calculation properties

This bounded suite exercises the real pure-Python NEP26 equation and relative-stay
functions. Generated integer-valued Decimal inputs provide exact algebraic
oracles for activity/currency separation, neutral adjustments and signed shadow
adjustments. Cohort properties check disjoint aggregation, row order, exclusions
and missing reference strata. Missing/nonfinite equation terms must fail closed.

These are software contracts. They do not establish IHACPA source parity, clinical
validity, current funding policy, Rust equivalence or empirical calibration.

The existing locked `test` and `property` dependency groups are sufficient. This
separate directory is collected explicitly by `calculation-properties.yml`, so
ordinary test environments do not acquire an undeclared Hypothesis dependency.
The workflow fails if its dependencies or selected tests are missing; it does not
silently skip this suite. No production dependency or numerical implementation is
changed.

```sh
uv export --locked --only-group test --only-group property --no-emit-project --output-file /tmp/mchs-property-requirements.txt
uv venv --python 3.15.1 .venv-properties
uv pip sync --python .venv-properties/bin/python --require-hashes /tmp/mchs-property-requirements.txt
CALCULATION_PROPERTY_EXAMPLES=1000 .venv-properties/bin/python -m pytest property_tests -q --hypothesis-seed=20261121
```

The default PR budget is 100 examples per property; the weekly/manual budget is
1,000. Inputs, example counts, test wall time (five minutes), address space (4 GiB)
and total job time (ten minutes) are bounded. Replay a failure using the printed
Hypothesis example and run seed. Reduce a confirmed defect to a readable regression
before changing production code; only synthetic counterexamples belong here.

## Verification receipt

Baseline: `7f02e4a97d24cc05fe2b3d5ad78f663be17b6da0`.
Exact Python 3.15.1, locked pytest 9.2.0 and Hypothesis 6.170.14:
eight properties passed at 100 examples (4.71 seconds) and at 1,000 examples
(12.46 seconds). No production files changed.

The full project environment did not install: NumPy 2.4.6 compiled from source
and its compiler process was killed. Consequently the full project test suite,
Rust bindings and coverage are not qualified by this receipt. The small locked
environment above imports and tests the actual pure calculation modules without
stubs or copied implementations. Existing release and full-validation gates remain.
