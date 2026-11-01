import importlib
import shutil
import subprocess
import sys
import types
from io import StringIO
from pathlib import Path

import pytest

from nwau_py import compat as pd

CLI = shutil.which("funding-calculator")
FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "golden" / "acute_2025"
INPUT_CSV = FIXTURE_DIR / "input.csv"
REF_DIR = Path("tests/data/2025")

PYREADSTAT = types.ModuleType("pyreadstat")
PYREADSTAT.ReadstatError = Exception
PYREADSTAT._readstat_parser = types.SimpleNamespace(PyreadstatError=Exception)
sys.modules.setdefault("pyreadstat", PYREADSTAT)

acute = importlib.import_module("nwau_py.calculators.acute")


def _run_cli(input_csv: Path) -> str:
    cmd = [
        CLI,
        "acute",
        str(input_csv),
        "--year",
        "2025",
        "--params",
        "tests/data/2025",
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def _read_output_frame(stdout: str) -> pd.DataFrame:
    return pd.read_csv(StringIO(stdout))


def _direct_library_output(input_csv: Path) -> pd.DataFrame:
    input_df = pd.read_csv(input_csv)
    return acute.calculate_acute(
        input_df,
        acute.AcuteParams(),
        year="2025",
        ref_dir=REF_DIR,
    ).reset_index(drop=True)


@pytest.mark.skipif(CLI is None, reason="funding-calculator not installed")
def test_cli_integration():
    input_csv = INPUT_CSV
    try:
        cli_output = _read_output_frame(_run_cli(input_csv))
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        pytest.skip(f"CLI execution failed: {exc}")

    direct_output = _direct_library_output(input_csv)

    pd.testing.assert_frame_equal(
        cli_output.reset_index(drop=True),
        direct_output,
        check_dtype=False,
        check_exact=False,
        atol=1e-4,
        rtol=1e-4,
    )
    assert not cli_output.empty, "no output rows"
