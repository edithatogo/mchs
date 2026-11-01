"""Tests for hardware-accelerated batch valuation and cross-platform matrix invariants."""

import pytest

from nwau_py import _rust


def test_get_acceleration_info():
    """Verify hardware acceleration metadata detection."""
    info = _rust.get_acceleration_info()
    assert isinstance(info, dict)
    assert "backend_name" in info
    assert "is_gpu" in info
    assert "simd_architecture" in info
    assert "available_threads" in info
    assert info["available_threads"] >= 1
    assert len(info["backend_name"]) > 0


def test_verify_128bit_invariants():
    """Verify bit-exact 128-bit cross-platform numerical invariants."""
    res = _rust.verify_128bit_invariants(1000)
    assert isinstance(res, dict)
    assert res["count"] == 1000
    assert res["passed"] is True
    assert res["checksum"] == res["golden"]
    assert res["checksum"] == "0xED9A975B0552E7E0"


def test_evaluate_batch_accelerated():
    """Verify high-throughput batch valuation across episodes."""
    episodes = [
        {
            "los": 5.0,
            "icu_hours": 0.0,
            "icu_rate": 0.0,
            "base_weight": 1.25,
            "inlier_lower": 2.0,
            "inlier_upper": 12.0,
            "short_stay_per_diem": 0.625,
            "long_stay_per_diem": 0.12,
            "adjustment_factor": 1.0,
            "private_deduction": 0.0,
            "same_day_flag": 0,
        },
        {
            "los": 1.0,
            "icu_hours": 0.0,
            "icu_rate": 0.0,
            "base_weight": 0.8,
            "inlier_lower": 1.0,
            "inlier_upper": 8.0,
            "short_stay_per_diem": 0.8,
            "long_stay_per_diem": 0.08,
            "adjustment_factor": 1.05,
            "private_deduction": 0.1,
            "same_day_flag": 1,
        },
    ]

    outputs = _rust.evaluate_batch_accelerated(episodes, 7418.0)
    assert len(outputs) == 2
    assert outputs[0]["error_code"] == 0
    assert pytest.approx(outputs[0]["nwau"], rel=1e-4) == 1.25
    assert pytest.approx(outputs[0]["funding"], rel=1e-2) == 1.25 * 7418.0

    assert outputs[1]["error_code"] == 0
    expected_nwau = 0.8 * 1.05 - 0.1
    assert pytest.approx(outputs[1]["nwau"], rel=1e-4) == expected_nwau
    assert pytest.approx(outputs[1]["funding"], rel=1e-2) == expected_nwau * 7418.0


def test_bootstrap_cohort():
    """Verify Monte Carlo bootstrap resampling convergence."""
    values = [float(x) for x in range(1, 101)]
    res = _rust.bootstrap_cohort(values, iterations=500)
    assert isinstance(res, dict)
    assert res["iterations"] == 500
    assert res["sample_size"] == 100
    assert pytest.approx(res["mean"], abs=5.0) == 50.5
    assert res["ci_lower_2_5"] <= res["median"]
    assert res["median"] <= res["ci_upper_97_5"]
    assert res["elapsed_ms"] > 0.0
