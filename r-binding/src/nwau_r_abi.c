#include <R.h>
#include <Rinternals.h>
#include <R_ext/Rdynload.h>
#include <dlfcn.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ============================================================================
 * C-ABI TYPE DEFINITIONS
 * ============================================================================ */

typedef struct {
    const char *ptr;
    size_t len;
} nwau_abi_string_view;

/* Acute */
typedef struct {
    nwau_abi_string_view drg;
    double los;
    double icu_hours;
    double icu_other;
    uint8_t pat_sameday_flag;
    uint8_t pat_private_flag;
    uint8_t pat_covid_flag;
    uint8_t eligible_paed_flag;
} nwau_abi_episode_input;

typedef struct {
    nwau_abi_string_view drg;
    double inlier_lower_bound;
    double inlier_upper_bound;
    double paediatric_multiplier;
    uint8_t same_day_list_flag;
    uint8_t bundled_icu_flag;
    double same_day_base_weight;
    double same_day_per_diem;
    double inlier_weight;
    double long_stay_per_diem;
    double private_service_adjustment;
} nwau_abi_reference_row;

typedef struct {
    double icu_rate;
    double covid_adjustment;
    double indigenous_adjustment;
    double remoteness_adjustment;
    double treatment_remoteness_adjustment;
    double radiotherapy_adjustment;
    double dialysis_adjustment;
    double private_accommodation_same_day;
    double private_accommodation_overnight;
} nwau_abi_adjustment_factors;

typedef struct {
    uint32_t error_code;
    uint32_t separation_category;
    double eligible_icu_hours;
    double los_icu_removed;
    double w01;
    double w02;
    double w03;
    double w04;
    double gwau;
    double private_service_deduction;
    double private_accommodation_deduction;
    double nwau25;
} nwau_abi_episode_output;

/* ED */
typedef struct {
    nwau_abi_string_view code;
    uint32_t classification_option;
    uint32_t eligibility_option;
    uint32_t compensable_status;
    uint32_t dva_status;
    uint32_t funding_source;
    double indigenous_adjustment;
    double remoteness_adjustment;
    double treatment_remoteness_adjustment;
} nwau_abi_ed_input;

typedef struct {
    nwau_abi_string_view code;
    double price_weight;
} nwau_abi_ed_reference_row;

typedef struct {
    uint32_t error_code;
    double w01;
    double gwau;
    double nwau;
} nwau_abi_ed_output;

/* Mental Health */
typedef struct {
    nwau_abi_string_view amhcc;
    double los;
    uint8_t pat_sameday_flag;
    uint8_t pat_private_flag;
    uint8_t state;
    double sc_pat_pub;
    double sc_nopat_pub;
    double specialist_paediatric_multiplier;
    double indigenous_adjustment;
    double remoteness_adjustment;
    double treatment_remoteness_adjustment;
    double private_serv_rate_national;
    double private_serv_rate_state;
    double private_accomm_sameday;
    double private_accomm_overnight;
    uint32_t ppsa_option;
} nwau_abi_mh_input;

typedef struct {
    nwau_abi_string_view amhcc;
    uint32_t price_cat;
    double inlier_lower_bound;
    double inlier_upper_bound;
    double sso_base_weight;
    double sso_per_diem;
    double inlier_weight;
    double lso_per_diem;
} nwau_abi_mh_admitted_reference_row;

typedef struct {
    uint32_t error_code;
    uint32_t substream;
    uint32_t separation_category;
    double w01;
    double gwau;
    double private_service_deduction;
    double private_accommodation_deduction;
    double nwau;
} nwau_abi_mh_output;

/* Outpatients */
typedef struct {
    nwau_abi_string_view clinic_code;
    uint32_t data_type;
    uint8_t multiprovider_flag;
    uint8_t eligible_paediatric_flag;
    uint8_t inscope_flag;
    double group_event_count;
    double indiv_event_count;
    double multidisciplinary_event_count;
    double indigenous_adjustment;
    double remoteness_adjustment;
    double treatment_remoteness_adjustment;
    double multiprovider_adjustment;
    double paediatric_adjustment;
} nwau_abi_outpatient_input;

typedef struct {
    nwau_abi_string_view clinic_code;
    double price_weight;
    double paediatric_adjustment;
} nwau_abi_outpatient_reference_row;

