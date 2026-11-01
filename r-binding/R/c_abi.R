# Formula logic remains in the shared core; this module provides direct in-process C-ABI bindings.

#' In-Process C-ABI Emergency Department Valuation
#' @export
nwau_ed_c_abi <- function(code, price_weight, classification_option = 3L, eligibility_option = 1L, compensable_status = 2L, dva_status = 2L) {
  n <- length(price_weight)
  if (length(code) == 1L && n != 1L) code <- rep(code, n)
  if (length(classification_option) == 1L && n != 1L) classification_option <- rep(classification_option, n)
  if (length(eligibility_option) == 1L && n != 1L) eligibility_option <- rep(eligibility_option, n)
  if (length(compensable_status) == 1L && n != 1L) compensable_status <- rep(compensable_status, n)
  if (length(dva_status) == 1L && n != 1L) dva_status <- rep(dva_status, n)

  .Call("r_nwau_calculate_ed",
        as.character(code),
        as.numeric(price_weight),
        as.integer(classification_option),
        as.integer(eligibility_option),
        as.integer(compensable_status),
        as.integer(dva_status))
}

#' In-Process C-ABI Acute Valuation
#' @export
nwau_acute_c_abi <- function(drg, los, inlier_lower_bound, inlier_upper_bound, inlier_weight,
                              paediatric_multiplier = 1.0, same_day_list_flag = 0L,
                              same_day_base_rate = 0.0, same_day_diem_rate = 0.0, long_stay_rate = 0.0, pat_sameday_flag = FALSE) {
  n <- length(los)
  if (length(drg) == 1L && n != 1L) drg <- rep(drg, n)
  if (length(inlier_lower_bound) == 1L && n != 1L) inlier_lower_bound <- rep(inlier_lower_bound, n)
  if (length(inlier_upper_bound) == 1L && n != 1L) inlier_upper_bound <- rep(inlier_upper_bound, n)
  if (length(inlier_weight) == 1L && n != 1L) inlier_weight <- rep(inlier_weight, n)
  if (length(paediatric_multiplier) == 1L && n != 1L) paediatric_multiplier <- rep(paediatric_multiplier, n)
  if (length(pat_sameday_flag) == 1L && n != 1L) pat_sameday_flag <- rep(pat_sameday_flag, n)
  if (length(same_day_list_flag) == 1L && n != 1L) same_day_list_flag <- rep(same_day_list_flag, n)
  if (length(same_day_base_rate) == 1L && n != 1L) same_day_base_rate <- rep(same_day_base_rate, n)
  if (length(same_day_diem_rate) == 1L && n != 1L) same_day_diem_rate <- rep(same_day_diem_rate, n)
  if (length(long_stay_rate) == 1L && n != 1L) long_stay_rate <- rep(long_stay_rate, n)

  .Call("r_nwau_calculate_acute_2025",
        as.character(drg),
        as.numeric(los),
        as.numeric(inlier_lower_bound),
        as.numeric(inlier_upper_bound),
        as.numeric(paediatric_multiplier),
        as.integer(same_day_list_flag),
        as.integer(pat_sameday_flag),
        as.numeric(same_day_base_rate),
        as.numeric(same_day_diem_rate),
        as.numeric(inlier_weight),
        as.numeric(long_stay_rate))
}

#' In-Process C-ABI Outpatients Valuation
#' @export
nwau_outpatients_c_abi <- function(clinic_code, price_weight, data_type = 1L, inscope_flag = 1L, paediatric_adjustment = 1.0) {
  n <- length(price_weight)
  if (length(clinic_code) == 1L && n != 1L) clinic_code <- rep(clinic_code, n)
  if (length(data_type) == 1L && n != 1L) data_type <- rep(data_type, n)
  if (length(inscope_flag) == 1L && n != 1L) inscope_flag <- rep(inscope_flag, n)
  if (length(paediatric_adjustment) == 1L && n != 1L) paediatric_adjustment <- rep(paediatric_adjustment, n)

  .Call("r_nwau_calculate_outpatients",
        as.character(clinic_code),
        as.numeric(price_weight),
        as.integer(data_type),
        as.integer(inscope_flag),
        as.numeric(paediatric_adjustment))
}

