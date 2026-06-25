# Review: AR-DRG Grouper Integration

## Findings

1. Resolved: The track now has `nwau_py.ar_drg_grouper`, a conservative
   interface for precomputed AR-DRG records and local user-supplied external
   grouper references.

2. Resolved: Version compatibility checks are linked to the AR-DRG mapping
   registry and fail closed for missing or mismatched ICD-10-AM, ACHI, ACS,
   and AR-DRG versions.

3. Resolved: Tests and contract fixtures cover precomputed records, local
   external references, diagnostics, provenance, missing reference details, and
   explicit non-redistribution of proprietary grouping logic.

## Blockers

- None for interface-contract scope.

## Remaining caveats

- This does not execute or bundle a proprietary AR-DRG grouper.
- Users must supply licensed grouping tools and tables locally.
- End-to-end grouper parity remains deferred to licensed product workflow and
  parity fixture tracks.
