from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "deferred_surface_cleanup_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
AUDIENCE = ROOT / "docs" / "roadmaps" / "audience-language-strategy.md"
DEFERRED = ROOT / "docs" / "roadmaps" / "deferred-surface-status.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_deferred_surface_cleanup_archive_files_exist():
    for path in [
        TRACK / "metadata.json",
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "review.md",
    ]:
        assert path.exists(), path


def test_deferred_surface_cleanup_metadata_is_bounded():
    metadata = json.loads(_read(TRACK / "metadata.json"))

    assert metadata["track_id"] == "deferred_surface_cleanup_20260513"
    assert metadata["track_class"] == "governance"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]
    assert metadata["gap_register"]

    evidence = set(metadata["completion_evidence"])
    for expected in [
        "docs/roadmaps/audience-language-strategy.md",
        "docs/roadmaps/deferred-surface-status.md",
        "tests/test_deferred_surface_cleanup_track.py",
    ]:
        assert expected in evidence


def test_deferred_surface_cleanup_registry_points_to_archive():
    registry = _read(TRACKS)

    assert "**Track: Deferred Surface Cleanup**" in registry
    assert "./archive/deferred_surface_cleanup_20260513/" in registry
    assert "./tracks/deferred_surface_cleanup_20260513/" not in registry


def test_deferred_surface_docs_prevent_support_overclaims():
    audience = _read(AUDIENCE)
    deferred = _read(DEFERRED)
    combined = f"{audience}\n{deferred}"

    for phrase in [
        "no_new_development",
        "historical",
        "No surface may claim GA status without completing all eight criteria.",
        "A package manifest is not registry publication evidence.",
        "A contract schema is not implementation evidence.",
        "A binding is complete only if it delegates to the shared core",
    ]:
        assert phrase in combined
    assert "audience/owner evidence gate" in combined.lower()

    for forbidden in [
        "Scala/Spark | GA",
        "Swift | GA",
        "MATLAB | GA",
        "SQL/DuckDB | GA",
    ]:
        assert forbidden not in combined
