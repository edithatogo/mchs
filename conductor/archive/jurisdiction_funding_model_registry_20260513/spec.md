# Specification: Jurisdiction Funding Model Registry

## Overview

Create a registry for Australian state and territory funding models. The
registry should preserve jurisdiction-specific terminology and source caveats
while mapping comparable outputs to the generic HWAU abstraction.

## Requirements

- Cover NSW, VIC, QLD, WA, SA, TAS, ACT, and NT.
- Source jurisdiction-specific price or activity unit models by financial year.
- Record source terms such as State Price, State Efficient Price, Queensland
  Efficient Price, QWAU, WIES, WAU, NWAU, and ACT applicable price.
- Capture local adjustments, supplements, exclusions, block-funded components,
  transition notes, and stream applicability.
- Mark jurisdictions/years as public, local-only, blocked, or unknown.
- Preserve provenance and licence status for every source.

## Acceptance Criteria

- Jurisdiction registry schema exists.
- Each state and territory has an explicit registry row or blocked-source row.
- Tests cover at least NSW, QLD, VIC, WA, SA, TAS, ACT, and NT source statuses.
- Parallel valuation can select jurisdiction-specific price schedules.
