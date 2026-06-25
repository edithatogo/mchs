from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "swift_package_index_submission_20260524"
TRACK = ROOT / "conductor" / "tracks" / TRACK_ID
if not TRACK.exists():
    TRACK = ROOT / "conductor" / "archive" / TRACK_ID
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


def test_swift_package_index_track_is_published_with_public_spi_evidence():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _swift_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "completed"
    assert metadata["current_status"] == "published_verified"
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is True
    assert metadata["publication_status"] == "published_verified"
    assert "- [x] **Track: Swift Package Index Submission**" in tracks
    assert f"./archive/{TRACK_ID}/" in tracks or f"./tracks/{TRACK_ID}/" in tracks

    assert registry["current_status"] == "published_verified"
    assert (
        registry["submission_url"]
        == "https://swiftpackageindex.com/edithatogo/mchs-swift"
    )
    assert registry["localReadinessResolved"] is True
    assert registry["blocker"] is None
    assert registry["submissionEvidence"]["state"] == "published_verified"
    assert registry["submissionEvidence"]["stateReason"] == "completed"
    assert (
        registry["submissionEvidence"]["packageListPullRequest"]
        == "https://github.com/SwiftPackageIndex/PackageList/pull/13999"
    )
    assert (
        registry["submissionEvidence"]["packageListMergeCommit"]
        == "ffdaf6cf883878adcb7f31691f6120e3d7f64c48"
    )


def test_swift_package_index_evidence_has_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _swift_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert "merged PackageList PR 13999" in evidence["discovery_result"]
    assert "raw PackageList main containing" in evidence["discovery_result"]
    assert "returned HTTP 200" in evidence["discovery_result"]
    assert "stable v0.1.0" in evidence["discovery_result"]
    assert "state=closed state_reason=completed" in evidence[
        "submission_issue_live_result"
    ]
    assert evidence["packagelist_pr"] == (
        "https://github.com/SwiftPackageIndex/PackageList/pull/13999"
    )
    assert evidence["packagelist_pr_state"] == "MERGED"
    assert (
        evidence["packagelist_merge_commit"]
        == "ffdaf6cf883878adcb7f31691f6120e3d7f64c48"
    )
    assert "mchs-swift.git" in evidence["raw_packagelist_probe"]
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
    assert "HTTP 200" in evidence["latest_public_probe"]
    assert "SPM snippet using from: 0.1.0" in evidence["latest_public_probe"]
    assert "fixedPublicationMetadata" in registry["preparationEvidence"]
    assert "returned HTTP 200" in registry["preparationEvidence"]["discovery"]
    assert "latestSubmissionProbe" in registry["preparationEvidence"]
    assert "packageListPullRequest" in registry["preparationEvidence"]
    assert (
        registry["preparationEvidence"]["rawPackageListProbe"]
        == "https://raw.githubusercontent.com/SwiftPackageIndex/PackageList/main/packages.json contains https://github.com/edithatogo/mchs-swift.git."
    )
    assert "latestReleaseProbe" in registry["preparationEvidence"]
    assert "latestPublicProbe" in registry["preparationEvidence"]
    assert "pkg.go.dev" not in plan
    assert "Publication is verified" in plan
    assert "Pending Swift Package Index listing/version evidence" not in plan
