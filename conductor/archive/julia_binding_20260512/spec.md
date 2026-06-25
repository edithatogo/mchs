# Specification: Julia Binding

## Overview
Provide a Julia integration path for high-performance analytics and health-economics workflows. Julia should consume the shared calculator core through a C ABI or Arrow/CLI interface rather than reimplementing formulas.

## Functional Requirements
- Evaluate C ABI, PythonCall, and Arrow/CLI integration paths.
- Define a Julia package API for batch calculation and validation diagnostics.
- Reuse shared golden fixtures.
- Document DataFrame/Arrow workflow examples.

## Acceptance Criteria
- A selected Julia binding strategy is documented.
- Julia examples validate against shared fixtures.
- No formula logic is duplicated in Julia.