typedef struct {
    uint32_t error_code;
    double w01;
    double gwau;
    double nwau;
} nwau_abi_outpatient_output;

/* Subacute */
typedef struct {
    nwau_abi_string_view ansnap;
    double los;
    uint8_t pat_sameday_flag;
    uint8_t pat_private_flag;
    uint8_t pat_public_flag;
    double age;
    uint8_t state;
    double indigenous_adjustment;
    double remoteness_adjustment;
    double treatment_remoteness_adjustment;
    double radiotherapy_adjustment;
    double dialysis_adjustment;
    double private_serv_rate_national;
    double private_serv_rate_state;
    double private_accomm_sameday;
    double private_accomm_overnight;
    uint32_t ppsa_option;
} nwau_abi_subacute_input;

typedef struct {
    nwau_abi_string_view ansnap;
    uint8_t sameday_list_flag;
    double inlier_lower_bound;
    double inlier_upper_bound;
    double pw_sameday;
    double pw_sso_perdiem;
    double pw_inlier;
    double pw_lso_perdiem;
} nwau_abi_subacute_reference_row;

typedef struct {
    uint32_t error_code;
    uint32_t separation_category;
    double w01;
    double gwau;
    double private_service_deduction;
    double private_accommodation_deduction;
    double nwau;
} nwau_abi_subacute_output;

/* ============================================================================
 * FUNCTION POINTER TYPES & DYNAMIC RESOLUTION
 * ============================================================================ */

typedef uint32_t (*fn_calculate_acute)(
    const nwau_abi_episode_input *,
    const nwau_abi_reference_row *,
    const nwau_abi_adjustment_factors *,
    nwau_abi_episode_output *
);

typedef uint32_t (*fn_calculate_ed)(
    const nwau_abi_ed_input *,
    const nwau_abi_ed_reference_row *,
    nwau_abi_ed_output *
);

typedef uint32_t (*fn_calculate_mh)(
    const nwau_abi_mh_input *,
    const nwau_abi_mh_admitted_reference_row *,
    nwau_abi_mh_output *
);

typedef uint32_t (*fn_calculate_outpatients)(
    const nwau_abi_outpatient_input *,
    const nwau_abi_outpatient_reference_row *,
    nwau_abi_outpatient_output *
);

typedef uint32_t (*fn_calculate_subacute)(
    const nwau_abi_subacute_input *,
    const nwau_abi_subacute_reference_row *,
    nwau_abi_subacute_output *
);

static void *g_lib_handle = NULL;
static fn_calculate_acute g_calc_acute = NULL;
static fn_calculate_ed g_calc_ed = NULL;
static fn_calculate_mh g_calc_mh = NULL;
static fn_calculate_outpatients g_calc_op = NULL;
static fn_calculate_subacute g_calc_sub = NULL;

static int ensure_lib_loaded(void) {
    if (g_lib_handle != NULL) return 0;

    const char *env_path = getenv("LIBNWAU_C_ABI_PATH");
    if (env_path != NULL && strlen(env_path) > 0) {
        g_lib_handle = dlopen(env_path, RTLD_NOW | RTLD_LOCAL);
    }

    if (g_lib_handle == NULL) {
        const char *candidates[] = {
            "rust/target/debug/libnwau_c_abi.dylib",
            "rust/target/release/libnwau_c_abi.dylib",
            "../rust/target/debug/libnwau_c_abi.dylib",
            "../rust/target/release/libnwau_c_abi.dylib",
            "../../rust/target/debug/libnwau_c_abi.dylib",
            "../../rust/target/release/libnwau_c_abi.dylib",
            "../../../rust/target/debug/libnwau_c_abi.dylib",
            "../../../rust/target/release/libnwau_c_abi.dylib",
            "rust/target/debug/libnwau_c_abi.so",
            "rust/target/release/libnwau_c_abi.so",
            "../rust/target/debug/libnwau_c_abi.so",
            "../../rust/target/debug/libnwau_c_abi.so",
            "../../../rust/target/debug/libnwau_c_abi.so",
            "libnwau_c_abi.dylib",
            "libnwau_c_abi.so",
            NULL
        };

        for (int i = 0; candidates[i] != NULL; i++) {
            g_lib_handle = dlopen(candidates[i], RTLD_NOW | RTLD_LOCAL);
            if (g_lib_handle != NULL) break;
        }
    }

    if (g_lib_handle == NULL) {
        warning("Failed to dlopen libnwau_c_abi: %s", dlerror());
        return -1;
    }

    g_calc_acute = (fn_calculate_acute)dlsym(g_lib_handle, "nwau_abi_calculate_acute_2025");
    g_calc_ed = (fn_calculate_ed)dlsym(g_lib_handle, "nwau_abi_calculate_ed");
    g_calc_mh = (fn_calculate_mh)dlsym(g_lib_handle, "nwau_abi_calculate_mh");
    g_calc_op = (fn_calculate_outpatients)dlsym(g_lib_handle, "nwau_abi_calculate_outpatients");
    g_calc_sub = (fn_calculate_subacute)dlsym(g_lib_handle, "nwau_abi_calculate_subacute");

    return 0;
}

