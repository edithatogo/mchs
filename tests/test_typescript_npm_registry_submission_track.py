from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "typescript_npm_registry_submission_20260524"
TRACK = ROOT / "conductor" / "tracks" / TRACK_ID
if not TRACK.exists():
    TRACK = ROOT / "conductor" / "archive" / TRACK_ID
TRACKS = ROOT / "conductor" / "tracks.md"
CONTRACT = (
    ROOT
    / "contracts"
    / "language-registry-submissions"
    / "language-registry-submissions.contract.json"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _typescript_registry() -> dict:
    data = json.loads(_read(CONTRACT))
    return next(registry for registry in data["registries"] if registry["id"] == "typescript_npm")


def test_typescript_npm_track_is_published_and_registered_complete():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _typescript_registry()
    tracks = _read(TRACKS)

    assert metadata["status"] == "completed"
    assert metadata["current_status"] == "published_verified"
    assert metadata["publication_claimed"] is True
    assert metadata["publication_url"] == registry["submission_url"]
    assert "- [x] **Track: TypeScript/WASM npm Registry Submission**" in tracks
    assert f"./archive/{TRACK_ID}/" in tracks or f"./tracks/{TRACK_ID}/" in tracks

    assert registry["current_status"] == "published_verified"
    assert registry["localReadinessResolved"] is True
    assert registry["blocker"] is None


def test_typescript_npm_publication_evidence_is_immutable():
    metadata = json.loads(_read(TRACK / "metadata.json"))
    registry = _typescript_registry()
    plan = _read(TRACK / "plan.md")
    spec = _read(TRACK / "spec.md")

    evidence = metadata["publication_evidence"]
    contract_evidence = registry["publicationEvidence"]
    assert evidence["name"] == "@edithatogo/mchs-wasm-binding"
    assert evidence["version"] == "0.1.0"
    assert evidence["tarball"] == contract_evidence["tarball"]
    assert evidence["integrity"] == contract_evidence["integrity"]
    assert evidence["published_at"] == contract_evidence["publishedAt"]
    assert "https://registry.npmjs.org/@edithatogo%2fmchs-wasm-binding" in plan
    assert "@edithatogo/mchs-wasm-binding@0.1.0" in spec
