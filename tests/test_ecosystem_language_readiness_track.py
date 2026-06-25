from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "ecosystem_language_readiness_20260507"
CONDUCTOR_INDEX = ROOT / "conductor" / "index.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ecosystem_language_readiness_track_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "parallelization.md",
        TRACK / "standards-matrix.md",
        TRACK / "health_standards.md",
        TRACK / "community_pathways.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
    ]:
        assert path.exists(), path


def test_ecosystem_language_readiness_track_scope_is_recorded():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    parallelization = _read_text(TRACK / "parallelization.md")
    matrix = _read_text(TRACK / "standards-matrix.md")
    health_standards = _read_text(TRACK / "health_standards.md")
    community_pathways = _read_text(TRACK / "community_pathways.md")
    track_index = _read_text(TRACK / "index.md")
    conductor_index = _read_text(CONDUCTOR_INDEX)

    assert metadata["status"] in {"complete", "completed"}
    assert metadata["track_id"] == "ecosystem_language_readiness_20260507"
    assert metadata["updated_at"] == "2026-05-07T01:03:51Z"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert (TRACK / "review.md").exists()

    for phrase in [
        "Python was the only executable calculator package surface in this snapshot",
        "docs-site is an npm-managed Astro/Starlight surface",
        "No R package, Julia package, C# solution/project",
        "Package/version management evidence precedes any language readiness claim",
        "Shared public contracts and golden fixtures precede any non-Python",
        "Health standards are documented separately as advisory guidance",
        "citation metadata",
        "manifest-level version pinning",
        "package-surface tracks supersede its inventory rows",
    ]:
        assert phrase in spec

    for phase in [
        "Repository Inventory and Matrix Schema",
        "Ecosystem Standards and Decision Criteria",
        "Governance and Boundary Notes",
        "health standards guidance and watch-list items",
    ]:
        assert phase in plan

    assert "Conductor - Automated Review and Checkpoint" in plan
    assert "Document the canonical matrix schema" in plan
    assert "Health Standards" in track_index
    assert "Community Contribution Pathways" in track_index
    assert "Ecosystem Standards and Language Readiness Track" in conductor_index

    for phrase in [
        "Subagent Workstreams",
        "Write Ownership",
        "Merge Order",
        "Python package readiness",
        "Docs-site package maturity",
        "Deferred surfaces",
        "current evidence, transitional artifacts, and intended-state guidance",
    ]:
        assert phrase in parallelization

    for phrase in [
        "Python and docs-site",
        "C#",
        "Power Platform",
        "R package or wrapper",
        "Julia package or kernel complete-with-gaps",
        "implemented, documented-only, missing, and deferred",
        "Package/version management evidence precedes any language readiness claim",
        "dated snapshot inventory",
    ]:
        assert phrase in matrix

    for phrase in [
        "ICD-10-AM",
        "ACHI",
        "ACS",
        "AR-DRG",
        "HL7 v2",
        "FHIR R4",
        "IHE PAM, PDQ, PIX, PIXm, PDQm, and PMIR",
    ]:
        assert phrase in health_standards

    for phrase in [
        "pyOpenSci",
        "rOpenSci",
        "JOSS",
        "license",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "CITATION.cff",
    ]:
        assert phrase in community_pathways

    for phrase in [
        "PEP 621-style metadata",
        "with `mypy` treated as",
        "Documentation that explains install, usage, validation, and the supported",
        "Community and governance files such as `LICENSE`, `CONTRIBUTING.md`,",
        "`CODE_OF_CONDUCT.md`, and `CITATION.cff` where publication readiness is",
        "versioned release artifact",
    ]:
        assert phrase in _read_text(TRACK / "python_readiness.md")
