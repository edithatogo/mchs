# Specification: Julia Monorepo Consolidation & Direct C-ABI Binding (Option A)

## Objective
Unify the Julia wrapper as a first-class citizen inside the MCHS monorepo at `julia-binding/`. Transition from external CLI sub-process execution to high-performance, in-process foreign function calls (`ccall`) targeting `libnwau_c_abi`. Prepare the separate GitHub repository `edithatogo/NationalWeightedActivityUnitWrapper.jl` for formal public archival.

## Requirements
1. **Canonical Monorepo Source (Option A):**
   - `julia-binding/` is the sole development and testing location for the Julia package.
   - All code, C-ABI bindings, and unit tests execute within monorepo CI.
2. **Direct C-ABI Inversion:**
   - Eliminate subprocess shell executions (`run(\`funding-calculator ...\`)`).
   - Call native C-ABI symbols (`nwau_calculate_acute`, `nwau_calculate_ed`, etc.) via Julia's zero-overhead `ccall`.
   - Leverage modern Julia 1.11+ features, including `Memory{T}` buffers and `Arrow.jl` zero-copy tables.
3. **Public Archival of Separate Repository:**
   - Push a final release to `edithatogo/NationalWeightedActivityUnitWrapper.jl` updating the README with a prominent deprecation and migration banner redirecting users to `edithatogo/mchs` (`julia-binding/`).
   - Archive the separate GitHub repository as read-only.
4. **Target Modern Julia Versions Only:**
   - Target Julia `>= 1.11` (dropping legacy 1.10 shims), taking full advantage of modern Julia 1.11+ compiler and memory layout enhancements.
