# Plan: C# Calculation Engine and Power Platform Adapter

## Phase 1: Engine Architecture [checkpoint: b32ee73]

- [x] Task: Write architecture checks for shared contracts [b32ee73]
    - [x] Verify contracts can map to C# models
    - [x] Verify golden fixtures do not depend on Python-specific types
    - [x] Verify the C# engine can consume the same public contract metadata as the web demo
- [x] Task: Document C# engine architecture [b32ee73]
    - [x] Define project layout, secure service boundary, and model generation path
    - [x] Define logging and privacy rules
    - [x] Define how fixture packs are loaded for parity and regression testing
- [x] Task: Conductor - User Manual Verification 'Engine Architecture' (Protocol in workflow.md) [b32ee73]

## Phase 2: Power Platform Boundary [checkpoint: b32ee73]

- [x] Task: Write integration design checks [b32ee73]
    - [x] Verify Power Platform inputs map to public contracts
    - [x] Verify outputs and errors are structured for app workflows
    - [x] Verify Power Platform remains orchestration-only while the C# service performs calculation
- [x] Task: Document Power Platform adapter [b32ee73]
    - [x] Define Custom Connector or Azure Function approach
    - [x] Define Dataverse responsibilities and non-responsibilities
    - [x] Define how the adapter consumes contract and fixture identifiers
- [x] Task: Conductor - User Manual Verification 'Power Platform Boundary' (Protocol in workflow.md) [b32ee73]

## Phase 3: Contract and Fixture Alignment [checkpoint: b32ee73]

- [x] Task: Write parity checks against shared fixtures [b32ee73]
    - [x] Verify C# payloads round-trip against the public contract
    - [x] Verify fixture outputs match the declared tolerance and parity type
- [x] Task: Document release and rollout rules [b32ee73]
    - [x] Define how contract updates, fixture updates, and engine updates stay synchronized
    - [x] Define the gate for enabling real-data workflows through the service boundary
- [x] Task: Conductor - User Manual Verification 'Contract and Fixture Alignment' (Protocol in workflow.md) [b32ee73]
