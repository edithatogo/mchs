from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MAVEN_TRACK = ROOT / "conductor" / "tracks" / "jvm_maven_central_registry_submission_20260524"
MATLAB_TRACK = ROOT / "conductor" / "tracks" / "matlab_file_exchange_submission_20260524"
STATA_TRACK = ROOT / "conductor" / "tracks" / "stata_ssc_submission_20260524"
RUNBOOK = ROOT / "contracts" / "language-registry-submissions" / "external-submission-runbook.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_maven_matlab_and_stata_tracks_have_submission_checklists():
    maven = _read(MAVEN_TRACK / "submission_checklist.md")
    matlab = _read(MATLAB_TRACK / "submission_checklist.md")
    stata = _read(STATA_TRACK / "submission_checklist.md")

    assert "Maven Central Submission Checklist" in maven
    assert "Central Portal bundle" in maven
    assert "public signing key" in maven
    assert "repo1.maven.org/maven2/io/github/edithatogo/mchs-jvm-bindings/maven-metadata.xml" in maven

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
        "conductor/tracks/jvm_maven_central_registry_submission_20260524/submission_checklist.md"
        in runbook
    )
    assert (
        "conductor/tracks/matlab_file_exchange_submission_20260524/submission_checklist.md"
        in runbook
    )
    assert (
        "conductor/tracks/stata_ssc_submission_20260524/submission_checklist.md"
        in runbook
    )
