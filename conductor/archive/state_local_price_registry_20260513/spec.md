# Specification: State and Local Price Registry

## Overview

Create a registry for national, state-specific, local, and discounted prices
applied to HWAU outputs over time. The registry sources public or locally
licensed price schedules and records provenance instead of hard-coding values.

## Requirements

- Source National Efficient Price by year where applicable.
- Source state or jurisdiction-specific HWAU/NWAU prices by year.
- Support local health network, hospital, program, or institutional prices
  where public or locally licensed sources exist.
- Support discounted price mechanisms: fixed price, multiplier, percentage
  discount, cap/floor, or local override formula.
- Record source URL/path, retrieval date, checksum, licence, jurisdiction,
  effective period, currency, and support status.
- Fail closed when a price schedule is unavailable or not licensed for
  redistribution.

## Acceptance Criteria

- Versioned price schedule schema exists.
- Public-source and local-only source categories are explicit.
- Discounted price rules are represented declaratively.
- Tests cover national, state, local, discounted, missing, and blocked price
  schedules.
