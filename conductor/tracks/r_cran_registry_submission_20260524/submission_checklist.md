# CRAN Submission Checklist

This checklist captures the exact steps required to finish the `nwauR` CRAN gate. It is intentionally fail-closed: do not claim publication until CRAN has accepted the package and the public package page is visible.

## Inputs

- Package: `nwauR`
- Version: `0.1.0`
- Source surface: `r-binding/`
- Prepared artifact: `nwauR_0.1.0.tar.gz`
- Maintainer email: `dylan.mordaunt@vuw.ac.nz`
- CRAN submission URL: `https://cran.r-project.org/submit.html`

## Required steps

1. Rebuild the tarball from the repository root.
   ```bash
   R CMD build r-binding
   ```

2. Re-run the package check on the tarball.
   ```bash
   R CMD check --no-manual nwauR_0.1.0.tar.gz
   ```

3. Re-run the CRAN-style local gate check.
   ```bash
   _R_CHECK_CRAN_INCOMING_REMOTE_=false R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz
   ```

4. Re-run the live CRAN metadata check when network conditions allow.
   ```bash
   R CMD check --as-cran --no-manual nwauR_0.1.0.tar.gz
   ```

5. Submit the tarball through the CRAN upload form.
   - URL: `https://cran.r-project.org/submit.html`
   - Use the maintainer email recorded in `r-binding/DESCRIPTION`
   - Upload `nwauR_0.1.0.tar.gz`
   - State: submitted; maintainer confirmation/review remains external-gated.

6. Capture the CRAN incoming/pretest evidence.
   - Confirm the CRAN maintainer email sent to `dylan.mordaunt@vuw.ac.nz`
   - Record the message identifier or incoming URL
   - Note any CRAN reviewer notes or maintainer mail

7. If CRAN requests changes, patch the package and repeat steps 1 to 6.
   - Recompute the tarball SHA-256
   - Update the track evidence with the new checksum and submission notes

8. Verify publication on the CRAN package page.
   ```text
   https://cran.r-project.org/package=nwauR
   ```

## Evidence to record in the track

- Submission URL or incoming message identifier
- Final tarball SHA-256
- CRAN reviewer comments or acceptance note
- Package page URL and version `0.1.0`

## Completion rule

Do not mark the track complete until CRAN publication or accepted-review evidence exists and the public package page is visible.
