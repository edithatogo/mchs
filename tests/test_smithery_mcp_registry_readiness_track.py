from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "smithery_mcp_registry_readiness_20260517"
STATUS = (
    ROOT / "contracts" / "mcp" / "registry" / "registry-submission-status-20260524.json"
)
BUNDLE = ROOT / "contracts" / "mcp" / "registry" / "smithery" / "mchs-0.2.2.mcpb"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = ROOT / "contracts" / "mcp" / "registry" / "smithery-readiness-contract.md"
MCP_README = ROOT / "contracts" / "mcp" / "README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_smithery_track_is_complete_for_stdio_bundle_publication():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    tracks = _read(TRACKS)
    status = json.loads(_read(STATUS))

    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert metadata["publication_status"] == "published-stdio-bundle"
    assert metadata["hosted_streamable_http_status"] == "optional-future"
    assert "**Track: Smithery MCP Registry Readiness**" in tracks
    assert "- [x] **Track: Smithery MCP Registry Readiness**" in tracks

    smithery = status["registries"]["smithery"]
    assert smithery["status"] == "published_stdio_bundle"
    assert smithery["qualifiedName"] == "edithatogo/mchs"
    assert smithery["deploymentId"] == "200f2fd3-86c4-4122-b3bf-98abe5aa62f1"
    assert smithery["runtime"] == "python"
    assert smithery["listingPublicationClaimed"] is True
    assert smithery["registryApiObservation"]["connectionType"] == "stdio"
    assert status["claimBoundary"]["smitheryPublished"] is True


def test_smithery_bundle_checksum_and_claim_boundary_are_truthful():
    status = json.loads(_read(STATUS))
    smithery = status["registries"]["smithery"]

    assert BUNDLE.is_file()
    assert hashlib.sha256(BUNDLE.read_bytes()).hexdigest() == smithery["bundleSha256"]
    assert "stdio bundle" in _read(TRACK / "plan.md")
    assert "hosted Streamable HTTP publication remains optional/future" in _read(
        CONTRACT
    )
    assert "hosted Streamable HTTP publication remains optional/future" in _read(
        MCP_README
    )
