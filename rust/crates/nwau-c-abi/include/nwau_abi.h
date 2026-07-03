#ifndef NWAU_ABI_H
#define NWAU_ABI_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * C ABI for the NWAU proof of concept.
 *
 * Ownership and lifetime rules:
 * - `nwau_abi_string_view.ptr` is a borrowed pointer. The callee never takes
 *   ownership and never frees it.
 * - `nwau_abi_kernel_label()` and `nwau_abi_status_message()` return borrowed
 *   static views. The caller must not free them and may use them until process
 *   exit.
 * - Input string views are borrowed for the duration of the call. The caller
 *   must keep the backing storage alive until the function returns.
 * - `nwau_abi_calculate_acute_2025()` writes into caller-provided output
 *   storage. The caller owns that storage and is responsible for allocating it
 *   before the call.
 *
 * Error semantics:
 * - All exported functions return plain status values or borrowed views.
 * - `nwau_abi_calculate_acute_2025()` validates non-null pointers, delegates
 *   to the Rust acute 2025 core, writes deterministic output, and returns
 *   `NWAU_ABI_STATUS_OK` for valid pointer shapes.
 */

#if defined(_WIN32)
#  if defined(NWAU_ABI_BUILDING_DLL)
#    define NWAU_ABI_API __declspec(dllexport)
#  else
#    define NWAU_ABI_API __declspec(dllimport)
#  endif
#else
#  define NWAU_ABI_API
#endif

typedef struct nwau_abi_string_view {
    const char *ptr;
    size_t len;
} nwau_abi_string_view;

typedef struct nwau_abi_episode_input {
    nwau_abi_string_view drg;
    double los;
    double icu_hours;
    double icu_other;
    uint8_t pat_sameday_flag;
    uint8_t pat_private_flag;
    uint8_t pat_covid_flag;
    uint8_t eligible_paed_flag;
} nwau_abi_episode_input;

typedef struct nwau_abi_reference_row {
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

typedef struct nwau_abi_adjustment_factors {
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

typedef struct nwau_abi_episode_output {
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

typedef uint32_t nwau_abi_status;

#define NWAU_ABI_VERSION_MAJOR UINT32_C(0)
#define NWAU_ABI_VERSION_MINOR UINT32_C(2)
#define NWAU_ABI_VERSION_PATCH UINT32_C(0)
#define NWAU_ABI_STATUS_OK UINT32_C(0)
#define NWAU_ABI_STATUS_INVALID_ARGUMENT UINT32_C(1)
#define NWAU_ABI_STATUS_UNIMPLEMENTED UINT32_C(2)
#define NWAU_ABI_STATUS_UNKNOWN UINT32_C(4294967295)

NWAU_ABI_API uint32_t nwau_abi_version_major(void);
NWAU_ABI_API uint32_t nwau_abi_version_minor(void);
NWAU_ABI_API uint32_t nwau_abi_version_patch(void);
NWAU_ABI_API nwau_abi_string_view nwau_abi_kernel_label(void);
NWAU_ABI_API nwau_abi_string_view nwau_abi_status_message(nwau_abi_status status);
NWAU_ABI_API nwau_abi_status nwau_abi_calculate_acute_2025(
    const nwau_abi_episode_input *input,
    const nwau_abi_reference_row *reference,
    const nwau_abi_adjustment_factors *adjustments,
    nwau_abi_episode_output *out);

#ifdef __cplusplus
}
#endif

#endif /* NWAU_ABI_H */
