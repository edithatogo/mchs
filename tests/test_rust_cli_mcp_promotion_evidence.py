from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "contracts" / "runtime" / "rust-cli-mcp-promotion-matrix.json"
REPORT = ROOT / "docs" / "release-evidence-rust-cli-mcp-promotion.md"
DECISION = ROOT / "docs" / "adr" / "0008-rust-cli-mcp-runtime-promotion.md"
SCRIPT = ROOT / "scripts" / "validate_rust_cli_mcp_promotion.py"
WORKFLOW = ROOT / ".github" / "workflows" / "rust-cli-mcp-promotion.yml"


def _load_matrix() -> dict[str, object]:
    return json.loads(MATRIX.read_text(encoding="utf-8"))


def test_promotion_matrix_is_fail_closed_and_explicit() -> None:
    matrix = _load_matrix()
    assert matrix["defaultRuntimeDecision"] == "remain-python-default-rust-opt-in"
    assert matrix["rustDefaultAllowed"] is False

    surfaces = matrix["surfaces"]
    assert surfaces["cli.acute.2025.csv"]["status"] == "rust-opt-in"
    assert surfaces["mcp.calculate.acute.2025.json"]["status"] == "rust-opt-in"
    assert surfaces["mcp.validate_input.acute.2025.json"]["status"] == "rust-opt-in"
    assert surfaces["cli.ed.2025.csv"]["status"] == "python-only"
    assert surfaces["mcp.calculate.ed.2025.json"]["status"] == "unsupported"

    for surface_id, surface in surfaces.items():
        assert surface["defaultRuntime"] in {"python", "none"}
        assert surface["rustDefault"] is False, surface_id
        assert surface["evidence"], surface_id
        for evidence_path in surface["evidence"]:
            assert (ROOT / evidence_path).exists(), (surface_id, evidence_path)


def test_promotion_matrix_records_required_evidence_and_rollback() -> None:
    matrix = _load_matrix()
    evidence = matrix["requiredEvidenceForRustDefault"]

    assert "rust_core_tests" in evidence
    assert "python_compatibility_tests" in evidence
    assert "cli_parity_tests" in evidence
    assert "mcp_parity_tests" in evidence
    assert "unsupported_surface_inventory" in evidence
    assert matrix["rollback"]["cli"] == "--runtime python or unset NWAU_RUNTIME"
    assert matrix["rollback"]["mcp"] == 'omit options.runtime or set "python"'


def test_promotion_report_and_decision_do_not_overclaim_defaults() -> None:
    report = REPORT.read_text(encoding="utf-8")
    decision = DECISION.read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "Rust remains opt-in for CLI and MCP acute 2025" in report
    assert "No Rust-default surface is promoted" in report
    assert "Decision: keep Python/default compatibility" in decision
    assert "Rollback" in decision
    assert "No CLI or MCP Rust-default claim is made" in readme


def test_promotion_validator_fails_closed() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr or result.stdout
    payload = json.loads(result.stdout)
    assert payload["passed"] is True
    assert payload["rustDefaultAllowed"] is False
    assert payload["defaultRuntimeDecision"] == "remain-python-default-rust-opt-in"
    assert payload["surfaceCounts"]["rust-opt-in"] >= 3
    assert payload["surfaceCounts"]["unsupported"] >= 1


def test_promotion_workflow_runs_and_triggers_on_all_gate_inputs() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")

    for path in (
        "tests/test_rust_cli_mcp_promotion_evidence.py",
        "tests/test_rust_cli_core_migration.py",
        "tests/test_rust_mcp_core_migration.py",
        "tests/test_mcp_server.py",
        "tests/test_rust_migration_track_hardening.py",
        "scripts/validate_rust_cli_mcp_promotion.py",
        "scripts/validate_rust_migration_track_governance.py",
    ):
        assert path in workflow

    assert "python3 scripts/validate_rust_cli_mcp_promotion.py --json" in workflow
    assert "cargo test -p nwau-core -p nwau-c-abi" in workflow
