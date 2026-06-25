# Review: JVM Maven Central Registry Submission

## Status

Reviewed on 2026-06-25. Archive eligible as a published-verified registry
track.

## Scope Reviewed

- Maven Central metadata exposes
  `io.github.edithatogo:mchs-jvm-bindings:0.1.0`.
- Track metadata records Central deployment, POM/JAR URLs, public checksums,
  namespace verification, signing evidence, and token revocation notes.
- Tests cover registry contract evidence, Gradle Central readiness gates, docs,
  and external-gate wording.

## Findings

- No live Central blocker remains for version `0.1.0`.
- Future versions require new signed artifacts and publication probes.
- This is a package publication claim, not a broad runtime support claim.

## Validation

- `curl -fsSL https://repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml`
- `uv run pytest tests/test_jvm_maven_central_registry_submission_track.py`
- `python scripts/validate_language_registry_submission_tracks.py`
- `python conductor/scripts/stub_detector.py --root . --json`
