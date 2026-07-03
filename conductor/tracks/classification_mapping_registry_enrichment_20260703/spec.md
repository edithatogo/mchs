# Classification Mapping Registry Enrichment

## Overview

The repository should expose all relevant public classification mapping metadata and provide safe local hooks for licensed mapping tables.

## Requirements

- Enrich AR-DRG, ICD-10-AM, ACHI, ACS, AECC, UDG, Tier 2, and AMHCC metadata where public redistribution is allowed.
- Represent licensed mapping tables as local-only assets with version, checksum, and provenance metadata.
- Validate compatibility between pricing year, stream, coding set, and classifier/grouper provider.
- Avoid silent crosswalks between versions or classification systems.
- Document whether each mapping is public metadata, local-only, unsupported, or out-of-scope.

## Acceptance Criteria

- Registry validation rejects incompatible stream/year/classification combinations.
- Public metadata fixtures can be loaded without licensed assets.
- Local-only mapping hooks can validate safe placeholder fixtures without committing restricted data.
- Documentation states that DRG derivation from ICD/ACHI requires licensed tooling or user-provided mappings.

## Out of Scope

- Bundling proprietary mapping tables.
- Implementing AR-DRG grouping rules.
