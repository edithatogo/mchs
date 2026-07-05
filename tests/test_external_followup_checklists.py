from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SWIFT_TRACK = (
    ROOT / "conductor" / "archive" / "swift_package_index_submission_20260524"
)
CONDA_TRACK = (
    ROOT / "conductor" / "tracks" / "conda_forge_feedstock_submission_20260524"
)
RUNBOOK = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "external-submission-runbook.md"
)
GATES = ROOT / "docs" / "roadmaps" / "language-registry-external-gates.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_swift_and_conda_followup_checklists_exist_and_are_linked():
    swift = _read(SWIFT_TRACK / "public_probe_checklist.md")
    conda = _read(CONDA_TRACK / "review_checklist.md")

    assert "Swift Package Index Public Probe Checklist" in swift
    assert "swiftpackageindex.com/edithatogo/mchs-swift" in swift
    assert "MCHSBind" in swift
    assert "403/404" in swift or "403" in swift or "404" in swift

    assert "conda-forge Review Checklist" in conda
    assert "staged-recipes" in conda
    assert "nwau-py" in conda
    assert "0.2.2" in conda

    runbook = _read(RUNBOOK)
    gates = _read(GATES)

    assert (
        "conductor/archive/swift_package_index_submission_20260524/public_probe_checklist.md"
        in runbook
    )
    assert (
        "conductor/tracks/conda_forge_feedstock_submission_20260524/review_checklist.md"
        in runbook
    )
    assert (
        "conductor/tracks/conda_forge_feedstock_submission_20260524/review_checklist.md"
        in gates
    )
