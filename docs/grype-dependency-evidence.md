# Grype dependency evidence

The P0 rollout uses the immutable `repository-standards` Grype action with a
Critical release threshold. Pull-request findings are advisory. Missing or
invalid inventories, database failures, scanner errors and evidence failures
fail both modes. Existing privacy, scientific, provenance and publication gates
remain required; a clean vulnerability report does not replace them.

## Inventory and publication binding

The Python release and independent PyPI publication workflows run
`.github/scripts/generate_release_sbom.sh` before publication. It converts the
frozen `uv.lock` runtime requirements, including `pricing-import`, to validated
CycloneDX 1.6. It records the exact wheel, sdist, lock, manifest and SBOM hashes.
The release retains `sbom.cdx.json`; the PyPI path independently scans the graph
from its checked-out release source and verifies its candidate hashes.

This is a resolved source dependency inventory. It does not establish installed
dependency or native-library completeness. A local Python 3.15.1 installation
attempt required building locked NumPy and failed when its C++ compiler process
was killed. The lock and runtime policy were preserved. A future installed
qualifier needs successful evidence from the supported runtime before this
scope can be expanded.

The manual crates.io route scans a resolved Cargo inventory after locked
packaging. The NuGet route scans the built assemblies and `.deps.json` metadata
and binds the exact `.nupkg` hashes. Internal .NET project identities are retained
because the current package has no external NuGet dependencies. These inventories
do not cover the consumer's system runtime or independently supplied native tools.

## Retention and monitoring

The shared action retains the normalized inventory, report, database metadata,
source identity, policy outcome and hashes. Caller-owned subject receipts are
retained separately, including on failure. Release evidence retention is 30 days.
The weekly job resolves the latest published non-prerelease release once and
checks the exact `sbom.cdx.json` asset identity and GitHub-provided SHA-256 before
scanning. An older release without that asset produces an explicit failure;
rebuilding current source is not a substitute for released evidence.

## Qualification still required

Hosted runs must demonstrate the new callers on their actual revision. The
Maven Central, VS Code extension and environment deployment routes are outside
this first rollout; their own artifacts need qualified resolved inventories
before claiming portfolio-wide publication coverage. R/Julia declarations,
operating-system dependencies and external runtime tools are not inferred from
Python or Cargo lockfiles. Existing dependency auditors remain in place.
