# Track c_abi_binding_20260512 Context

- [Strategy](./strategy.md)
- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [CI Notes](./ci_notes.md)
- [Metadata](./metadata.json)

## Status

Complete with gates. The track now contains a conservative Rust workspace C ABI
crate, committed header, consumer documentation, CI notes, and repository
tests. The current scalar acute 2025 entry point delegates to the shared Rust
core for valid pointer-shaped calls and fails closed for invalid pointers. It
does not claim production readiness until fixture parity passes through the C
boundary and ABI compatibility checks are part of CI.
