from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks"
RUNBOOK = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "external-submission-runbook.md"
)


CHECKLISTS = {
    "vcpkg_conan": TRACKS
    / "c_cpp_vcpkg_conan_submission_20260524"
    / "upstream_pr_checklist.md",
    "conda_forge": TRACKS
    / "conda_forge_feedstock_submission_20260524"
    / "review_checklist.md",
    "docker_mcp": TRACKS
    / "docker_mcp_registry_readiness_20260517"
    / "requirements_notes.md",
    "maven_central": TRACKS
    / "jvm_maven_central_registry_submission_20260524"
    / "submission_checklist.md",
    "matlab_notes": TRACKS
    / "matlab_file_exchange_submission_20260524"
    / "file_exchange_submission_notes.md",
    "matlab_checklist": TRACKS
    / "matlab_file_exchange_submission_20260524"
    / "submission_checklist.md",
    "cran": TRACKS / "r_cran_registry_submission_20260524" / "submission_checklist.md",
    "smithery_mcp": TRACKS
    / "smithery_mcp_registry_readiness_20260517"
    / "requirements_notes.md",
    "stata_checklist": TRACKS
    / "stata_ssc_submission_20260524"
    / "submission_checklist.md",
    "swift_spi": TRACKS
    / "swift_package_index_submission_20260524"
    / "public_probe_checklist.md",
    "vscode_openvsx": TRACKS
    / "vscode_openvsx_registry_submission_20260524"
    / "access_checklist.md",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_registry_submission_checklists_are_present_and_indexed() -> None:
    runbook = _read(RUNBOOK)

    for path in CHECKLISTS.values():
        assert path.exists(), path
        relative = path.relative_to(ROOT).as_posix()
        assert relative in runbook


def test_registry_submission_checklists_are_fail_closed() -> None:
    required_phrases = {
        "vcpkg_conan": ["Do not mark the track complete", "ConanCenter", "vcpkg"],
        "conda_forge": ["Do not mark the track complete", "staged-recipes PR"],
        "docker_mcp": ["Remaining gate", "container_publication_evidence"],
        "maven_central": [
            "Do not mark the track complete",
            "io.github.edithatogo:mchs",
            "maven-metadata.xml",
        ],
        "matlab_checklist": ["Do not mark the track complete", "File Exchange"],
        "cran": ["Do not mark the track complete", "dylan.mordaunt@vuw.ac.nz"],
        "smithery_mcp": ["Remaining gate", "http_publication_evidence"],
        "stata_checklist": [
            "Do not mark the track complete",
            "installable from SSC",
            "Do not send maintainer email",
        ],
        "swift_spi": ["Do not mark the track complete", "swiftpackageindex.com"],
        "vscode_openvsx": [
            "Do not mark the track complete",
            "partial publication",
            "VSCE_PAT",
        ],
    }

    for checklist_id, phrases in required_phrases.items():
        text = _read(CHECKLISTS[checklist_id])
        for phrase in phrases:
            assert phrase in text, f"{checklist_id} missing {phrase!r}"


def test_stata_checklist_keeps_future_email_approval_gated() -> None:
    checklist = _read(CHECKLISTS["stata_checklist"])

    assert "http://fmwww.bc.edu/repec/bocode/m/mchs.pkg" in checklist
    assert "Do not send maintainer email" in checklist
    assert "without explicit approval" in checklist


def test_cran_metadata_uses_reachable_maintainer_email() -> None:
    description = _read(ROOT / "r-binding" / "DESCRIPTION")
    metadata = _read(TRACKS / "r_cran_registry_submission_20260524" / "metadata.json")
    runbook = _read(RUNBOOK)
    checklist = _read(CHECKLISTS["cran"])
    cran_comments = _read(ROOT / "r-binding" / "cran-comments.md")

    assert "dylan.mordaunt@vuw.ac.nz" in description
    assert "dylan.mordaunt@vuw.ac.nz" in metadata
    assert "dylan.mordaunt@vuw.ac.nz" in runbook
    assert "dylan.mordaunt@vuw.ac.nz" in checklist
    assert "dylan.mordaunt@vuw.ac.nz" in cran_comments
    assert "d.a.mordaunt@gmail.com" not in description
    assert "d.a.mordaunt@gmail.com" not in metadata
    assert "d.a.mordaunt@gmail.com" not in checklist
    assert "d.a.mordaunt@gmail.com" not in cran_comments
