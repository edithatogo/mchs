from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

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
    return next(
        registry
        for registry in data["registries"]
        if registry["id"] == "jvm_maven_central"
    )


def _contains_url_host(text: str, host: str) -> bool:
    return any(
        urlparse(match.group(0)).hostname == host
        for match in re.finditer(r"https?://[^\s`),]+|hkps://[^\s`),]+", text)
    )


def test_jvm_maven_central_track_is_published_and_verified():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _jvm_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "completed"
    assert metadata["current_status"] == "published_verified"
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is True
    assert metadata["publication_status"] == "published_verified"
    assert metadata["blocker"] is None
    assert "- [x] **Track: JVM Maven Central Registry Submission**" in tracks

    assert registry["current_status"] == "published_verified"
    assert registry["package"] == "io.github.edithatogo:mchs-jvm-bindings"
    assert registry["submission_url"] == (
        "https://repo1.maven.org/maven2/io/github/edithatogo/"
        "mchs-jvm-bindings/maven-metadata.xml"
    )
    assert registry["localReadinessResolved"] is True
    assert registry["blocker"] is None


def test_jvm_maven_central_publication_evidence_is_recorded():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _jvm_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    publication = evidence["publication_evidence"]
    assert evidence["coordinate"] == "io.github.edithatogo:mchs-jvm-bindings:0.1.0"
    assert evidence["discovery_url"].endswith(
        "/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml"
    )
    assert (
        "Initial Maven Central metadata probe returned HTTP 404"
        in evidence["discovery_result"]
    )
    assert "returned HTTP 200" in evidence["discovery_result"]
    assert "2026-06-12" in evidence["discovery_result"]
    assert (
        evidence["build_command"]
        == "gradle -p bindings/jvm validateCentralPortalReadiness build"
    )
    assert evidence["build_result"] == "BUILD SUCCESSFUL"
    assert evidence["generated_artifacts"] == [
        "mchs-jvm-bindings-0.1.0.jar",
        "mchs-jvm-bindings-0.1.0-sources.jar",
        "mchs-jvm-bindings-0.1.0-javadoc.jar",
    ]
    assert all(len(value) == 64 for value in evidence["sha256"].values())
    assert "Local GPG signature verification succeeds" in evidence["signing_check"]
    assert "Central validation succeeded" in evidence["signing_check"]
    assert "namespaceVerified=true" in evidence["latest_readiness_report"]
    assert "publisherCredentialsPresent=false" in evidence["latest_readiness_report"]
    assert "signingCredentialsPresent=false" in evidence["latest_readiness_report"]
    assert (
        "https://github.com/edithatogo/f7fztfn9vz" in evidence["namespace_verification"]
    )
    assert "mchs-jvm-bindings-0.1.0-central-bundle.zip" in evidence["central_bundle"]
    assert (
        "d0024c9f97b6cc23081139948a6b22508b5a06e20f96b75dc9b07082d2e56f42"
        in evidence["central_bundle"]
    )
    assert "d.a.mordaunt@gmail.com" in evidence["signing_key"]
    assert _contains_url_host(evidence["signing_key"], "keyserver.ubuntu.com")
    assert "central_user_token" in evidence
    assert "revoked" in evidence["central_user_token"]
    assert "mchs-jvm-010-retry2-20260612" in evidence["central_user_token"]
    assert "5fb01ae9-2609-4284-9427-5830e08bcbb5" in evidence["submission_upload"]
    assert "HTTP 204" in evidence["submission_upload"]
    assert evidence["latest_external_blockers"] is None
    assert "returned HTTP 200" in evidence["latest_public_metadata_probe"]
    assert "latest/release/version 0.1.0" in evidence["latest_public_metadata_probe"]
    assert publication["deployment_id"] == "5fb01ae9-2609-4284-9427-5830e08bcbb5"
    assert publication["metadata_url"] == registry["submission_url"]
    assert publication["version"] == "0.1.0"
    assert publication["jar_sha256"] == evidence["sha256"]["jar"]
    assert len(publication["pom_sha256"]) == 64
    assert registry["preparationEvidence"]["coordinate"] == evidence["coordinate"]
    assert registry["preparationEvidence"]["buildResult"] == "BUILD SUCCESSFUL"
    assert (
        "checkPomFileForMavenPublication passed"
        in registry["preparationEvidence"]["pomValidation"]
    )
    assert (
        "publicationUpload=not-attempted"
        in registry["preparationEvidence"]["readinessReport"]
    )
    assert (
        registry["submissionEvidence"]["deploymentId"] == publication["deployment_id"]
    )
    assert registry["submissionEvidence"]["state"] == "published_verified"
    assert registry["publicationEvidence"]["jarSha256"] == publication["jar_sha256"]
    assert "Publication is not claimed" not in plan
    assert "Publication is verified on repo1.maven.org" in plan


def test_jvm_gradle_defines_central_readiness_without_publish_credentials():
    build = _read(JVM_BUILD)

    assert 'artifactId = "mchs-jvm-bindings"' in build
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
        assert "namespace" in text or "Namespace" in text
        assert "SHA-256" in text or "public key" in text or "public-key" in text

    assert "gradle -p bindings/jvm validateCentralPortalReadiness build" in runbook
    assert _contains_url_host(spec, "repo1.maven.org")
    assert "successful Publisher API deployment" in gates
