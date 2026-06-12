from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "swift_package_index_submission_20260524"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _swift_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry
        for registry in data["registries"]
        if registry["id"] == "swift_package_index"
    )


def test_swift_package_index_track_is_submitted_with_closed_issue_pending_probe():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _swift_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "submitted"
    assert metadata["current_status"] == "submitted_accepted_pending_spi_public_probe"
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is False
    assert metadata["publication_status"] == "not_published"
    assert "- [~] **Track: Swift Package Index Submission**" in tracks

    assert registry["current_status"] == "submitted_accepted_pending_spi_public_probe"
    assert (
        registry["submission_url"]
        == "https://github.com/SwiftPackageIndex/PackageList/issues/13717"
    )
    assert registry["localReadinessResolved"] is True
    assert "closed as completed" in registry["blocker"]
    assert "publication metadata is fixed" in registry["blocker"]
    assert (
        registry["submissionEvidence"]["state"]
        == "closed_completed_public_probe_blocked"
    )
    assert registry["submissionEvidence"]["stateReason"] == "completed"


def test_swift_package_index_evidence_has_no_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _swift_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert "PackageList issue still closed as completed" in evidence["discovery_result"]
    assert "HTTP 403 Cloudflare challenge" in evidence["discovery_result"]
    assert "without visible MCHSBind or 0.1.0 version evidence" in evidence[
        "discovery_result"
    ]
    assert "state=closed state_reason=completed" in evidence[
        "submission_issue_live_result"
    ]
    assert evidence["build_command"] == "swift build"
    assert evidence["build_result"] == "Build complete"
    assert registry["preparationEvidence"]["testAttempt"].startswith(
        "swift test exits with no tests found"
    )
    assert (
        registry["preparationEvidence"]["release"]
        == "https://github.com/edithatogo/mchs-swift/releases/tag/v0.1.0"
    )
    assert "tag_name=v0.1.0" in evidence["release_probe_result"]
    assert "HTTP 403" in evidence["latest_public_probe"]
    assert "fixedPublicationMetadata" in registry["preparationEvidence"]
    assert "HTTP 403 Cloudflare challenge" in registry["preparationEvidence"]["discovery"]
    assert "latestSubmissionProbe" in registry["preparationEvidence"]
    assert "latestReleaseProbe" in registry["preparationEvidence"]
    assert "latestPublicProbe" in registry["preparationEvidence"]
    assert "pkg.go.dev" not in plan
    assert "Publication is not claimed" in plan
