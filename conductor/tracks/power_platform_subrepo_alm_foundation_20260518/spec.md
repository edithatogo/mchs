# Specification: Power Platform Subrepo ALM Foundation

## Overview

Repair and formalize the Power Platform subrepo/submodule boundary and define the source-control layout for a real unpacked solution.

This track is part of the Power Platform completion program. It converts the
current design-only scaffold into a real, source-controlled, ALM-managed Power
Platform delivery surface while preserving the rule that Power Platform is an
orchestration layer and never a calculator formula implementation.

## Dependencies

- `power_platform_binding_20260512`

## Functional Requirements

- Produce concrete implementation artifacts, not only markdown guidance.
- Keep calculation behavior in the shared runtime or secured service boundary.
- Keep all committed examples synthetic and public-safe.
- Make environment-specific values configurable through environment variables,
  connection references, or deployment settings.
- Record evidence for every claim: source artifact, validation output,
  deployment output, or explicit external blocker.

## Non-Functional Requirements

- Use supported Microsoft Power Platform ALM tooling (`pac`) for solution
  lifecycle operations.
- Avoid storing secrets, patient-level data, private NSW operational data, or
  unsupported formula copies in source control.
- Make local and CI validation deterministic where credentials are not needed.
- Treat deployment and publication as gated operations requiring explicit target
  environment evidence.

## Acceptance Criteria

- Power Platform assets live in a configured subrepo or documented subtree with no broken gitlink state, and ALM ownership is explicit.
- The track updates the relevant Power Platform README, contract, and evidence
  documents.
- The track includes validation or explicitly records the external credential,
  tenant, or environment blocker.
- No completion claim is made without matching evidence.

## Out of Scope

- Reimplementing calculator formulas in Power Fx, Dataverse plugins, flows, or
  custom connector policies.
- Committing real patient-level data or private NSW datasets.
- Claiming production readiness before target-environment deployment and smoke
  evidence exist.
