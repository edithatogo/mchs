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

### Open VSX / Visual Studio Marketplace `mchs-tools`

Current state: VSIX is buildable; Open VSX CLI still prompts for a namespace
PAT instead of publishing; Visual Studio Marketplace publisher/PAT access is not
configured.

Required external inputs:

- Valid `OVSX_PAT` for namespace `edithatogo`.
- Visual Studio Marketplace publisher identity.
- Visual Studio Marketplace PAT with extension publish permissions.

Completion evidence required:

- Successful Open VSX publish or public Open VSX API/listing response.
- Successful Visual Studio Marketplace publish or marketplace extension query
  returning `edithatogo.mchs-tools`.

### CRAN `nwauR`

Current state: source package builds and `R CMD check --no-manual` passes from a
temporary build directory; no public CRAN listing exists.

Required external action:

- Replace placeholder maintainer `MCHS <opensource@example.com>` in `r-binding/DESCRIPTION` with the real CRAN-confirmable maintainer name and email.
- CRAN maintainer submission using the generated `nwauR_0.1.0.tar.gz` artifact.
- CRAN review response and acceptance.

Completion evidence required:

- CRAN incoming/pretest confirmation or maintainer acceptance email.
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
