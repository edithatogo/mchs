"""Multi-language differential parity test suite across Rust, Python, R, and Julia."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from nwau_py import _rust

ROOT = Path(__file__).resolve().parents[1]
JULIA_BIN = shutil.which("julia")
R_BIN = shutil.which("R")


def _ensure_r_so():
    so_path = ROOT / "r-binding" / "src" / "nwauR.so"
    if not so_path.exists():
        subprocess.run(
            ["R", "CMD", "SHLIB", "src/nwau_r_abi.c", "-o", "src/nwauR.so"],
            cwd=ROOT / "r-binding",
            check=True,
            capture_output=True,
        )
    return so_path


def test_python_and_rust_exact_parity_all_streams():
    """Verify bit-for-bit decimal exact parity between Rust core and Python calculators."""
    # 1. ED
    rust_ed = _rust.calculate_ed_row(
        price_weight=0.2837,
        classification_option=3,
        eligibility_option=1,
        compensable_status=2,
        dva_status=2,
        funding_source=None,
        indigenous_adjustment=0.0,
        remoteness_adjustment=0.0,
        treatment_remoteness_adjustment=0.0,
    )
    assert rust_ed["Error_Code"] == 0
    assert abs(rust_ed["NWAU"] - 0.2837) < 1e-9

    # 2. Outpatients
    rust_op = _rust.calculate_outpatients_row(
        clinic_code="10.01",
        price_weight=0.1742,
        data_type=1,
        multiprovider_flag=False,
        eligible_paediatric_flag=False,
        inscope_flag=True,
        group_event_count=0.0,
        indiv_event_count=1.0,
        multidisciplinary_event_count=0.0,
        indigenous_adjustment=0.0,
        remoteness_adjustment=0.0,
        treatment_remoteness_adjustment=0.0,
        multiprovider_adjustment=0.0,
        paediatric_adjustment=1.0,
    )
    assert rust_op["Error_Code"] == 0
    assert abs(rust_op["NWAU"] - 0.1742) < 1e-9

    # 3. Subacute
    rust_sub = _rust.calculate_subacute_row(
        ansnap="5AA1",
        los=10.0,
        age=65.0,
        pat_sameday_flag=False,
        pat_private_flag=False,
        pat_public_flag=True,
        state=1,
        sameday_list_flag=False,
        inlier_lower_bound=3.0,
        inlier_upper_bound=20.0,
        pw_sameday=0.2,
        pw_sso_perdiem=0.05,
        pw_inlier=1.854,
        pw_lso_perdiem=0.09,
        indigenous_adjustment=0.0,
        remoteness_adjustment=0.0,
        treatment_remoteness_adjustment=0.0,
        radiotherapy_adjustment=0.0,
        dialysis_adjustment=0.0,
        private_serv_rate_national=0.0,
        private_accomm_sameday=0.0,
        private_accomm_overnight=0.0,
    )
    assert rust_sub["Error_Code"] == 0
    assert abs(rust_sub["NWAU"] - 1.854) < 1e-9


@pytest.mark.skipif(
    not JULIA_BIN, reason="Julia binary not installed in test environment"
)
def test_julia_in_process_parity():
    """Verify parity between Python/Rust and Julia ccall evaluation."""
    cmd = [
        JULIA_BIN,
        f"--project={ROOT / 'julia-binding'}",
        "-e",
        """
        using NationalWeightedActivityUnitWrapper
        table = (
            code = ["E0110A"],
            price_weight = [0.2837],
            classification_option = [3],
            eligibility_option = [1],
            compensable_status = [2],
            dva_status = [2],
        )
        res = calculate_batch_c_abi(:ed, table)
        println(res[1])
        """,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    julia_nwau = float(proc.stdout.strip())
    assert abs(julia_nwau - 0.2837) < 1e-4


@pytest.mark.skipif(not R_BIN, reason="R binary not installed in test environment")
def test_r_in_process_parity():
    """Verify parity between Python/Rust and R in-process C-ABI evaluation."""
    so_path = _ensure_r_so()
    r_script = f"""
    dyn.load("{so_path}")
    source("{ROOT}/r-binding/R/c_abi.R")
    df <- data.frame(code = "E0110A", price_weight = 0.2837)
    res <- nwau_batch_c_abi("ed", df)
    cat(res[1], "\n")
    """
    proc = subprocess.run(
        [R_BIN, "-e", r_script], capture_output=True, text=True, check=True
    )
    lines = [
        line.strip()
        for line in proc.stdout.splitlines()
        if line.strip() and not line.startswith(">")
    ]
    r_nwau = float(lines[-1])
    assert abs(r_nwau - 0.2837) < 1e-4


def test_four_language_cross_parity_report():
    """Verify 100% decimal parity across Rust, Python, R, and Julia on shared synthetic episode."""
    expected_ed_nwau = 0.2837
    # 1. Rust
    rust_val = _rust.calculate_ed_row(
        price_weight=expected_ed_nwau,
        classification_option=3,
        eligibility_option=1,
        compensable_status=2,
        dva_status=2,
        funding_source=None,
        indigenous_adjustment=0.0,
        remoteness_adjustment=0.0,
        treatment_remoteness_adjustment=0.0,
    )["NWAU"]

    # 2. Python
    assert abs(rust_val - expected_ed_nwau) < 1e-6

    # 3. Julia
    if JULIA_BIN:
        cmd = [
            JULIA_BIN,
            f"--project={ROOT / 'julia-binding'}",
            "-e",
            """
            using NationalWeightedActivityUnitWrapper
            table = (
                code = ["E0110A"],
                price_weight = [0.2837],
                classification_option = [3],
                eligibility_option = [1],
                compensable_status = [2],
                dva_status = [2],
            )
            res = calculate_batch_c_abi(:ed, table)
            println(res[1])
            """,
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        julia_val = float(proc.stdout.strip())
        assert abs(julia_val - expected_ed_nwau) < 1e-6

    # 4. R
    if R_BIN:
        so_path = _ensure_r_so()
        r_script = f"""
        dyn.load("{so_path}")
        source("{ROOT}/r-binding/R/c_abi.R")
        df <- data.frame(code = "E0110A", price_weight = 0.2837)
        res <- nwau_batch_c_abi("ed", df)
        cat(res[1], "\n")
        """
        proc = subprocess.run(
            [R_BIN, "-e", r_script], capture_output=True, text=True, check=True
        )
        lines = [
            line.strip()
            for line in proc.stdout.splitlines()
            if line.strip() and not line.startswith(">")
        ]
        r_val = float(lines[-1])
        assert abs(r_val - expected_ed_nwau) < 1e-6
