from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "starlight_docs_site_20260506"
CONDUCTOR_INDEX = ROOT / "conductor" / "index.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_starlight_docs_site_track_metadata_and_docs_exist():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    index = _read_text(TRACK / "index.md")
    conductor_index = _read_text(CONDUCTOR_INDEX)

    assert metadata["track_id"] == "starlight_docs_site_20260506"
    assert metadata["type"] == "feature"
    assert metadata["status"] in {"complete", "completed"}
    assert metadata["created_at"] == "2026-05-06T08:18:23Z"
    assert metadata["updated_at"] == "2026-05-06T12:48:04Z"
    assert metadata["description"] == "Starlight documentation site and versioning"
    assert metadata.get("track_class") == "publication"
    assert metadata.get("current_state") == "complete"
    assert metadata.get("completion_evidence") == ["docs", "workflows", "tests"]

    assert "Starlight-based static site" in spec
    assert "@astrojs/starlight" in spec
    assert "0.38.5" in spec
    assert "starlight-links-validator" in spec
    assert "starlight-openapi" in spec
    assert "Pagefind" in spec
    assert "GitHub Pages" in spec
    assert "De-implement temporary or legacy docs entry points" in spec

    assert "Roadmap, Versioning, and Site Contract" in plan
    assert "Scaffold and Content Migration" in plan
    assert "De-implementation and Deployment" in plan
    assert "Refinement and Feature Completion" in plan
    assert "Conductor - Automated Review and Checkpoint" in plan

    assert "Specification" in index
    assert "Implementation Plan" in index
    assert "Metadata" in index
    assert (
        "[Starlight Docs Site Track](./archive/starlight_docs_site_20260506/)"
        in conductor_index
    )
