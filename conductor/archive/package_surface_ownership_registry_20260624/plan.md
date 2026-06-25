# Plan: Package Surface Ownership Registry

## Phase 1: Contract Shape

- [x] Task: Define the surface schema.
    - [x] Require id, display name, category, lifecycle state, support status, path, manifests, owner track, CI gate, release target, evidence boundary, and artifact policy.
    - [x] Allow planned and registry-only surfaces to omit local manifests only when explicitly marked non-implemented.
    - [x] Require implemented package surfaces to point to existing files.
- [x] Task: Conductor - User Manual Verification 'Contract Shape' (Protocol in workflow.md)

## Phase 2: Surface Inventory

- [x] Task: Register implemented package roots.
    - [x] Include Python, Rust, docs-site, R, Julia, Go, .NET, Swift, JVM, WASM, VS Code, Power Platform, Stata, MATLAB, conda, Conan, and Homebrew.
    - [x] Record release target, support state, and validation command.
- [x] Task: Register planned or external surfaces.
    - [x] Include CRAN, Maven Central, vcpkg, Swift Package Index, and other registry gates without overclaiming publication.
    - [x] Link each surface to its Conductor owner track.
- [x] Task: Conductor - User Manual Verification 'Surface Inventory' (Protocol in workflow.md)

## Phase 3: Registry Validation

- [x] Task: Add validator coverage.
    - [x] Detect unregistered package manifests.
    - [x] Detect duplicate manifest ownership.
    - [x] Detect implemented surfaces with missing manifests.
- [x] Task: Run focused validation.
    - [x] Run `uv run python scripts/validate_repository_topology.py`.
    - [x] Run `uv run pytest tests/test_repository_topology_governance.py`.
- [x] Task: Conductor - User Manual Verification 'Registry Validation' (Protocol in workflow.md)
