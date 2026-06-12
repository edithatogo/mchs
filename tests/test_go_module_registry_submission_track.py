from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "go_module_registry_submission_20260524"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _go_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry
        for registry in data["registries"]
        if registry["id"] == "go_module_proxy"
    )


def test_go_module_track_is_published_to_proxy_and_pkg_go_dev():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _go_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "completed"
    assert metadata["current_status"] == "published_verified"
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is True
    assert metadata["publication_status"] == "published_verified"
    assert "- [x] **Track: Go Module Registry Submission**" in tracks

    assert registry["current_status"] == "published_verified"
    assert (
        registry["submission_url"]
        == "https://proxy.golang.org/github.com/edithatogo/mchs/bindings/go/@v/v0.1.0.info"
    )
    assert registry["localReadinessResolved"] is True
    assert registry["blocker"] is None


def test_go_module_publication_evidence_is_recorded_with_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _go_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert evidence["discovery_result"] == "Go module proxy lists v0.1.0"
    assert evidence["proxy_version_list"] == "v0.1.0"
    assert "indexed version 0.1.0" in evidence["pkg_go_dev_result"]
    assert evidence["test_command"] == "go test ./..."
    assert "All Go packages passed" in evidence["test_result"]
    assert "fixedLocalBlocker" in registry["preparationEvidence"]
    assert registry["publicationEvidence"]["scope"] == "go_module_proxy_and_pkg_go_dev"
    assert "indexed version 0.1.0" in registry["publicationEvidence"]["pkgGoDevStatus"]
    assert registry["submissionEvidence"]["pkgGoDevStatus"] == 200
    assert "pkg.go.dev exposes version `0.1.0`" in plan
