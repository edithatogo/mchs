import os
import sys
from pathlib import Path
from typing import Any, cast

import pandas as pd
import pytest
from click.testing import CliRunner

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from nwau_py import rust_bridge
from nwau_py.cli import main as cli_main


def test_runtime_boundary_document_pins_contract_terms():
    doc = Path("docs/roadmaps/rust-cli-runtime-boundary.md").read_text(
        encoding="utf-8"
    )

    assert "Python default" in doc
    assert "Rust opt-in" in doc
    assert "Rust default" in doc
    assert "`--runtime python|rust|auto`" in doc
    assert "`NWAU_RUNTIME`" in doc
    assert "rtol=1e-4" in doc
    assert "atol=1e-4" in doc
    assert "contracts/interop/cli-file-interop.contract.json" in doc
    assert "MCHS-CLI-RUST-UNSUPPORTED" in doc
    assert "MCHS-CLI-RUST-UNAVAILABLE" in doc


def test_surface_inventory_and_evidence_do_not_claim_rust_default():
    inventory = Path("docs/roadmaps/rust-cli-surface-inventory.md").read_text(
        encoding="utf-8"
    )
    evidence = Path("docs/release-evidence-rust-cli-core-migration.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "`acute`" in inventory
    assert "`ed`" in inventory
    assert "`non-admitted`" in inventory
    assert "Python-only; `--runtime rust` fails closed" in inventory
    assert "does not claim Rust default status" in evidence
    assert "Python remains the default" in readme
    assert "opt-in acute 2025 CSV execution" in readme


def test_cli_accepts_rust_runtime_for_acute_2025(monkeypatch, tmp_path):
    def rust_calculator(df, params, *, year, ref_dir=None):
        output = df.copy()
        output[f"NWAU{year[-2:]}"] = 1.25
        return output

    monkeypatch.setattr(
        cli_main.acute_calculator, "calculate_acute_rust_2025", rust_calculator
    )
    monkeypatch.setattr(
        cli_main.acute_calculator, "_load_price_weights", lambda *_args: pd.DataFrame()
    )

    input_csv = tmp_path / "acute.csv"
    pd.DataFrame(
        {
            "DRG": ["A01A"],
            "LOS": [1],
            "ICU_HOURS": [0],
            "ICU_OTHER": [0],
            "PAT_SAMEDAY_FLAG": [0],
            "PAT_PRIVATE_FLAG": [0],
            "PAT_COVID_FLAG": [0],
        }
    ).to_csv(input_csv, index=False)

    output_csv = tmp_path / "out.csv"
    result = CliRunner().invoke(
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
            str(output_csv),
        ],
    )

    assert result.exit_code == 0, result.output
    assert pd.read_csv(output_csv)["NWAU25"].tolist() == [1.25]


def test_cli_rust_acute_2025_matches_python_cli_golden_fixture(
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

    input_csv = Path("tests/fixtures/golden/acute_2025/input.csv")
    python_output = tmp_path / "python.csv"
    rust_output = tmp_path / "rust.csv"
    runner = CliRunner()

    for runtime, output in (("python", python_output), ("rust", rust_output)):
        result = runner.invoke(
            cast(Any, cli_main.cli),
            [
                "acute",
                str(input_csv),
                "--year",
                "2025",
                "--params",
                "tests/data/2025",
                "--runtime",
                runtime,
                "--output",
                str(output),
            ],
        )
        assert result.exit_code == 0, result.output

    pd.testing.assert_frame_equal(
        pd.read_csv(rust_output),
        pd.read_csv(python_output),
        check_dtype=False,
        check_exact=False,
        rtol=1e-4,
        atol=1e-4,
    )


def test_cli_rejects_rust_runtime_for_unsupported_surface(tmp_path):
    input_csv = tmp_path / "ed.csv"
    pd.DataFrame({"AECC": ["1"], "LOS": [1]}).to_csv(input_csv, index=False)

    result = CliRunner().invoke(
        cast(Any, cli_main.cli),
        [
            "ed",
            str(input_csv),
            "--year",
            "2025",
            "--runtime",
            "rust",
            "--output",
            str(tmp_path / "out.csv"),
        ],
    )

    assert result.exit_code != 0
    assert "MCHS-CLI-RUST-UNSUPPORTED" in result.output
    assert "acute 2025" in result.output


def test_explicit_runtime_option_takes_precedence_over_environment(
    monkeypatch,
):
    monkeypatch.setenv("NWAU_RUNTIME", "rust")

    assert cli_main._resolve_runtime("python") == "python"


def test_invalid_environment_runtime_fails_closed(monkeypatch, tmp_path):
    monkeypatch.setenv("NWAU_RUNTIME", "turbo")
    input_csv = tmp_path / "acute.csv"
    pd.DataFrame({"DRG": ["A01A"]}).to_csv(input_csv, index=False)

    result = CliRunner().invoke(
        cast(Any, cli_main.cli),
        ["acute", str(input_csv), "--year", "2025"],
        env={**os.environ, "NWAU_RUNTIME": "turbo"},
    )

    assert result.exit_code != 0
    assert "MCHS-CLI-RUNTIME-INVALID" in result.output
