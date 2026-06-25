from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "rust_core_continuation_20260524"
TRACK = ROOT / "conductor" / "tracks" / TRACK_ID
if not TRACK.exists():
    TRACK = ROOT / "conductor" / "archive" / TRACK_ID
TRACKS = ROOT / "conductor" / "tracks.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_rust_core_continuation_keeps_rust_progression_active():
    for path in [
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACK / "spec.md",
        TRACK / "plan.md",
    ]:
        assert path.exists(), path

    metadata = json.loads(_read(TRACK / "metadata.json"))
    tracks = _read(TRACKS)
    spec = _read(TRACK / "spec.md")
    plan = _read(TRACK / "plan.md")

    assert metadata["track_id"] == "rust_core_continuation_20260524"
    assert metadata["track_class"] == "core"
    assert metadata["priority"] == "immediate"
    assert metadata["current_state"] == "complete"
    assert metadata["no_stub_enforce"] is True

    assert "**Track: Rust Core Continuation**" in tracks
    assert "stream-by-stream promotion" in tracks

    for phrase in [
        "Python remains the validated public baseline",
        "parity evidence",
        "release-candidate",
        "GA states",
        "shared contracts",
    ]:
        assert phrase in spec

    for phrase in [
        "Build a stream promotion matrix",
        "Write failing Rust and Python parity tests",
        "Implement the selected Rust kernel behavior",
        "Update support-status documentation and README claims",
    ]:
        assert phrase in plan


def test_rust_core_continuation_covers_required_streams_and_gates():
    plan = _read(TRACK / "plan.md")
    metadata = json.loads(_read(TRACK / "metadata.json"))

    for stream in [
        "acute",
        "ED",
        "admitted mental health",
        "community mental health",
        "subacute",
        "outpatient",
        "adjustment",
        "HAC",
        "AHR",
        "state/local pricing",
        "classification-adjacent",
    ]:
        assert stream in plan

    assert "rust-kernel-parity" in metadata["workstreams"]
    assert "python-binding-promotion" in metadata["workstreams"]
    assert "support-status" in metadata["workstreams"]
