from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "jvm_maven_central_registry_submission_20260524"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
JVM_BUILD = ROOT / "bindings" / "jvm" / "build.gradle.kts"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _jvm_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(registry for registry in data["registries"] if registry["id"] == "jvm_maven_central")


def test_jvm_maven_central_track_is_blocked_by_external_release_requirements():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _jvm_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "blocked"
    assert metadata["current_status"] == "uploaded_validation_failed_pending_pgp_keyserver_propagation_and_release"
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is False
    assert metadata["publication_status"] == "not_published"
    assert "- [~] **Track: JVM Maven Central Registry Submission**" in tracks

    assert registry["current_status"] == "uploaded_validation_failed_pending_pgp_keyserver_propagation_and_release"
    assert registry["package"] == "io.github.edithatogo:mchs-jvm-bindings"
    assert registry["submission_url"] is None
    assert registry["localReadinessResolved"] is True
    assert "validation fails" in registry["blocker"]
    assert "public PGP key" in registry["blocker"]


def test_jvm_maven_central_preparation_evidence_is_recorded_without_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _jvm_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert evidence["coordinate"] == "io.github.edithatogo:mchs-jvm-bindings:0.1.0"
    assert evidence["discovery_url"].endswith(
        "/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml"
    )
    assert evidence["discovery_result"].startswith("404 no existing Maven Central metadata")
    assert "2026-06-12" in evidence["discovery_result"]
    assert evidence["build_command"] == "gradle -p bindings/jvm validateCentralPortalReadiness build"
    assert evidence["build_result"] == "BUILD SUCCESSFUL"
    assert evidence["generated_artifacts"] == [
        "mchs-jvm-bindings-0.1.0.jar",
        "mchs-jvm-bindings-0.1.0-sources.jar",
        "mchs-jvm-bindings-0.1.0-javadoc.jar",
    ]
    assert all(len(value) == 64 for value in evidence["sha256"].values())
    assert "Local GPG signature verification succeeds" in evidence["signing_check"]
    assert "cannot discover that public key" in evidence["signing_check"]
    assert "namespaceVerified=true" in evidence["latest_readiness_report"]
    assert "publisherCredentialsPresent=false" in evidence["latest_readiness_report"]
    assert "signingCredentialsPresent=false" in evidence["latest_readiness_report"]
    assert "https://github.com/edithatogo/f7fztfn9vz" in evidence["namespace_verification"]
    assert "mchs-jvm-bindings-0.1.0-central-bundle.zip" in evidence["central_bundle"]
    assert "d0024c9f97b6cc23081139948a6b22508b5a06e20f96b75dc9b07082d2e56f42" in evidence["central_bundle"]
    assert "d.a.mordaunt@gmail.com" in evidence["signing_key"]
    assert "keyserver.ubuntu.com" in evidence["signing_key"]
    assert "central_user_token" in evidence
    assert "revoked" in evidence["central_user_token"]
    assert "7ced6d47-59ee-40fb-9c9b-09b1aa9f8491" in evidence["submission_upload"]
    assert "Central Portal namespace io.github.edithatogo is verified" in evidence[
        "latest_external_blockers"
    ]
    assert "Publisher API upload succeeds" in evidence["latest_external_blockers"]
    assert "cannot find public key" in evidence["latest_external_blockers"]
    assert "release/public metadata is not claimed" in evidence["latest_external_blockers"]
    assert registry["preparationEvidence"]["coordinate"] == evidence["coordinate"]
    assert registry["preparationEvidence"]["buildResult"] == "BUILD SUCCESSFUL"
    assert "checkPomFileForMavenPublication passed" in registry["preparationEvidence"]["pomValidation"]
    assert "publicationUpload=not-attempted" in registry["preparationEvidence"]["readinessReport"]
    assert "Publication is not claimed" in plan


def test_jvm_gradle_build_defines_central_portal_readiness_without_publish_credentials():
    build = _read(JVM_BUILD)

    assert "artifactId = \"mchs-jvm-bindings\"" in build
    assert "withSourcesJar()" in build
    assert "withJavadocJar()" in build
    assert "checkPomFileForMavenPublication" in build
    assert "generateMetadataFileForMavenPublication" in build
    assert "validateCentralPortalReadiness" in build
    assert "publicationUpload=not-attempted" in build
    assert "mavenCentralNamespaceVerified" in build
    assert "MAVEN_CENTRAL_USERNAME" in build
    assert "MAVEN_CENTRAL_PASSWORD" in build
    assert "MAVEN_CENTRAL_SIGNING_KEY" in build
    assert "MAVEN_CENTRAL_SIGNING_PASSWORD" in build
    assert "releaseMode.get() && blockers.isNotEmpty()" in build


def test_jvm_docs_name_central_portal_namespace_and_signing_gates():
    spec = _read(TRACK / "spec.md")
    runbook = _read(
        ROOT
        / "contracts"
        / "language-registry-submissions"
        / "external-submission-runbook.md"
    )
    gates = _read(ROOT / "docs" / "roadmaps" / "language-registry-external-gates.md")
    matrix = _read(ROOT / "docs" / "roadmaps" / "polyglot-packaging-release-matrix.md")

    for text in (spec, runbook, gates, matrix):
        assert "io.github.edithatogo:mchs-jvm-bindings" in text
        assert "namespace" in text
        assert "public key" in text or "public-key" in text

    assert "gradle -p bindings/jvm validateCentralPortalReadiness build" in runbook
    assert "Maven Central metadata probe" in spec
    assert "Central Portal upload bundle" in gates