/* ============================================================================
 * R EXTERN ".Call" VECTORIZED EVALUATION WRAPPERS
 * ============================================================================ */

SEXP r_nwau_calculate_ed(
    SEXP r_codes,
    SEXP r_price_weights,
    SEXP r_cls_opts,
    SEXP r_elg_opts,
    SEXP r_cmp_statuses,
    SEXP r_dva_statuses
) {
    if (ensure_lib_loaded() != 0 || g_calc_ed == NULL) {
        error("libnwau_c_abi is not available");
    }

    R_xlen_t n = XLENGTH(r_price_weights);
    SEXP out_nwau = PROTECT(allocVector(REALSXP, n));
    double *out_ptr = REAL(out_nwau);
    double *pw_ptr = REAL(r_price_weights);
    int *cls_ptr = INTEGER(r_cls_opts);
    int *elg_ptr = INTEGER(r_elg_opts);
    int *cmp_ptr = INTEGER(r_cmp_statuses);
    int *dva_ptr = INTEGER(r_dva_statuses);

    for (R_xlen_t i = 0; i < n; i++) {
        const char *code_str = CHAR(STRING_ELT(r_codes, i));
        nwau_abi_ed_input input;
        memset(&input, 0, sizeof(input));
        input.code.ptr = code_str;
        input.code.len = strlen(code_str);
        input.classification_option = (uint32_t)cls_ptr[i];
        input.eligibility_option = (uint32_t)elg_ptr[i];
        input.compensable_status = (uint32_t)cmp_ptr[i];
        input.dva_status = (uint32_t)dva_ptr[i];

        nwau_abi_ed_reference_row ref;
        ref.code = input.code;
        ref.price_weight = pw_ptr[i];

        nwau_abi_ed_output out;
        memset(&out, 0, sizeof(out));
        uint32_t status = g_calc_ed(&input, &ref, &out);
        out_ptr[i] = (status == 0 && out.error_code == 0) ? out.nwau : NA_REAL;
    }

    UNPROTECT(1);
    return out_nwau;
}

