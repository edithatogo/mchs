from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)
TRACKS = ROOT / "conductor" / "tracks"
TRACKS_MD = ROOT / "conductor" / "tracks.md"
REQUIRED_PHASES = ["Discovery", "Preparation", "Submission", "Publication Evidence"]


def main() -> None:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert data["claimBoundary"]["allRegistryTracksCreated"] is True
    assert data["claimBoundary"]["allRegistrySubmissionsCompleted"] is False
    assert data["claimBoundary"]["allRegistryPublicationsVerified"] is False

    tracks_md = TRACKS_MD.read_text(encoding="utf-8")
    registries = data["registries"]
    assert len(registries) >= 15
    seen = set()

    for registry in registries:
        track_id = registry["track"]
        assert track_id not in seen, track_id
        seen.add(track_id)

        track_dir = TRACKS / track_id
        assert track_dir.exists(), track_id
        for filename in ("metadata.json", "spec.md", "plan.md", "index.md"):
            assert (track_dir / filename).exists(), f"{track_id}/{filename}"

        metadata = json.loads((track_dir / "metadata.json").read_text(encoding="utf-8"))
        assert metadata["track_id"] == track_id
        assert metadata["registry_id"] == registry["id"]
        assert metadata["current_status"] == registry["current_status"], track_id
        assert (
            metadata["local_readiness_resolved"] == registry["localReadinessResolved"]
        )

        if registry["current_status"] == "published_verified":
            assert registry["blocker"] is None, registry["id"]
            assert metadata["status"] == "completed", track_id
            assert metadata["publication_claimed"] is True, track_id
            assert metadata["publication_status"] == "published_verified", track_id
            assert f"- [x] **Track: {registry['title']}**" in tracks_md, track_id
        else:
            assert registry["blocker"], registry["id"]
            assert metadata["status"] in {"blocked", "submitted"}, track_id
            assert metadata["publication_claimed"] is False, track_id
            assert metadata["publication_status"] != "published_verified", track_id
            assert f"- [~] **Track: {registry['title']}**" in tracks_md, track_id

        spec = (track_dir / "spec.md").read_text(encoding="utf-8")
        plan = (track_dir / "plan.md").read_text(encoding="utf-8")
        assert registry["registry"] in spec
        assert registry["package"] in spec
        for phase in REQUIRED_PHASES:
            assert "## Phase" in plan and phase in plan, f"{track_id} missing {phase}"
        assert f"./tracks/{track_id}/" in tracks_md

    print("Language registry submission tracks contract passed.")


if __name__ == "__main__":
    main()
