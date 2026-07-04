from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "conda_forge_feedstock_submission_20260524"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
RECIPE = ROOT / "packaging" / "conda-forge" / "meta.yaml"
LIVE_PROBE = TRACK / "live_probe_20260705.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _conda_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry for registry in data["registries"] if registry["id"] == "conda_forge"
    )


def test_conda_forge_track_is_blocked_by_feedstock_pr_review():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _conda_registry()
    tracks = _read(TRACKS)

    assert (TRACK / "review.md").exists()
    assert metadata["status"] == "submitted"
    assert (
        metadata["current_status"]
        == "submitted_checks_passed_pending_staged_recipes_review"
    )
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is False
    assert metadata["publication_status"] == "not_published"
    assert "- [~] **Track: conda-forge Feedstock Submission**" in tracks

    assert (
        registry["current_status"]
        == "submitted_checks_passed_pending_staged_recipes_review"
    )
    assert (
        registry["submission_url"]
        == "https://github.com/conda-forge/staged-recipes/pull/33452"
    )
    assert registry["localReadinessResolved"] is True
    assert "linux_64, osx_64, win_64" in registry["blocker"]
    assert "maintainer review/merge/feedstock publication" in registry["blocker"]


def test_conda_forge_recipe_evidence_is_recorded_without_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _conda_registry()
    plan = _read(TRACK / "plan.md")

    evidence = metadata["package_evidence"]
    assert RECIPE.exists()
    assert (
        evidence["source_sha256"]
        == "c0998035a2e0ceebe913717170994ef668159c6e384524932c55c18fc1ce0480"
    )
    assert evidence["source_sha256"] in _read(RECIPE)
    assert "build:" in _read(RECIPE)
    assert "number: 0" in _read(RECIPE)
    assert "license_file: LICENSE" in _read(RECIPE)
    assert "recipe-maintainers:" in _read(RECIPE)
    assert "funding-calculator --help" in _read(RECIPE)
    assert (
        "review, merge, and feedstock publication"
        in registry["preparationEvidence"]["remainingExternalBlocker"]
    )
    assert "fixedLintFeedback" in registry["preparationEvidence"]
    assert (
        registry["submissionEvidence"]["state"]
        == "open_checks_passed_pending_staged_recipes_review"
    )
    assert (
        registry["submissionEvidence"]["commit"]
        == "bffc5bf1a85389dc695adfd96c87bf2413f4db25"
    )
    assert (
        "bffc5bf1a85389dc695adfd96c87bf2413f4db25"
        in metadata["package_evidence"]["branch_update"]
    )
    assert "conda-forge-linter" in metadata["package_evidence"]["branch_update"]
    assert "state=open" in metadata["package_evidence"]["latest_live_pr_probe"]
    assert (
        "nwau-py-feedstock repository still return HTTP 404"
        in metadata["package_evidence"]["latest_live_pr_probe"]
    )
    assert "Publication is not claimed" in plan


def test_conda_forge_latest_live_probe_records_external_gate():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    probe = json.loads(_read(LIVE_PROBE))

    assert probe["checked_at"] == "2026-07-05T00:00:00+10:00"
    assert probe["submission_pr"]["state"] == "OPEN"
    assert probe["submission_pr"]["merged_at"] is None
    assert probe["submission_pr"]["head_sha"] == (
        "bffc5bf1a85389dc695adfd96c87bf2413f4db25"
    )
    assert probe["submission_pr"]["checks"] == "passing"
    assert probe["anaconda_package"]["status_code"] == 404
    assert probe["feedstock_repository"]["status_code"] == 404
    assert probe["publication_claimed"] is False
    assert probe["next_action"] == "wait-for-conda-forge-maintainer-review"
    assert metadata["package_evidence"]["latest_live_probe_file"] == str(
        LIVE_PROBE.relative_to(ROOT)
    )
