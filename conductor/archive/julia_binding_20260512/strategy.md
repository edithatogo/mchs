# Strategy: Julia Binding Initial Path

## Decision
Start with **CLI/file integration** as the initial Julia binding path. CSV is
the executable prototype because the current shared CLI accepts and emits CSV.
Arrow remains the target interchange format for larger cross-language batches
once the language-neutral file contract is implemented.

## Comparison

### C ABI
- Stability: medium. A C ABI is portable in principle, but every exported symbol and struct layout becomes a hard compatibility contract.
- Maintenance: medium to high. Headers, shared-library packaging, and ABI compatibility testing add ongoing cost.
- Package/binary distribution: good for performance, but versioned native artifacts increase release complexity across platforms.
- Single-sourced formula logic: good if the ABI exposes the core engine directly, but the surface area is easy to drift as the API grows.

### PythonCall
- Stability: medium. The Julia side is convenient, but the stack now depends on Python runtime compatibility and Python package resolution.
- Maintenance: high. Two language ecosystems, plus Python dependency pinning, make support and releases more fragile.
- Package/binary distribution: weakest of the three for a clean Julia-first distribution story because Python becomes a required runtime dependency.
- Single-sourced formula logic: acceptable only if Python remains a thin wrapper; otherwise it tends to become an extra orchestration layer.

### CLI/file
- Stability: suitable for an initial prototype. The CLI boundary is observable
  and debuggable, and CSV matches the current executable contract.
- Maintenance: low to medium. The contract is mostly command behavior plus file
  shape, which is simpler than maintaining a native ABI.
- Package/binary distribution: conservative for an initial rollout because
  Julia can call a versioned executable without exposing native symbols.
- Single-sourced formula logic: strong. The formulas stay in one implementation
  of the calculator core, with Julia limited to data preparation, invocation,
  and result handoff.

## Recommendation

Use CLI/file integration first, with the Julia package acting as a thin
orchestration layer around the shared calculator core. Treat Arrow as the target
batch interchange format when the shared CLI/file contract grows beyond CSV.

## Why this path first

1. It minimizes the initial compatibility surface.
2. It keeps formula logic single-sourced outside Julia.
3. It avoids native ABI fragility while the Rust core contract is still maturing.
4. It leaves room to add Arrow and then a C ABI later if profiling shows the CLI
   boundary is the bottleneck.

## Deferred paths

- Promote to C ABI only after the core contract is stable and there is a clear performance need.
- Avoid PythonCall as the primary integration path unless the project already needs Python for other reasons.

## Validation contract

- Julia package tests must verify the command-building surface without executing
  calculator formulas in Julia.
- Repository tests must assert that the Julia wrapper does not duplicate known
  formula constants, adjustment names, or validation fallback logic.
- Shared golden fixture parity remains owned by the shared calculator contract;
  the Julia wrapper can only claim release readiness after it executes those
  fixtures through the shared CLI/file boundary.
