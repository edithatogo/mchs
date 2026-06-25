# Plan: Arrow and Polars Data Bundle Migration

## Phase 1: Bundle Contract [checkpoint: d3df5f0]

- [x] Task: Write tests for Arrow/Parquet bundle metadata and boundary rules [d3df5f0]
    - [x] Verify schema version, bundle identity, pricing year, source artifact reference, checksum, and backend-neutral declarations
    - [x] Verify bundle loading failures are actionable and mention the violated contract
- [x] Task: Define the dataframe-neutral runtime bundle contract [d3df5f0]
    - [x] Add manifest structure with typed metadata and source provenance
    - [x] Add extraction target layout for Arrow/Parquet payloads and schema files
    - [x] Specify where pandas stays adapter-only and where Arrow is the canonical contract
- [x] Task: Conductor - User Manual Verification 'Bundle Contract' (Protocol in workflow.md) [d3df5f0]

## Phase 2: Polars Pilot [checkpoint: d3df5f0]

- [x] Task: Write parity tests for one calculator data path over the shared bundle contract [d3df5f0]
    - [x] Compare current adapter output and Polars adapter output on the same Arrow/Parquet bundle
    - [x] Cover nulls, categorical values, numeric precision, and schema preservation
- [x] Task: Implement a Polars pilot behind the dataframe-neutral boundary [d3df5f0]
    - [x] Keep pandas behavior available through the adapter layer only
    - [x] Avoid broad calculator rewrites or hidden source-table conversions
- [x] Task: Conductor - User Manual Verification 'Polars Pilot' (Protocol in workflow.md) [d3df5f0]

## Phase 3: Migration Guidance [checkpoint: d3df5f0]

- [x] Task: Write migration rules for bundle consumers [d3df5f0]
    - [x] Document bundle creation, validation, and loading responsibilities
    - [x] Document how future engines can consume the same Arrow/Parquet bundle without changing the contract
- [x] Task: Record the approved bundle boundary in the relevant ADR [d3df5f0]
    - [x] Summarize why Arrow/Parquet is canonical
    - [x] Summarize why the bundle layer stays dataframe-neutral
- [x] Task: Conductor - User Manual Verification 'Migration Guidance' (Protocol in workflow.md) [d3df5f0]
