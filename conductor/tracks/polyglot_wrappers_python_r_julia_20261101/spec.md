# Specification: Zero-Copy Polyglot Wrappers (Python, R, Julia)

## Objective
Convert all three client-facing language packages (`nwau_py`, `nwauR`, and `NationalWeightedActivityUnitWrapper.jl`) into ultra-thin, zero-copy adapters delegating 100% of mathematical computation to `nwau-core`.

## Requirements
1. **Python Inversion (`pyo3-polars`):**
   - Replace scalar row-by-row FFI with vectorized Polars expression plugins (`#[polars_expr]`).
   - Allow execution across Polars series directly inside the Polars engine threadpool without acquiring the Python GIL.
   - Refactor `nwau_py/calculators/*.py` to delete duplicated pure-Python formula algorithms.
2. **Julia Zero-Overhead `ccall`:**
   - Call native C ABI functions in `libnwau_c_abi` directly via Julia's `ccall`.
   - Accept Julia `DataFrame` or `Arrow.Table`, compute NWAU in Rust, and return typed Julia arrays.
3. **R Integration:**
   - Wire `nwauR` to call `libnwau_c_abi` via `extendr` or native C FFI using `nanoarrow`.
   - Support R `data.frame`, `data.table`, and `arrow::Table` with zero memory copies.
4. **Parity & Invariant Verification:**
   - Every language wrapper must produce bit-for-bit identical results on shared synthetic episode fixtures.
