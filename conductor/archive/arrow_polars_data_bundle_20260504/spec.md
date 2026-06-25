# Specification: Arrow and Polars Data Bundle Migration

## Goal

Define a dataframe-neutral runtime data bundle boundary that stores extracted calculator reference data in Arrow/Parquet and can be consumed by Polars without changing calculator behavior.

## Requirements

- Arrow/Parquet is the canonical persisted bundle format for calculator reference data and extracted tabular assets.
- The bundle layer must be dataframe-neutral. It should expose typed schema, manifest, and tabular payload contracts rather than pandas-specific or Polars-specific objects.
- The bundle contract must support Arrow-native interchange so other engines can consume the same data without lossy conversion.
- Bundle loading must validate manifest version, checksum, pricing year, source artifact reference, and declared schema before returning data.
- pandas may remain available behind an adapter during migration, but the bundle layer itself must not depend on pandas behavior.
- Polars should be introduced behind stable interfaces that operate on the same bundle contract.

## Acceptance Criteria

- A pilot bundle is stored as Parquet with an Arrow-compatible schema and a committed manifest.
- The manifest includes bundle identity, schema version, pricing year, source artifact references, checksums, row counts, and declared backend neutrality.
- A loader can consume the pilot bundle through the dataframe-neutral boundary and return the same calculator inputs expected by the current implementation.
- A Polars adapter can consume the same bundle without changing calculator outputs for the pilot path.
- Migration rules document where pandas remains an adapter detail and where Arrow/Parquet is the canonical contract.
