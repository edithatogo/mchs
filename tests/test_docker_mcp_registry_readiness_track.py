from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "docker_mcp_registry_readiness_20260517"
TRACKS = ROOT / "conductor" / "tracks.md"
STATUS = (
    ROOT / "contracts" / "mcp" / "registry" / "registry-submission-status-20260524.json"
)
CONTRACT = (
    ROOT
    / "contracts"
    / "mcp"
    / "registry"
    / "docker-mcp-registry-readiness-contract.md"
)
MCP_README = ROOT / "contracts" / "mcp" / "README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_docker_track_is_complete_for_submission_not_catalog_publication():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    status = json.loads(_read(STATUS))
    tracks = _read(TRACKS)

    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["publication_status"] == "submitted-review-pending"
    assert metadata["catalog_publication_claimed"] is False
    assert (TRACK / "review.md").exists()
    assert "- [x] **Track: Docker MCP Registry Readiness**" in tracks
    assert "./archive/docker_mcp_registry_readiness_20260517/" in tracks
    assert "./tracks/docker_mcp_registry_readiness_20260517/" not in tracks

    docker = status["registries"]["dockerMcpRegistry"]
    assert docker["status"] == "submitted_review_pending"
    assert (
        docker["activePullRequest"]
        == "https://github.com/docker/mcp-registry/pull/3799"
    )
    assert docker["catalogPublicationClaimed"] is False
    assert "2026-06-16" in docker["latestObservedReviewState"]
    assert "mergeable=MERGEABLE" in docker["latestObservedReviewState"]
    assert "mergeStateStatus=BLOCKED" in docker["latestObservedReviewState"]
    assert "reviewDecision=REVIEW_REQUIRED" in docker["latestObservedReviewState"]
    assert status["claimBoundary"]["dockerCatalogPublished"] is False
    assert status["claimBoundary"]["allRegistryPublicationsCompleted"] is False


def test_docker_submission_evidence_paths_and_claim_boundary_exist():
    for rel in [
        "Dockerfile",
        ".dockerignore",
        "contracts/mcp/registry/docker/submission.md",
        "contracts/mcp/registry/docker/servers/mchs/server.yaml",
        "contracts/mcp/registry/docker/servers/mchs/tools.json",
        "contracts/mcp/registry/docker/servers/mchs/readme.md",
    ]:
        assert (ROOT / rel).exists(), rel

    plan = _read(TRACK / "plan.md")
    assert "go run ./cmd/validate --name mchs" in plan
    assert "review-pending" in plan
    assert "Docker Catalog publication is not claimed" in _read(CONTRACT)
    assert "Docker Catalog publication remains review-pending" in _read(MCP_README)
    assert "On 2026-06-16" in _read(
        ROOT / "contracts/mcp/registry/docker/submission.md"
    )
