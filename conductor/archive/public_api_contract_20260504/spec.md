# Specification: Public Calculator API Contract

## Goal

Define the versioned public contract package that becomes the next delivery gate for all downstream calculator surfaces.

## Requirements

- Contracts must be versioned and treated as the source of truth for adapter behavior.
- Contracts must expose supported calculators, years, required fields, optional parameters, output fields, validation status, and numeric precision expectations.
- Error responses must be structured, explainable, and suitable for CLI, Python, web, C#, and Power Platform consumers.
- Contracts must be generated or verified from the calculator core where possible, but the public contract is the delivery gate for downstream implementation.

## Acceptance Criteria

- Contract documentation exists for at least one calculator.
- The contract maps to Python API and CLI behavior.
- The contract is suitable for OpenAPI or C# model generation later.
- Calculator core and downstream adapter expansion remain gated by this contract definition.
