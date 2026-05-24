# Smithery MCPB Bundle Manifest

`manifest.json` is the archive-root manifest used for the accepted Smithery
MCPB release. It is stored here as publication evidence, but it is not intended
to be zipped from this directory by itself.

The published bundle was assembled by copying this manifest to the root of a
staging directory beside these project files:

```text
manifest.json
pyproject.toml
LICENSE
README.md
MANIFEST.in
nwau_py/
excel_calculator/src/
excel_calculator/scripts/
```

The `entry_point` and `PYTHONPATH` values in the manifest are therefore
intentionally relative to the MCPB archive root after staging, not to this
repository documentation directory.
