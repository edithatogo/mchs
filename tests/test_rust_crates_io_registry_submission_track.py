from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "rust_crates_io_registry_submission_20260524"
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _rust_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(
        registry
        for registry in data["registries"]
        if registry["id"] == "rust_crates_io"
    )


def test_rust_crates_io_track_is_published_verified():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _rust_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "completed"
    assert metadata["current_status"] == "published_verified"
    assert metadata["local_readiness_resolved"] is True
    assert metadata["publication_claimed"] is True
    assert metadata["publication_status"] == "published_verified"
    assert "- [x] **Track: Rust crates.io Registry Submission**" in tracks

    assert registry["current_status"] == "published_verified"
    assert registry["submission_url"] == "https://crates.io/crates/nwau-core/0.1.0"
    assert registry["localReadinessResolved"] is True
    assert registry["blocker"] is None


def test_rust_crates_io_evidence_records_publication_claim():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    plan = _read(TRACK / "plan.md")
    spec = _read(TRACK / "spec.md")
    evidence = metadata["package_evidence"]

    assert evidence["package_command"] == (
        "cargo package --allow-dirty --locked --manifest-path "
        "rust/crates/nwau-core/Cargo.toml"
    )
    assert "Packaged 16 files" in evidence["package_result"]
    assert (
        "cargo publish --dry-run --allow-dirty --locked"
        in evidence["publish_dry_run_command"]
    )
    assert (
        "aborted upload because this was a dry run"
        in evidence["publish_dry_run_result"]
    )
    assert evidence["auth_probe_command"] == "cargo owner --list nwau-core"
    assert "no token found" in evidence["auth_probe_result"]
    assert "committed and pushed" in evidence["workflow_clean_checkout_note"]
    assert evidence["public_url"] == "https://crates.io/crates/nwau-core/0.1.0"
    assert evidence["checksum"] == (
        "c755101f5e206a92892250f35a4474a7fcac1cebb6d4782a5b97f8f6aa243547"
    )
    assert evidence["yanked"] is False
    assert "Publication is verified" in plan
    assert "Published and verified" in spec
    assert "Credential cleanup complete" in evidence["secret_safety_note"]
