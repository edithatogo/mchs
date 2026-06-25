# Specification: R Binding

## Overview
Provide an R integration path for analysts doing health economics, costing studies, and reporting. The R surface must call the shared calculator core or CLI/data-file interface and must not reimplement formulas.

## Functional Requirements
- Evaluate extendr, reticulate, and CLI/Arrow-file integration paths.
- Define an R package API for batch calculation and validation diagnostics.
- Reuse shared golden fixtures and synthetic costing-study examples.
- Document installation and use from R Markdown/Quarto.

## Acceptance Criteria
- A selected R binding strategy is documented with tradeoffs.
- Formula logic remains single-sourced outside the R wrapper.
- R examples run against synthetic fixtures.
