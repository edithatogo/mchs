# Specification: End-to-End Validated Canary

## Overview
Prove the full implementation lifecycle for one calculator stream and one
pricing year before broad expansion. The canary should demonstrate source
discovery, source archive, formula extraction, versioned schemas, SAS parity,
Excel formula parity, fixture parity, Python baseline, Rust canary, CLI/Arrow
output, documentation, and release evidence.

## Functional Requirements
- Select one stream/year with available SAS and Excel sources.
- Create a reference-data manifest and formula/parameter bundle.
- Record SAS parity and Excel formula parity.
- Record output fixture parity.
- Validate Python, Rust canary, and CLI/Arrow outputs against shared fixtures.
- Publish a Starlight docs page explaining the validated lifecycle and caveats.

## Non-Functional Requirements
- Do not generalise canary results to other years or streams.
- Evidence must be durable and linked from manifests/docs.
- Rust remains opt-in until parity evidence is complete.

## Acceptance Criteria
- One stream/year has complete lifecycle evidence.
- Validation gates can distinguish canary-validated behavior from roadmap-only behavior.
- The canary becomes the template for future stream/year implementations.
