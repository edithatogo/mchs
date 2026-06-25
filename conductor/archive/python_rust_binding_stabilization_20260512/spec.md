# Specification: Python Rust Binding Stabilization

## Overview
Stabilize the Python binding layer over the Rust calculator core using pyo3 and maturin. Python remains the primary public API until Rust parity is proven calculator by calculator.

## Functional Requirements
- Define the stable Python-to-Rust boundary for batch calculator calls.
- Keep Rust-backed execution opt-in until parity is recorded.
- Share golden fixtures between pure Python and Rust-backed paths.
- Document packaging, wheels, fallback behavior, and platform support.

## Acceptance Criteria
- Python users can opt into Rust-backed execution for validated calculators.
- Pure Python fallback remains available where Rust parity is incomplete.
- CI builds and tests the extension across the supported Python matrix.
