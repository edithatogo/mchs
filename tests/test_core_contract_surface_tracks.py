from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks.md"
CORE_ROADMAP = ROOT / "docs" / "roadmaps" / "core-contract-surfaces.md"
AUDIENCE_ROADMAP = ROOT / "docs" / "roadmaps" / "audience-language-strategy.md"

TRACK_IDS = [
    "canonical_contract_foundation_20260513",
    "cli_file_contracts_20260513",
    "http_api_contract_20260513",
    "mcp_contract_20260513",
    "openai_tool_adapter_20260513",
    "audience_language_strategy_20260513",
]

ARCHIVED_TRACK_IDS = {
    "audience_language_strategy_20260513",
    "canonical_contract_foundation_20260513",
    "cli_file_contracts_20260513",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _track_root(track_id: str) -> Path:
    root = ROOT / "conductor" / "tracks" / track_id
    if root.exists():
        return root
    return ROOT / "conductor" / "archive" / track_id


def test_core_contract_surface_tracks_exist_and_are_ordered():
    tracks_text = _read(TRACKS)
    positions = []

    for track_id in TRACK_IDS:
        root = _track_root(track_id)
        assert (root / "index.md").exists()
        assert (root / "spec.md").exists()
        assert (root / "plan.md").exists()
        metadata = json.loads(_read(root / "metadata.json"))
        assert metadata["track_id"] == track_id
        assert metadata["status"] in {"new", "completed"}
        if root.parent.name == "archive":
            assert metadata["support_scope"]
            assert metadata["gap_register"]
            assert f"./archive/{track_id}/" in tracks_text
        assert track_id in tracks_text
        positions.append(tracks_text.index(track_id))

    assert positions == sorted(positions)
    assert tracks_text.index("rust_core_ga_20260513") < positions[0]


def test_http_api_openapi_contract_validates_without_duplicate_keys():
    result = subprocess.run(
        [sys.executable, "scripts/validate_http_api_contract.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_contract_surface_and_language_strategy_are_audience_driven():
    core = _read(CORE_ROADMAP)
    audience = _read(AUDIENCE_ROADMAP)

    for phrase in [
        "Canonical domain schemas",
        "CLI/file contracts",
        "HTTP API contract",
        "MCP contract",
        "OpenAI tool adapter",
        "Avoid exposing `/v1/chat/completions`",
    ]:
        assert phrase in core

    for phrase in [
        "Researchers",
        "Enterprise engineers",
        "Python",
        "R",
        "Julia",
        "CLI/file",
        "HTTP API",
        "MCP and OpenAI tool adapters",
        "Scala/Spark",
        "MATLAB",
    ]:
        assert phrase in audience
