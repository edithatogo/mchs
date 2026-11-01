# Specification: Bleeding-Edge Cross-Platform & Hardware Acceleration Matrix

## Objective
Design and implement an automated cross-platform test matrix and hardware acceleration tier supporting all four languages across bleeding-edge toolchains (Rust 1.99.1+, Python 3.15.1, Julia 1.11+, R 4.5+):
1. **Tier 1 (Apple Silicon Native):** macOS + ARM64 (M-series) + Metal Shaders / MLX / Apple Accelerate for massive Monte Carlo resampling and matrix pricing operations.
2. **Tier 2 (Desktop & Server Platforms):** Windows x86_64, Windows ARM64, Linux x86_64, and Linux aarch64.
3. **Tier 3 (Universal GPU Compute):**
   - Nvidia: CUDA (via `candle-core` / PTX / `wgpu`)
   - AMD: ROCm / HIP compute kernels
   - Intel: oneAPI / SYCL / Level Zero (via OpenCL / `wgpu`)
   - Universal Driverless Fallback: WebGPU / Vulkan Compute shaders via Rust `wgpu`

## Architecture Requirements
1. **Toolchain Alignment (Bleeding-Edge Only):**
   - Rust: Compiler strictly locked to `1.99.1+` leveraging modern GATs, `std::simd`, and 2024 edition optimizations.
   - Python: `3.15.1` with free-threading (`nogil`) and PyO3 0.29.0 / Polars 2.1.0 zero-copy expression plugins.
   - Julia: Minimum supported version strictly `>= 1.11`, dropping legacy 1.10 shims.
   - R: Modern `R >= 4.5.0` with ALTREP zero-copy memory mapping.
2. **Unified Compute Abstraction (`wgpu` / `candle`):**
   - Use bleeding-edge Rust tensor / compute shader backends (`wgpu` for pure compute shaders, `candle` for ML/Bayesian models).
   - This prevents maintaining four separate C++ vendor SDKs, allowing one Rust compute kernel to compile directly to Metal (macOS), CUDA (Nvidia), ROCm (AMD), and Vulkan/Level Zero (Intel).
3. **Bit-Exact Cross-Platform Invariants:**
   - Numerical outputs must be bit-for-bit identical across all CPU architectures (ARM64 vs x86_64) using 128-bit fixed-point decimal arithmetic.
   - GPU-accelerated Monte Carlo bootstrap estimators must produce identical empirical intervals within validated tolerance epsilon.
4. **Automated GitHub Actions Matrix:**
   - Matrix testing Rust, Python, R, and Julia across `macos-14`/`macos-15` (ARM64), `ubuntu-24.04` (x64), `ubuntu-24.04-arm` (aarch64), and `windows-latest`.
