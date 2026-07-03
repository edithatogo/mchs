# Pricing Metadata Single Source

## Overview

Pricing-year metadata must be loaded from the canonical reference-data manifest instead of duplicated constants in Python, tests, docs, or generated support outputs. NEP25 must be corrected to 7258 and NEP26 must remain 7418.

## Requirements

- Treat `reference-data/<year>/manifest.yaml` as authoritative for NEP, NEC, classification versions, source provenance, and validation status.
- Replace direct hardcoded pricing constants with manifest-backed loading or generated artifacts.
- Fail closed when a pricing year lacks required pricing metadata for a claimed executable or validated support state.
- Update validation, diff, CLI, MCP/API, and documentation outputs to consume the same metadata source.
- Preserve explicit gap records for source-only years and incomplete stream/year evidence.

## Acceptance Criteria

- Tests prove NEP25 is 7258 and NEP26 is 7418 from manifests.
- No test or runtime path depends on a second manually maintained NEP constant table.
- `validate-year` and `diff-year` report pricing facts from the manifest-backed source.
- Public support/capability docs do not overclaim validation when manifest evidence is incomplete.

## Out of Scope

- Adding new IHACPA source artifacts.
- Implementing unvalidated calculator streams.
- Mojo adoption.
