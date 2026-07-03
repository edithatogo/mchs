# Maven Central Submission Checklist

This checklist captures the external steps required to finish `io.github.edithatogo:mchs-jvm-bindings@0.1.0`.

## Inputs

- Package: `io.github.edithatogo:mchs-jvm-bindings`
- Version: `0.1.0`
- Local surface: `bindings/jvm/`
- Prepared artifacts:
  - `bindings/jvm/build/libs/mchs-jvm-bindings-0.1.0.jar`
  - `bindings/jvm/build/libs/mchs-jvm-bindings-0.1.0-sources.jar`
  - `bindings/jvm/build/libs/mchs-jvm-bindings-0.1.0-javadoc.jar`
- Prepared Central Portal bundle: `build/mchs-jvm-bindings-0.1.0-central-bundle.zip`
- Bundle SHA-256: `d0024c9f97b6cc23081139948a6b22508b5a06e20f96b75dc9b07082d2e56f42`
- Verified namespace: `io.github.edithatogo`
- Verification repository: `https://github.com/edithatogo/f7fztfn9vz`
- Last upload attempts:
  - `89d0d2a9-91c6-4994-9f8e-fdd34bb501d0` failed validation: Central could not discover public key `BB03C82343A653EE44BD5CDA9DF6B142F065199E`.
  - `fccefc51-9ccb-4466-8f85-8a47bc16cf3c` failed validation with the same public-key discovery error after supported keyserver upload.
  - `7ced6d47-59ee-40fb-9c9b-09b1aa9f8491` failed validation with the same public-key discovery error after a propagation wait.
  - `5fb01ae9-2609-4284-9427-5830e08bcbb5` validated after supported keyserver propagation and was published by Publisher API with HTTP 204.
- Public metadata: `https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml`
- Public JAR: `https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/0.1.0/mchs-jvm-bindings-0.1.0.jar`
- Adjacent coordinate note: `io.github.edithatogo:mchs` dry-run or publication work is separate from this track unless the contract target is intentionally changed.

## Required steps

1. Keep the Central Portal namespace `io.github.edithatogo` verified.
2. Confirm Central can discover public signing key `BB03C82343A653EE44BD5CDA9DF6B142F065199E` from a supported keyserver. Completed after supported keyserver propagation; the successful deployment validated and published.
   - `gpg --keyserver hkps://keyserver.ubuntu.com --send-keys BB03C82343A653EE44BD5CDA9DF6B142F065199E` returned success.
   - `gpg --keyserver hkps://pgp.mit.edu --send-keys BB03C82343A653EE44BD5CDA9DF6B142F065199E` returned success.
   - A clean temporary keyring can receive the key from `hkps://keyserver.ubuntu.com`.
3. Create a fresh short-lived Central user token for the upload session. Completed for `mchs-jvm-010-retry2-20260612`; token revoked after use.
4. Re-upload `build/mchs-jvm-bindings-0.1.0-central-bundle.zip` through Central Portal or the Publisher API. Completed as deployment `5fb01ae9-2609-4284-9427-5830e08bcbb5`.
5. Release the deployment after Central validation succeeds. Completed; Publisher API returned HTTP 204.
6. Record the release/deployment identifier, submission URL, and any reviewer notes. Completed in metadata/contract evidence.
7. Verify the public metadata exposes version `0.1.0`. Completed on repo1.maven.org.
   ```text
   https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml
   ```

## Evidence to record

- Namespace verification evidence: `io.github.edithatogo` verified via `https://github.com/edithatogo/f7fztfn9vz`
- Central Portal publisher identity and credential notes
- Signing key source, format, and password handling
- Readiness report output
- Release or deployment URL
- Public metadata URL showing `0.1.0`

## Completion rule

Do not mark the track complete until the Central Portal release for `io.github.edithatogo:mchs-jvm-bindings` is accepted and the public Maven metadata exposes version `0.1.0`.

Completion evidence is now present: Maven Central metadata exposes version `0.1.0` and the public JAR hash matches the local artifact.
