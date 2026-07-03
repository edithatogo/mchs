# AR-DRG Grouper Provider Runtime

## Overview

The project should support DRG derivation workflows through declared external providers while avoiding proprietary grouping logic in the repository.

## Requirements

- Provide providers for precomputed DRG input, local command execution, local service calls, file-exchange workflows, and optional containers.
- Require provider declarations to include version, license boundary, input/output schema, provenance, and validation status.
- Fail closed when provider configuration, licensed assets, or required classifications are missing.
- Return provenance-bearing classifier outputs that downstream calculators can consume.
- Keep provider execution separate from calculator formulas and support matrix generation.

## Acceptance Criteria

- Precomputed and local-command fixtures pass with deterministic provenance.
- Missing or incompatible providers produce actionable `blocked_licensed` or unsupported status.
- Provider output is validated before admitted acute calculators consume it.
- No proprietary grouping rules or restricted assets are committed.

## Out of Scope

- Writing an AR-DRG grouper.
- Validating proprietary grouper outputs without user-provided licensed fixtures.