SEXP r_nwau_calculate_acute_2025(
    SEXP r_drgs,
    SEXP r_los,
    SEXP r_inlier_lower,
    SEXP r_inlier_upper,
    SEXP r_paed_mult,
    SEXP r_same_day_flag,
    SEXP r_same_day_base_weight,
    SEXP r_same_day_per_diem,
    SEXP r_inlier_weight,
    SEXP r_long_stay_per_diem
) {
    if (ensure_lib_loaded() != 0 || g_calc_acute == NULL) {
        error("libnwau_c_abi is not available");
    }

    R_xlen_t n = XLENGTH(r_los);
    SEXP out_nwau = PROTECT(allocVector(REALSXP, n));
    double *out_ptr = REAL(out_nwau);
    double *los_ptr = REAL(r_los);
    double *lb_ptr = REAL(r_inlier_lower);
    double *ub_ptr = REAL(r_inlier_upper);
    double *paed_ptr = REAL(r_paed_mult);
    int *sd_flag_ptr = INTEGER(r_same_day_flag);
    double *sd_base_ptr = REAL(r_same_day_base_weight);
    double *sd_diem_ptr = REAL(r_same_day_per_diem);
    double *iw_ptr = REAL(r_inlier_weight);
    double *ls_diem_ptr = REAL(r_long_stay_per_diem);

    nwau_abi_adjustment_factors adj;
    memset(&adj, 0, sizeof(adj));

    for (R_xlen_t i = 0; i < n; i++) {
        const char *drg_str = CHAR(STRING_ELT(r_drgs, i));
        nwau_abi_episode_input input;
        memset(&input, 0, sizeof(input));
        input.drg.ptr = drg_str;
        input.drg.len = strlen(drg_str);
        input.los = los_ptr[i];
        input.pat_sameday_flag = (uint8_t)sd_flag_ptr[i];

        nwau_abi_reference_row ref;
        memset(&ref, 0, sizeof(ref));
        ref.drg = input.drg;
        ref.inlier_lower_bound = lb_ptr[i];
        ref.inlier_upper_bound = ub_ptr[i];
        ref.paediatric_multiplier = paed_ptr[i];
        ref.same_day_base_weight = sd_base_ptr[i];
        ref.same_day_per_diem = sd_diem_ptr[i];
        ref.inlier_weight = iw_ptr[i];
        ref.long_stay_per_diem = ls_diem_ptr[i];

        nwau_abi_episode_output out;
        memset(&out, 0, sizeof(out));
        uint32_t status = g_calc_acute(&input, &ref, &adj, &out);
        out_ptr[i] = (status == 0 && out.error_code == 0) ? out.nwau25 : NA_REAL;
    }

    UNPROTECT(1);
    return out_nwau;
}

SEXP r_nwau_calculate_outpatients(
    SEXP r_clinic_codes,
    SEXP r_price_weights,
    SEXP r_data_types,
    SEXP r_inscope_flags,
    SEXP r_paed_adjs
) {
    if (ensure_lib_loaded() != 0 || g_calc_op == NULL) {
        error("libnwau_c_abi is not available");
    }

    R_xlen_t n = XLENGTH(r_price_weights);
    SEXP out_nwau = PROTECT(allocVector(REALSXP, n));
    double *out_ptr = REAL(out_nwau);
    double *pw_ptr = REAL(r_price_weights);
    int *dt_ptr = INTEGER(r_data_types);
    int *inscope_ptr = INTEGER(r_inscope_flags);
    double *paed_ptr = REAL(r_paed_adjs);

    for (R_xlen_t i = 0; i < n; i++) {
        const char *clinic_str = CHAR(STRING_ELT(r_clinic_codes, i));
        nwau_abi_outpatient_input input;
        memset(&input, 0, sizeof(input));
        input.clinic_code.ptr = clinic_str;
        input.clinic_code.len = strlen(clinic_str);
        input.data_type = (uint32_t)dt_ptr[i];
        input.inscope_flag = (uint8_t)inscope_ptr[i];
        input.indiv_event_count = 1.0;
        input.paediatric_adjustment = paed_ptr[i];

        nwau_abi_outpatient_reference_row ref;
        ref.clinic_code = input.clinic_code;
        ref.price_weight = pw_ptr[i];
        ref.paediatric_adjustment = paed_ptr[i];

        nwau_abi_outpatient_output out;
        memset(&out, 0, sizeof(out));
        uint32_t status = g_calc_op(&input, &ref, &out);
        out_ptr[i] = (status == 0 && out.error_code == 0) ? out.nwau : NA_REAL;
    }

    UNPROTECT(1);
    return out_nwau;
}

