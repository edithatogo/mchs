# Conda qualification

`recipe.yaml` is the active rattler-build 0.77.0 recipe. It builds this checkout,
not an older published sdist, and retains installed Python import, pip dependency
consistency and CLI checks. Python is constrained to 3.15.1–3.15.x.

`meta.yaml` preserves the published 0.2.2 source URL/hash for downstream migration
and metadata comparisons; CI no longer invokes conda-build/conda-verify.
The host build stack could not solve on Python 3.15.1, so the user approved the
standalone Rust builder (issue #402, parent #396). No older Python fallback.

Use `pixi exec --spec rattler-build=0.77.0 -- rattler-build build --recipe conda/recipe/recipe.yaml --channel conda-forge`.
Builds do not upload packages. Source filtering excludes caches, Git internals and
local compiled extensions; the noarch package contains the Python implementation.
