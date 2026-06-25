# Specification: C ABI Binding

## Overview
Define a stable C ABI over the shared calculator core for institutional systems and downstream bindings that cannot directly use Python or Rust. This is a low-level integration surface and should be added only after core parity and schemas are stable.

## Functional Requirements
- Define FFI-safe data structures, memory ownership, and error handling.
- Prefer Arrow C Data Interface or file-based Arrow boundaries where practical.
- Add C header generation and ABI compatibility checks.
- Add examples for C and downstream binding consumers.

## Acceptance Criteria
- ABI versioning and compatibility policy are documented.
- Memory ownership and error semantics are tested.
- C ABI outputs match shared golden fixtures.
