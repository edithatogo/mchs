from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKS = ROOT / "conductor" / "tracks"


def _metadata(track_id: str) -> dict[str, object]:
    return json.loads((TRACKS / track_id / "metadata.json").read_text())


def _text(track_id: str, filename: str) -> str:
    return (TRACKS / track_id / filename).read_text()


def test_rust_migration_tracks_have_normalized_metadata() -> None:
    expectations = {
        "rust_cli_core_migration_20260703": {
            "track_class": "binding",
            "current_state": "roadmap-only",
            "publication_status": "published-with-gaps",
        },
        "rust_mcp_core_migration_20260703": {
            "track_class": "binding",
            "current_state": "roadmap-only",
            "publication_status": "published-with-gaps",
        },
        "rust_cli_mcp_promotion_evidence_20260703": {
            "track_class": "validator",
            "current_state": "roadmap-only",
            "publication_status": "future-only",
        },
    }

    for track_id, expected in expectations.items():
        metadata = _metadata(track_id)
        for key, value in expected.items():
            assert metadata.get(key) == value, (track_id, key, metadata.get(key))


def test_rust_migration_governance_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_rust_migration_track_governance.py"],
        check=False,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr or result.stdout


def test_cli_migration_track_pins_runtime_selection_contract() -> None:
    spec = _text("rust_cli_core_migration_20260703", "spec.md")
    plan = _text("rust_cli_core_migration_20260703", "plan.md")
    combined = f"{spec}\n{plan}"

    assert "--runtime python|rust|auto" in combined
    assert "default runtime remains `python`" in combined
    assert "NWAU_RUNTIME" in combined
    assert "explicit CLI `--runtime` option takes precedence" in combined
    assert "fail closed" in combined


def test_mcp_migration_track_separates_transport_from_formula_runtime() -> None:
    spec = _text("rust_mcp_core_migration_20260703", "spec.md")
    plan = _text("rust_mcp_core_migration_20260703", "plan.md")
    combined = f"{spec}\n{plan}"

    assert "Python stdio transport" in combined
    assert "formula runtime" in combined
    assert "Rust-backed dispatcher" in combined
    assert "reuse the CLI runtime policy and parity fixtures" in combined
    assert "must not shell out to the CLI" in combined


def test_cli_and_mcp_tracks_pin_acute_2025_first_slice() -> None:
    cli = (
        _text("rust_cli_core_migration_20260703", "spec.md")
        + "\n"
        + _text("rust_cli_core_migration_20260703", "plan.md")
    )
    mcp = (
        _text("rust_mcp_core_migration_20260703", "spec.md")
        + "\n"
        + _text("rust_mcp_core_migration_20260703", "plan.md")
    )

    for combined in (cli, mcp):
        assert "acute 2025" in combined
        assert "first Rust-backed implementation slice" in combined
        assert "existing Rust canary/kernel evidence" in combined
        assert "follow-on coverage" in combined


def test_cli_and_mcp_plans_include_contract_hardening_prephase() -> None:
    for track_id in (
        "rust_cli_core_migration_20260703",
        "rust_mcp_core_migration_20260703",
    ):
        plan = _text(track_id, "plan.md")

        assert "Contract Hardening Pre-Phase" in plan
        assert "numeric tolerance and rounding policy" in plan
        assert "schema parity source" in plan
        assert "unsupported diagnostic codes" in plan
        assert "support-status wording" in plan
        assert "Rust canary, Rust opt-in, Python default, and Rust default" in plan


def test_status_matrix_recommends_hardening_before_migration_tracks() -> None:
    matrix = json.loads((ROOT / "conductor" / "status-matrix.json").read_text())
    recommended = matrix["recommendedNextTracks"]

    hardening = recommended.index("rust_migration_track_hardening_20260703")
    cli = recommended.index("rust_cli_core_migration_20260703")
    mcp = recommended.index("rust_mcp_core_migration_20260703")
    promotion = recommended.index("rust_cli_mcp_promotion_evidence_20260703")

    assert hardening < cli < mcp < promotion
