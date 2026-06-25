from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks.md"

TRACK_IDS = [
    "support_status_matrix_20260513",
    "jurisdiction_price_source_index_20260513",
    "rust_crate_boundary_rename_20260513",
    "github_pages_api_architecture_20260513",
    "release_evidence_bundle_20260513",
]

ROADMAPS = [
    ROOT / "docs" / "roadmaps" / "coordination" / "parallel-agent-coordination.md",
    ROOT / "docs" / "roadmaps" / "schemas" / "support-status-matrix.md",
    ROOT / "docs" / "roadmaps" / "schemas" / "canonical-schema-priority.md",
    ROOT / "docs" / "roadmaps" / "jurisdiction-price-source-index.md",
    ROOT / "docs" / "roadmaps" / "rust-crate-boundaries.md",
    ROOT / "docs" / "roadmaps" / "github-pages-api-architecture.md",
    ROOT / "docs" / "roadmaps" / "openai-tool-adapter-strategy.md",
    ROOT / "docs" / "roadmaps" / "release" / "evidence-bundle-format.md",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _track_root(track_id: str) -> Path:
    root = ROOT / "conductor" / "tracks" / track_id
    if root.exists():
        return root
    return ROOT / "conductor" / "archive" / track_id


def test_coordination_notice_and_tracks_are_present():
    tracks = _read(TRACKS)

    for path in ROADMAPS:
        assert path.exists(), path

    for track_id in TRACK_IDS:
        root = _track_root(track_id)
        assert (root / "index.md").exists()
        assert (root / "metadata.json").exists()
        assert (root / "spec.md").exists()
        assert (root / "plan.md").exists()
        metadata = json.loads(_read(root / "metadata.json"))
        assert metadata["track_id"] == track_id
        assert metadata["status"] == "completed"
        assert track_id in tracks

    coordination = _read(ROADMAPS[0])
    assert "Parallel-agent notice" in coordination
    assert "Cline/deepseek" in coordination
    assert "stage only owned files" in coordination


def test_status_schema_release_and_architecture_guardrails_are_explicit():
    support = _read(ROOT / "docs" / "roadmaps" / "schemas" / "support-status-matrix.md")
    schemas = _read(
        ROOT / "docs" / "roadmaps" / "schemas" / "canonical-schema-priority.md"
    )
    crates = _read(ROOT / "docs" / "roadmaps" / "rust-crate-boundaries.md")
    pages = _read(ROOT / "docs" / "roadmaps" / "github-pages-api-architecture.md")
    openai = _read(ROOT / "docs" / "roadmaps" / "openai-tool-adapter-strategy.md")
    evidence = _read(
        ROOT / "docs" / "roadmaps" / "release" / "evidence-bundle-format.md"
    )

    for status in [
        "`unsupported`",
        "`blocked`",
        "`planned`",
        "`deferred`",
        "`canary`",
        "`opt_in`",
        "`preview`",
        "`release_candidate`",
        "`ga`",
        "`no_new_development`",
        "`historical`",
    ]:
        assert status in support

    for schema in [
        "support-status.schema.json",
        "calculator-request.schema.json",
        "hwau-output.schema.json",
        "price-schedule.schema.json",
        "valuation-output.schema.json",
        "evidence-bundle.schema.json",
    ]:
        assert schema in schemas

    assert "mchs-core" in crates
    assert "mchs-cli" in crates
    assert "mchs-mcp" in crates
    assert "mchs-dotnet" in crates
    assert "GitHub Pages cannot host a server-side API" in pages
    assert "Do not claim that GitHub Pages runs the production API backend" in pages
    assert "Generate OpenAI tool definitions from canonical schemas" in openai
    assert "Avoid `/v1/chat/completions`" in openai
    assert "SBOM" in evidence
    assert "If any required evidence is missing" in evidence
