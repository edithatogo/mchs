from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
MATLAB_BUNDLE = ROOT / "bindings" / "matlab" / "mchs-matlab-interop-0.1.0.zip"
STATA_BUNDLE = ROOT / "bindings" / "stata" / "mchs-stata-interop-0.1.0.zip"


def _track(track_id: str) -> Path:
    for base in (ROOT / "conductor" / "tracks", ROOT / "conductor" / "archive"):
        candidate = base / track_id
        if candidate.exists():
            return candidate
    raise AssertionError(f"missing Conductor track or archive: {track_id}")


def _contract_registry(registry_id: str) -> dict:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    return next(item for item in contract["registries"] if item["id"] == registry_id)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _zip_names(path: Path) -> set[str]:
    with ZipFile(path) as archive:
        return set(archive.namelist())


def _squash(text: str) -> str:
    return " ".join(text.split())


def test_matlab_file_exchange_bundle_matches_registry_evidence():
    registry = _contract_registry("matlab_file_exchange")
    evidence = registry["preparationEvidence"]
    metadata = json.loads(
        (_track("matlab_file_exchange_submission_20260524") / "metadata.json").read_text(
            encoding="utf-8"
        )
    )

    assert registry["current_status"] == "published_verified"
    assert metadata["publication_claimed"] is True
    assert (
        registry["submission_url"]
        == "https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop"
    )
    assert evidence["sha256"] == _sha256(MATLAB_BUNDLE)
    assert metadata["package_evidence"]["bundle_sha256"] == evidence["sha256"]
    assert "184067-mchs-matlab-interop" in evidence["latestPublicProbe"]
    assert "version 0.1.0" in evidence["latestPublicProbe"]
    assert evidence["remainingExternalBlocker"] is None
    assert (
        "184067-mchs-matlab-interop"
        in metadata["package_evidence"]["latest_public_probe"]
    )
    assert metadata["package_evidence"]["remaining_external_blocker"] is None
    assert registry["publicationEvidence"]["version"] == "0.1.0"
    assert registry["publicationEvidence"]["submissionId"] == "184067"

    names = _zip_names(MATLAB_BUNDLE)
    assert {
        "README.md",
        "LICENSE",
        "file-exchange-submission.json",
        "matlab-interop-notes.md",
        "mchs/README.md",
        "mchs/validateInput.m",
        "mchs/importResultTable.m",
        "mchs/invokeCli.m",
        "examples/cli_invocation_demo.m",
        "examples/file_import_demo.m",
    }.issubset(names)

    with ZipFile(MATLAB_BUNDLE) as archive:
        submission = json.loads(
            archive.read("file-exchange-submission.json").decode("utf-8")
        )
        readme = archive.read("README.md").decode("utf-8")

    assert submission["license"] == "MIT"
    assert submission["publication_claimed"] is True
    assert (
        submission["publication_url"]
        == "https://www.mathworks.com/matlabcentral/fileexchange/184067-mchs-matlab-interop"
    )
    squashed_readme = _squash(readme)
    assert "published on MathWorks File Exchange as version `0.1.0`" in squashed_readme
    assert "MATLAB/Octave are not installed" in squashed_readme


def test_stata_ssc_bundle_matches_registry_evidence():
    registry = _contract_registry("stata_ssc")
    evidence = registry["preparationEvidence"]
    metadata = json.loads(
        (_track("stata_ssc_submission_20260524") / "metadata.json").read_text(
            encoding="utf-8"
        )
    )

    assert registry["current_status"] == "published_verified"
    assert metadata["publication_claimed"] is True
    assert registry["submission_url"] == "http://fmwww.bc.edu/repec/bocode/m/mchs.pkg"
    assert evidence["sha256"] == _sha256(STATA_BUNDLE)
    assert metadata["package_evidence"]["bundle_sha256"] == evidence["sha256"]
    assert "submissionEmailEvidence" in evidence
    assert "maintainerIdentityClarification" in evidence
    assert "maintainerFeedback" in evidence
    assert "feedbackFix" in evidence
    assert "emailSendGuardrail" in evidence
    assert "correctedArchiveReplyDraft" in evidence
    assert "fionnandniamh@gmail.com" in evidence["latestEmailProbe"]
    assert (
        "author contact information seems to be missing" in evidence["latestEmailProbe"]
    )
    assert (
        "No outbound response with the corrected archive was sent"
        in evidence["latestEmailProbe"]
    )
    assert "explicit user approval" in evidence["emailSendGuardrail"]
    assert evidence["remainingExternalBlocker"] is None
    assert "latestPublicProbe" in evidence
    assert "mchs.pkg" in evidence["latestPublicProbe"]
    assert "mchs.ado" in evidence["latestPublicProbe"]
    assert "mchs.sthlp" in evidence["latestPublicProbe"]
    assert registry["publicationEvidence"]["url"] == (
        "http://fmwww.bc.edu/repec/bocode/m/mchs.pkg"
    )
    assert registry["publicationEvidence"]["packageName"] == "mchs"
    assert registry["publicationEvidence"]["localArchiveVersion"] == "0.1.0"

    names = _zip_names(STATA_BUNDLE)
    assert {
        "mchs.ado",
        "mchs.sthlp",
        "pkg-mchs.pkg",
        "README.md",
        "LICENSE",
        "stata-interop-notes.md",
        "examples/file_import_workflow.do",
        "examples/nwau_cli_invocation.do",
    }.issubset(names)

    with ZipFile(STATA_BUNDLE) as archive:
        package_manifest = archive.read("pkg-mchs.pkg").decode("utf-8")
        help_file = archive.read("mchs.sthlp").decode("utf-8")
        readme = archive.read("README.md").decode("utf-8")

    for required_file in [
        "F mchs.ado",
        "F mchs.sthlp",
        "F README.md",
        "F LICENSE",
        "F examples/file_import_workflow.do",
        "F examples/nwau_cli_invocation.do",
    ]:
        assert required_file in package_manifest

    squashed_readme = _squash(readme)
    squashed_help = _squash(help_file)
    assert "published on the Boston College SSC/RePEc archive" in squashed_readme
    assert "no Stata runtime validation is claimed" in squashed_readme
    assert "dylan mordaunt" in squashed_readme.lower()
    assert "dylan.mordaunt@vuw.ac.nz" in squashed_readme
    assert "dylan mordaunt" in squashed_help.lower()
    assert "dylan.mordaunt@vuw.ac.nz" in squashed_help
    assert "Stata is not installed" in squashed_readme