#' In-Process C-ABI Subacute Valuation
#' @export
nwau_subacute_c_abi <- function(ansnap, los, pw_inlier, inlier_lower_bound, inlier_upper_bound, age = 50.0) {
  n <- length(pw_inlier)
  if (length(ansnap) == 1L && n != 1L) ansnap <- rep(ansnap, n)
  if (length(los) == 1L && n != 1L) los <- rep(los, n)
  if (length(inlier_lower_bound) == 1L && n != 1L) inlier_lower_bound <- rep(inlier_lower_bound, n)
  if (length(inlier_upper_bound) == 1L && n != 1L) inlier_upper_bound <- rep(inlier_upper_bound, n)
  if (length(age) == 1L && n != 1L) age <- rep(age, n)

  .Call("r_nwau_calculate_subacute",
        as.character(ansnap),
        as.numeric(los),
        as.numeric(pw_inlier),
        as.numeric(inlier_lower_bound),
        as.numeric(inlier_upper_bound),
        as.numeric(age))
}

#' In-Process C-ABI Mental Health Valuation
#' @export
nwau_mh_c_abi <- function(amhcc, los, inlier_weight, inlier_lower_bound, inlier_upper_bound, price_cat = 1L) {
  n <- length(inlier_weight)
  if (length(amhcc) == 1L && n != 1L) amhcc <- rep(amhcc, n)
  if (length(los) == 1L && n != 1L) los <- rep(los, n)
  if (length(inlier_lower_bound) == 1L && n != 1L) inlier_lower_bound <- rep(inlier_lower_bound, n)
  if (length(inlier_upper_bound) == 1L && n != 1L) inlier_upper_bound <- rep(inlier_upper_bound, n)
  if (length(price_cat) == 1L && n != 1L) price_cat <- rep(price_cat, n)

  .Call("r_nwau_calculate_mh",
        as.character(amhcc),
        as.numeric(los),
        as.numeric(inlier_weight),
        as.numeric(inlier_lower_bound),
        as.numeric(inlier_upper_bound),
        as.integer(price_cat))
}

#' Batch in-process valuation over tabular datasets (data.frame, arrow, data.table)
#' @export
nwau_batch_c_abi <- function(stream, df) {
  stream <- match.arg(stream, c("ed", "acute", "outpatients", "subacute", "mh"))
  if (stream == "ed") {
    cls <- if ("classification_option" %in% names(df)) df$classification_option else 3L
    elg <- if ("eligibility_option" %in% names(df)) df$eligibility_option else 1L
    cmp <- if ("compensable_status" %in% names(df)) df$compensable_status else 2L
    dva <- if ("dva_status" %in% names(df)) df$dva_status else 2L
    nwau_ed_c_abi(df$code, df$price_weight, cls, elg, cmp, dva)
  } else if (stream == "acute") {
    pm <- if ("paediatric_multiplier" %in% names(df)) df$paediatric_multiplier else 1.0
    sd <- if ("same_day_list_flag" %in% names(df)) df$same_day_list_flag else 0L
    sb <- if ("same_day_base_weight" %in% names(df)) df$same_day_base_weight else 0.0
    sp <- if ("same_day_per_diem" %in% names(df)) df$same_day_per_diem else 0.0
    ls <- if ("long_stay_per_diem" %in% names(df)) df$long_stay_per_diem else 0.0
    nwau_acute_c_abi(df$drg, df$los, df$inlier_lower_bound, df$inlier_upper_bound, df$inlier_weight,
                     pm, sd, sb, sp, ls, if ("pat_sameday_flag" %in% names(df)) df$pat_sameday_flag else FALSE)
  } else if (stream == "outpatients") {
    dt <- if ("data_type" %in% names(df)) df$data_type else 1L
    ins <- if ("inscope_flag" %in% names(df)) df$inscope_flag else 1L
    pa <- if ("paediatric_adjustment" %in% names(df)) df$paediatric_adjustment else 1.0
    nwau_outpatients_c_abi(df$clinic_code, df$price_weight, dt, ins, pa)
  } else if (stream == "subacute") {
    age <- if ("age" %in% names(df)) df$age else 50.0
    nwau_subacute_c_abi(df$ansnap, df$los, df$pw_inlier, df$inlier_lower_bound, df$inlier_upper_bound, age)
  } else if (stream == "mh") {
    pc <- if ("price_cat" %in% names(df)) df$price_cat else 1L
    nwau_mh_c_abi(df$amhcc, df$los, df$inlier_weight, df$inlier_lower_bound, df$inlier_upper_bound, pc)
  }
}
