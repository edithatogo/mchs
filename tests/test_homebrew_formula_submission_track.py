from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "homebrew_formula_submission_20260524"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
FORMULA = ROOT / "packaging" / "homebrew" / "nwau-py.rb"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _homebrew_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry for registry in data["registries"] if registry["id"] == "homebrew"
    )


def test_homebrew_track_is_published_to_personal_tap_with_core_review_optional():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _homebrew_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert metadata["current_status"] == "published_verified"
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is True
    assert metadata["publication_status"] == "published_verified"
    assert "- [x] **Track: Homebrew Formula Submission**" in tracks

    assert registry["current_status"] == "published_verified"
    assert registry["submission_url"] == "https://github.com/edithatogo/homebrew-mchs"
    assert registry["localReadinessResolved"] is True
    assert registry["blocker"] is None
    assert (
        "Homebrew/core publication requires upstream PR/review"
        in registry["preparationEvidence"]["remainingExternalBlocker"]
    )


def test_homebrew_formula_evidence_is_recorded_with_personal_tap_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _homebrew_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert FORMULA.exists()
    assert (
        evidence["source_sha256"]
        == "c0998035a2e0ceebe913717170994ef668159c6e384524932c55c18fc1ce0480"
    )
    assert "HTTP 404" in evidence["core_formula_api_result"]
    assert "default_branch=main" in evidence["tap_repository_api_result"]
    assert evidence["source_sha256"] in _read(FORMULA)
    assert "Click" in registry["preparationEvidence"]["fixedLocalBlocker"]
    assert "passed" in registry["preparationEvidence"]["auditResult"]
    assert "brew test" in registry["preparationEvidence"]["installTestResult"]
    assert "passed" in registry["preparationEvidence"]["installTestResult"]
    assert (
        "temporary inreplace patch"
        in registry["preparationEvidence"]["fixedFutureReleaseBlocker"]
    )
    assert "HTTP 404" in registry["preparationEvidence"]["latestCoreProbe"]
    assert "default_branch=main" in registry["preparationEvidence"]["latestTapProbe"]
    assert (
        registry["submissionEvidence"]["state"]
        == "published_to_personal_tap_audit_install_test_passing"
    )
    assert (
        registry["submissionEvidence"]["commit"]
        == "fa12ed26c1d6a289b40bf59c9bacbb9a5e42f823"
    )
    assert registry["publicationEvidence"]["scope"] == "personal_tap"
    assert registry["publicationEvidence"]["audit"] == "passed"
    assert registry["publicationEvidence"]["installTest"] == "passed"
    assert registry["publicationEvidence"]["sourceInstall"] == "passed"
    assert "personal Homebrew tap" in plan
    assert "optional upstream review gate" in plan
