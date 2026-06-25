from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "calculator_core_abstractions_20260504"
TRACKS = ROOT / "conductor" / "tracks.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_calculator_core_track_archive_files_exist():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "metadata.json",
        TRACK / "index.md",
        TRACK / "review.md",
    ]:
        assert path.exists(), path


def test_calculator_core_metadata_records_dependency_scope_and_evidence():
    metadata = json.loads(_read_text(TRACK / "metadata.json"))

    assert metadata["track_id"] == "calculator_core_abstractions_20260504"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert "public_api_contract_20260504" in metadata["dependencies"]
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert "nwau_py/contracts.py" in metadata["completion_evidence"]
    assert "nwau_py/reference_data.py" in metadata["completion_evidence"]


def test_calculator_core_registry_points_to_archive():
    registry = _read_text(TRACKS)

    assert "Calculator Core Abstraction and Validation Models" in registry
    assert "./archive/calculator_core_abstractions_20260504/" in registry


def test_calculator_core_spec_keeps_adapters_out_of_formula_logic():
    spec = _read_text(TRACK / "spec.md")

    assert "Calculator orchestration must be separate from deterministic formula logic" in spec
    assert "Reference data resolution must be deterministic" in spec
    assert "CLI, web, Python API, and C# adapters must not embed" in spec
