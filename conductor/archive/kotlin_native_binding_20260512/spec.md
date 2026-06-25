# Specification: Kotlin/Native Binding

## Overview
Provide a Kotlin/Native integration roadmap for native clients and analytics
adapters. Kotlin/Native is the authored Kotlin surface for this track. Java/JVM
support is outside the initial scope and must not be required by the product
runtime.

The Kotlin/Native surface consumes the shared Rust core through a C ABI,
service, or Arrow/Parquet file contract and must not duplicate formula logic.

## Functional Requirements
- Evaluate C ABI, service boundary, and Arrow/Parquet file interop.
- Define Kotlin/Native data classes with C ABI, service, and file boundaries.
- Reuse shared golden fixtures and schema conformance tests.
- Document Kotlin/Native artifact publication only after stability gates are met.

## Strategy Notes

- Initial strategy: C ABI plus Arrow/Parquet file interop, selected to keep the
  Kotlin surface native while retaining a conservative batch validation path.
- Fallback strategy: service boundary, for callers that need online
  request/response behavior without local native linking.
- Deferred strategy: Java/JVM integration, until there is a separate business
  case and a non-primary track.
- Kotlin-first API guidance: prefer immutable data classes, explicit nullability,
  schema/version fields, and thin adapters; use `BigDecimal` for values that
  must not absorb binary floating-point drift.

## Acceptance Criteria
- Kotlin/Native integration strategy is selected and documented.
- Kotlin/Native examples validate against shared fixtures.
- Formula logic remains single-sourced.
- No JVM runtime, Maven publication, or Gradle build is required by this track.
