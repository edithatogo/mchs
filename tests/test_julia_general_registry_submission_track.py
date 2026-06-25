from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "julia_general_registry_submission_20260524"
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


def _julia_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry for registry in data["registries"] if registry["id"] == "julia_general"
    )


def test_julia_general_track_is_published_verified():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _julia_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "completed"
    assert metadata["current_status"] == "published_verified"
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is True
    assert metadata["publication_status"] == "published_verified"
    assert "- [x] **Track: Julia General Registry Submission**" in tracks
    assert f"./archive/{TRACK_ID}/" in tracks or f"./tracks/{TRACK_ID}/" in tracks

    assert registry["current_status"] == "published_verified"
    assert registry["package"] == "NationalWeightedActivityUnitWrapper"
    assert (
        registry["submission_url"]
        == "https://github.com/JuliaRegistries/General/pull/156254"
    )
    assert registry["localReadinessResolved"] is True
    assert registry["blocker"] is None
    assert registry["submissionEvidence"]["state"] == "published_verified"
    assert (
        registry["submissionEvidence"]["url"]
        == "https://github.com/JuliaRegistries/General/pull/156254"
    )
    assert (
        registry["submissionEvidence"]["repository"]
        == "https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl"
    )
    assert (
        registry["submissionEvidence"]["triggerIssue"]
        == "https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl/issues/1"
    )
    assert (
        registry["submissionEvidence"]["commit"]
        == "56ddec5ae29513e80717d4625f82c024a211c949"
    )
    assert (
        registry["submissionEvidence"]["prHead"]
        == "bb63b2a81ec2ded2c5675f09fb6cd63128f10a07"
    )
    assert registry["submissionEvidence"]["uuid"] == (
        "58dad789-f56a-4ab3-a66f-c15139bf9cbe"
    )
    assert registry["submissionEvidence"]["checks"] == "successful"
    assert registry["submissionEvidence"]["automergeWait"] == "3-day new-package wait"
    assert registry["submissionEvidence"]["mergedAt"] == "2026-05-28T15:34:44Z"
    assert registry["publicationEvidence"]["url"] == (
        "https://github.com/JuliaRegistries/General/pull/156254"
    )
    assert registry["publicationEvidence"]["mergedAt"] == "2026-05-28T15:34:44Z"
    readme = _read(ROOT / "README.md")
    assert "Published" in readme
    assert "NationalWeightedActivityUnitWrapper 0.1.0" in readme


def test_julia_general_submission_evidence_is_recorded_with_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _julia_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert (
        evidence["discovery_result"]
        == "404 Not Found/no existing public package listing"
    )
    assert (
        evidence["discovery_url"]
        == "https://juliahub.com/api/packages/NationalWeightedActivityUnitWrapper"
    )
    assert evidence["replacement_package_candidate"] == "NationalWeightedActivityUnitWrapper"
    assert "Pkg.test()" in evidence["test_command"]
    assert "tests passed" in evidence["test_result"]
    assert (
        registry["preparationEvidence"]["testResult"]
        == "Existing Julia binding tests passed with 2 passing testsets before the replacement registration rename; julia-binding files were not changed in this evidence pass."
    )
    assert "Publication evidence is verified upstream" in plan
    assert "https://github.com/JuliaRegistries/General/pull/156254" in plan
    assert registry["preparationEvidence"]["license"] == "MIT"
    assert (
        registry["preparationEvidence"]["replacementPackageCandidate"]
        == "NationalWeightedActivityUnitWrapper"
    )
    assert (
        registry["preparationEvidence"]["repository"]
        == "https://github.com/edithatogo/NationalWeightedActivityUnitWrapper.jl"
    )
    assert registry["preparationEvidence"]["uuid"] == (
        "58dad789-f56a-4ab3-a66f-c15139bf9cbe"
    )
    assert registry["preparationEvidence"]["remainingExternalBlocker"] is None
