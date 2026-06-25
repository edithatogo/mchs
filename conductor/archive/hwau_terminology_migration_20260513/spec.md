# Specification: HWAU Terminology Migration

## Overview

Use healthcare weighted activity unit, abbreviated `hwau`, as the generic
library abstraction. Preserve `nwau` as Australian National Weighted Activity
Unit source terminology and compatibility alias.

## Requirements

- Add `hwau` to canonical schemas, docs, examples, and APIs.
- Preserve `nwau` as a source-specific alias for Australian references.
- Avoid breaking compatibility for existing Australian NWAU examples.
- Document the distinction between generic HWAU and Australia-specific NWAU.
- Ensure pricing outputs can refer to `price_per_hwau`.

## Acceptance Criteria

- Canonical contracts identify `hwau` as the generic domain field.
- NWAU remains documented as Australian source terminology.
- Documentation avoids presenting NWAU as the global library concept.
- Tests cover aliasing and backwards-compatible Australian examples.
