# Strategy: C ABI Binding

## Decision
Use a conservative, versioned C ABI around the shared calculator core, with
opaque handles for stateful objects and Arrow C Data Interface for in-process
batch interchange. Use Arrow file boundaries only for persisted or cross-
process exchange when a file handoff is the better contract than direct memory
sharing.

This is intentionally narrow:
- the ABI exposes a small, stable surface for institutional embedding
- all formula logic stays in the shared core
- the C layer is a transport and lifecycle boundary, not a second calculator

## ABI shape

### Export model
- Prefix all exported symbols with `nwau_abi_` and add a major-version
  namespace only when a future breaking ABI requires parallel symbol families.
- Prefer opaque handles for engines, requests, and result sets.
- Keep public structs POD-only, append-only, and explicit about sizes.
- Expose runtime version query functions and compile-time version macros.

### Versioning policy
- Version the ABI with `major.minor.patch` semantics.
- Major bumps indicate breaking changes to symbol names, struct layouts, or
  semantic contracts.
- Minor bumps may add optional fields or new functions without breaking older
  callers.
- Patch bumps are for non-contractual fixes only.
- A consumer must be able to query the runtime ABI version before allocating
  or calling optional APIs.

### Compatibility rules
- Within a major version, do not reorder fields, change enum ordinals, or
  change ownership semantics.
- New fields must be appended to structs and default safely when missing.
- New functions must be additive and fail closed when the runtime is older than
  the caller expects.
- Source compatibility is best effort, but binary compatibility is the primary
  contract.

## Memory ownership

### Input ownership
- Callers retain ownership of input buffers, file paths, and Arrow arrays unless
  a specific API says otherwise.
- Borrowed inputs remain valid for the duration of the call only.
- The ABI must never require the caller to free memory with a different
  allocator than the one it used.

### Output ownership
- Results returned by the ABI must come with explicit release functions.
- Strings, buffers, and metadata blobs returned by the ABI are owned by the
  library until released by the caller through the matching destroy function.
- Every allocated object must have a single, documented release path.

### Handle lifecycle
- Handles are opaque and invalid after release.
- Double release must be safe to detect and return an error or no-op according
  to the API contract, but never crash.
- No API should expose internal pointers that outlive the owning handle.

## Error semantics
- Use explicit status codes for all entry points.
- Reserve a single code for success and a small, documented set of errors for
  validation, version mismatch, unsupported feature, I/O failure, allocation
  failure, and internal failure.
- Error messages should be retrievable through a caller-supplied buffer or a
  released error object.
- Errors must be deterministic and should not depend on host language
  exception behavior.
- The ABI must fail closed on invalid handles, invalid sizes, and version
  mismatches.

## Arrow boundary

### Preferred in-process boundary
- Use the Arrow C Data Interface for columnar batch input and output when a
  caller can share memory directly.
- Treat Arrow schema and array metadata as part of the contract.
- Release callbacks must follow the Arrow interface rules and not depend on
  Python, Rust, or JVM ownership conventions.

### File boundary
- Use Arrow IPC stream or file boundaries when a persisted handoff is required
  or when the caller cannot share process memory safely.
- Keep the file contract language-neutral and explicit about schema, nullability
  rules, and encoding.
- Do not introduce a parallel custom binary format for the same payload shape.

### Boundary policy
- The ABI should prefer Arrow for batch payloads instead of bespoke struct trees
  once the payloads are no longer scalar-only.
- Scalar entry points may remain available, but they are not the long-term
  growth path for large batch use.

## Unsupported Python-specific behavior
- Do not expose Python callback hooks, Python exceptions, or Python object
  lifetimes through the C ABI.
- Do not require NumPy, pandas, or Python date/time coercion rules at the ABI
  boundary.
- Do not depend on Python-specific truthiness, duck typing, or implicit numeric
  promotion behavior.
- Do not treat GIL-related behavior, reference counting, or pickled state as
  part of the contract.

## Deferrals
- Defer streaming execution, async callbacks, and re-entrant mutation APIs.
- Defer custom allocator injection unless a concrete cross-platform need is
  demonstrated.
- Defer broad plugin-style extension points until the base ABI is fixture-
  stable.
- Defer production-readiness claims until shared golden fixture parity is
  demonstrated through the C boundary.

## Readiness bar
- The ABI is a private preview implementation and contract definition, not a
  production claim.
- No readiness claim should mention production use, institutional adoption, or
  long-term stability until the C surface matches shared golden fixtures and the
  compatibility checks are in place.
- Fixture parity is the gate for any stronger language about maturity.
