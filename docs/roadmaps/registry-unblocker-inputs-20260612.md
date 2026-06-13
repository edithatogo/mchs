# Registry Unblocker Inputs - 2026-06-12

This checklist records the exact external inputs needed before the remaining
registry tracks can move from prepared/submitted to published or complete. It is
operator-facing by design: do not mark any item complete without public registry
evidence, accepted upstream review, or authenticated workflow output.

## Maintainer-review gates

### conda-forge `nwau-py`

Current state: staged-recipes PR is open, mergeable, and all visible checks are
green.

Required external action:

- conda-forge maintainer review and merge of `https://github.com/conda-forge/staged-recipes/pull/33452`.
- Feedstock creation by conda-forge automation.
- Public Anaconda propagation for `conda-forge/nwau-py` at version `0.2.2`.

Completion evidence required:

- Merged PR or feedstock creation evidence.
- Public Anaconda package/version response for `nwau-py==0.2.2`.

### ConanCenter `nwau-c-abi`

Current state: ConanCenter PR is open and mergeable; CLA is signed; job
scheduler remains action-required.

Required external action:

- ConanCenter maintainer job scheduling/review for `https://github.com/conan-io/conan-center-index/pull/30262`.
- Upstream CI execution and maintainer acceptance.

Completion evidence required:

- ConanCenter PR merged or accepted by maintainers.
- Public ConanCenter package/version evidence for `nwau-c-abi/0.1.0`.

## Account or credential gates

### Maven Central `io.github.edithatogo:mchs`

Current state: JVM module and fail-closed publishing workflow are prepared; dry
run passes; no required Central secrets are configured.

Required external inputs:

- Central Portal namespace verification for `io.github.edithatogo`.
- `CENTRAL_PORTAL_DEPLOY_URL`.
- `CENTRAL_PORTAL_USERNAME`.
- `CENTRAL_PORTAL_PASSWORD`.
- `MAVEN_SIGNING_KEY`.
- `MAVEN_SIGNING_PASSWORD`.

Completion evidence required:

- Authenticated Central Portal publish workflow run with `dry_run=false`.
- Public Maven Central metadata for `io.github.edithatogo:mchs:0.1.0`.

### Open VSX `mchs-tools`

Current state: VSIX is buildable; the merged VS Code extension publish workflow
dry-run packages successfully; Visual Studio Marketplace exposes
`edithatogo.mchs-tools` version `0.1.0` publicly; Open VSX Access Tokens became
available after the Eclipse publisher agreement was accepted; namespace
`edithatogo` was created; workflow run
`https://github.com/edithatogo/mchs/actions/runs/27455601114` published
`edithatogo.mchs-tools v0.1.0`; the Open VSX extension page returns HTTP 200,
while the API endpoint may still be propagating.

Required external inputs:

- None for initial `0.1.0` publication.

Completion evidence required:

- Successful Open VSX publish workflow and public Open VSX listing response.

### CRAN `nwauR`

Current state: source package builds and `R CMD check --no-manual` passes from a
temporary build directory; no public CRAN listing exists.

Required external action:

- Maintainer metadata uses `Dylan Mordaunt <d.a.mordaunt@gmail.com>`; CRAN upload was submitted on 2026-06-13 as package id 344701 and the maintainer confirmation email was sent.
- CRAN maintainer email confirmation for submitted package id 344701.
- CRAN review response and acceptance.

Completion evidence required:

- CRAN maintainer confirmation email and subsequent CRAN incoming/pretest or acceptance email.
- Public CRAN package page, CRANDB record, or archive entry for `nwauR`.

### MATLAB File Exchange `mchs-matlab-interop`

Current state: upload bundle exists and checksum is verified; MATLAB/Octave
runtime validation is not claimed; no public File Exchange listing exists.

Required external action:

- MathWorks account session with File Exchange upload permission.
- Upload `bindings/matlab/mchs-matlab-interop-0.1.0.zip`.
- Complete File Exchange review workflow.

Completion evidence required:

- Public File Exchange listing for `mchs-matlab-interop`.
- Uploaded bundle/version metadata matching `0.1.0`.

## Public listing propagation gates

### Swift Package Index `MCHSBind`

Current state: PackageList contains `https://github.com/edithatogo/mchs-swift.git`,
but public SPI package page/API/version evidence is not accessible from this
environment.

Required external action:

- Wait for SPI ingestion/listing propagation or verify from a browser/network
  path that can pass Cloudflare.

Completion evidence required:

- Public SPI package page or API response for `edithatogo/mchs-swift`.
- Version/build evidence for tag `v0.1.0`.

## Power Platform live readiness gates

Current state: aggregate preflight remains blocked but contract-valid across the
six readiness checks.

Required external inputs:

- Real public HTTPS service-boundary base URL with `/healthz` and
  `/.well-known/mcp/server-card.json`.
- GitHub repository secrets `POWER_PLATFORM_ENVIRONMENT_URL`,
  `POWER_PLATFORM_APPLICATION_ID`, `POWER_PLATFORM_CLIENT_SECRET`, and
  `POWER_PLATFORM_TENANT_ID`.
- Real PAC app `appId`, `playUrl`, and custom connector `connectionId`.
- Real Power Automate flow run IDs, run statuses, and HTTPS run URLs.
- NSW tenant DLP policy, connector-policy, monitoring, and support evidence.
- Standalone Power Platform remote record or explicit governance waiver.

Completion evidence required:

- Passing `scripts/preflight_power_platform_readiness.py` output.
- Passing official Power Platform Actions live-gate workflow run.
- Checked-in evidence records preserving the claim boundary until every live
  field is real.
