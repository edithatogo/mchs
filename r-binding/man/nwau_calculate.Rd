\name{nwau_calculate}
\alias{nwau_calculate}
\alias{nwau_acute}
\alias{nwau_ed}
\alias{nwau_non_admitted}
\alias{nwau_diagnose}
\title{Run NWAU calculations through the shared Python CLI}
\usage{
nwau_calculate(input, stream = c("acute", "ed", "non-admitted"), year = NULL,
  params = NULL, output = NULL, python = nwau_default_python(),
  module = nwau_default_module())
nwau_acute(input, year = NULL, params = NULL, output = NULL,
  python = nwau_default_python(), module = nwau_default_module())
nwau_ed(input, year = NULL, params = NULL, output = NULL,
  python = nwau_default_python(), module = nwau_default_module())
nwau_non_admitted(input, year = NULL, params = NULL, output = NULL,
  python = nwau_default_python(), module = nwau_default_module())
nwau_diagnose(input, stream = c("acute", "ed", "non-admitted"), year = NULL,
  params = NULL, python = nwau_default_python(),
  module = nwau_default_module())
}
\arguments{
\item{input}{A data frame or path to a CSV input file.}
\item{stream}{Calculator stream to run.}
\item{year}{Optional pricing year.}
\item{params}{Optional path to calculator reference data.}
\item{output}{Optional output CSV path.}
\item{python}{Python executable used to invoke the shared CLI.}
\item{module}{Python module path for the shared CLI.}
}
\description{
These helpers are thin wrappers over \code{python -m nwau_py.cli.main}. They
perform file handoff and result loading only; calculator formulas and
validation remain in the shared Python implementation.
}
\value{
\code{nwau_calculate()} and stream helpers return a data frame. \code{nwau_diagnose()}
returns a list containing command status, command arguments, output, and error
message fields.
}
\examples{
\dontrun{
input <- data.frame(DRG = "801A", LOS = 1)
diagnostic <- nwau_diagnose(input, stream = "acute", year = 2025)
diagnostic$ok
}
}
