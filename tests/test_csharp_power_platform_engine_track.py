from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "csharp_power_platform_engine_20260504"
TRACKS = ROOT / "conductor" / "tracks.md"
CSHARP_ARCH = ROOT / "conductor" / "csharp-architecture.md"
POWER_PLATFORM = ROOT / "conductor" / "power-platform-boundary.md"
ADR = ROOT / "docs" / "adr" / "0005-web-and-power-platform-delivery.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_csharp_power_platform_track_archive_files_exist():
    for path in [
        TRACK / "metadata.json",
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "review.md",
    ]:
        assert path.exists(), path


def test_csharp_power_platform_metadata_records_bounded_scope():
    metadata = json.loads(_read(TRACK / "metadata.json"))

    assert metadata["track_id"] == "csharp_power_platform_engine_20260504"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert metadata["publication_status"] == "not-applicable"

    evidence = set(metadata["completion_evidence"])
    for expected in [
        "conductor/csharp-architecture.md",
        "conductor/power-platform-boundary.md",
        "docs/adr/0005-web-and-power-platform-delivery.md",
        "tests/test_csharp_architecture.py",
        "tests/test_rust_core_architecture_track.py",
        "tests/test_rust_core_boundary_contracts.py",
        "tests/test_csharp_power_platform_engine_track.py",
    ]:
        assert expected in evidence

    gaps = " ".join(gap["gap"].lower() for gap in metadata["gap_register"])
    assert "no executable c# calculation engine" in gaps
    assert "no nuget/package publication evidence" in gaps
    assert "no live power platform tenant/runtime validation" in gaps


def test_csharp_power_platform_registry_points_to_archive():
    registry = _read(TRACKS)

    assert "**Track: C# Calculation Engine and Power Platform Adapter**" in registry
    assert "./archive/csharp_power_platform_engine_20260504/" in registry
    assert "./tracks/csharp_power_platform_engine_20260504/" not in registry


def test_csharp_power_platform_docs_do_not_claim_formula_ownership():
    combined = "\n".join([_read(CSHARP_ARCH), _read(POWER_PLATFORM), _read(ADR)])

    assert "downstream adapter or service integration target" in combined
    assert "live in the Rust core rather than in C#" in combined
    assert "Power Platform should not duplicate formula logic" in combined
    assert "orchestration surface" in combined
    assert "not a C#-owned engine" in combined
