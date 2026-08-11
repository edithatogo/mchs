from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pytest
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nwau_py import mcp_server, rust_bridge
from nwau_py.cli import main as cli_main


def _structured(result: dict[str, Any]) -> dict[str, Any]:
    return cast(dict[str, Any], result["structuredContent"])


def _acute_fixture_row() -> dict[str, Any]:
    return cast(
        dict[str, Any],
        pd.read_csv("tests/fixtures/golden/acute_2025/input.csv").iloc[0].to_dict(),
    )


def test_mcp_runtime_boundary_documents_contract_terms():
    boundary = Path("docs/roadmaps/rust-mcp-runtime-boundary.md").read_text(
        encoding="utf-8"
    )
    inventory = Path("docs/roadmaps/rust-mcp-surface-inventory.md").read_text(
        encoding="utf-8"
    )

    assert "Python stdio transport" in boundary
    assert "Rust opt-in" in boundary
    assert "options.runtime" in boundary
    assert "rtol=1e-4" in boundary
    assert "atol=1e-4" in boundary
    assert "MCHS-MCP-RUST-UNSUPPORTED" in boundary
    assert "must not shell out to the CLI" in boundary
    assert "`mchs.calculate`" in inventory
    assert "Rust opt-in for `acute` year `2025`" in inventory


def test_mcp_support_status_separates_transport_from_formula_runtime():
    payload = json.loads(
        mcp_server.read_resource("mchs://support/status")["contents"][0]["text"]
    )

    assert payload["transport"]["runtime"] == "python-stdio"
    assert payload["formulaRuntime"]["rustOptIn"]["calculatorId"] == "acute"
    assert payload["formulaRuntime"]["rustOptIn"]["year"] == "2025"
    assert payload["formulaRuntime"]["default"] == "python-boundary"


def test_mcp_calculate_accepts_rust_runtime_for_acute_2025(monkeypatch):
    def rust_calculator(df, params, *, year, ref_dir=None):
        output = df.copy()
        output[f"NWAU{year[-2:]}"] = 2.5
        return output

    monkeypatch.setattr(
        mcp_server.acute_calculator, "calculate_acute_rust_2025", rust_calculator
    )

    result = mcp_server.call_tool(
        "mchs.calculate",
        {
            "calculatorId": "acute",
            "year": "2025",
            "inputs": _acute_fixture_row(),
            "options": {"runtime": "rust", "refDir": "tests/data/2025"},
        },
    )
    payload = _structured(result)

    assert payload["calculatorId"] == "acute"
    assert payload["runtime"] == "rust"
    assert payload["result"]["NWAU25"] == 2.5
    assert payload["provenance"]["formulaRuntime"] == "rust"


def test_mcp_validate_input_accepts_rust_runtime_for_acute_2025(monkeypatch):
    calls = []

    def build_contract(*, params, year, ref_dir=None, **_kwargs):
        calls.append((year, ref_dir))
        return {"year": year}

    def validate_frame(df, contract):
        assert df.iloc[0]["DRG"] == _acute_fixture_row()["DRG"]
        assert contract["year"] == "2025"

    monkeypatch.setattr(
        mcp_server.acute_calculator, "build_acute_contract", build_contract
    )
    monkeypatch.setattr(
        mcp_server.acute_calculator, "validate_acute_input_frame", validate_frame
    )

    result = mcp_server.call_tool(
        "mchs.validate_input",
        {
            "calculatorId": "acute",
            "year": "2025",
            "inputs": _acute_fixture_row(),
            "options": {"runtime": "rust", "refDir": "tests/data/2025"},
        },
    )
    payload = _structured(result)

    assert payload["valid"] is True
    assert payload["runtime"] == "rust"
    assert payload["diagnostics"]["diagnostics"][0]["message"].startswith(
        "Input validated for the Rust-backed"
    )
    assert calls == [("2025", Path("tests/data/2025"))]


def test_mcp_calculate_rejects_unsupported_rust_surface():
    result = mcp_server.call_tool(
        "mchs.calculate",
        {
            "calculatorId": "ed",
            "year": "2025",
            "inputs": {"AECC": "1"},
            "options": {"runtime": "rust"},
        },
    )

    assert result["isError"] is True
    assert "MCHS-MCP-RUST-UNSUPPORTED" in result["content"][0]["text"]
    assert "acute 2025" in result["content"][0]["text"]


def test_mcp_calculate_rejects_invalid_runtime():
    result = mcp_server.call_tool(
        "mchs.calculate",
        {
            "calculatorId": "acute",
            "year": "2025",
            "inputs": _acute_fixture_row(),
            "options": {"runtime": "turbo"},
        },
    )

    assert result["isError"] is True
    assert "MCHS-MCP-RUNTIME-INVALID" in result["content"][0]["text"]


def test_mcp_rust_acute_2025_matches_rust_cli_when_extension_available(
    monkeypatch, tmp_path
):
    try:
        rust_bridge.load_rust_extension()
    except ImportError as exc:
        pytest.skip(f"Rust extension unavailable: {exc}")

    def _weights(*_args, **_kwargs) -> pd.DataFrame:
        df = pd.read_csv("tests/data/nep25_aa_price_weights.csv")
        df["DRG"] = df["DRG"].str.strip("b'")
        return df

    monkeypatch.setattr(cli_main.acute_calculator, "_load_price_weights", _weights)
    monkeypatch.setattr(mcp_server.acute_calculator, "_load_price_weights", _weights)

    input_csv = Path("tests/fixtures/golden/acute_2025/input.csv")
    cli_output = tmp_path / "rust_cli.csv"
    cli_result = CliRunner().invoke(
        cast(Any, cli_main.cli),
        [
            "acute",
            str(input_csv),
            "--year",
            "2025",
            "--params",
            "tests/data/2025",
            "--runtime",
            "rust",
            "--output",
            str(cli_output),
        ],
    )
    assert cli_result.exit_code == 0, cli_result.output

    mcp_result = mcp_server.call_tool(
        "mchs.calculate",
        {
            "calculatorId": "acute",
            "year": "2025",
            "inputs": _acute_fixture_row(),
            "options": {"runtime": "rust", "refDir": "tests/data/2025"},
        },
    )

    cli_row = pd.read_csv(cli_output).iloc[0].to_dict()
    mcp_row = _structured(mcp_result)["result"]
    assert float(mcp_row["NWAU25"]) == pytest.approx(
        float(cli_row["NWAU25"]), rel=1e-4, abs=1e-4
    )
