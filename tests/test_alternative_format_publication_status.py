from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = (
    ROOT
    / "docs"
    / "roadmaps"
    / "release"
    / "alternative-format-publication-status-20260521.json"
)
MATRIX = ROOT / "docs" / "roadmaps" / "polyglot-packaging-release-matrix.md"


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_alternative_format_publication_status_is_fail_closed() -> None:
    status = _json(STATUS)

    assert status["claimBoundary"] == {
        "allAlternativeFormatsPublished": False,
        "registryPublicationComplete": False,
        "productionReadinessClaimed": False,
    }
    assert status["baselinePublishedSurface"]["surface"] == "Python"
    assert status["baselinePublishedSurface"]["alternativeFormat"] is False
    assert status["alternativeFormats"]
    assert all(item["published"] is False for item in status["alternativeFormats"])
    assert all(item["status"] != "published" for item in status["alternativeFormats"])


def test_alternative_format_publication_status_matches_release_matrix() -> None:
    status = _json(STATUS)
    matrix = MATRIX.read_text(encoding="utf-8")

    for item in status["alternativeFormats"]:
        assert item.get("matrixSurface", item["surface"]) in matrix

    normalized = " ".join(matrix.split())
    assert (
        "do not assert publication on any surface unless the target registry page"
        in normalized
    )
