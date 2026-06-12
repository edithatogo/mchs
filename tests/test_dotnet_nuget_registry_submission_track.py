from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "dotnet_nuget_registry_submission_20260524"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
PACKAGE = (
    ROOT
    / "bindings"
    / "dotnet"
    / "bin"
    / "Release"
    / "Mchs.Bindings.DotNet.0.1.0.nupkg"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _dotnet_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry for registry in data["registries"] if registry["id"] == "dotnet_nuget"
    )


def test_dotnet_nuget_track_is_published_verified():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _dotnet_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "completed"
    assert metadata["current_status"] == "published_verified"
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is True
    assert metadata["publication_status"] == "published_verified"
    assert "- [x] **Track: .NET NuGet Registry Submission**" in tracks

    assert registry["current_status"] == "published_verified"
    assert (
        registry["submission_url"]
        == "https://api.nuget.org/v3-flatcontainer/mchs.bindings.dotnet/index.json"
    )
    assert registry["localReadinessResolved"] is True
    assert registry["blocker"] is None


def test_dotnet_nuget_package_evidence_records_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _dotnet_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert evidence["package_artifact"].endswith("Mchs.Bindings.DotNet.0.1.0.nupkg")
    assert PACKAGE.name in evidence["package_artifact"]
    assert evidence["package_sha256"] == (
        "e6195abe5c49780b640844da12fb3eec756a963db8d14570de6bcc7901ceb211"
    )
    assert (
        "SHA-256 e6195abe5c49780b640844da12fb3eec756a963db8d14570de6bcc7901ceb211"
        in registry["preparationEvidence"]["packageVerification"]
    )
    assert (
        registry["publicationEvidence"]["url"]
        == registry["publicationEvidence"]["flatContainerUrl"]
    )
    assert registry["publicationEvidence"]["flatContainerResponse"] == {
        "versions": ["0.1.0"]
    }
    assert registry["publicationEvidence"]["packageBlobUrl"].endswith(
        "/mchs.bindings.dotnet.0.1.0.nupkg"
    )
    assert (
        "HTML package page returned 404"
        in registry["publicationEvidence"]["packagePageNote"]
    )
    assert "Publication is claimed from public NuGet flat-container evidence" in plan
