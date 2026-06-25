from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "duckdb_sql_binding_20260512"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
SUPPORT_MATRIX = ROOT / "contracts" / "support" / "support-matrix.json"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return cast(dict[str, Any], payload)


def test_duckdb_sql_track_is_historical_not_adapter_ready():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "binding_strategy.md",
        TRACK / "metadata.json",
        TRACKS_REGISTRY,
        SUPPORT_MATRIX,
    ]:
        assert path.exists(), path

    metadata = _load_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    strategy = _read_text(TRACK / "binding_strategy.md")
    tracks = _read_text(TRACKS_REGISTRY)
    support = _load_json(SUPPORT_MATRIX)
    entries = {entry["id"]: entry for entry in support["entries"]}

    assert metadata["track_id"] == "duckdb_sql_binding_20260512"
    assert metadata["status"] == "completed"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["support_scope"]
    assert metadata["gap_register"]
    assert (TRACK / "review.md").exists()
    assert metadata["primary_contract"] == (
        "none; retained as historical roadmap context"
    )
    assert metadata["completion_evidence"] == [
        "conductor/archive/duckdb_sql_binding_20260512/spec.md",
        "conductor/archive/duckdb_sql_binding_20260512/plan.md",
        "conductor/archive/duckdb_sql_binding_20260512/binding_strategy.md",
        "tests/test_duckdb_sql_binding_track.py",
        "contracts/support/support-matrix.json",
    ]

    sql_surface = entries["surface.sql-duckdb"]
    assert sql_surface["status"] == "historical"
    assert sql_surface["ready_for_implementation"] is False
    assert "Historical/deprioritized" in tracks
    assert "Do not develop SQL/DuckDB as an active surface" in tracks
    assert "./archive/duckdb_sql_binding_20260512/" in tracks
    assert "./tracks/duckdb_sql_binding_20260512/" not in tracks

    combined = "\n".join([spec, plan, strategy])
    for phrase in [
        "historical",
        "no current DuckDB extension",
        "no `contracts/sql-duckdb/`",
        "read/query file-boundary adapter",
        "pre-computed Parquet or CSV outputs",
        "must not host calculator formula logic",
    ]:
        assert phrase in combined


def test_duckdb_sql_has_no_live_contract_or_binding_folder():
    absent_paths = [
        ROOT / "contracts" / "sql-duckdb",
        ROOT / "duckdb",
        ROOT / "duckdb-binding",
        ROOT / "bindings" / "duckdb",
        ROOT / "bindings" / "sql-duckdb",
        ROOT / "sql-duckdb",
    ]

    for path in absent_paths:
        assert not path.exists(), path


def test_duckdb_sql_historical_notes_do_not_claim_formula_logic():
    text = "\n".join(
        _read_text(path)
        for path in [
            TRACK / "spec.md",
            TRACK / "plan.md",
            TRACK / "binding_strategy.md",
        ]
    ).lower()

    for forbidden in [
        "formula logic in sql",
        "classifier logic in sql",
        "grouper logic in sql",
        "duckdb adapter is ready",
        "production-ready",
        "preview-ready",
    ]:
        assert forbidden not in text
