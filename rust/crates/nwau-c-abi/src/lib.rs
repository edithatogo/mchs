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
pub const NWAU_ABI_VERSION_MINOR: u32 = 3;
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

/// # Safety
///
/// Caller must ensure all pointer arguments are non-null and point to valid,
/// properly aligned data. String views with non-zero length must point to
/// valid UTF-8 bytes. `out` must point to a writable region of at least
/// `size_of::<NwauAbiEpisodeOutput>()` bytes.
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_calculate_acute_2026(
    input: *const NwauAbiEpisodeInput,
    reference: *const NwauAbiReferenceRow,
    adjustments: *const NwauAbiAdjustmentFactors,
    out: *mut NwauAbiEpisodeOutput,
) -> NwauAbiStatus {
    nwau_abi_calculate_acute_2025(input, reference, adjustments, out)
}

// ============================================================================
// Multi-Stream C-ABI: ED, Mental Health, Outpatients, and Subacute
// ============================================================================

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiEdInput {
    pub code: NwauAbiStringView,
    pub classification_option: u32,
    pub eligibility_option: u32,
    pub compensable_status: u32,
    pub dva_status: u32,
    pub funding_source: u32,
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiEdReferenceRow {
    pub code: NwauAbiStringView,
    pub price_weight: f64,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiEdOutput {
    pub error_code: u32,
    pub w01: f64,
    pub gwau: f64,
    pub nwau: f64,
}

/// # Safety
///
/// Caller must ensure all pointer arguments are non-null and point to valid,
/// properly aligned data. String views with non-zero length must point to
/// valid UTF-8 bytes. `out` must point to a writable region of at least
/// `size_of::<NwauAbiEdOutput>()` bytes.
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_calculate_ed(
    input: *const NwauAbiEdInput,
    reference: *const NwauAbiEdReferenceRow,
    out: *mut NwauAbiEdOutput,
) -> NwauAbiStatus {
    if input.is_null() || reference.is_null() || out.is_null() {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    }
    let input = unsafe { &*input };
    let reference = unsafe { &*reference };
    let Some(code) = (unsafe { view_to_str(&input.code) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };
    let Some(ref_code) = (unsafe { view_to_str(&reference.code) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };

    let class_opt = match input.classification_option {
        1 => nwau_core::EdClassificationOption::UdgMapped,
        2 => nwau_core::EdClassificationOption::UdgDirect,
        _ => nwau_core::EdClassificationOption::AeccDirect,
    };
    let elig_opt = match input.eligibility_option {
        1 => nwau_core::EdEligibilityOption::CompensableDva,
        _ => nwau_core::EdEligibilityOption::FundingSource,
    };

    let ed_input = nwau_core::EdEpisodeInput {
        code,
        classification_option: class_opt,
        eligibility_option: elig_opt,
        compensable_status: if input.compensable_status > 0 {
            Some(input.compensable_status as u8)
        } else {
            None
        },
        dva_status: if input.dva_status > 0 {
            Some(input.dva_status as u8)
        } else {
            None
        },
        funding_source: if input.funding_source > 0 {
            Some(input.funding_source as u8)
        } else {
            None
        },
    };

    let ed_ref = nwau_core::EdReferenceRow {
        code: ref_code,
        price_weight: reference.price_weight,
    };

    let ed_adj = nwau_core::EdAdjustmentFactors {
        indigenous_adjustment: input.indigenous_adjustment,
        remoteness_adjustment: input.remoteness_adjustment,
        treatment_remoteness_adjustment: input.treatment_remoteness_adjustment,
    };

    let inscope = [1, 2, 8];
    let res = nwau_core::calculate_ed(ed_input, Some(ed_ref), ed_adj, &inscope);
    unsafe {
        *out = NwauAbiEdOutput {
            error_code: res.error_code as u32,
            w01: res.w01,
            gwau: res.gwau,
            nwau: res.nwau,
        };
    }
    NWAU_ABI_STATUS_OK
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiMhInput {
    pub amhcc: NwauAbiStringView,
    pub los: f64,
    pub pat_sameday_flag: u8,
    pub pat_private_flag: u8,
    pub state: u8,
    pub sc_pat_pub: f64,
    pub sc_nopat_pub: f64,
    pub specialist_paediatric_multiplier: f64,
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
    pub private_serv_rate_national: f64,
    pub private_serv_rate_state: f64,
    pub private_accomm_sameday: f64,
    pub private_accomm_overnight: f64,
    pub ppsa_option: u32,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiMhAdmittedReferenceRow {
    pub amhcc: NwauAbiStringView,
    pub price_cat: u32,
    pub inlier_lower_bound: f64,
    pub inlier_upper_bound: f64,
    pub sso_base_weight: f64,
    pub sso_per_diem: f64,
    pub inlier_weight: f64,
    pub lso_per_diem: f64,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiMhOutput {
    pub error_code: u32,
    pub substream: u32,
    pub separation_category: u32,
    pub w01: f64,
    pub gwau: f64,
    pub private_service_deduction: f64,
    pub private_accommodation_deduction: f64,
    pub nwau: f64,
}

/// # Safety
///
/// Caller must ensure all pointer arguments are non-null and point to valid,
/// properly aligned data. String views with non-zero length must point to
/// valid UTF-8 bytes. `out` must point to a writable region of at least
/// `size_of::<NwauAbiMhOutput>()` bytes.
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_calculate_mh(
    input: *const NwauAbiMhInput,
    reference: *const NwauAbiMhAdmittedReferenceRow,
    out: *mut NwauAbiMhOutput,
) -> NwauAbiStatus {
    if input.is_null() || reference.is_null() || out.is_null() {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    }
    let input = unsafe { &*input };
    let reference = unsafe { &*reference };
    let Some(amhcc) = (unsafe { view_to_str(&input.amhcc) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };
    let Some(ref_amhcc) = (unsafe { view_to_str(&reference.amhcc) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };

    let mh_input = nwau_core::MhEpisodeInput {
        amhcc,
        los: input.los,
        pat_sameday_flag: input.pat_sameday_flag != 0,
        pat_private_flag: input.pat_private_flag != 0,
        state: input.state,
        sc_pat_pub: input.sc_pat_pub,
        sc_nopat_pub: input.sc_nopat_pub,
    };

    let mh_ref = nwau_core::MhAdmittedReferenceRow {
        amhcc: ref_amhcc,
        price_cat: reference.price_cat as u8,
        inlier_lower_bound: reference.inlier_lower_bound,
        inlier_upper_bound: reference.inlier_upper_bound,
        sso_base_weight: reference.sso_base_weight,
        sso_per_diem: reference.sso_per_diem,
        inlier_weight: reference.inlier_weight,
        lso_per_diem: reference.lso_per_diem,
    };

    let mh_adj = nwau_core::MhAdjustmentFactors {
        specialist_paediatric_multiplier: input.specialist_paediatric_multiplier,
        indigenous_adjustment: input.indigenous_adjustment,
        remoteness_adjustment: input.remoteness_adjustment,
        treatment_remoteness_adjustment: input.treatment_remoteness_adjustment,
        private_serv_rate_national: input.private_serv_rate_national,
        private_serv_rate_state: input.private_serv_rate_state,
        private_accomm_sameday: input.private_accomm_sameday,
        private_accomm_overnight: input.private_accomm_overnight,
    };

    let ppsa = match input.ppsa_option {
        2 => nwau_core::MhPpsaOption::StateLevel,
        _ => nwau_core::MhPpsaOption::National,
    };

    let res = nwau_core::calculate_mh(mh_input, Some(mh_ref), None, mh_adj, ppsa);
    unsafe {
        *out = NwauAbiMhOutput {
            error_code: res.error_code as u32,
            substream: match res.substream {
                nwau_core::MhSubstream::Admitted => 0,
                nwau_core::MhSubstream::Community => 1,
            },
            separation_category: res.separation_category.map(|s| s as u32).unwrap_or(0),
            w01: res.w01,
            gwau: res.gwau,
            private_service_deduction: res.private_service_deduction,
            private_accommodation_deduction: res.private_accommodation_deduction,
            nwau: res.nwau,
        };
    }
    NWAU_ABI_STATUS_OK
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiOutpatientInput {
    pub clinic_code: NwauAbiStringView,
    pub data_type: u32,
    pub multiprovider_flag: u8,
    pub eligible_paediatric_flag: u8,
    pub inscope_flag: u8,
    pub group_event_count: f64,
    pub indiv_event_count: f64,
    pub multidisciplinary_event_count: f64,
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
    pub multiprovider_adjustment: f64,
    pub paediatric_adjustment: f64,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiOutpatientReferenceRow {
    pub clinic_code: NwauAbiStringView,
    pub price_weight: f64,
    pub paediatric_adjustment: f64,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiOutpatientOutput {
    pub error_code: u32,
    pub w01: f64,
    pub gwau: f64,
    pub nwau: f64,
}

/// # Safety
///
/// Caller must ensure all pointer arguments are non-null and point to valid,
/// properly aligned data. String views with non-zero length must point to
/// valid UTF-8 bytes. `out` must point to a writable region of at least
/// `size_of::<NwauAbiOutpatientOutput>()` bytes.
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_calculate_outpatients(
    input: *const NwauAbiOutpatientInput,
    reference: *const NwauAbiOutpatientReferenceRow,
    out: *mut NwauAbiOutpatientOutput,
) -> NwauAbiStatus {
    if input.is_null() || reference.is_null() || out.is_null() {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    }
    let input = unsafe { &*input };
    let reference = unsafe { &*reference };
    let Some(clinic_code) = (unsafe { view_to_str(&input.clinic_code) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };
    let Some(ref_clinic) = (unsafe { view_to_str(&reference.clinic_code) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };

    let op_input = nwau_core::OutpatientEpisodeInput {
        clinic_code,
        data_type: match input.data_type {
            2 => nwau_core::OutpatientDataType::AggregateCount,
            _ => nwau_core::OutpatientDataType::EventLevel,
        },
        multiprovider_flag: input.multiprovider_flag != 0,
        eligible_paediatric_flag: input.eligible_paediatric_flag != 0,
        inscope_flag: input.inscope_flag != 0,
        group_event_count: input.group_event_count,
        indiv_event_count: input.indiv_event_count,
        multidisciplinary_event_count: input.multidisciplinary_event_count,
    };

    let op_ref = nwau_core::OutpatientReferenceRow {
        clinic_code: ref_clinic,
        price_weight: reference.price_weight,
        paediatric_adjustment: reference.paediatric_adjustment,
    };

    let op_adj = nwau_core::OutpatientAdjustmentFactors {
        indigenous_adjustment: input.indigenous_adjustment,
        remoteness_adjustment: input.remoteness_adjustment,
        treatment_remoteness_adjustment: input.treatment_remoteness_adjustment,
        multiprovider_adjustment: input.multiprovider_adjustment,
        paediatric_adjustment: input.paediatric_adjustment,
    };

    let res = nwau_core::calculate_outpatients(op_input, Some(op_ref), op_adj);
    unsafe {
        *out = NwauAbiOutpatientOutput {
            error_code: res.error_code as u32,
            w01: res.w01,
            gwau: res.gwau,
            nwau: res.nwau,
        };
    }
    NWAU_ABI_STATUS_OK
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiSubacuteInput {
    pub ansnap: NwauAbiStringView,
    pub los: f64,
    pub pat_sameday_flag: u8,
    pub pat_private_flag: u8,
    pub pat_public_flag: u8,
    pub age: f64,
    pub state: u8,
    pub indigenous_adjustment: f64,
    pub remoteness_adjustment: f64,
    pub treatment_remoteness_adjustment: f64,
    pub radiotherapy_adjustment: f64,
    pub dialysis_adjustment: f64,
    pub private_serv_rate_national: f64,
    pub private_serv_rate_state: f64,
    pub private_accomm_sameday: f64,
    pub private_accomm_overnight: f64,
    pub ppsa_option: u32,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiSubacuteReferenceRow {
    pub ansnap: NwauAbiStringView,
    pub sameday_list_flag: u8,
    pub inlier_lower_bound: f64,
    pub inlier_upper_bound: f64,
    pub pw_sameday: f64,
    pub pw_sso_perdiem: f64,
    pub pw_inlier: f64,
    pub pw_lso_perdiem: f64,
}

#[repr(C)]
#[derive(Clone, Copy, Debug, Default, PartialEq)]
pub struct NwauAbiSubacuteOutput {
    pub error_code: u32,
    pub separation_category: u32,
    pub w01: f64,
    pub gwau: f64,
    pub private_service_deduction: f64,
    pub private_accommodation_deduction: f64,
    pub nwau: f64,
}

/// # Safety
///
/// Caller must ensure all pointer arguments are non-null and point to valid,
/// properly aligned data. String views with non-zero length must point to
/// valid UTF-8 bytes. `out` must point to a writable region of at least
/// `size_of::<NwauAbiSubacuteOutput>()` bytes.
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_calculate_subacute(
    input: *const NwauAbiSubacuteInput,
    reference: *const NwauAbiSubacuteReferenceRow,
    out: *mut NwauAbiSubacuteOutput,
) -> NwauAbiStatus {
    if input.is_null() || reference.is_null() || out.is_null() {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    }
    let input = unsafe { &*input };
    let reference = unsafe { &*reference };
    let Some(ansnap) = (unsafe { view_to_str(&input.ansnap) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };
    let Some(ref_ansnap) = (unsafe { view_to_str(&reference.ansnap) }) else {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    };

    let sa_input = nwau_core::SubacuteEpisodeInput {
        ansnap,
        los: input.los,
        pat_sameday_flag: input.pat_sameday_flag != 0,
        pat_private_flag: input.pat_private_flag != 0,
        pat_public_flag: input.pat_public_flag != 0,
        age: input.age,
        state: input.state,
    };

    let sa_ref = nwau_core::SubacuteReferenceRow {
        ansnap: ref_ansnap,
        sameday_list_flag: reference.sameday_list_flag != 0,
        inlier_lower_bound: reference.inlier_lower_bound,
        inlier_upper_bound: reference.inlier_upper_bound,
        pw_sameday: reference.pw_sameday,
        pw_sso_perdiem: reference.pw_sso_perdiem,
        pw_inlier: reference.pw_inlier,
        pw_lso_perdiem: reference.pw_lso_perdiem,
    };

    let sa_adj = nwau_core::SubacuteAdjustmentFactors {
        indigenous_adjustment: input.indigenous_adjustment,
        remoteness_adjustment: input.remoteness_adjustment,
        treatment_remoteness_adjustment: input.treatment_remoteness_adjustment,
        radiotherapy_adjustment: input.radiotherapy_adjustment,
        dialysis_adjustment: input.dialysis_adjustment,
        private_serv_rate_national: input.private_serv_rate_national,
        private_serv_rate_state: input.private_serv_rate_state,
        private_accomm_sameday: input.private_accomm_sameday,
        private_accomm_overnight: input.private_accomm_overnight,
    };

    let ppsa = match input.ppsa_option {
        2 => nwau_core::SubacutePpsaOption::StateLevel,
        _ => nwau_core::SubacutePpsaOption::National,
    };

    let res = nwau_core::calculate_subacute(sa_input, Some(sa_ref), sa_adj, ppsa);
    unsafe {
        *out = NwauAbiSubacuteOutput {
            error_code: res.error_code as u32,
            separation_category: res.separation_category.map(|s| s as u32).unwrap_or(0),
            w01: res.w01,
            gwau: res.gwau,
            private_service_deduction: res.private_service_deduction,
            private_accommodation_deduction: res.private_accommodation_deduction,
            nwau: res.nwau,
        };
    }
    NWAU_ABI_STATUS_OK
}

/// Verify 128-bit architecture invariants via C ABI.
///
/// # Safety
///
/// Caller must ensure `out_checksum` is non-null and points to a writable `u64`.
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_verify_128bit_invariants(
    count: usize,
    out_checksum: *mut u64,
) -> NwauAbiStatus {
    if out_checksum.is_null() {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    }
    match nwau_core::accel::verify_128bit_invariants(count) {
        Ok(chk) => {
            unsafe {
                *out_checksum = chk;
            }
            NWAU_ABI_STATUS_OK
        }
        Err(_) => NWAU_ABI_STATUS_INVALID_ARGUMENT,
    }
}

/// Run hardware-accelerated batch valuation across a slice of episodes.
///
/// # Safety
///
/// Caller must ensure `inputs` points to at least `count` readable `EpisodeGpuInput` structs,
/// and `outputs` points to at least `count` writable `EpisodeGpuOutput` structs.
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_evaluate_batch_accelerated(
    inputs: *const nwau_core::EpisodeGpuInput,
    count: usize,
    nep: f32,
    outputs: *mut nwau_core::EpisodeGpuOutput,
) -> NwauAbiStatus {
    if inputs.is_null() || outputs.is_null() {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    }
    let input_slice = unsafe { slice::from_raw_parts(inputs, count) };
    let device = nwau_core::ComputeDevice::auto();
    let res = device.evaluate_batch(input_slice, Some(nep));
    let out_slice = unsafe { slice::from_raw_parts_mut(outputs, count) };
    out_slice.copy_from_slice(&res);
    NWAU_ABI_STATUS_OK
}

/// Run Monte Carlo bootstrap resampling via C ABI.
///
/// # Safety
///
/// Caller must ensure `values` points to at least `count` readable `f64` floats,
/// and `out_stats` points to at least 5 writable `f64` floats: [mean, std_err, ci_lower_2_5, median, ci_upper_97_5].
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_bootstrap_cohort(
    values: *const f64,
    count: usize,
    iterations: usize,
    out_stats: *mut f64,
) -> NwauAbiStatus {
    if values.is_null() || out_stats.is_null() || count == 0 || iterations == 0 {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    }
    let val_slice = unsafe { slice::from_raw_parts(values, count) };
    let device = nwau_core::ComputeDevice::auto();
    let res = device.bootstrap(val_slice, iterations, None);
    unsafe {
        *out_stats.add(0) = res.mean;
        *out_stats.add(1) = res.std_err;
        *out_stats.add(2) = res.ci_lower_2_5;
        *out_stats.add(3) = res.median;
        *out_stats.add(4) = res.ci_upper_97_5;
    }
    NWAU_ABI_STATUS_OK
}

/// Copy active acceleration backend name into `out_buf`.
///
/// # Safety
///
/// Caller must ensure `out_buf` points to at least `buf_len` writable bytes.
#[no_mangle]
pub unsafe extern "C" fn nwau_abi_get_acceleration_backend(
    out_buf: *mut c_char,
    buf_len: usize,
) -> NwauAbiStatus {
    if out_buf.is_null() || buf_len == 0 {
        return NWAU_ABI_STATUS_INVALID_ARGUMENT;
    }
    let device = nwau_core::ComputeDevice::auto();
    let info = device.acceleration_info();
    let bytes = info.backend_name.as_bytes();
    let copy_len = bytes.len().min(buf_len - 1);
    unsafe {
        core::ptr::copy_nonoverlapping(bytes.as_ptr() as *const c_char, out_buf, copy_len);
        *out_buf.add(copy_len) = 0;
    }
    NWAU_ABI_STATUS_OK
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn version_queries_match() {
        assert_eq!(nwau_abi_version_major(), 0);
        assert_eq!(nwau_abi_version_minor(), 3);
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
    fn test_abi_multi_stream_functions() {
        // 1. ED ABI Test
        let ed_code = b"E0110A\0";
        let ed_input = NwauAbiEdInput {
            code: NwauAbiStringView {
                ptr: ed_code.as_ptr() as *const c_char,
                len: 6,
            },
            classification_option: 3,
            eligibility_option: 2,
            funding_source: 1,
            ..NwauAbiEdInput::default()
        };
        let ed_ref = NwauAbiEdReferenceRow {
            code: NwauAbiStringView {
                ptr: ed_code.as_ptr() as *const c_char,
                len: 6,
            },
            price_weight: 0.2837,
        };
        let mut ed_out = NwauAbiEdOutput::default();
        let status = unsafe { nwau_abi_calculate_ed(&ed_input, &ed_ref, &mut ed_out) };
        assert_eq!(status, NWAU_ABI_STATUS_OK);
        assert_eq!(ed_out.error_code, 0);
        assert!((ed_out.nwau - 0.2837).abs() < 1e-4);

        // 2. Outpatient ABI Test
        let op_code = b"10.01\0";
        let op_input = NwauAbiOutpatientInput {
            clinic_code: NwauAbiStringView {
                ptr: op_code.as_ptr() as *const c_char,
                len: 5,
            },
            data_type: 1,
            inscope_flag: 1,
            ..NwauAbiOutpatientInput::default()
        };
        let op_ref = NwauAbiOutpatientReferenceRow {
            clinic_code: NwauAbiStringView {
                ptr: op_code.as_ptr() as *const c_char,
                len: 5,
            },
            price_weight: 0.1742,
            paediatric_adjustment: 1.0,
        };
        let mut op_out = NwauAbiOutpatientOutput::default();
        let status = unsafe { nwau_abi_calculate_outpatients(&op_input, &op_ref, &mut op_out) };
        assert_eq!(status, NWAU_ABI_STATUS_OK);
        assert_eq!(op_out.error_code, 0);
        assert!((op_out.nwau - 0.1742).abs() < 1e-4);
    }

    #[test]
    fn test_abi_acceleration_functions() {
        // 1. Verify 128-bit architecture invariants
        let mut chk: u64 = 0;
        let status = unsafe { nwau_abi_verify_128bit_invariants(1000, &mut chk) };
        assert_eq!(status, NWAU_ABI_STATUS_OK);
        assert_eq!(chk, nwau_core::accel::GOLDEN_128BIT_INVARIANT_CHECKSUM);

        // 2. Query acceleration backend
        let mut buf = [0u8; 64];
        let status =
            unsafe { nwau_abi_get_acceleration_backend(buf.as_mut_ptr() as *mut c_char, 64) };
        assert_eq!(status, NWAU_ABI_STATUS_OK);
        let backend = core::str::from_utf8(&buf)
            .unwrap()
            .trim_matches(char::from(0));
        assert!(!backend.is_empty());

        // 3. Batch evaluation
        let episodes = nwau_core::accel::generate_invariant_test_fixtures(50);
        let mut outputs = vec![nwau_core::EpisodeGpuOutput::default(); 50];
        let status = unsafe {
            nwau_abi_evaluate_batch_accelerated(episodes.as_ptr(), 50, 7418.0, outputs.as_mut_ptr())
        };
        assert_eq!(status, NWAU_ABI_STATUS_OK);
        assert_eq!(outputs.len(), 50);
        assert!(outputs[0].nwau >= 0.0);

        // 4. Bootstrap cohort
        let values: [f64; 10] = [1.0, 1.2, 1.5, 2.0, 2.2, 2.5, 3.0, 3.2, 3.5, 4.0];
        let mut stats = [0.0f64; 5];
        let status =
            unsafe { nwau_abi_bootstrap_cohort(values.as_ptr(), 10, 100, stats.as_mut_ptr()) };
        assert_eq!(status, NWAU_ABI_STATUS_OK);
        assert!(stats[0] > 0.0); // mean
        assert!(stats[1] > 0.0); // std_err
        assert!(stats[2] <= stats[3]); // ci_lower <= median
        assert!(stats[3] <= stats[4]); // median <= ci_upper
    }
}
