#!/usr/bin/env bash
# Bind the exact wheel to the frozen runtime lock inventory; no install claim.
set -euo pipefail
dist=${1:-dist}
sbom=${2:-dist/sbom.cdx.json}
evidence=${3:-.grype-inputs}
shopt -s nullglob
wheels=("$dist"/*.whl)
sdists=("$dist"/*.tar.gz)
if [ "${#wheels[@]}" -ne 1 ] || [ "${#sdists[@]}" -ne 1 ]; then
  echo 'Expected exactly one wheel and one source distribution.' >&2
  exit 1
fi
mkdir -p "$evidence" "$(dirname "$sbom")"
sha256sum "${wheels[@]}" "${sdists[@]}" > "$evidence/subjects.sha256"
git rev-parse HEAD > "$evidence/source-commit.txt"
sha256sum uv.lock pyproject.toml >> "$evidence/subjects.sha256"
printf '%s\n' 'Resolved frozen uv runtime lock, including pricing-import. This is a source dependency inventory, not an installed-environment or binary dependency completeness claim.' > "$evidence/scope.txt"
uv export --frozen --no-dev --no-emit-project --extra pricing-import \
  --format requirements-txt --output-file "$evidence/runtime-requirements.txt"
uvx --python 3.15.1 --from cyclonedx-bom==7.3.0 cyclonedx-py requirements \
  "$evidence/runtime-requirements.txt" --sv 1.6 \
  --output-reproducible --of JSON --validate -o "$sbom"
sha256sum "$sbom" >> "$evidence/subjects.sha256"
sha256sum --check "$evidence/subjects.sha256"
