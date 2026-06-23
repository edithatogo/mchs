nwau_streams <- c("acute", "ed", "non-admitted")

nwau_default_python <- function() {
  python <- getOption("nwau.python")
  if (!is.null(python) && nzchar(python)) {
    return(python)
  }

  for (candidate in c("python3", "python")) {
    if (nzchar(Sys.which(candidate))) {
      return(candidate)
    }
  }

  "python3"
}

nwau_default_module <- function() {
  module <- getOption("nwau.module")
  if (!is.null(module) && nzchar(module)) {
    return(module)
  }

  "nwau_py.cli.main"
}

nwau_validate_csv_path <- function(path, field) {
  if (!is.character(path) || length(path) != 1L || !nzchar(path)) {
    stop(sprintf("`%s` must be a single non-empty file path.", field), call. = FALSE)
  }

  expanded <- path.expand(path)
  if (!file.exists(expanded)) {
    stop(sprintf("`%s` must point to an existing CSV file.", field), call. = FALSE)
  }
  if (dir.exists(expanded)) {
    stop(sprintf("`%s` must point to a CSV file, not a directory.", field), call. = FALSE)
  }
  if (!grepl("\\.csv$", expanded, ignore.case = TRUE)) {
    stop(sprintf("`%s` must point to a .csv file.", field), call. = FALSE)
  }

  normalizePath(expanded, winslash = "/", mustWork = TRUE)
}

validate_nwau_input <- function(input) {
  if (is.data.frame(input)) {
    if (ncol(input) == 0L) {
      stop("`input` data.frame must contain at least one column.", call. = FALSE)
    }
    if (any(!nzchar(names(input)))) {
      stop("`input` data.frame columns must be named for CSV handoff.", call. = FALSE)
    }
    return(invisible(TRUE))
  }

  nwau_validate_csv_path(input, "input")
  invisible(TRUE)
}

nwau_as_input_path <- function(input) {
  if (is.data.frame(input)) {
    validate_nwau_input(input)
    path <- tempfile(pattern = "nwau-input-", fileext = ".csv")
    utils::write.csv(input, path, row.names = FALSE, na = "")
    return(list(
      path = path,
      cleanup = function() unlink(path)
    ))
  }

  if (is.character(input) && length(input) == 1L) {
    return(list(
      path = nwau_validate_csv_path(input, "input"),
      cleanup = function() invisible(NULL)
    ))
  }

  stop("`input` must be a data.frame or an existing CSV file path.", call. = FALSE)
}

nwau_output_path <- function(output, stream) {
  if (is.null(output)) {
    path <- tempfile(pattern = paste0("nwau-", stream, "-"), fileext = ".csv")
    return(list(
      path = path,
      cleanup = function() unlink(path),
      temporary = TRUE
    ))
  }

  if (!is.character(output) || length(output) != 1L || !nzchar(output)) {
    stop("`output` must be NULL or a single file path.", call. = FALSE)
  }

  expanded <- path.expand(output)
  if (dir.exists(expanded)) {
    stop("`output` must point to a CSV file path, not a directory.", call. = FALSE)
  }
  if (!grepl("\\.csv$", expanded, ignore.case = TRUE)) {
    stop("`output` must point to a .csv file.", call. = FALSE)
  }

  parent <- dirname(expanded)
  if (!dir.exists(parent)) {
    stop("`output` parent directory must exist.", call. = FALSE)
  }

  list(
    path = normalizePath(expanded, winslash = "/", mustWork = FALSE),
    cleanup = function() invisible(NULL),
    temporary = FALSE
  )
}

nwau_build_args <- function(stream, input_csv, output_csv, year, params, module) {
  if (!is.character(module) || length(module) != 1L || !nzchar(module)) {
    stop("`module` must be a single non-empty Python module path.", call. = FALSE)
  }

  command <- c(
    "-m", module,
    if (stream == "non-admitted") "non-admitted" else stream,
    input_csv,
    "--output", output_csv
  )

  if (!is.null(year)) {
    command <- c(command, "--year", as.character(year))
  }

  if (!is.null(params)) {
    if (!is.character(params) || length(params) != 1L || !nzchar(params)) {
      stop("`params` must be NULL or a single directory path.", call. = FALSE)
    }
    expanded_params <- path.expand(params)
    if (!dir.exists(expanded_params)) {
      stop("`params` must point to an existing directory.", call. = FALSE)
    }
    command <- c(command, "--params", normalizePath(expanded_params, winslash = "/", mustWork = TRUE))
  }

  command
}

nwau_system2 <- function(python, args) {
  error_message <- NULL
  output <- tryCatch(
    system2(python, args, stdout = TRUE, stderr = TRUE),
    error = function(e) {
      error_message <<- conditionMessage(e)
      character()
    }
  )

  status <- attr(output, "status")
  if (is.null(status)) {
    status <- if (is.null(error_message)) 0L else 127L
  }

  list(
    command = c(python, args),
    output = unname(output),
    status = as.integer(status),
    error_message = error_message
  )
}