SEXP r_nwau_calculate_subacute(
    SEXP r_ansnap_codes,
    SEXP r_los,
    SEXP r_pw_inliers,
    SEXP r_inlier_lower,
    SEXP r_inlier_upper,
    SEXP r_ages
) {
    if (ensure_lib_loaded() != 0 || g_calc_sub == NULL) {
        error("libnwau_c_abi is not available");
    }

    R_xlen_t n = XLENGTH(r_pw_inliers);
    SEXP out_nwau = PROTECT(allocVector(REALSXP, n));
    double *out_ptr = REAL(out_nwau);
    double *los_ptr = REAL(r_los);
    double *pw_ptr = REAL(r_pw_inliers);
    double *lb_ptr = REAL(r_inlier_lower);
    double *ub_ptr = REAL(r_inlier_upper);
    double *age_ptr = REAL(r_ages);

    for (R_xlen_t i = 0; i < n; i++) {
        const char *ansnap_str = CHAR(STRING_ELT(r_ansnap_codes, i));
        nwau_abi_subacute_input input;
        memset(&input, 0, sizeof(input));
        input.ansnap.ptr = ansnap_str;
        input.ansnap.len = strlen(ansnap_str);
        input.los = los_ptr[i];
        input.age = age_ptr[i];
        input.pat_public_flag = 1;
        input.state = 1;

        nwau_abi_subacute_reference_row ref;
        memset(&ref, 0, sizeof(ref));
        ref.ansnap = input.ansnap;
        ref.inlier_lower_bound = lb_ptr[i];
        ref.inlier_upper_bound = ub_ptr[i];
        ref.pw_inlier = pw_ptr[i];

        nwau_abi_subacute_output out;
        memset(&out, 0, sizeof(out));
        uint32_t status = g_calc_sub(&input, &ref, &out);
        out_ptr[i] = (status == 0 && out.error_code == 0) ? out.nwau : NA_REAL;
    }

    UNPROTECT(1);
    return out_nwau;
}

SEXP r_nwau_calculate_mh(
    SEXP r_amhcc_codes,
    SEXP r_los,
    SEXP r_inlier_weights,
    SEXP r_inlier_lower,
    SEXP r_inlier_upper,
    SEXP r_price_cats
) {
    if (ensure_lib_loaded() != 0 || g_calc_mh == NULL) {
        error("libnwau_c_abi is not available");
    }

    R_xlen_t n = XLENGTH(r_inlier_weights);
    SEXP out_nwau = PROTECT(allocVector(REALSXP, n));
    double *out_ptr = REAL(out_nwau);
    double *los_ptr = REAL(r_los);
    double *iw_ptr = REAL(r_inlier_weights);
    double *lb_ptr = REAL(r_inlier_lower);
    double *ub_ptr = REAL(r_inlier_upper);
    int *cat_ptr = INTEGER(r_price_cats);

    for (R_xlen_t i = 0; i < n; i++) {
        const char *amhcc_str = CHAR(STRING_ELT(r_amhcc_codes, i));
        nwau_abi_mh_input input;
        memset(&input, 0, sizeof(input));
        input.amhcc.ptr = amhcc_str;
        input.amhcc.len = strlen(amhcc_str);
        input.los = los_ptr[i];
        input.state = 1;
        input.specialist_paediatric_multiplier = 1.0;

        nwau_abi_mh_admitted_reference_row ref;
        memset(&ref, 0, sizeof(ref));
        ref.amhcc = input.amhcc;
        ref.price_cat = (uint32_t)cat_ptr[i];
        ref.inlier_lower_bound = lb_ptr[i];
        ref.inlier_upper_bound = ub_ptr[i];
        ref.inlier_weight = iw_ptr[i];

        nwau_abi_mh_output out;
        memset(&out, 0, sizeof(out));
        uint32_t status = g_calc_mh(&input, &ref, &out);
        out_ptr[i] = (status == 0 && out.error_code == 0) ? out.nwau : NA_REAL;
    }

    UNPROTECT(1);
    return out_nwau;
}

/* ============================================================================
 * R REGISTRATION
 * ============================================================================ */

static const R_CallMethodDef CallEntries[] = {
    {"r_nwau_calculate_ed", (DL_FUNC) &r_nwau_calculate_ed, 6},
    {"r_nwau_calculate_acute_2025", (DL_FUNC) &r_nwau_calculate_acute_2025, 10},
    {"r_nwau_calculate_outpatients", (DL_FUNC) &r_nwau_calculate_outpatients, 5},
    {"r_nwau_calculate_subacute", (DL_FUNC) &r_nwau_calculate_subacute, 6},
    {"r_nwau_calculate_mh", (DL_FUNC) &r_nwau_calculate_mh, 6},
    {NULL, NULL, 0}
};

void R_init_nwauR(DllInfo *dll) {
    R_registerRoutines(dll, NULL, CallEntries, NULL, NULL);
    R_useDynamicSymbols(dll, FALSE);
}
