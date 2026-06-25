# Specification: C# Calculation Engine and Power Platform Adapter

## Goal

Define the C#/.NET service-boundary architecture that can support Power Platform workflows while preserving parity with Python, the Rust-core direction, and IHACPA sources. The completed scope is architecture and boundary governance, not an executable C# calculation engine.

## Requirements

- C# must consume the shared public contract and golden fixtures.
- Power Platform should act as an orchestration surface, not the source of calculator logic.
- Any C#/.NET service should sit behind a secure service boundary such as an Azure Function or custom connector target and consume shared calculator contracts rather than duplicating formula logic.
- Logging must avoid patient-level field values.
- Real-data workflows must be validated against the public contract and not rely on Power Platform-native formula logic.
- Fixture compatibility should be versioned so Python, C#, and the web demo can consume the same evidence set.

## Acceptance Criteria

- C#/.NET service-boundary architecture is documented.
- Shared fixtures can drive future C# tests.
- Power Platform integration boundaries are explicit.
- The service boundary and contract mapping are clear enough to support later web and API adapters.
