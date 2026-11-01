test_that("in-process C-ABI valuation works across all 5 streams", {
  so_path <- file.path("..", "..", "src", "nwauR.so")
  if (file.exists(so_path)) {
    dyn.load(so_path)
  }

  # 1. ED
  ed_val <- nwau_ed_c_abi(code = "E0110A", price_weight = 0.2837)
  expect_equal(round(ed_val, 4), 0.2837)

  # 2. Outpatients
  op_val <- nwau_outpatients_c_abi(clinic_code = "10.01", price_weight = 0.1742)
  expect_equal(round(op_val, 4), 0.1742)

  # 3. Subacute
  sub_val <- nwau_subacute_c_abi(ansnap = "5AA1", los = 10.0, pw_inlier = 1.854,
                                 inlier_lower_bound = 3.0, inlier_upper_bound = 20.0)
  expect_equal(round(sub_val, 4), 1.8540)

  # 4. Mental Health
  mh_val <- nwau_mh_c_abi(amhcc = "101A", los = 5.0, inlier_weight = 1.2345,
                          inlier_lower_bound = 2.0, inlier_upper_bound = 10.0)
  expect_equal(round(mh_val, 4), 1.2345)

  # 5. Acute
  acute_val <- nwau_acute_c_abi(drg = "801A", los = 10.0, inlier_lower_bound = 8.0,
                                inlier_upper_bound = 35.0, inlier_weight = 9.2472)
  expect_equal(round(acute_val, 4), 9.2472)

  # 6. Batch evaluation
  df_ed <- data.frame(code = c("E0110A", "E0110B"), price_weight = c(0.2837, 0.1542))
  batch_ed <- nwau_batch_c_abi("ed", df_ed)
  expect_equal(round(batch_ed[1], 4), 0.2837)
  expect_equal(round(batch_ed[2], 4), 0.1542)
})

test_that("vector lengths and patient and reference same-day flags are independent", {
  expect_error(nwau_ed_c_abi(code = c("A", "B"), price_weight = c(.1, .2, .3)),
               "argument lengths must match")
  value <- nwau_acute_c_abi(drg = "A", los = c(1, 1, 1), inlier_lower_bound = 2,
                            inlier_upper_bound = 10, inlier_weight = 1,
                            same_day_base_rate = .4, same_day_diem_rate = .2,
                            same_day_list_flag = c(1L, 1L, 0L),
                            pat_sameday_flag = c(TRUE, FALSE, TRUE))
  expect_equal(value, c(.4, .6, .6))
})
