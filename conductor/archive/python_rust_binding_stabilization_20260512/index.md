# Track python_rust_binding_stabilization_20260512 Context

- The Python-to-Rust acute 2025 bridge remains opt-in and preserves the
  pure-Python calculator path as the default validated API.
- Binding-contract documentation is published in the governance docs, covering
  batch schema, error mapping, opt-in status, and packaging posture.
- CI now includes a cross-platform maturin wheel build/install smoke test.
- Track validation covers Rust bridge diagnostics, pure-Python fallback,
  golden fixture parity, Rust cargo tests, Rust clippy, and local wheel import.

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
