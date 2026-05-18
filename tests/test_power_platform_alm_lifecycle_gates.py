from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_power_platform_alm_gates.py"
LIFECYCLE_SCRIPT = ROOT / "scripts" / "power-platform-alm-lifecycle-gates.sh"
GATE_DOC = ROOT / "power-platform" / "pipelines" / "pack-check-import-gates.md"
WORKFLOW = ROOT / ".github" / "workflows" / "power-platform-alm.yml"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_power_platform_alm_lifecycle_contract_files_exist():
    assert VALIDATOR.exists(), VALIDATOR
    assert LIFECYCLE_SCRIPT.exists(), LIFECYCLE_SCRIPT
    assert GATE_DOC.exists(), GATE_DOC


def test_power_platform_alm_lifecycle_validator_enforces_expected_gates():
    text = _read_text(VALIDATOR)
    for term in [
        "pack",
        "check",
        "import",
        "pack-check-import-gates.md",
        "COMMAND_SURFACES",
    ]:
        assert term in text


def test_power_platform_alm_lifecycle_shell_runner_has_gate_contract():
    text = _read_text(LIFECYCLE_SCRIPT)
    for term in [
        "--gate",
        "pack",
        "check",
        "import",
        "validate_power_platform_alm_gates.py",
    ]:
        assert term in text


def test_power_platform_alm_lifecycle_validator_runs_non_interactively():
    completed = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0
    assert "Power Platform ALM gate contract is valid" in completed.stdout


def test_power_platform_alm_lifecycle_workflow_runs_pack_check_import_matrix():
    text = _read_text(WORKFLOW)
    assert "pack-check-import-gates" in text
    assert "gate: [pack, check, import]" in text
    assert "power-platform-alm-lifecycle-gates.sh --gate" in text
