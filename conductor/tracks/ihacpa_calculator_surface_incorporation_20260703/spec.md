# IHACPA Calculator Surface Incorporation

## Overview

The repository should include every IHACPA calculator, specification, and public metadata surface that can be redistributed, while recording gaps and licensing boundaries for material that cannot be committed.

## Requirements

- Inventory historical and present IHACPA calculator surfaces by pricing year and stream.
- Incorporate redistributable public metadata, source manifests, extracted formulas, and parameter records where licensing permits.
- Do not commit restricted classification tables, proprietary grouping logic, or licensed manuals by disclaimer alone.
- Represent runtime-installable or user-provided assets as local-only references with license caveats.
- Keep source-only and validation-backed support states distinct.

## Acceptance Criteria

- Each relevant year/stream has a manifest-backed status: incorporated, source-only, restricted-local-only, unavailable, or out-of-scope.
- Redistributable additions include provenance, source URL, retrieval date, checksum where available, and license decision.
- Restricted assets are represented by local-only setup guidance and gap records.
- Documentation and support matrices match the inventory.

## Out of Scope

- Reimplementing proprietary grouping logic.
- Claiming parity for streams without fixture or source evidence.
