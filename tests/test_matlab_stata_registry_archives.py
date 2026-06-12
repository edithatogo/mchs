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
        (
            ROOT
            / "conductor"
            / "tracks"
            / "matlab_file_exchange_submission_20260524"
            / "metadata.json"
        ).read_text(encoding="utf-8")
    )

    assert registry["current_status"] == "prepared_pending_file_exchange_upload_review"
    assert metadata["publication_claimed"] is False
    assert registry["submission_url"] is None
    assert evidence["sha256"] == _sha256(MATLAB_BUNDLE)
    assert metadata["package_evidence"]["bundle_sha256"] == evidence["sha256"]

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
    assert submission["publication_claimed"] is False
    squashed_readme = _squash(readme)
    assert "no MathWorks File Exchange upload has been performed" in squashed_readme
    assert "MATLAB/Octave are not installed" in squashed_readme


def test_stata_ssc_bundle_matches_registry_evidence():
    registry = _contract_registry("stata_ssc")
    evidence = registry["preparationEvidence"]
    metadata = json.loads(
        (
            ROOT
            / "conductor"
            / "tracks"
            / "stata_ssc_submission_20260524"
            / "metadata.json"
        ).read_text(encoding="utf-8")
    )

    assert registry["current_status"] == "submitted_pending_ssc_maintainer_review"
    assert metadata["publication_claimed"] is False
    assert registry["submission_url"] == "mailto:baum@bc.edu"
    assert evidence["sha256"] == _sha256(STATA_BUNDLE)
    assert metadata["package_evidence"]["bundle_sha256"] == evidence["sha256"]
    assert "submissionEmailEvidence" in evidence
    assert "maintainerIdentityClarification" in evidence
    assert "d.a.mordaunt@gmail.com" in evidence["latestEmailProbe"]
    assert "no inbound SSC maintainer response has been captured" in evidence[
        "latestEmailProbe"
    ]

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
    assert "No SSC submission has been performed or claimed" in squashed_readme
    assert "Stata is not installed" in squashed_readme
