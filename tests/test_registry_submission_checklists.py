from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUNBOOK = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "external-submission-runbook.md"
)


def _track(track_id: str) -> Path:
    for base in (ROOT / "conductor" / "tracks", ROOT / "conductor" / "archive"):
        candidate = base / track_id
        if candidate.exists():
            return candidate
    raise AssertionError(f"missing Conductor track or archive: {track_id}")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_maven_matlab_and_stata_tracks_have_submission_checklists():
    maven = _read(
        _track("jvm_maven_central_registry_submission_20260524")
        / "submission_checklist.md"
    )
    matlab = _read(
        _track("matlab_file_exchange_submission_20260524") / "submission_checklist.md"
    )
    stata = _read(_track("stata_ssc_submission_20260524") / "submission_checklist.md")

    assert "Maven Central Submission Checklist" in maven
    assert "Central Portal bundle" in maven
    assert "public signing key" in maven
    assert "Confirm Central can discover public signing key" in maven
    assert "successful deployment validated and published" in maven
    assert "Wait for Central to discover public signing key" not in maven
    assert (
        "repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml"
        in maven
    )

    assert "MATLAB File Exchange Submission Checklist" in matlab
    assert "mchs-matlab-interop-0.1.0.zip" in matlab
    assert "file-exchange-submission.json" in matlab
    assert "MathWorks File Exchange" in matlab

    assert "Stata SSC Submission Checklist" in stata
    assert "mchs-stata-interop-0.1.0.zip" in stata
    assert "pkg-mchs.pkg" in stata
    assert "installable from SSC" in stata


def test_external_submission_runbook_links_the_new_checklists():
    runbook = _read(RUNBOOK)

    assert (
        "conductor/archive/jvm_maven_central_registry_submission_20260524/submission_checklist.md"
        in runbook
    )
    assert (
        "conductor/archive/matlab_file_exchange_submission_20260524/submission_checklist.md"
        in runbook
    )
    assert (
        "conductor/archive/stata_ssc_submission_20260524/submission_checklist.md"
        in runbook
    )
