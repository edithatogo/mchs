# Specification: Contract Schema Export

## Overview
Export versioned schemas for the public calculator contract and validation
ecosystem. These schemas are the foundation for Rust core, Arrow interfaces,
bindings, CLI/file workflows, docs, and release evidence.

## Functional Requirements
- Export schemas for calculator inputs, outputs, diagnostics, provenance,
  pricing-year manifests, formula bundles, fixture manifests, and evidence
  records.
- Version schemas independently from package versions and pricing years.
- Generate JSON Schema or equivalent artifacts from typed models where
  practical.
- Link schema artifacts to binding conformance tests and docs.

## Acceptance Criteria
- Schema artifacts exist in a stable location.
- Tests prove schema export is deterministic.
- Binding tracks can reference schema artifacts as dependencies.
- Docs explain schema, package, pricing-year, and bundle version separation.
