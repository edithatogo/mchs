from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "tracks" / "rust_core_ga_20260513"
TRACKS = ROOT / "conductor" / "tracks.md"
ROADMAP = ROOT / "docs" / "roadmaps" / "rust-core-ga.md"
POLYGLOT = ROOT / "docs" / "roadmaps" / "polyglot-rust-core.md"
ARCHITECTURE = ROOT / "docs" / "roadmaps" / "polyglot-rust-core-architecture.md"
PROMOTION_MATRIX = ROOT / "docs" / "roadmaps" / "rust-core-promotion-matrix.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_rust_core_ga_is_completed_and_defers_adapter_tracks_to_evidence_gates():
    for path in [
        ROADMAP,
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACK / "spec.md",
        TRACK / "plan.md",
    ]:
        assert path.exists(), path

    metadata = json.loads(_read(TRACK / "metadata.json"))
    tracks = _read(TRACKS)
    roadmap = _read(ROADMAP)
    polyglot = _read(POLYGLOT)
    architecture = _read(ARCHITECTURE)

    assert metadata["track_id"] == "rust_core_ga_20260513"
    assert metadata["priority"] == "immediate"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete"
    assert metadata["deprioritizes"] == [
        "scala_spark_binding_20260513",
        "swift_binding_20260513",
        "stata_interop_binding_20260513",
        "matlab_interop_binding_20260513",
    ]

    assert "**Track: Rust Core GA**" in tracks
    assert "Immediate priority" in tracks
    for label in [
        "Scala/Spark Binding",
        "Swift Binding",
        "Stata Interoperability",
        "MATLAB Interoperability",
    ]:
        assert label in tracks
    assert tracks.count("audience/owner evidence gate") >= 3
    assert "Historical/deprioritized" in tracks

    for phrase in [
        "Rust Core GA Roadmap",
        "immediate priority",
        "greater than 90 percent",
        "SAS/Excel parity",
        "Rust crate",
        "CLI/file contract",
        "Python binding",
        "Arrow/Parquet",
        "Definition of done",
    ]:
        assert phrase in roadmap

    assert "Rust Core GA is now the immediate priority" in polyglot
    assert "Rust Core GA roadmap" in architecture


def test_rust_core_continuation_phase_1_promotion_matrix_is_conservative():
    assert PROMOTION_MATRIX.exists(), PROMOTION_MATRIX

    matrix = _read(PROMOTION_MATRIX)

    for heading in [
        "Rust Core Promotion Matrix",
        "State Vocabulary",
        "Stream Matrix",
        "Promotion Order",
        "Phase 1 Validation Notes",
    ]:
        assert heading in matrix

    for column in [
        "Stream or surface",
        "Current state",
        "Evidence",
        "Owner",
        "Next action",
        "Validation command",
    ]:
        assert column in matrix

    for stream in [
        "Acute admitted",
        "Emergency department",
        "Admitted mental health",
        "Community mental health",
        "Subacute",
        "Outpatient",
        "Adjustment factors",
        "Hospital-acquired complications (HAC)",
        "Avoidable hospital readmissions (AHR)",
        "State and local pricing",
        "Classification-adjacent surfaces",
    ]:
        assert stream in matrix

    assert "No stream is marked `GA` in this Phase 1 baseline." in matrix
    assert "| Acute admitted | `canary` |" in matrix
    assert "| Subacute | internal `canary` / public `blocked` |" in matrix
    assert "Missing source evidence stays `blocked` or `not-ready`" in matrix
