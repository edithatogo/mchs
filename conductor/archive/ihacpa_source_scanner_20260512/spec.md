# Specification: IHACPA Source Scanner

## Overview
Add tooling to discover and record future IHACPA releases, including NEP/NEC determinations, technical specifications, price-weight tables, NWAU calculators, costing reports, and classification resources.

## Functional Requirements
- Add `funding-calculator sources scan` to discover relevant IHACPA source pages and downloadable artifacts.
- Add `funding-calculator sources add-year <year>` to create or update a pricing-year manifest from discovered sources.
- Capture URLs, filenames, checksums, retrieval timestamps, and source categories.
- Record missing or inaccessible artifacts as gap records.
- Avoid downloading or committing licensed/non-redistributable material unless allowed.

## Non-Functional Requirements
- Network scans must be reproducible enough to diff results.
- Scanner output must be reviewable before files are committed.
- Tooling must not overclaim validation status from discovery alone.

## Acceptance Criteria
- Scanner can produce a draft manifest for a new pricing year.
- Scanner can run in a dry-run mode.
- Tests cover parsing, gap records, and unchanged-source detection.
- CLI, docs, and contract fixtures all use the installed `funding-calculator` entrypoint rather than an undocumented alias.
- Discovery output remains conservative and does not claim calculator parity or release readiness.
