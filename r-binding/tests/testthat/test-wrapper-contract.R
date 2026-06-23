test_that("package exposes wrapper-only API", {
  expect_true(exists("nwau_calculate"))
  expect_true(exists("nwau_acute"))
  expect_true(exists("nwau_ed"))
  expect_true(exists("nwau_non_admitted"))
  expect_true(exists("nwau_diagnose"))
  expect_true(exists("nwau_cli_contract"))
  expect_true(exists("validate_nwau_input"))
})

test_that("diagnose reports CLI failures without formula fallback", {
  result <- nwau_diagnose(
    data.frame(DRG = "801A", LOS = 1),
    stream = "acute",
    python = "definitely-not-a-python-binary"
  )

  expect_false(result$ok)
  expect_true(result$status != 0L)
  expect_true(any(grepl("definitely-not-a-python-binary", result$command)))
})

test_that("input validation enforces concrete CSV handoff", {
  expect_error(validate_nwau_input(data.frame()), "at least one column")
  expect_error(validate_nwau_input(tempdir()), "CSV file, not a directory")
  expect_error(validate_nwau_input("missing.csv"), "existing CSV file")

  input <- tempfile(fileext = ".txt")
  writeLines("DRG,LOS", input)
  expect_error(validate_nwau_input(input), ".csv file", fixed = TRUE)
})

test_that("output validation catches missing CLI artifacts", {
  expect_error(parse_nwau_output(tempfile(fileext = ".csv")), "did not create output CSV")
})

test_that("successful CSV readback preserves Python-produced columns", {
  output <- tempfile(fileext = ".csv")
  writeLines(c("episode_id,nwau", "A,1.25"), output)

  result <- parse_nwau_output(output)

  expect_equal(names(result), c("episode_id", "nwau"))
  expect_equal(result$episode_id, "A")
  expect_equal(result$nwau, 1.25)
})

test_that("argument construction records the selected shared CLI boundary", {
  input <- tempfile(fileext = ".csv")
  output <- tempfile(fileext = ".csv")
  params <- tempdir()

  args <- nwau_build_args(
    stream = "non-admitted",
    input_csv = input,
    output_csv = output,
    year = 2025,
    params = params,
    module = "nwau_py.cli.main"
  )

  expect_equal(args[1:2], c("-m", "nwau_py.cli.main"))
  expect_true("non-admitted" %in% args)
  expect_true("--output" %in% args)
  expect_true("--year" %in% args)
  expect_true("--params" %in% args)
})

test_that("CLI contract probe reports command failures without formula fallback", {
  result <- nwau_cli_contract(python = "definitely-not-a-python-binary")

  expect_false(result$ok)
  expect_true(result$status != 0L)
  expect_null(result$contract)
  expect_true(any(grepl("interop", result$command)))
})

test_that("CLI contract probe captures successful contract output", {
  python <- tempfile(fileext = if (.Platform$OS.type == "windows") ".bat" else "")
  if (.Platform$OS.type == "windows") {
    writeLines(c("@echo off", "echo {\"contract\":\"cli_file_interop\"}"), python)
  } else {
    writeLines(c("#!/usr/bin/env sh", "echo '{\"contract\":\"cli_file_interop\"}'"), python)
    Sys.chmod(python, "0755")
  }

  result <- nwau_cli_contract(python = python, module = "nwau_py.cli.main")

  expect_true(result$ok)
  expect_equal(result$status, 0L)
  expect_match(result$contract, "cli_file_interop")
  expect_true(any(grepl("interop", result$command)))
})
