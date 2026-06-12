from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "r_cran_registry_submission_20260524"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
PACKAGE = ROOT / "nwauR_0.1.0.tar.gz"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _r_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(registry for registry in data["registries"] if registry["id"] == "r_cran")


def test_r_cran_track_is_submitted_pending_external_publication_review():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _r_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "submitted"
    assert (
        metadata["current_status"]
        == "submitted_confirmed_pending_cran_pretest_review_publication"
    )
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is False
    assert metadata["publication_status"] == "not_published"
    assert "- [~] **Track: R CRAN Registry Submission**" in tracks

    assert (
        registry["current_status"]
        == "submitted_confirmed_pending_cran_pretest_review_publication"
    )
    assert registry["submission_url"] == "https://cran.r-project.org/submit.html"
    assert registry["localReadinessResolved"] is True
    assert "confirmation link has been clicked" in registry["blocker"]


def test_r_cran_package_evidence_is_recorded_without_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _r_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert PACKAGE.exists()
    assert evidence["package_artifact"].endswith("nwauR_0.1.0.tar.gz")
    assert evidence["package_sha256"] == (
        "73e10d07e32153f8830b1b2a638637c058323963b34d854ead45deac9b849848"
    )
    assert registry["preparationEvidence"]["packageSha256"] == evidence["package_sha256"]
    assert evidence["check_result"] == "Status: OK"
    assert evidence["as_cran_check_result"] == "Status: OK"
    assert evidence["as_cran_check_note"] == "None"
    assert "expected CRAN incoming 'New submission' note" in evidence[
        "live_cran_remote_check_result"
    ]
    assert evidence["submission_surface"] == "https://cran.r-project.org/submit.html"
    assert "submitted" in evidence["submission_state"].lower()
    assert "user clicked the confirmation link" in evidence["submission_state"]
    assert "CRAN Submission of nwauR 0.1.0 - Confirmation Link" in evidence[
        "confirmation_email"
    ]
    assert "incoming/pretest" in evidence["next_required_evidence"]
    assert "successfully to CRAN submission team" in evidence["confirmation_result"]
    assert (
        registry["preparationEvidence"]["asCranCheckResult"]
        == evidence["as_cran_check_result"]
    )
    assert (
        registry["preparationEvidence"]["asCranCheckNote"]
        == evidence["as_cran_check_note"]
    )
    assert "expected CRAN incoming 'New submission' note" in registry[
        "preparationEvidence"
    ]["liveCranRemoteCheckResult"]
    assert "Publication is not claimed" in plan
    assert "submitted_confirmed_pending_cran_pretest_review_publication" in plan


def test_r_package_source_matches_cran_ready_boundary():
    description = _read(ROOT / "r-binding" / "DESCRIPTION")
    readme = _read(ROOT / "r-binding" / "README.md")

    assert "LazyData:" not in description
    assert "nwau_py CLI module" in description
    assert "What this package provides" in readme
    assert "What this prototype provides" not in readme
