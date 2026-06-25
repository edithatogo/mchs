# Specification: Modernization Foundation

## Track Description

Umbrella coordination for the modernization roadmap. This track does not own implementation work that belongs in the focused tracks listed in `../tracks.md`; it exists to preserve sequencing, dependency gates, and governance context.

## Background

The repository already has focused tracks for source archiving, validation evidence, tooling and CI, calculator core abstractions, public API contracts, Arrow/Polars migration, web delivery, C# and Power Platform delivery, and release governance. The umbrella track should no longer duplicate those scopes.

The remaining purpose of this track is to keep the roadmap coherent so downstream work is sequenced correctly and does not skip prerequisite governance decisions.

## Goals

- Maintain a clear dependency order across the modernization roadmap.
- Preserve the implementation boundary between the umbrella track and the focused tracks.
- Ensure each downstream track has a prerequisite gate before work begins.
- Keep the roadmap aligned with the project's policy on source provenance, validation evidence, and contract stability.

## Non-Goals

- Do not implement calculator features, CI jobs, adapters, or data migrations here.
- Do not restate the detailed scope owned by the focused tracks.
- Do not claim the umbrella track is a substitute for focused implementation work.

## Requirements

- The track registry must order the roadmap as: source archive, validation evidence, tooling and CI, calculator core contracts, fixtures and public API, Arrow/Polars, web, C#, and release governance.
- Each focused track must have an explicit dependency or gate statement.
- The umbrella track must be described as coordination only.
- The roadmap must make it obvious that implementation work belongs in the focused tracks, not here.

## Acceptance Criteria

- The track registry expresses the delivery order and prerequisites clearly.
- The umbrella modernization track is marked as coordination only and no longer reads like a duplicate implementation program.
- Future reviewers can see at a glance which track is the prerequisite for each downstream slice.
