//! C ABI for the NWAU proof of concept.
//!
//! Exposes extern "C" entrypoints for use by foreign-language callers.

use core::ffi::c_char;
use core::{slice, str};

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct NwauAbiStringView {
    pub ptr: *const c_char,
    pub len: usize,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiEpisodeInput {
    pub drg: NwauAbiStringView,
    pub los: f64,
    pub icu_hours: f64,
    pub icu_other: f64,
    pub pat_sameday_flag: u8,
    pub pat_private_flag: u8,
    pub pat_covid_flag: u8,
    pub eligible_paed_flag: u8,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiReferenceRow {
    pub drg: NwauAbiStringView,
    pub inlier_lower_bound: f64,
    pub inlier_upper_bound: f64,
    pub paediatric_multiplier: f64,
    pub same_day_list_flag: u8,
    pub bundled_icu_flag: u8,
    pub same_day_base_weight: f64,
    pub same_day_per_diem: f64,
    pub inlier_weight: f64,
    pub long_stay_per_diem: f64,
    pub private_service_adjustment: f64,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiAdjustmentFactors {
    pub icu_rate: f64,
    pub covid_adjustment: f64,
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
    pub radiotherapy_adjustment: f64,
    pub dialysis_adjustment: f64,
    pub private_accommodation_same_day: f64,
    pub private_accommodation_overnight: f64,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiEpisodeOutput {
    pub error_code: u32,
    pub separation_category: u32,
    pub eligible_icu_hours: f64,
    pub los_icu_removed: f64,
    pub w01: f64,
    pub w02: f64,
    pub w03: f64,
    pub w04: f64,
    pub gwau: f64,
    pub private_service_deduction: f64,
    pub private_accommodation_deduction: f64,
    pub nwau25: f64,
}

pub type NwauAbiStatus = u32;

pub const NWAU_ABI_VERSION_MAJOR: u32 = 0;
pub const NWAU_ABI_VERSION_MINOR: u32 = 2;
pub const NWAU_ABI_VERSION_PATCH: u32 = 0;
pub const NWAU_ABI_STATUS_OK: NwauAbiStatus = 0;
pub const NWAU_ABI_STATUS_INVALID_ARGUMENT: NwauAbiStatus = 1;
pub const NWAU_ABI_STATUS_UNIMPLEMENTED: NwauAbiStatus = 2;

fn static_view(text: &'static str) -> NwauAbiStringView {
    NwauAbiStringView {
        ptr: text.as_ptr() as *const c_char,
        len: text.len(),
    }
}

unsafe fn view_to_str<'a>(view: &NwauAbiStringView) -> Option<&'a str> {
    if view.len == 0 {
        return Some("");
    }
    if view.ptr.is_null() {
        return None;
    }
    let bytes = unsafe { slice::from_raw_parts(view.ptr as *const u8, view.len) };
    str::from_utf8(bytes).ok()
}
#[no_mangle]
pub extern "C" fn nwau_abi_version_major() -> u32 {
    NWAU_ABI_VERSION_MAJOR
}

#[no_mangle]
pub extern "C" fn nwau_abi_version_minor() -> u32 {
    NWAU_ABI_VERSION_MINOR
}

#[no_mangle]
pub extern "C" fn nwau_abi_version_patch() -> u32 {
    NWAU_ABI_VERSION_PATCH
}

#[no_mangle]
pub extern "C" fn nwau_abi_kernel_label() -> NwauAbiStringView {
    static_view("acute 2025")
}

#[no_mangle]
pub extern "C" fn nwau_abi_status_message(status: NwauAbiStatus) -> NwauAbiStringView {
    match status {
        NWAU_ABI_STATUS_OK => static_view("ok"),
        NWAU_ABI_STATUS_INVALID_ARGUMENT => static_view("invalid argument"),
        NWAU_ABI_STATUS_UNIMPLEMENTED => static_view("unimplemented"),
        _ => static_view("unknown status"),
    }
}

/// # Safety
///
/// Caller must ensure all pointer arguments are non-null and point to valid,
/// properly aligned data. String views with non-zero length must point to
/// valid UTF-8 bytes. `out` must point to a writable region of at least
/// `size_of::<NwauAbiEpisodeOutput>()` bytes.
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_calculate_acute_2025(
    input: *const NwauAbiEpisodeInput,
    reference: *const NwauAbiReferenceRow,
    adjustments: *const NwauAbiAdjustmentFactors,
    out: *mut NwauAbiEpisodeOutput,
) -> NwauAbiStatus {
    if input.is_null() || reference.is_null() || adjustments.is_null() || out.is_null() {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    }
    let input = unsafe { &*input };
    let reference = unsafe { &*reference };
    let adjustments = unsafe { &*adjustments };
    let Some(drg) = (unsafe { view_to_str(&input.drg) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };
    let Some(ref_drg) = (unsafe { view_to_str(&reference.drg) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };
    let validation = nwau_core::AcuteValidationState::valid();
    let acute_input = nwau_core::AcuteEpisodeInput {
        drg,
        los: input.los,
        icu_hours: input.icu_hours,
        icu_other: input.icu_other,
        pat_sameday_flag: input.pat_sameday_flag != 0,
        pat_private_flag: input.pat_private_flag != 0,
        pat_covid_flag: input.pat_covid_flag != 0,
        eligible_paed_flag: input.eligible_paed_flag != 0,
        validation,
    };
    let acute_ref = nwau_core::AcuteReferenceRow {
        drg: ref_drg,
        inlier_lower_bound: reference.inlier_lower_bound,
        inlier_upper_bound: reference.inlier_upper_bound,
        paediatric_multiplier: reference.paediatric_multiplier,
        same_day_list_flag: reference.same_day_list_flag != 0,
        bundled_icu_flag: reference.bundled_icu_flag != 0,
        same_day_base_weight: reference.same_day_base_weight,
        same_day_per_diem: reference.same_day_per_diem,
        inlier_weight: reference.inlier_weight,
        long_stay_per_diem: reference.long_stay_per_diem,
        private_service_adjustment: reference.private_service_adjustment,
    };
    let acute_adj = nwau_core::AcuteAdjustmentFactors {
        icu_rate: adjustments.icu_rate,
        covid_adjustment: adjustments.covid_adjustment,
        indigenous_adjustment: adjustments.indigenous_adjustment,
        remoteness_adjustment: adjustments.remoteness_adjustment,
        treatment_remoteness_adjustment: adjustments.treatment_remoteness_adjustment,
        radiotherapy_adjustment: adjustments.radiotherapy_adjustment,
        dialysis_adjustment: adjustments.dialysis_adjustment,
        private_accommodation_same_day: adjustments.private_accommodation_same_day,
        private_accommodation_overnight: adjustments.private_accommodation_overnight,
    };
    let result = nwau_core::calculate_acute_2025(acute_input, acute_ref, acute_adj);
    unsafe {
        *out = NwauAbiEpisodeOutput {
            error_code: result.error_code as u32,
            separation_category: result.separation_category.map(|s| s as u32).unwrap_or(0),
            eligible_icu_hours: result.eligible_icu_hours,
            los_icu_removed: result.los_icu_removed,
            w01: result.w01,
            w02: result.w02,
            w03: result.w03,
            w04: result.w04,
            gwau: result.gwau,
            private_service_deduction: result.private_service_deduction,
            private_accommodation_deduction: result.private_accommodation_deduction,
            nwau25: result.nwau25,
        };
    }
    NWAU_ABI_STATUS_OK
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn version_queries_match() {
        assert_eq!(nwau_abi_version_major(), 0);
        assert_eq!(nwau_abi_version_minor(), 2);
        assert_eq!(nwau_abi_version_patch(), 0);
    }
    #[test]
    fn null_inputs_fail_closed() {
        let status = unsafe {
            nwau_abi_calculate_acute_2025(
                core::ptr::null(),
                core::ptr::null(),
                core::ptr::null(),
                core::ptr::null_mut(),
            )
        };
        assert_eq!(status, NWAU_ABI_STATUS_INVALID_ARGUMENT);
    }
    #[test]
    fn null_string_view_with_length_fails_closed() {
        let input = NwauAbiEpisodeInput {
            drg: NwauAbiStringView {
                ptr: core::ptr::null(),
                len: 4,
            },
            los: 10.0,
            icu_hours: 0.0,
            icu_other: 0.0,
            pat_sameday_flag: 0,
            pat_private_flag: 0,
            pat_covid_flag: 0,
            eligible_paed_flag: 0,
        };
        let ref_drg = b"801A";
        let reference = NwauAbiReferenceRow {
            drg: NwauAbiStringView {
                ptr: ref_drg.as_ptr() as *const c_char,
                len: ref_drg.len(),
            },
            ..NwauAbiReferenceRow::default()
        };
        let adjustments = NwauAbiAdjustmentFactors::default();
        let mut output = NwauAbiEpisodeOutput::default();
        let status =
            unsafe { nwau_abi_calculate_acute_2025(&input, &reference, &adjustments, &mut output) };
        assert_eq!(status, NWAU_ABI_STATUS_INVALID_ARGUMENT);
    }
    #[test]
    fn invalid_utf8_string_view_fails_closed() {
        let drg = [0xff, 0xfe];
        let input = NwauAbiEpisodeInput {
            drg: NwauAbiStringView {
                ptr: drg.as_ptr() as *const c_char,
                len: drg.len(),
            },
            los: 10.0,
            icu_hours: 0.0,
            icu_other: 0.0,
            pat_sameday_flag: 0,
            pat_private_flag: 0,
            pat_covid_flag: 0,
            eligible_paed_flag: 0,
        };
        let ref_drg = b"801A";
        let reference = NwauAbiReferenceRow {
            drg: NwauAbiStringView {
                ptr: ref_drg.as_ptr() as *const c_char,
                len: ref_drg.len(),
            },
            ..NwauAbiReferenceRow::default()
        };
        let adjustments = NwauAbiAdjustmentFactors::default();
        let mut output = NwauAbiEpisodeOutput::default();
        let status =
            unsafe { nwau_abi_calculate_acute_2025(&input, &reference, &adjustments, &mut output) };
        assert_eq!(status, NWAU_ABI_STATUS_INVALID_ARGUMENT);
    }
    #[test]
    fn valid_pointer_shape_returns_ok() {
        let drg = b"801A\0";
        let input = NwauAbiEpisodeInput {
            drg: NwauAbiStringView {
                ptr: drg.as_ptr() as *const c_char,
                len: 4,
            },
            los: 10.0,
            icu_hours: 0.0,
            icu_other: 0.0,
            pat_sameday_flag: 0,
            pat_private_flag: 0,
            pat_covid_flag: 0,
            eligible_paed_flag: 0,
        };
        let ref_drg = b"801A\0";
        let reference = NwauAbiReferenceRow {
            drg: NwauAbiStringView {
                ptr: ref_drg.as_ptr() as *const c_char,
                len: 4,
            },
            inlier_lower_bound: 7.0,
            inlier_upper_bound: 72.0,
            paediatric_multiplier: 1.35,
            same_day_list_flag: 0,
            bundled_icu_flag: 0,
            same_day_base_weight: 0.9527,
            same_day_per_diem: 1.1849,
            inlier_weight: 9.2472,
            long_stay_per_diem: 0.26,
            private_service_adjustment: 0.0,
        };
        let adjustments = NwauAbiAdjustmentFactors::default();
        let mut output = NwauAbiEpisodeOutput::default();
        let status =
            unsafe { nwau_abi_calculate_acute_2025(&input, &reference, &adjustments, &mut output) };
        assert_eq!(status, NWAU_ABI_STATUS_OK);
        assert_eq!(output.error_code, 0);
        assert!((output.nwau25 - 9.2472).abs() < 1e-4);
    }
}
