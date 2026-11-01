# Implementation Plan: Cross-Platform & Hardware Acceleration Matrix

## Phase 1: Apple Silicon & Metal / MLX Optimization
- [ ] Task: Benchmark `nwau-core` and Python/Julia wrappers on Darwin ARM64 with Apple Accelerate and Metal compute shaders.
- [ ] Task: Implement Metal compute kernel for parallel 100k episode valuation and bootstrap intervals.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1: Apple Silicon & Metal' (Protocol in workflow.md)

## Phase 2: Cross-Platform OS Matrix (Windows, Linux, ARM64)
- [ ] Task: Configure GitHub Actions workflow running Rust, Python, R, and Julia across macOS, Windows, Linux x64, and Linux ARM64.
- [ ] Task: Assert exact 128-bit numerical invariants match across architectures.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2: Cross-Platform Matrix' (Protocol in workflow.md)

## Phase 3: GPU Acceleration Tier (Nvidia CUDA, AMD ROCm, Intel oneAPI)
- [ ] Task: Implement `wgpu` / `candle-core` compute pipeline supporting CUDA, ROCm, Level-Zero, and WebGPU.
- [ ] Task: Verify GPU acceleration fallbacks gracefully to multi-core Rayon CPU execution when no GPU is present.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3: GPU Acceleration Tier' (Protocol in workflow.md)
