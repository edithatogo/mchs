# Review: AR-DRG ICD/ACHI/ACS Mapping Registry

## Findings

1. Resolved: The track now has a strict metadata registry in
   `nwau_py.ar_drg_mapping_registry` for 2025 and 2026 AR-DRG, ICD-10-AM,
   ACHI, and ACS version bindings.

2. Resolved: Registry records separate public metadata, local-only licensed
   asset hints, and derived validation fixture placeholders.

3. Resolved: Tests cover compatible and incompatible version sets, invalid
   years, local-only boundary wording, docs, contracts, and acute contract
   linkage.

## Blockers

- None for metadata-registry scope.

## Remaining caveats

- This does not reimplement proprietary AR-DRG grouping logic.
- Licensed ICD-10-AM, ACHI, ACS, AR-DRG grouping, and mapping tables remain
  user-supplied local assets.
- Table-level parity fixtures are deferred to the AR-DRG grouper and parity
  fixture tracks.