nwau_cli_error <- function(result) {
  command <- paste(shQuote(result$command), collapse = " ")
  output <- if (length(result$output)) paste(result$output, collapse = "\n") else ""
  details <- c(
    sprintf("NWAU CLI command failed with status %s.", result$status),
    paste("Command:", command)
  )

  if (nzchar(result$error_message %||% "")) {
    details <- c(details, paste("Error:", result$error_message))
  }

  if (nzchar(output)) {
    details <- c(details, "Output:", output)
  }

  paste(details, collapse = "\n")
}

`%||%` <- function(x, y) {
  if (is.null(x) || length(x) == 0L || is.na(x) || !nzchar(x)) {
    y
  } else {
    x
  }
}

nwau_run_cli <- function(
    input,
    stream = c("acute", "ed", "non-admitted"),
    year = NULL,
    params = NULL,
    output = NULL,
    python = nwau_default_python(),
    module = nwau_default_module()) {
  stream <- match.arg(stream, nwau_streams)
  input_ref <- nwau_as_input_path(input)
  output_ref <- nwau_output_path(output, stream)
  args <- nwau_build_args(stream, input_ref$path, output_ref$path, year, params, module)

  result <- nwau_system2(python, args)
  result$input_csv <- input_ref$path
  result$output_csv <- output_ref$path
  result$cleanup_input <- input_ref$cleanup
  result$cleanup_output <- output_ref$cleanup
  result$output_temporary <- isTRUE(output_ref$temporary)
  result
}

nwau_assert_output_file <- function(path) {
  if (!file.exists(path)) {
    stop(sprintf("NWAU CLI completed but did not create output CSV: %s", path), call. = FALSE)
  }
  if (file.info(path)$size == 0L) {
    stop(sprintf("NWAU CLI completed but output CSV is empty: %s", path), call. = FALSE)
  }
  invisible(TRUE)
}

parse_nwau_output <- function(output_csv) {
  nwau_assert_output_file(output_csv)
  utils::read.csv(output_csv, stringsAsFactors = FALSE, check.names = FALSE)
}

nwau_calculate <- function(
    input,
    stream = c("acute", "ed", "non-admitted"),
    year = NULL,
    params = NULL,
    output = NULL,
    python = nwau_default_python(),
    module = nwau_default_module()) {
  result <- nwau_run_cli(
    input = input,
    stream = stream,
    year = year,
    params = params,
    output = output,
    python = python,
    module = module
  )

  on.exit(result$cleanup_input(), add = TRUE)
  if (isTRUE(result$output_temporary)) {
    on.exit(result$cleanup_output(), add = TRUE)
  }

  if (result$status != 0L) {
    stop(nwau_cli_error(result), call. = FALSE)
  }

  parse_nwau_output(result$output_csv)
}

nwau_acute <- function(input, year = NULL, params = NULL, output = NULL, python = nwau_default_python(), module = nwau_default_module()) {
  nwau_calculate(
    input = input,
    stream = "acute",
    year = year,
    params = params,
    output = output,
    python = python,
    module = module
  )
}

nwau_ed <- function(input, year = NULL, params = NULL, output = NULL, python = nwau_default_python(), module = nwau_default_module()) {
  nwau_calculate(
    input = input,
    stream = "ed",
    year = year,
    params = params,
    output = output,
    python = python,
    module = module
  )
}

nwau_non_admitted <- function(input, year = NULL, params = NULL, output = NULL, python = nwau_default_python(), module = nwau_default_module()) {
  nwau_calculate(
    input = input,
    stream = "non-admitted",
    year = year,
    params = params,
    output = output,
    python = python,
    module = module
  )
}

nwau_diagnose <- function(
    input,
    stream = c("acute", "ed", "non-admitted"),
    year = NULL,
    params = NULL,
    python = nwau_default_python(),
    module = nwau_default_module()) {
  result <- nwau_run_cli(
    input = input,
    stream = stream,
    year = year,
    params = params,
    output = NULL,
    python = python,
    module = module
  )

  on.exit(result$cleanup_input(), add = TRUE)
  on.exit(result$cleanup_output(), add = TRUE)

  list(
    ok = result$status == 0L,
    status = result$status,
    command = result$command,
    output = result$output,
    error_message = result$error_message
  )
}

nwau_cli_contract <- function(
    python = nwau_default_python(),
    module = nwau_default_module()) {
  args <- c("-m", module, "interop", "contract")
  result <- nwau_system2(python, args)
  list(
    ok = result$status == 0L,
    status = result$status,
    command = result$command,
    contract = if (result$status == 0L) paste(result$output, collapse = "\n") else NULL,
    output = result$output,
    error_message = result$error_message
  )
}
