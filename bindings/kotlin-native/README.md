# Kotlin/Native binding

This boundary adapter is Kotlin/Native-first. It is intended for consumers who want
Kotlin ergonomics without a JVM runtime dependency.

## Boundary

- Kotlin/Native calls the shared Rust core through a C ABI, service, or
  file/Arrow boundary.
- Kotlin code defines request/response envelopes and diagnostics adapters.
- Formula logic remains in the Rust core or shared calculator contract.

## Non-goals

- No JVM runtime dependency.
- No Java-authored binding.
- No duplicated formula implementation.
- No Kotlin/Native artifact publication claim.

## Adapter behavior

`FileBoundaryNativeBindingClient` validates the public request envelope before a
caller hands the file paths to the shared-core CLI, C ABI, or service boundary.
It fails closed when required routing fields are missing or paths are absolute
or traversal-shaped, and returns `ENVELOPE_VALIDATED` only when the request is
shaped for caller-owned shared-core execution.

## Build note

Kotlin/Native avoids a JVM runtime artifact. Kotlin build tools still need a
compiler toolchain during development, depending on the chosen build system. The
product boundary should not require Java or a JVM.
