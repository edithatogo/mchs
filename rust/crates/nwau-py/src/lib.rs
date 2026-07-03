//! PyO3 bindings for the NWAU acute 2025 kernel.
//!
//! This crate exposes the kernel as a native Python module via maturin.

#![allow(clippy::useless_conversion)]

use nwau_core::Kernel;
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList};

#[pyfunction(name = "kernel_label")]
fn kernel_label() -> &'static str {
    nwau_core::kernel_label()
}

#[pyfunction(name = "core_version")]
fn core_version() -> &'static str {
    env!("CARGO_PKG_VERSION")
}

#[pyfunction(name = "list_calculators")]
fn list_calculators() -> Vec<&'static str> {
    vec!["acute-2025", "sub-acute"]
}

#[pyfunction(name = "is_drg_in_scope")]
fn is_drg_in_scope(drg: &str) -> bool {
    let registry = nwau_core::DrgRegistry::new().with_acute_2025_fixtures();
    registry.is_acute_in_scope(drg)
}

#[allow(clippy::too_many_arguments)]
#[pyfunction(name = "calculate_acute_2025_row")]
fn calculate_acute_2025_row<'py>(
    py: Python<'py>,
    drg: &'py str,
    los: f64,
    icu_hours: f64,
    icu_other: f64,
    pat_sameday_flag: bool,
    pat_private_flag: bool,
    pat_covid_flag: bool,
    eligible_paed_flag: bool,
    inlier_lower_bound: f64,
    inlier_upper_bound: f64,
    paediatric_multiplier: f64,
    same_day_list_flag: bool,
    bundled_icu_flag: bool,
    same_day_base_weight: f64,
    same_day_per_diem: f64,
    inlier_weight: f64,
    long_stay_per_diem: f64,
    private_service_adjustment: f64,
    icu_rate: f64,
    covid_adjustment: f64,
    indigenous_adjustment: f64,
    remoteness_adjustment: f64,
    treatment_remoteness_adjustment: f64,
    radiotherapy_adjustment: f64,
    dialysis_adjustment: f64,
    private_accommodation_same_day: f64,
    private_accommodation_overnight: f64,
) -> Result<Bound<'py, PyDict>, PyErr> {
    let validation = nwau_core::AcuteValidationState::valid();
    let output = nwau_core::calculate_acute_2025(
        nwau_core::AcuteEpisodeInput {
            drg,
            los,
            icu_hours,
            icu_other,
            pat_sameday_flag,
            pat_private_flag,
            pat_covid_flag,
            eligible_paed_flag,
            validation,
        },
        nwau_core::AcuteReferenceRow {
            drg,
            inlier_lower_bound,
            inlier_upper_bound,
            paediatric_multiplier,
            same_day_list_flag,
            bundled_icu_flag,
            same_day_base_weight,
            same_day_per_diem,
            inlier_weight,
            long_stay_per_diem,
            private_service_adjustment,
        },
        nwau_core::AcuteAdjustmentFactors {
            icu_rate,
            covid_adjustment,
            indigenous_adjustment,
            remoteness_adjustment,
            treatment_remoteness_adjustment,
            radiotherapy_adjustment,
            dialysis_adjustment,
            private_accommodation_same_day,
            private_accommodation_overnight,
        },
    );
    let dict = PyDict::new(py);
    dict.set_item("NWAU25", output.nwau25)?;
    dict.set_item("Error_Code", output.error_code)?;
    dict.set_item(
        "Separation_Category",
        output
            .separation_category
            .map(|cat| cat as i32)
            .unwrap_or(0),
    )?;
    dict.set_item("kernel_label", nwau_core::kernel_label())?;
    Ok(dict)
}
#[pyfunction(name = "calculate_batch")]
fn calculate_batch<'py>(
    py: Python<'py>,
    episodes_json: &str,
    reference_json: &str,
) -> Result<Bound<'py, PyList>, PyErr> {
    let episodes: Vec<nwau_core::EpisodeRow> =
        serde_json::from_str(episodes_json).map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!("invalid episodes JSON: {e}"))
        })?;
    let references: Vec<nwau_core::ReferenceRow> =
        serde_json::from_str(reference_json).map_err(|e| {
            pyo3::exceptions::PyValueError::new_err(format!("invalid reference JSON: {e}"))
        })?;
    let kernel = nwau_core::Acute2025Kernel::new();
    let adjustments = nwau_core::AdjustmentFactors::default();
    let results = PyList::new(py, Vec::<Bound<'py, PyDict>>::new())?;
    for ep in &episodes {
        let ref_row = references.iter().find(|r| r.drg == ep.drg).ok_or_else(|| {
            pyo3::exceptions::PyValueError::new_err(format!("no reference row for DRG: {}", ep.drg))
        })?;
        let output = kernel.calculate(ep, ref_row, &adjustments);
        let d = PyDict::new(py);
        d.set_item("DRG", &ep.drg)?;
        d.set_item("NWAU", output.nwau)?;
        d.set_item("Error_Code", output.error_code)?;
        results.append(d)?;
    }
    Ok(results)
}

#[pymodule]
fn _rust(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add(
        "__doc__",
        "Rust-backed Python bindings for the acute 2025 kernel.",
    )?;
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add(
        "__all__",
        PyList::new(
            _py,
            [
                "kernel_label",
                "core_version",
                "list_calculators",
                "is_drg_in_scope",
                "calculate_acute_2025_row",
                "calculate_batch",
                "__version__",
            ],
        )?,
    )?;
    m.add_function(wrap_pyfunction!(kernel_label, m)?)?;
    m.add_function(wrap_pyfunction!(core_version, m)?)?;
    m.add_function(wrap_pyfunction!(list_calculators, m)?)?;
    m.add_function(wrap_pyfunction!(is_drg_in_scope, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_acute_2025_row, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_batch, m)?)?;
    Ok(())
}
