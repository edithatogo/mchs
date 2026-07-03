# Maven Central Submission Checklist

This checklist captures the external steps required to finish `io.github.edithatogo:mchs@0.1.0`.

## Inputs

- Package: `io.github.edithatogo:mchs`
- Version: `0.1.0`
- Local surface: `bindings/jvm/`
- Prepared dry-run workflow: `.github/workflows/publish-maven-central.yml`
- Dry-run evidence: GitHub Actions run `https://github.com/edithatogo/mchs/actions/runs/27456830098`
- Adjacent artifact note: public metadata for `io.github.edithatogo:mchs-jvm-bindings:0.1.0` exists, but it does not close this track unless the contract target is intentionally changed.

## Required steps

1. Verify the Central Portal namespace `io.github.edithatogo`.
2. Export the in-memory signing key and configure `MAVEN_SIGNING_KEY` and `MAVEN_SIGNING_PASSWORD` only as publish-session secrets.
3. Configure `CENTRAL_PORTAL_DEPLOY_URL`, `CENTRAL_PORTAL_USERNAME`, and `CENTRAL_PORTAL_PASSWORD` only after Central Portal credentials are created.
4. Re-run the dry-run workflow with `dry_run=true`.
5. Run the authenticated publish workflow with `dry_run=false`.
6. Release or close the deployment after Central validation succeeds.
7. Record the release/deployment identifier, submission URL, and any reviewer notes.
8. Verify the public metadata exposes version `0.1.0`.
   ```text
   https://repo1.maven.org/maven2/io/github/edithatogo/mchs/maven-metadata.xml
   ```

## Evidence to record

- Namespace verification evidence for `io.github.edithatogo`
- Central Portal publisher identity and credential notes
- Signing key source, format, and password handling
- Readiness report output
- Release or deployment URL
- Public metadata URL showing `0.1.0`

## Completion rule

Do not mark the track complete until the Central Portal release for `io.github.edithatogo:mchs` is accepted and the public Maven metadata exposes version `0.1.0`.
