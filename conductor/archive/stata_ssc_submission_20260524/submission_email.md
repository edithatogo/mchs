# SSC submission email draft

To: baum@bc.edu
Subject: SSC submission: mchs-stata-interop 0.1.0

Dear Professor Baum,

I would like to submit a new Stata package for consideration in the SSC archive.

Package: mchs-stata-interop
Version: 0.1.0
Author/maintainer: Dylan Mordaunt <dylan.mordaunt@vuw.ac.nz>
License: MIT
Repository: https://github.com/edithatogo/mchs
Archive: bindings/stata/mchs-stata-interop-0.1.0.zip
Archive SHA-256: 58592db4e6feb5bdfc78a3fd34b91e0e86f859dc06de5fdf40cd7a8f2a7b0ffd

Short description:

mchs-stata-interop provides boundary-only Stata integration files for the MCHS/NWAU tooling. The package includes ado/help/pkg metadata and examples for invoking the external command-line/file workflow without reimplementing pricing or clinical formula logic in Stata.

Included files:

- mchs.ado
- mchs.sthlp
- pkg-mchs.pkg
- README.md
- LICENSE
- stata-interop-notes.md
- examples/file_import_workflow.do
- examples/nwau_cli_invocation.do

The prepared SSC package index is `bindings/stata/pkg-mchs.pkg`. No Stata runtime validation is claimed from this machine because Stata is not installed locally; the package is intentionally limited to a thin interop boundary around external files/CLI behavior.

Please let me know if you would prefer a different archive layout, package name, or metadata wording for SSC review.

Kind regards,
Dylan Mordaunt
