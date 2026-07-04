from __future__ import annotations

import hashlib
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
LIVE_PROBE = TRACK / "live_probe_20260705.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _r_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry for registry in data["registries"] if registry["id"] == "r_cran"
    )


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    assert "Live probe on 2026-07-05" in registry["blocker"]
    assert "public package publication remain pending" in registry["blocker"]


def test_r_cran_package_evidence_is_recorded_without_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _r_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert evidence["package_artifact"].endswith("nwauR_0.1.0.tar.gz")
    if PACKAGE.exists():
        assert evidence["package_sha256"] == _sha256(PACKAGE)
    assert (
        registry["preparationEvidence"]["packageSha256"] == evidence["package_sha256"]
    )
    assert evidence["check_result"] == "Status: OK"
    assert evidence["as_cran_check_result"] == "Status: OK"
    assert evidence["as_cran_check_note"] == "None"
    assert (
        "expected CRAN incoming 'New submission' note"
        in evidence["live_cran_remote_check_result"]
    )
    assert evidence["submission_surface"] == "https://cran.r-project.org/submit.html"
    assert "submitted" in evidence["submission_state"].lower()
    assert "user clicked the confirmation link" in evidence["submission_state"]
    assert (
        "CRAN Submission of nwauR 0.1.0 - Confirmation Link"
        in evidence["confirmation_email"]
    )
    assert "incoming/pretest" in evidence["next_required_evidence"]
    assert "successfully to CRAN submission team" in evidence["confirmation_result"]
    assert (
        "resolved to https://cran.r-project.org/web/packages/nwauR/index.html"
        in evidence["latest_publication_probe"]
    )
    assert "returned HTTP 404" in evidence["latest_publication_probe"]
    assert "CRANDB is not positive publication evidence" in evidence[
        "post_confirmation_public_probe"
    ]
    assert "Package: nwauR" in evidence["post_confirmation_public_probe"]
    assert "No accounts found" in evidence["latest_mail_probe"]
    assert (
        "https://cran.r-project.org/package=nwauR resolved to "
        "https://cran.r-project.org/web/packages/nwauR/index.html"
        in registry["preparationEvidence"]["latestPublicationProbe"]
    )
    assert "returned HTTP 404" in registry["preparationEvidence"][
        "latestPublicationProbe"
    ]
    assert (
        "https://cran.r-project.org/src/contrib/PACKAGES returned HTTP 200"
        in registry["preparationEvidence"]["latestPublicationProbe"]
    )
    assert "latestMailProbe" in registry["preparationEvidence"]
    assert (
        registry["preparationEvidence"]["asCranCheckResult"]
        == evidence["as_cran_check_result"]
    )
    assert (
        registry["preparationEvidence"]["asCranCheckNote"]
        == evidence["as_cran_check_note"]
    )
    assert (
        "expected CRAN incoming 'New submission' note"
        in registry["preparationEvidence"]["liveCranRemoteCheckResult"]
    )
    assert "Publication is not claimed" in plan
    assert "submitted_confirmed_pending_cran_pretest_review_publication" in plan


def test_r_cran_latest_live_probe_records_external_gate():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _r_registry()
    probe = json.loads(_read(LIVE_PROBE))

    evidence = metadata["package_evidence"]
    assert evidence["latest_live_probe_file"].endswith("live_probe_20260705.json")
    assert probe["checked_at"] == "2026-07-05T00:00:00+10:00"
    assert probe["publication_claimed"] is False
    assert probe["external_gate"] == (
        "CRAN incoming/pretest evidence, reviewer response if requested, "
        "and public package publication remain pending."
    )
    assert probe["probes"]["package_page"]["status"] == 404
    assert probe["probes"]["canonical_page"]["status"] == 404
    assert probe["probes"]["crandb"]["status"] == 404
    assert probe["probes"]["packages_index"]["status"] == 200
    assert probe["probes"]["packages_index"]["contains_package"] is False
    assert (
        "2026-07-05: https://cran.r-project.org/package=nwauR"
        in evidence["latest_publication_probe"]
    )
    assert "HTTP 404" in evidence["latest_publication_probe"]
    assert "Package: nwauR" in evidence["latest_publication_probe"]
    assert registry["preparationEvidence"]["latestLiveProbeFile"].endswith(
        "live_probe_20260705.json"
    )
    assert "2026-07-05" in registry["preparationEvidence"]["latestPublicationProbe"]


def test_r_package_source_matches_cran_ready_boundary():
    description = _read(ROOT / "r-binding" / "DESCRIPTION")
    readme = _read(ROOT / "r-binding" / "README.md")

    assert "LazyData:" not in description
    assert "nwau_py CLI module" in description
    assert "What this package provides" in readme
    assert "What this prototype provides" not in readme
